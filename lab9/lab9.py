import hashlib
import json
import math
import os
import random


def is_prime(n, k=10):
    if n < 2:
        return False
    for p in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        if n == p:
            return True
        if n % p == 0:
            return False
    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2
    for _ in range(k):
        a = random.randrange(2, n - 1)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True


def get_prime(bits=32):
    while True:
        n = random.getrandbits(bits) | 1 | (1 << (bits - 1))
        if is_prime(n):
            return n


def generate_params():
    while True:
        q = get_prime(32)
        p = 2 * q + 1
        if is_prime(p):
            break
    while True:
        g = random.randint(2, p - 2)
        if pow(g, 2, p) != 1 and pow(g, q, p) != 1:
            break
    return p, g


def generate_keys():
    p, g = generate_params()
    x = random.randint(2, p - 2)
    y = pow(g, x, p)
    return {"p": p, "g": g, "y": y}, {"p": p, "g": g, "x": x}


def sign_file(file_path, private_key_path, signature_path):
    if not os.path.exists(file_path):
        print("Файл для подписи не найден")
        return
    if not os.path.exists(private_key_path):
        print("Файл закрытого ключа не найден")
        return

    with open(private_key_path, "r", encoding="utf-8") as f:
        priv_key = json.load(f)

    p = priv_key["p"]
    g = priv_key["g"]
    x = priv_key["x"]

    with open(file_path, "rb") as f:
        data = f.read()

    hash_bytes = hashlib.sha256(data).digest()
    signature = []

    for byte in hash_bytes:
        while True:
            k = random.randint(2, p - 2)
            if math.gcd(k, p - 1) == 1:
                a = pow(g, k, p)
                k_inv = pow(k, -1, p - 1)
                b = ((byte - x * a) * k_inv) % (p - 1)
                if b != 0:
                    signature.append((a, b))
                    break

    with open(signature_path, "w", encoding="utf-8") as f:
        json.dump(signature, f)

    print("Файл успешно подписан")


def verify_file(file_path, public_key_path, signature_path):
    if not os.path.exists(file_path):
        print("Проверяемый файл не найден")
        return
    if not os.path.exists(public_key_path):
        print("Файл открытого ключа не найден")
        return
    if not os.path.exists(signature_path):
        print("Файл подписи не найден")
        return

    with open(public_key_path, "r", encoding="utf-8") as f:
        pub_key = json.load(f)

    p = pub_key["p"]
    g = pub_key["g"]
    y = pub_key["y"]

    with open(signature_path, "r", encoding="utf-8") as f:
        signature = json.load(f)

    with open(file_path, "rb") as f:
        data = f.read()

    hash_bytes = hashlib.sha256(data).digest()

    if len(signature) != len(hash_bytes):
        print("Подпись неверна")
        return

    for byte, (a, b) in zip(hash_bytes, signature):
        if not (1 <= a < p):
            print("Подпись неверна")
            return
        v1 = (pow(y, a, p) * pow(a, b, p)) % p
        v2 = pow(g, byte, p)
        if v1 != v2:
            print("Подпись неверна")
            return

    print("Подпись верна")


def main():
    while True:
        print("1. Генерация ключей")
        print("2. Подписать файл")
        print("3. Проверить подпись")
        print("4. Выход")
        choice = input("Выберите действие: ").strip()

        if choice == "1":
            pub_path = input("Имя файла открытого ключа (elgamal_pub.json): ").strip() or "elgamal_pub.json"
            priv_path = input("Имя файла закрытого ключа (elgamal_priv.json): ").strip() or "elgamal_priv.json"
            pub, priv = generate_keys()
            with open(pub_path, "w", encoding="utf-8") as f:
                json.dump(pub, f)
            with open(priv_path, "w", encoding="utf-8") as f:
                json.dump(priv, f)
            print("Ключи успешно сгенерированы")
        elif choice == "2":
            file_path = input("Путь к файлу: ").strip()
            priv_path = input("Путь к закрытому ключу: ").strip()
            sig_path = input("Путь для сохранения подписи (signature.sig): ").strip() or "signature.sig"
            sign_file(file_path, priv_path, sig_path)
        elif choice == "3":
            file_path = input("Путь к файлу: ").strip()
            pub_path = input("Путь к открытому ключу: ").strip()
            sig_path = input("Путь к файлу подписи: ").strip()
            verify_file(file_path, pub_path, sig_path)
        elif choice == "4":
            break
        else:
            print("Неверный выбор")


if __name__ == "__main__":
    main()
    