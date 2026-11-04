import hashlib
import math
import secrets


def is_prime(n: int, k: int = 40) -> bool:
    if n < 2:
        return False
    if n in (2, 3):
        return True
    if n % 2 == 0:
        return False

    r, s = 0, n - 1
    while s % 2 == 0:
        r += 1
        s //= 2

    for _ in range(k):
        a = secrets.randbelow(n - 3) + 2
        x = pow(a, s, n)
        if x in (1, n - 1):
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True


def generate_prime(bits: int = 512) -> int:
    while True:
        candidate = (secrets.randbits(bits) | (1 << (bits - 1))) | 1
        if is_prime(candidate):
            return candidate


def extended_gcd(a: int, b: int):
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y


def mod_inverse(a: int, m: int) -> int:
    gcd, x, _ = extended_gcd(a, m)
    if gcd != 1:
        raise ValueError("Обратного элемента не существует!")
    return (x % m + m) % m


class VotingServer:

    def __init__(self, key_bits: int = 512):
        self.p = generate_prime(key_bits // 2)
        self.q = generate_prime(key_bits // 2)
        self.n = self.p * self.q
        self.phi = (self.p - 1) * (self.q - 1)

        self.e = 65537
        while math.gcd(self.e, self.phi) != 1:
            self.e = secrets.randbelow(self.phi - 2) + 2

        self.d = mod_inverse(self.e, self.phi)

        self.registered_voters = set()
        self.accepted_bulletins = set()
        self.results = {"Да": 0, "Нет": 0, "Воздержался": 0}

    @property
    def public_key(self):
        return self.e, self.n

    def register_and_blind_sign(
        self, voter_id: str, blinded_message: int
    ) -> int:
        if voter_id in self.registered_voters:
            raise ValueError(
                f"Ошибка: Избиратель '{voter_id}' уже получал подписной бюллетень!"
            )

        self.registered_voters.add(voter_id)
        blind_signature = pow(blinded_message, self.d, self.n)
        return blind_signature

    def tally_vote(self, raw_bulletin: str, signature: int) -> bool:
        m = (
            int(hashlib.sha256(raw_bulletin.encode("utf-8")).hexdigest(), 16)
            % self.n
        )
        v = pow(signature, self.e, self.n)

        if v != m:
            print("[-] ОШИБКА: Подпись бюллетеня недействительна!")
            return False

        if raw_bulletin in self.accepted_bulletins:
            print(
                "[-] ОШИБКА: Попытка повторного голосования с тем же бюллетенем!"
            )
            return False

        vote = raw_bulletin.split("_")[-1]
        if vote in self.results:
            self.accepted_bulletins.add(raw_bulletin)
            self.results[vote] += 1
            return True
        else:
            print("[-] ОШИБКА: Некорректный вариант ответа в бюллетене!")
            return False


class VoterClient:

    def __init__(self, voter_id: str, server_public_key: tuple):
        self.voter_id = voter_id
        self.e, self.n = server_public_key
        self.r = None
        self.bulletin = None
        self.m = None
        self.signature = None

    def prepare_blinded_ballot(self, choice: str) -> int:
        nonce = secrets.token_hex(16)
        self.bulletin = f"{nonce}_{choice}"
        self.m = (
            int(hashlib.sha256(self.bulletin.encode("utf-8")).hexdigest(), 16)
            % self.n
        )

        while True:
            self.r = secrets.randbelow(self.n - 2) + 2
            if math.gcd(self.r, self.n) == 1:
                break

        r_pow_e = pow(self.r, self.e, self.n)
        blinded_message = (self.m * r_pow_e) % self.n
        return blinded_message

    def unblind_signature(self, blind_signature: int) -> int:
        r_inv = mod_inverse(self.r, self.n)
        self.signature = (blind_signature * r_inv) % self.n
        return self.signature

    def get_signed_ballot(self):
        return self.bulletin, self.signature


if __name__ == "__main__":
    print("=" * 70)
    print("ДЕМОНСТРАЦИЯ СИСТЕМЫ ГОЛОСОВАНИЯ СО 'СЛЕПОЙ' ПОДПИСЬЮ ЧАУМА")
    print("=" * 70)

    server = VotingServer(key_bits=512)
    e, n = server.public_key
    print("\n[СЕРВЕР] Сгенерированы параметры RSA:")
    print(f"  • p: {server.p}")
    print(f"  • q: {server.q}")
    print(f"  • Открытый модуль (n): {n}")
    print(f"  • Открытая экспонента (e): {e}")
    print(f"  • Закрытая экспонента (d): {server.d}")

    voter = VoterClient(
        voter_id="Иванов И.И. (Паспорт: 1234-567890)",
        server_public_key=server.public_key,
    )

    options = ["Да", "Нет", "Воздержался"]
    print(f"\nВопрос: 'Одобряете ли вы принятие нового законопроекта?'")
    print(f"Варианты ответа: {options}")

    chosen_option = "Да"
    print(f"\n[КЛИЕНТ] Избиратель выбрал: '{chosen_option}'")

    blinded_msg = voter.prepare_blinded_ballot(chosen_option)
    print(f"[КЛИЕНТ] Сформирован бюллетень: {voter.bulletin}")
    print(f"  • Хэш бюллетеня (m): {voter.m}")
    print(f"  • Случайный маскирующий множитель (r): {voter.r}")
    print(f"  • Замаскированное сообщение (m'): {blinded_msg}")

    print(f"\n[СЕРВЕР] Избиратель {voter.voter_id} запросил подпись бюллетеня.")
    print("  • Сервер видит только m' и НЕ знает, за что голосует гражданин!")
    blind_sig = server.register_and_blind_sign(voter.voter_id, blinded_msg)
    print(f"  • Вычислена слепая подпись (s'): {blind_sig}")

    valid_sig = voter.unblind_signature(blind_sig)
    print(f"\n[КЛИЕНТ] Снятие ослепления: s = s' * r^(-1) mod n")
    print(f"  • Итоговая цифровая подпись RSA под бюллетенем (s): {valid_sig}")

    raw_ballot, ballot_sig = voter.get_signed_ballot()
    print(f"\n[АНОНИМНЫЙ КАНАЛ] Отправка голоса на сервер подсчёта...")
    print(f"  • Передаются только: ({raw_ballot}, s)")

    success = server.tally_vote(raw_ballot, ballot_sig)
    if success:
        print("[СЕРВЕР] Подпись верифицирована! Голос успешно учтен.")
    else:
        print("[СЕРВЕР] Бюллетень отклонён.")

    print(
        "\n--- Проверка защиты: попытка повторного вброса того же бюллетеня ---"
    )
    server.tally_vote(raw_ballot, ballot_sig)

    print(
        "\n--- Проверка защиты: попытка повторного получения подписи тем же лицом ---"
    )
    try:
        server.register_and_blind_sign(voter.voter_id, blinded_msg)
    except ValueError as err:
        print(err)

    print("\n" + "=" * 70)
    print("ИТОГИ ГОЛОСОВАНИЯ НА СЕРВЕРЕ:")
    for opt, cnt in server.results.items():
        print(f"  {opt}: {cnt}")
    print("=" * 70)
    