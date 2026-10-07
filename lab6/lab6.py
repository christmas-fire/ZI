import os
import random
import math

def miller_rabin_test(n, k=10):
    if n == 2 or n == 3: return True
    if n <= 1 or n % 2 == 0: return False
    
    r, s = 0, n - 1
    while s % 2 == 0:
        r += 1
        s //= 2
        
    for _ in range(k):
        a = random.randrange(2, n - 1)
        x = pow(a, s, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

def generate_prime(bits=64):
    while True:
        p = random.getrandbits(bits)
        p |= (1 << (bits - 1)) | 1
        if miller_rabin_test(p):
            return p

def generate_keys(bits=64):
    print(f"Генерация простых чисел p и q ({bits} бит)...")
    p = generate_prime(bits)
    q = generate_prime(bits)
    while q == p:
        q = generate_prime(bits)
        
    n = p * q
    phi = (p - 1) * (q - 1)
    
    d_b = 65537
    if math.gcd(d_b, phi) != 1:
        while True:
            d_b = random.randrange(3, phi, 2)
            if math.gcd(d_b, phi) == 1:
                break
                
    c_b = pow(d_b, -1, phi)
    
    return p, q, n, c_b, d_b


def encrypt_file(input_path, output_path, n, d_b):
    chunk_size = (n.bit_length() - 1) // 8 
    n_bytes = (n.bit_length() + 7) // 8
    
    original_size = os.path.getsize(input_path)

    with open(input_path, 'rb') as f_in, open(output_path, 'wb') as f_out:
        f_out.write(original_size.to_bytes(8, 'big'))

        while True:
            chunk = f_in.read(chunk_size)
            if not chunk:
                break
                
            m = int.from_bytes(chunk, 'big')
            
            e = pow(m, d_b, n)
            
            f_out.write(e.to_bytes(n_bytes, 'big'))
            
    print(f"Файл зашифрован: {output_path}")

def decrypt_file(input_path, output_path, n, c_b):
    chunk_size = (n.bit_length() - 1) // 8
    n_bytes = (n.bit_length() + 7) // 8

    with open(input_path, 'rb') as f_in, open(output_path, 'wb') as f_out:
        orig_size_bytes = f_in.read(8)
        if not orig_size_bytes: return
        original_size = int.from_bytes(orig_size_bytes, 'big')

        bytes_written = 0
        while True:
            e_bytes = f_in.read(n_bytes)
            
            if not e_bytes:
                break

            e = int.from_bytes(e_bytes, 'big')

            m = pow(e, c_b, n)
            
            m_bytes = m.to_bytes(chunk_size, 'big')

            remaining = original_size - bytes_written
            if remaining < chunk_size:
                f_out.write(m_bytes[-remaining:])
                bytes_written += remaining
            else:
                f_out.write(m_bytes)
                bytes_written += chunk_size

    print(f"Файл расшифрован: {output_path}")


def main():
    while True:
        print("1. Ввод параметров (p, q, D_B) с клавиатуры")
        print("2. Автоматическая генерация параметров")
        print("0. Выход")
        
        choice = input("Выберите действие: ")

        if choice == '0':
            break
            
        if choice not in ('1', '2'):
            print("Неверный выбор.")
            continue

        if choice == '1':
            try:
                p = int(input("Введите простое число p: "))
                q = int(input("Введите простое число q: "))
                
                n = p * q
                if n <= 255:
                    print("Ошибка: произведение N = p*q слишком маленькое. Задайте p и q больше (N должно быть > 255).")
                    continue
                    
                d_b = int(input("Введите открытый ключ D_B: "))
                phi = (p - 1) * (q - 1)
                
                if math.gcd(d_b, phi) != 1:
                    print(f"Ошибка: D_B ({d_b}) и phi(N) ({phi}) не взаимно простые! Протокол не будет работать.")
                    continue
                
                c_b = pow(d_b, -1, phi)
                print(f"Вычислен модуль N = {n}")
                print(f"Вычислен секретный ключ C_B = {c_b}")
                
            except ValueError:
                print("Ошибка: необходимо вводить целые числа.")
                continue

        elif choice == '2':
            p, q, n, c_b, d_b = generate_keys(bits=64) 
            print("\nСгенерированные параметры")
            print(f"p   = {p}")
            print(f"q   = {q}")
            print(f"N   = {n} (Модуль)")
            print(f"D_B = {d_b} (Открытый ключ - для шифрования)")
            print(f"C_B = {c_b} (Секретный ключ - для расшифровки)")
            print("---------------------------------")

        input_file = input("\nВведите путь к файлу для шифрования: ")
        
        if not os.path.exists(input_file):
            print("Ошибка: Указанный файл не существует!")
            continue

        base_name = os.path.basename(input_file)
        name, ext = os.path.splitext(base_name)
        
        enc_file = f"encrypted_{name}.bin"
        dec_file = f"decrypted_{name}{ext}"
        
        try:
            encrypt_file(input_file, enc_file, n, d_b)
            
            decrypt_file(enc_file, dec_file, n, c_b)
            
            print(f"\nПроцесс завершен.")
            print(f"├── Исходный файл:      {input_file}")
            print(f"├── Зашифрованный файл: {enc_file}")
            print(f"└── Итоговый файл:      {dec_file}\n")
            
        except Exception as ex:
            print(f"Ошибка в процессе обработки файла: {ex}")

if __name__ == "__main__":
    main()
    