import math
import random


# ==================== Функции из Лаб. №1 и №2 ====================

def fast_pow(a, x, p):
    """Алгоритм быстрого возведения числа в степень по модулю: a^x mod p"""
    y = 1
    s = a
    for bit in bin(x)[2:]:
        y = (y * y) % p
        if bit == '1':
            y = (y * s) % p
        s = (s * s) % p
    return y


def gcd_extended(a, b):
    """Обобщенный алгоритм Евклида: возвращает gcd(a, b), x, y такие что ax + by = gcd(a, b)"""
    u1, u2, u3 = a, 1, 0
    v1, v2, v3 = b, 0, 1
    while v1 != 0:
        q = u1 // v1
        t1, t2, t3 = u1 % v1, u2 - q * v2, u3 - q * v3
        u1, u2, u3 = v1, v2, v3
        v1, v2, v3 = t1, t2, t3
    return u1, u2, u3


def ferma_test(p, k=100):
    """Тест простоты Ферма"""
    if p <= 1: return False
    if p == 2 or p == 3: return True
    if p % 2 == 0: return False

    for _ in range(k):
        a = random.randint(2, p - 2)
        if fast_pow(a, p - 1, p) != 1:
            return False
    return True


def get_random_prime(min_val=100, max_val=1000):
    """Генерация случайного простого числа с помощью теста Ферма"""
    while True:
        num = random.randint(min_val, max_val)
        if ferma_test(num):
            return num


# ==================== Лабораторная работа №3 ====================
# Система Диффи-Хеллмана

def diffie_hellman_keyboard():
    print('\n[Режим 1: Ввод параметров p, g, X_A, X_B с клавиатуры]')
    p = int(input('Введите простое число p: '))
    g = int(input('Введите первообразный корень g по модулю p: '))
    X_A = int(input('Введите закрытый ключ Алисы X_A (1 < X_A < p-1): '))
    X_B = int(input('Введите закрытый ключ Боба X_B (1 < X_B < p-1): '))

    run_diffie_hellman_process(p, g, X_A, X_B)


def diffie_hellman_auto():
    print('\n[Режим 2: Автоматическая генерация параметров p, g, X_A, X_B]')
    
    # Генерация безопасного простого числа p = 2*q + 1 (или просто большого простого)
    # Для демонстрации сгенерируем простое p в диапазоне [500, 2000]
    while True:
        q = get_random_prime(200, 1000)
        p = 2 * q + 1
        if ferma_test(p):
            break
            
    print(f'Сгенерировано безопасное простое число p = {p} (q = {q})')

    # Генерация первообразного корня g
    # Если p = 2q+1, то g подходит, если 2 <= g < p-1 и g^q mod p != 1
    g = 2
    while g < p - 1:
        if fast_pow(g, q, p) != 1:
            break
        g += 1
    print(f'Сгенерирован первообразный корень g = {g}')

    # Генерация закрытых ключей абонентов
    X_A = random.randint(2, p - 2)
    X_B = random.randint(2, p - 2)
    print(f'Сгенерирован закрытый ключ Алисы X_A = {X_A}')
    print(f'Сгенерирован закрытый ключ Боба X_B = {X_B}')

    run_diffie_hellman_process(p, g, X_A, X_B)


def run_diffie_hellman_process(p, g, X_A, X_B):
    """Вычисление открытых и общих секретных ключей по схеме Диффи-Хеллмана"""
    print('\n--- Процесс обмена ключами Диффи-Хеллмана ---')
    
    # Шаг 1. Вычисление открытых ключей
    Y_A = fast_pow(g, X_A, p)
    Y_B = fast_pow(g, X_B, p)
    
    print(f'Открытый ключ Алисы Y_A = g^X_A mod p = {g}^{X_A} mod {p} = {Y_A}')
    print(f'Открытый ключ Боба   Y_B = g^X_B mod p = {g}^{X_B} mod {p} = {Y_B}')

    # Шаг 2. Вычисление общего секретного ключа
    # Алиса вычисляет Z_AB = (Y_B)^X_A mod p
    Z_AB = fast_pow(Y_B, X_A, p)
    
    # Боб вычисляет Z_BA = (Y_A)^X_B mod p
    Z_BA = fast_pow(Y_A, X_B, p)

    print(f'Алиса вычисляет общий ключ Z_AB = Y_B^X_A mod p = {Z_AB}')
    print(f'Боб вычисляет общий ключ   Z_BA = Y_A^X_B mod p = {Z_BA}')

    if Z_AB == Z_BA:
        print(f'\n Успех! Общий секретный ключ успешно сформирован и равен: {Z_AB}')
    else:
        print('\n Ошибка! Ключи не совпадают.')


# ==================== Главная точка входа ====================

if __name__ == '__main__':
    print('Криптографическая библиотека — Лабораторная работа №3')
    print('Схема построения общего ключа Диффи-Хеллмана')
    print('Выберите режим работы:')
    print('1. Ввод p, g, X_A, X_B с клавиатуры')
    print('2. Автоматическая генерация всех параметров')
    
    choice = input('Ваш выбор (1 или 2): ').strip()

    if choice == '1':
        diffie_hellman_keyboard()
    elif choice == '2':
        diffie_hellman_auto()
    else:
        print('Неверный выбор. Запуск автоматической генерации по умолчанию...')
        diffie_hellman_auto()