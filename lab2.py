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


def ferma_test(p, k=50):
  if p <= 1:
    return False
  if p == 2:
    return True
  if p % 2 == 0:
    return False

  for _ in range(k):
    a = random.randint(2, p - 2)
    if gcd_extended(a, p)[0] != 1:
      return False
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
    m = math.ceil(math.sqrt(p))

    baby_steps = {}
    curr = y % p
    for j in range(m):
        baby_steps[curr] = j
        curr = (curr * a) % p
        
    a_m = fast_pow(a, m, p)
    
    giant_step = a_m
    for i in range(1, m + 1):
        if giant_step in baby_steps:
            j = baby_steps[giant_step]
            x = i * m - j
            return x
        giant_step = (giant_step * a_m) % p
        
    return None


if __name__ == '__main__':
    print('Выберите режим работы:')
    print('1. Ввод с клавиатуры')
    print('2. Автоматическая генерация')
    choice = input('Ваш выбор (1/2): ')

    if choice == '1':
        a = int(input('Введите a: '))
        y = int(input('Введите y: '))
        p = int(input('Введите p: '))
    else:
        p = 101
        a = 2
        x = random.randint(1, p-1)
        y = fast_pow(a, x, p)
        print(f'Сгенерированы параметры: a={a}, p={p}. Получен y={y} (для x={x})')

    print(f'\nЗапуск поиска дискретного логарифма для {a}^x = {y} (mod {p})...')
    result = baby_step_giant_step(a, y, p)
    
    if result is not None:
        print(f'Успешно! Найденное x = {result}')
        if fast_pow(a, result, p) == y:
            print('Проверка пройдена: a^x mod p == y')
    else:
        print('Решение не найдено (возможно, a не является первообразным корнем).')