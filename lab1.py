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
  print(f'сгенерировано: a = {a}, b = {b}, p = {p}')
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


if __name__ == '__main__':
    print('1. Быстрое возведение в степень')
    print('2. Тест простоты (Ферма)')
    print('3. Обобщенный алгоритм Евклида')
    choice_action = input('Ваш выбор : ')

    print('1. Ввод с клавиатуры')
    print('2. Случайная генерация')
    print('3. Генерация простых чисел (для Евклида)')
    choice_data = input('Ваш выбор : ')

    if choice_action == '3':
        if choice_data == '1':
            a = int(input('Введите a: '))
            b = int(input('Введите b: '))
        elif choice_data == '2':
            a, b = random.randint(10, 100), random.randint(10, 100)
        else:
            a, b, p = generate_primes()
        p = None
        gcd_val, x, y = gcd_extended(a, b)
        print(f'{gcd_val}, x={x}, y={y}')  

    if choice_action == '2':
      if choice_data == '1':
        p = int(input('Введите модуль p: '))
        is_p = ferma_test(p)
        print(f'Тест Ферма для : {"простое" if is_p else "составное"}')
      elif choice_data == '2':
        p = generate_random()
        is_p = ferma_test(p)
        print(f'Тест Ферма для : {"простое" if is_p else "составное"}')
      else:
        p = get_random_prime()
        is_p = ferma_test(p)
        print(f'Тест Ферма для : {"простое" if is_p else "составное"}')

    if choice_action == '1':
        if choice_data == '1':
            a = int(input('Введите a: '))
            b = int(input('Введите b: '))
            p = int(input('Введите модуль p: '))
        elif choice_data == '2':
            a, b, c = random.randint(10, 100), random.randint(10, 100), random.randint(10, 100)
        else:
            a, b, c = generate_primes()
        y_pow = fast_pow(a, b, p)
        print(f'Результат: {a}^{b} mod {p} = {y_pow}')

    # else:
    #     if choice_data == '1':
    #         a = int(input('Введите a: '))
    #         b = int(input('Введите b: '))
    #         p = int(input('Введите модуль p: '))
    #     elif choice_data == '2':
    #         a, b, p = generate_random()
    #     else:
    #         a, b, p = generate_primes()

    # print('\n--- Результаты выполнения ---')
    # if choice_action == '1':
    #     y_pow = fast_pow(a, b, p)
    #     print(f'Результат: {a}^{b} mod {p} = {y_pow}')
        
    # elif choice_action == '2':
    #   if choice_data == '1':
    #     p = int(input('Введите модуль p: '))
    #     is_p = ferma_test(p)
    #     print(f'Тест Ферма для : {"простое" if is_p else "составное"}')
    #   elif choice_data == '2':
    #     p = generate_random()
    #     is_p = ferma_test(p)
    #     print(f'Тест Ферма для : {"простое" if is_p else "составное"}')
    #   else:
    #     p = get_random_prime()
    #     is_p = ferma_test(p)
    #     print(f'Тест Ферма для : {"простое" if is_p else "составное"}')



        
    # elif choice_action == '3':
    #     gcd_val, x, y = gcd_extended(a, b)
    #     print(f'{gcd_val}, x={x}, y={y}')  