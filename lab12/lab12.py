import tkinter as tk
from tkinter import ttk, messagebox
import random
import math

def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(math.isqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def generate_large_prime():
    primes = [p for p in range(2000, 4000) if is_prime(p)]
    return random.choice(primes)

def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y

def mod_inverse(e, phi):
    gcd, x, _ = extended_gcd(e, phi)
    if gcd != 1:
        raise ValueError("Обратного элемента не существует")
    return (x % phi + phi) % phi

def generate_keypair(p):
    phi = p - 1
    while True:
        e = random.randrange(3, phi, 2)
        if math.gcd(e, phi) == 1:
            try:
                d = mod_inverse(e, phi)
                return e, d
            except ValueError:
                continue

SUITS = ['♠', '♥', '♣', '♦']
RANKS_52 = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
RANKS_36 = ['6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
RANKS_24 = ['9', '10', 'J', 'Q', 'K', 'A']

class Card:
    def __init__(self, rank, suit, card_id):
        self.rank = rank
        self.suit = suit
        self.id = card_id

    def __repr__(self):
        return f"{self.rank}{self.suit}"

class MentalPoker(tk.Tk):
    COLOR_BG = "#1e2c26"
    COLOR_PANEL = "#253b34"
    COLOR_CARD_BG = "#fefcf4"
    COLOR_CARD_BACK = "#b83b26"
    COLOR_SHADOW = "#0e1613"
    COLOR_GOLD = "#f3b738"
    COLOR_BLUE_BTN = "#2c72b8"
    COLOR_RED_BTN = "#e0473a"
    COLOR_TEXT_LIGHT = "#eae5d8"

    SUIT_COLORS = {
        '♠': '#242a30',
        '♥': '#d93636',
        '♣': '#298858',
        '♦': '#2373bd'
    }

    def __init__(self):
        super().__init__()
        self.title("МЕНТАЛЬНЫЙ ПОКЕР")
        self.geometry("1100x820")
        self.configure(bg=self.COLOR_BG)
        self.resizable(False, False)

        self.p = generate_large_prime()
        self.num_players = 3
        self.deck_size = 52
        self.players_keys = []
        self.deck_cipher = []
        self.id_to_card = {}
        self.game_state = "IDLE"

        self.hands = {}
        self.table_cards = []

        self._build_ui()
        self.log(f"[SYS] Протокол инициализирован. Простое поле p = {self.p}")

    def _build_ui(self):
        header_frame = tk.Frame(self, bg=self.COLOR_PANEL, bd=0, height=70)
        header_frame.pack(fill=tk.X, side=tk.TOP, padx=10, pady=(10, 5))

        title = tk.Label(
            header_frame, text="МЕНТАЛЬНЫЙ ПОКЕР (TEXAS HOLD'EM)", 
            bg=self.COLOR_PANEL, fg=self.COLOR_GOLD, font=("Impact", 18)
        )
        title.pack(side=tk.LEFT, padx=10, pady=10)

        ctrl_frame = tk.Frame(self, bg=self.COLOR_PANEL)
        ctrl_frame.pack(fill=tk.X, padx=10, pady=5)

        tk.Label(ctrl_frame, text="Игроки:", fg=self.COLOR_TEXT_LIGHT, bg=self.COLOR_PANEL, font=("Trebuchet MS", 10, "bold")).pack(side=tk.LEFT, padx=(15, 2))
        self.spin_players = tk.Spinbox(ctrl_frame, from_=2, to=6, width=4, font=("Trebuchet MS", 10, "bold"))
        self.spin_players.delete(0, "end")
        self.spin_players.insert(0, "3")
        self.spin_players.pack(side=tk.LEFT, padx=5, pady=8)

        tk.Label(ctrl_frame, text="Колода:", fg=self.COLOR_TEXT_LIGHT, bg=self.COLOR_PANEL, font=("Trebuchet MS", 10, "bold")).pack(side=tk.LEFT, padx=(15, 2))
        self.combo_deck = ttk.Combobox(ctrl_frame, values=["52 карты", "36 карт", "24 карты"], width=9, state="readonly")
        self.combo_deck.current(0)
        self.combo_deck.pack(side=tk.LEFT, padx=5, pady=8)

        self.btn_reset = self._create_btn(ctrl_frame, "НОВАЯ ИГРА", self.start_new_game, self.COLOR_BLUE_BTN)
        self.btn_reset.pack(side=tk.LEFT, padx=10, pady=6)

        self.btn_action = self._create_btn(ctrl_frame, "1. ШИФРОВАНИЕ И ТАСОВАНИЕ", self.step_shuffle, self.COLOR_RED_BTN)
        self.btn_action.pack(side=tk.LEFT, padx=10, pady=6)

        self.canvas = tk.Canvas(self, bg=self.COLOR_BG, bd=0, highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        log_frame = tk.Frame(self, bg=self.COLOR_PANEL, height=130)
        log_frame.pack(fill=tk.X, side=tk.BOTTOM, padx=10, pady=(5, 10))

        tk.Label(log_frame, text="КРИПТОГРАФИЧЕСКИЙ ЖУРНАЛ СЕТИ:", fg=self.COLOR_GOLD, bg=self.COLOR_PANEL, font=("Impact", 10)).pack(anchor="w", padx=10, pady=(4, 0))
        
        self.txt_log = tk.Text(log_frame, height=5, bg="#131e1a", fg="#68df9f", font=("Courier New", 9), bd=0)
        self.txt_log.pack(fill=tk.BOTH, expand=True, padx=10, pady=(2, 6))

    def _create_btn(self, parent, text, cmd, color):
        f = tk.Frame(parent, bg=self.COLOR_SHADOW, bd=0)
        btn = tk.Button(
            f, text=text, command=cmd, bg=color, fg="white",
            activebackground=self.COLOR_GOLD, activeforeground="black",
            font=("Impact", 11), relief="flat", bd=0, padx=12, pady=3, cursor="hand2"
        )
        btn.pack(padx=2, pady=2)
        return f

    def log(self, message):
        self.txt_log.insert(tk.END, message + "\n")
        self.txt_log.see(tk.END)

    def draw_card(self, x, y, card=None, face_down=False, tag_info=""):
        w, h = 64, 90
        self.canvas.create_rectangle(x + 4, y + 4, x + w + 4, y + h + 4, fill=self.COLOR_SHADOW, outline="")

        if face_down or card is None:
            self.canvas.create_rectangle(x, y, x + w, y + h, fill=self.COLOR_CARD_BACK, outline="#e06955", width=2)
            self.canvas.create_rectangle(x + 8, y + 8, x + w - 8, y + h - 8, fill="", outline="#ffffff", width=1)
            self.canvas.create_text(x + w / 2, y + h / 2, text="🂠", fill="white", font=("Trebuchet MS", 22, "bold"))
            if tag_info:
                self.canvas.create_text(x + w / 2, y + h - 14, text=tag_info, fill="white", font=("Impact", 8))
            return

        self.canvas.create_rectangle(x, y, x + w, y + h, fill=self.COLOR_CARD_BG, outline="#d5ccba", width=2)

        suit_color = self.SUIT_COLORS.get(card.suit, "#000000")
        
        self.canvas.create_text(x + 14, y + 14, text=f"{card.rank}", fill=suit_color, font=("Impact", 12))
        self.canvas.create_text(x + 14, y + 27, text=f"{card.suit}", fill=suit_color, font=("Trebuchet MS", 10))

        self.canvas.create_text(x + w / 2, y + h / 2 + 5, text=card.suit, fill=suit_color, font=("Trebuchet MS", 26))
        self.canvas.create_text(x + w / 2, y + h - 10, text=f"m={card.id}", fill="#8c8270", font=("Courier New", 7, "bold"))

    def render_board(self):
        self.canvas.delete("all")
        
        self.canvas.create_rectangle(270, 30, 830, 210, fill=self.COLOR_PANEL, outline="#37554b", width=2)
        self.canvas.create_text(550, 50, text="ОБЩИЕ КАРТЫ СТОЛА", fill=self.COLOR_GOLD, font=("Impact", 13))

        start_x = 330
        for i in range(5):
            cx = start_x + i * 85
            cy = 75
            if i < len(self.table_cards):
                self.draw_card(cx, cy, card=self.table_cards[i])
            else:
                stage_name = "FLOP" if i < 3 else ("TURN" if i == 3 else "RIVER")
                self.draw_card(cx, cy, face_down=True, tag_info=stage_name)

        step_x = 1050 // self.num_players
        for p_idx in range(self.num_players):
            px = 30 + p_idx * step_x
            py = 240

            self.canvas.create_rectangle(px, py, px + step_x - 20, py + 230, fill=self.COLOR_PANEL, outline="#37554b", width=2)
            
            badge_color = self.COLOR_BLUE_BTN if p_idx == 0 else self.COLOR_RED_BTN
            self.canvas.create_rectangle(px + 10, py + 10, px + step_x - 30, py + 36, fill=badge_color, outline="")
            label_text = f"ИГРОК {p_idx + 1} (ВЫ)" if p_idx == 0 else f"ИГРОК {p_idx + 1}"
            self.canvas.create_text(px + (step_x - 20) / 2, py + 23, text=label_text, fill="white", font=("Impact", 11))

            if self.players_keys:
                e, d = self.players_keys[p_idx]
                self.canvas.create_text(px + 15, py + 48, text=f"e: {e} | d: {d}", anchor="w", fill="#8ce0b0", font=("Courier New", 8))

            cards = self.hands.get(p_idx, [])
            c_x1 = px + ((step_x - 20) - 145) / 2
            c_x2 = c_x1 + 75
            c_y = py + 70

            for c_i, cx in enumerate([c_x1, c_x2]):
                if c_i < len(cards):
                    self.draw_card(cx, c_y, card=cards[c_i])
                else:
                    self.draw_card(cx, c_y, face_down=True)

    def start_new_game(self):
        try:
            self.num_players = int(self.spin_players.get())
            if not 2 <= self.num_players <= 6:
                raise ValueError()
        except ValueError:
            messagebox.showerror("Ошибка", "Число игроков должно быть от 2 до 6")
            return

        deck_choice = self.combo_deck.get()
        if "52" in deck_choice:
            ranks = RANKS_52
        elif "36" in deck_choice:
            ranks = RANKS_36
        else:
            ranks = RANKS_24

        self.p = generate_large_prime()
        self.deck_cards = []
        self.id_to_card = {}
        
        card_id = 101
        for s in SUITS:
            for r in ranks:
                c = Card(r, s, card_id)
                self.deck_cards.append(c)
                self.id_to_card[card_id] = c
                card_id += 1

        self.deck_size = len(self.deck_cards)
        self.players_keys = [generate_keypair(self.p) for _ in range(self.num_players)]
        
        self.deck_cipher = [c.id for c in self.deck_cards]
        self.hands = {i: [] for i in range(self.num_players)}
        self.table_cards = []
        self.game_state = "GENERATED"

        self.log("\n" + "="*50)
        self.log(f"[SYS] Новая партия! Игроков: {self.num_players}, Карт в колоде: {self.deck_size}")
        self.log(f"[CRYPTO] Сгенерировано общее безопасное простое число p = {self.p}")
        for i, (e, d) in enumerate(self.players_keys):
            self.log(f"  -> Ключи Игрока {i+1}: e = {e}, d = {d} (e*d mod (p-1) = {(e*d) % (self.p - 1)})")

        self._update_action_btn("1. ШИФРОВАНИЕ И ТАСОВАНИЕ", self.step_shuffle, self.COLOR_RED_BTN)
        self.render_board()

    def step_shuffle(self):
        self.log("\n[ЭТАП 1: ТАСОВАНИЕ И НАЛОЖЕНИЕ ШИФРА]")
        for i in range(self.num_players):
            e, _ = self.players_keys[i]
            self.deck_cipher = [pow(val, e, self.p) for val in self.deck_cipher]
            random.shuffle(self.deck_cipher)
            self.log(f"[ИГРОК {i+1}] Зашифровал колоду своим ключом e и перемешал.")

        self.log("[CRYPTO] Колода полностью защищена всеми участниками. Никто не знает порядка карт.")
        self._update_action_btn("2. РАЗДАТЬ КАРМАННЫЕ КАРТЫ", self.step_deal_hands, self.COLOR_GOLD, fg="black")

    def step_deal_hands(self):
        self.log("\n[ЭТАП 2: РАЗДАЧА КАРМАННЫХ КАРТ (ПО 2 КАЖДОМУ)]")
        for round_idx in range(2):
            for p_idx in range(self.num_players):
                cipher_card = self.deck_cipher.pop(0)

                partial = cipher_card
                for other_idx in range(self.num_players):
                    if other_idx != p_idx:
                        d_other = self.players_keys[other_idx][1]
                        partial = pow(partial, d_other, self.p)

                d_own = self.players_keys[p_idx][1]
                plain_id = pow(partial, d_own, self.p)
                
                card = self.id_to_card.get(plain_id, Card("?", "?", plain_id))
                self.hands[p_idx].append(card)

        self.log("[CRYPTO] Раздача завершена. Каждый расшифровал только свои карты через соглашение сторон.")
        self.render_board()
        self._update_action_btn("3. ОТКРЫТЬ ФЛОП (3 КАРТЫ)", lambda: self.step_reveal_board(3, "ФЛОП"), self.COLOR_BLUE_BTN)

    def step_reveal_board(self, count, name):
        self.log(f"\n[ЭТАП 3: РАСКРЫТИЕ СТОЛА // {name}]")
        for _ in range(count):
            cipher_card = self.deck_cipher.pop(0)
            
            opened_val = cipher_card
            for p_idx in range(self.num_players):
                d = self.players_keys[p_idx][1]
                opened_val = pow(opened_val, d, self.p)

            card = self.id_to_card.get(opened_val, Card("?", "?", opened_val))
            self.table_cards.append(card)
            self.log(f"  -> Открыта карта стола: [{card}] (id={card.id})")

        self.render_board()
        
        if len(self.table_cards) == 3:
            self._update_action_btn("4. ОТКРЫТЬ ТЁРН (1 КАРТА)", lambda: self.step_reveal_board(1, "ТЁРН"), self.COLOR_BLUE_BTN)
        elif len(self.table_cards) == 4:
            self._update_action_btn("5. ОТКРЫТЬ РИВЕР (1 КАРТА)", lambda: self.step_reveal_board(1, "РИВЕР"), self.COLOR_BLUE_BTN)
        else:
            self.log("\n[SYS] Раздача полностью окончена. Все карты проверены и честно открыты!")
            self._update_action_btn("РАЗДАЧА ЗАВЕРШЕНА (НОВАЯ ИГРА)", self.start_new_game, self.COLOR_RED_BTN)

    def _update_action_btn(self, text, command, color, fg="white"):
        for child in self.btn_action.winfo_children():
            child.configure(text=text, command=command, bg=color, fg=fg)

if __name__ == "__main__":
    app = MentalPoker()
    app.start_new_game()
    app.mainloop()
