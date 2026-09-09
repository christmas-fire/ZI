import random


def fast_pow(a, x, p):
  """1) Функция быстрого возведения числа в степень по модулю: y = a^x mod p"""
  y = 1
  for bit in bin(x)[2:]:
    y = (y * y) % p
    if bit == '1':
      y = (y * a) % p
  return y


def gcd_extended(a, b):
  """3) Функция, реализующая обобщенный алгоритм Евклида.

  Находит НОД(a, b) и коэффициенты x, y такие, что ax + by = НОД(a, b).
  """
  u1, u2, u3 = a, 1, 0
  v1, v2, v3 = b, 0, 1
  while v1 != 0:
    q = u1 // v1
    t1, t2, t3 = u1 % v1, u2 - q * v2, u3 - q * v3
    u1, u2, u3 = v1, v2, v3
    v1, v2, v3 = t1, t2, t3
  return u1, u2, u3  # возвращает (gcd, x, y)


def ferma_test(p, k=50):
  """2) Функция, реализующая тест простоты Ферма."""
  if p <= 1:
    return False
  if p == 2:
    return True
  if p % 2 == 0:
    return False

  for _ in range(k):
    a = random.randint(2, p - 2)
    # Числа a и p должны быть взаимно просты
    if gcd_extended(a, p)[0] != 1:
      return False
    if fast_pow(a, p - 1, p) != 1:
      return False
  return True


# --- Способы ввода и генерации данных ---


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


# --- Демонстрация работы ---
if __name__ == '__main__':
  # Пример выбора режима работы
  print('Выберите режим работы:')
  print('1. Ввод с клавиатуры')
  print('2. Случайная генерация')
  print('3. Генерация простых чисел')

  choice = input('Ваш выбор (1/2/3): ')

  if choice == '1':
    a, b, p = input_from_keyboard()
  elif choice == '2':
    a, b, p = generate_random()
  else:
    a, b, p = generate_primes()

  # Выполнение функций библиотеки
  print('\n--- Результаты выполнения ---')
  y_pow = fast_pow(a, b, p)
  print(f'1) Быстрое возведение: {a}^{b} mod {p} = {y_pow}')

  is_prime_a = ferma_test(a)
  is_prime_b = ferma_test(b)
  print(
      f'2) Тест Ферма для a ({a}): {"простое" if is_prime_a else "составное"}'
  )
  print(
      f'   Тест Ферма для b ({b}): {"простое" if is_prime_b else "составное"}'
  )

  gcd_val, x, y = gcd_extended(a, b)
  print(f'3) Обобщенный алгоритм Евклида для ({a}, {b}):')
  print(
      f'   НОД({a}, {b}) = {gcd_val}, коэффициенты: x = {x}, y = {y} (Проверка:'
      f' {a}*({x}) + {b}*({y}) = {a*x + b*y})'
  )
  