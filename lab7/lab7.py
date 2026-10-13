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


def diffie_hellman_auto(bits=128):
    print(f"Генерация параметров Диффи-Хеллмана ({bits} бит)...")
    p, q = generate_safe_prime(bits)
    g = get_generator(p, q)
    
    a = random.randint(2, p - 2)
    b = random.randint(2, p - 2)
    
    A = pow(g, a, p)
    B = pow(g, b, p)
    
    secret_A = pow(B, a, p)
    secret_B = pow(A, b, p)
    
    assert secret_A == secret_B, "Ошибка протокола Диффи-Хеллмана!"
    
    return p, g, a, b, A, B, secret_A


def vernam_process_file(input_path, output_path, shared_secret):
    random.seed(shared_secret)
    
    chunk_size = 1024 * 64
    
    with open(input_path, 'rb') as f_in, open(output_path, 'wb') as f_out:
        while True:
            chunk = f_in.read(chunk_size)
            if not chunk:
                break
                
            try:
                key_chunk = random.randbytes(len(chunk))
            except AttributeError:
                key_chunk = bytes([random.randint(0, 255) for _ in range(len(chunk))])
            
            processed_chunk = bytes(b1 ^ b2 for b1, b2 in zip(chunk, key_chunk))
            
            f_out.write(processed_chunk)


def main():
    while True:
        print("1. Ввод параметров Диффи-Хеллмана (p, g, a, b) с клавиатуры")
        print("2. Автоматическая генерация ключей")
        print("0. Выход")
        
        choice = input("Выберите действие: ")

        if choice == '0':
            break
            
        if choice not in ('1', '2'):
            print("Неверный выбор.")
            continue

        shared_secret = None

        if choice == '1':
            try:
                p = int(input("Введите простое число p: "))
                g = int(input("Введите базу g: "))
                a = int(input("Введите закрытый ключ Алисы (a): "))
                b = int(input("Введите закрытый ключ Боба (b): "))
                
                A = pow(g, a, p)
                B = pow(g, b, p)
                
                secret_Alice = pow(B, a, p)
                secret_Bob = pow(A, b, p)
                
                if secret_Alice != secret_Bob:
                    print("Критическая ошибка: общие секреты не совпадают. Проверьте параметры!")
                    continue
                    
                shared_secret = secret_Alice
                print(f"\nОткрытый ключ Алисы (A): {A}")
                print(f"Открытый ключ Боба (B):  {B}")
                print(f"Вычислен общий секретный ключ (K) = {shared_secret}")
                
            except ValueError:
                print("Ошибка: необходимо вводить целые числа.")
                continue

        elif choice == '2':
            p, g, a, b, A, B, shared_secret = diffie_hellman_auto(bits=128)
            print("\nСгенерированные параметры Диффи-Хеллмана")
            print(f"p (модуль) = {p}")
            print(f"g (база)   = {g}")
            print(f"a (закр. Алисы) = {a}")
            print(f"b (закр. Боба)  = {b}")
            print(f"A (откр. Алисы) = {A}")
            print(f"B (откр. Боба)  = {B}")
            print(f"Общий секрет (K) = {shared_secret}")

        input_file = input("\nВведите путь к файлу для шифрования: ")
        
        if not os.path.exists(input_file):
            print("Ошибка: Указанный файл не существует!")
            continue

        base_name = os.path.basename(input_file)
        name, ext = os.path.splitext(base_name)
        
        enc_file = f"encrypted_{name}.bin"
        dec_file = f"decrypted_{name}{ext}"
        
        try:
            vernam_process_file(input_file, enc_file, shared_secret)
            print(f"Файл зашифрован: {enc_file}")
            
            vernam_process_file(enc_file, dec_file, shared_secret)
            print(f"Файл расшифрован: {dec_file}")
            
            print(f"\nПроцесс завершен.")
            print(f"├── Исходный файл:      {input_file}")
            print(f"├── Зашифрованный файл: {enc_file}")
            print(f"└── Итоговый файл:      {dec_file}")
            
        except Exception as ex:
            print(f"Ошибка в процессе обработки файла: {ex}")

if __name__ == "__main__":
    main()
