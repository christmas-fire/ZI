import os
import random

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


def generate_safe_prime(bits=128):
    while True:
        q = random.getrandbits(bits - 1)
        q |= (1 << (bits - 2)) | 1
        if miller_rabin_test(q):
            p = 2 * q + 1
            if miller_rabin_test(p):
                return p, q


def get_generator(p, q):
    while True:
        g = random.randint(2, p - 2)
        if pow(g, 2, p) != 1 and pow(g, q, p) != 1:
            return g


def generate_keys(bits=128):
    p, q = generate_safe_prime(bits)
    g = get_generator(p, q)
    c_b = random.randint(2, p - 2)
    d_b = pow(g, c_b, p)
    return p, g, c_b, d_b


def encrypt_file(input_path, output_path, p, g, d_b):
    chunk_size = (p.bit_length() - 1) // 8 
    p_bytes = (p.bit_length() + 7) // 8
    original_size = os.path.getsize(input_path)

    with open(input_path, 'rb') as f_in, open(output_path, 'wb') as f_out:
        f_out.write(original_size.to_bytes(8, 'big'))

        while True:
            chunk = f_in.read(chunk_size)
            if not chunk:
                break
                
            m = int.from_bytes(chunk, 'big')
            
            k = random.randint(1, p - 2)
            r = pow(g, k, p)
            e = (m * pow(d_b, k, p)) % p

            f_out.write(r.to_bytes(p_bytes, 'big'))
            f_out.write(e.to_bytes(p_bytes, 'big'))
            
    print(f"Файл зашифрован: {output_path}")

def decrypt_file(input_path, output_path, p, c_b):
    chunk_size = (p.bit_length() - 1) // 8
    p_bytes = (p.bit_length() + 7) // 8

    with open(input_path, 'rb') as f_in, open(output_path, 'wb') as f_out:
        orig_size_bytes = f_in.read(8)
        if not orig_size_bytes: return
        original_size = int.from_bytes(orig_size_bytes, 'big')

        bytes_written = 0
        while True:
            r_bytes = f_in.read(p_bytes)
            e_bytes = f_in.read(p_bytes)
            
            if not r_bytes or not e_bytes:
                break

            r = int.from_bytes(r_bytes, 'big')
            e = int.from_bytes(e_bytes, 'big')

            m = (e * pow(r, p - 1 - c_b, p)) % p
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
        print("1. Ввод параметров (p, g, C_B) с клавиатуры")
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
                p = int(input("Введите простое число p > 255: "))
                if p <= 255:
                    print("Ошибка: p <= 255")
                    continue
                    
                g = int(input("Введите число g: "))
                c_b = int(input("Введите секретный ключ C_B: "))
                d_b = pow(g, c_b, p)
                print(f"[*] Вычислен открытый ключ D_B = {d_b}")
            except ValueError:
                print("Ошибка: необходимо вводить целые числа.")
                continue

        elif choice == '2':
            p, g, c_b, d_b = generate_keys(bits=128)
            print("\nСгенерированные параметры")
            print(f"p   = {p}")
            print(f"g   = {g}")
            print(f"C_B = {c_b} (Секретный ключ)")
            print(f"D_B = {d_b} (Открытый ключ)")
            print("---------------------------------")

        input_file = input("\nВведите путь к файлу: ")
        
        if not os.path.exists(input_file):
            print("Ошибка: Указанный файл не существует!")
            continue

        base_name = os.path.basename(input_file)
        name, ext = os.path.splitext(base_name)
        
        enc_file = f"encrypted_{name}.bin"
        dec_file = f"decrypted_{name}{ext}"
        
        try:
            encrypt_file(input_file, enc_file, p, g, d_b)
            decrypt_file(enc_file, dec_file, p, c_b)
            
            print(f"\nПроцесс завершен")
            print(f"├── Исходный файл:      {input_file}")
            print(f"├── Зашифрованный файл: {enc_file}")
            print(f"└── Итоговый файл:      {dec_file}\n")
            
        except Exception as ex:
            print(f"Ошибка в процессе обработки файла: {ex}")

if __name__ == "__main__":
    main()
    

"""
Пытался скормить алгоритму файл metod.docx - методичка Рубана, весит почти 100 мб
Алгоритм не расчитаен на работу с файлами такого объема, т.к. мы делим данные на блоки по 15Б
В итоге мы получаем огромное кол-во блоков, для каждого из которого нужно выполнить дорогую операцию возведения в степень

-> время выполнения: >10 мин
"""
