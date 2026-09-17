import math
import random


def fast_pow(a, x, p):
  y = 1
  for bit in bin(x)[2:]:
    y = (y * y) % p
    if bit == '1':
      y = (y * a) % p
  return y


def gcd_extended(a, b):
  u1, u2, u3 = a, 1, 0
  v1, v2, v3 = b, 0, 1
  while v1 != 0:
    q = u1 // v1
    t1, t2, t3 = u1 % v1, u2 - q * v2, u3 - q * v3
    u1, u2, u3 = v1, v2, v3
    v1, v2, v3 = t1, t2, t3
  return u1, u2, u3


def ferma_test(p):
    if p <= 1: return False
    if p == 2 or p == 3: return True
    if p % 2 == 0: return False

    for _ in range(100):
        a = random.randint(2, p - 2)
        if fast_pow(a, p - 1, p) != 1:
            return False
            
    return True


def input_from_keyboard():
  print('\n[Ввод с клавиатуры]')
  a = int(input('Введите a: '))
  b = int(input('Введите b: '))
  p = int(input('Введите модуль p (для возведения в степень): '))
  return a, b, p


def generate_random():
  print('\n[Генерация случайных чисел внутри функции]')
  a = random.randint(10, 100)
  b = random.randint(10, 100)
  p = random.randint(100, 1000)
  print('сгенерировано: a = {a}, b = {b}, p = {p}')
  return a, b, p


def generate_primes():
  print(
      '\n[Генерация простых чисел a, b и p с использованием теста простоты'
      ' Ферма]'
  )

  def get_random_prime(min_val=10, max_val=500):
    while True:
      num = random.randint(min_val, max_val)
      if ferma_test(num):
        return num

  a = get_random_prime()
  b = get_random_prime()
  p = get_random_prime(100, 1000)
  print(f'Сгенерированы простые числа: a = {a}, b = {b}, модуль p = {p}')
  return a, b, p

  import math


def baby_step_giant_step(a, y, p):
    root = int(math.isqrt(p))
    if root * root < p:
        root += 1
    
    m, k = 0, 0
    if root * root == p:
        m = root
        k = root
    else:
        s = root + root
        m = 1
        k = s - m
        while m * k <= p:
            m += 1
            k = s - m
            
    print(f"m = {m}")
    print(f"k = {k}")
    
    lit = []
    big = []
    result = []

    for j in range(m):
        x = (fast_pow(y, 1, p) * fast_pow(a, j, p)) % p
        lit.append(x)
        
    for i in range(1, k + 1):
        x = fast_pow(a, m * i, p)
        big.append(x)
        
    pos = {}
    for idx, val in enumerate(big):
        if val not in pos:
            pos[val] = []
        pos[val].append(idx)
        
    count = 1
    for j in range(len(lit)):
        val_lit = lit[j]
        if val_lit in pos:
            for i in pos[val_lit]:
                x = (i + 1) * m - j
                print(f"X({count}) = {x}")
                result.append(x)
                count += 1
                
    return result


if __name__ == '__main__':
    print('Выберите режим работы:')
    print('1. Ввод с клавиатуры')
    print('2. Автоматическая генерация')
    choice = input('Ваш выбор : ')

    if choice == '1':
        a = int(input('Введите a: '))
        y = int(input('Введите y: '))
        p = int(input('Введите p: '))
    else:
        p = 101
        a = 2
        x = random.randint(1, p-1)
        y = fast_pow(a, x, p)
        print(f'Параметры: a={a}, p={p}. Получен y={y} (для x={x})')

    result = baby_step_giant_step(a, y, p)
    
    if result is not None:
        print(f'x = {result}')
        # if fast_pow(a, result[0], p) == y and fast_pow(a, result[1], p):
    else:
        print('Решение не найдено (возможно, a не является первообразным корнем).')