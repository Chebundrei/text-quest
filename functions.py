




































import random
import time
import sys
import os


# ==========================================
# СОСТОЯНИЕ
# ==========================================

inventory = []
hp = 100
max_hp = 100
gold = 50
day = 1
xp = 0
level = 1

castle_found = False
wolf_friend = False
fairy_friend = False
unicorn_friend = False
troll_defeated = False
dragon_defeated = False
undead_defeated = False
princess_saved = False
strange_key = False
escape_ready = False

reward_counts = {}


def reset_state():
    global inventory, hp, max_hp, gold, day, xp, level
    global castle_found, wolf_friend, fairy_friend, unicorn_friend
    global troll_defeated, dragon_defeated, undead_defeated
    global princess_saved, strange_key, escape_ready
    global reward_counts

    inventory = []
    hp = 100
    max_hp = 100
    gold = 50
    day = 1
    xp = 0
    level = 1

    castle_found = False
    wolf_friend = False
    fairy_friend = False
    unicorn_friend = False
    troll_defeated = False
    dragon_defeated = False
    undead_defeated = False
    princess_saved = False
    strange_key = False
    escape_ready = False

    reward_counts = {}


def can_reward(key, limit=2):
    return reward_counts.get(key, 0) < limit


def mark_reward(key):
    reward_counts[key] = reward_counts.get(key, 0) + 1


# ==========================================
# ЗВУК И ПАУЗЫ
# ==========================================

def sound(name):
    try:
        import winsound
    except ImportError:
        time.sleep(0.05)
        return
    paths = {
        "click": r"C:\Users\cl\Desktop\soundds\click.wav",
        "error": r"C:\Users\cl\Desktop\soundds\error.wav",
        "lose":  r"C:\Users\cl\Desktop\soundds\lose.wav",
        "win":   r"C:\Users\cl\Desktop\soundds\win.wav",
    }
    p = paths.get(name)
    if p and os.path.exists(p):
        try:
            winsound.PlaySound(p, winsound.SND_FILENAME | winsound.SND_ASYNC)
        except Exception:
            pass


def slow_print(text, delay=0.02):
    if text is None:
        text = ""
    for ch in text:
        sys.stdout.write(ch)
        sys.stdout.flush()
        time.sleep(delay)
    print()


def pause(seconds=1.0):
    time.sleep(seconds)


# ==========================================
# ASCII-ГРАФИКА
# ==========================================

ASCII_ART = {
"Развилка": r"""
         /\
        /  \
       /    \
      /      \
     /   /\   \
    /   /  \   \
   /___/    \___\
       |    |
   /\  |    |  /\
  /  \ |    | /  \
        РАЗВИЛКА
""",
"Лес": r"""
    /\  /\  /\
   /  \/  \/  \
  /   /\  /\   \
 /___/  \/  \___\
 /|\ /|\  /|\ /|\
        ЛЕС
""",
"Деревня": r"""
       /\
      /  \
     /____\
     | [] |
  ___|____|___
 |_____________|
    ДЕРЕВНЯ
""",
"Болото": r"""
    ~~~ ~~~ ~~~ ~~~
  _|_  _|_  _|_  _|_
 |   ||   ||   ||   |
 |___||___||___||___|
      БОЛОТО
""",
"Горы": r"""
        /\
       /  \
      /    \
     /  /\  \
   /__/____\__\
   |    /\    |
   |__/____\__|
      ГОРЫ
""",
"Море": r"""
~~~~~~~~~~~~~~~~~~~~~~~
  ~~~ ~~~ ~~~ ~~~ ~~~
 ~~~~~~~~ ~~~~~~~~
      ~~~~~~~~
        МОРЕ
""",
"Замок": r"""
        |\
       _|___|_
      |       |
      | [] [] |
      |  ___  |
      |_|___|_|
      |_______|
       ЗАМОК
""",
"Драконье логово": r"""
   __________________
  |   /\        /\   |
  |  /  \      /  \  |
  | | () |    | () | |
  |__\/________\/____|
    ДРАКОНЬЕ ЛОГОВО
""",
"Кладбище": r"""
    _____   _____
   |  +  | |  +  |
   |_____| |_____|
    КЛАДБИЩЕ
""",
"Руины": r"""
  _   _   _   _
 | |_| |_| |_| |
 |  _   _   _  |
 |_| |_| |_| |_|
     РУИНЫ
""",
"Лес фей": r"""
   *   .   *   .   *
  .  *  .  *  .  *  .
 *   .   *   .   *   .
    ЛЕС ФЕЙ
""",
"Долина единорогов": r"""
     /\   /\
    /  \_/  \
   |  o   o  |
    \  ===  /
     |_____|
   ДОЛИНА ЕДИНОРОГОВ
""",
"Победа": r"""
   *  *  *  *  *
  *  ПОБЕДА  *
   *  *  *  *  *
""",
"Поражение": r"""
   _______________
  |               |
  |  ТЫ ПРОИГРАЛ  |
  |_______________|
"""
}


def show_location(name):
    art = ASCII_ART.get(name)
    if art:
        print(art)


# ==========================================
# СТАТУС
# ==========================================

def show_status():
    bar = int(hp / max_hp * 20)
    bar = max(0, min(20, bar))
    line = "[" + "|" * bar + "." * (20 - bar) + "]"
    print()
    print("========== СТАТУС ==========")
    print(f"HP {hp}/{max_hp} {line}")
    print(f"Золото: {gold}   День: {day}   Ур.{level} (опыт {xp}/{level*10})")
    if inventory:
        print("Инвентарь: " + ", ".join(inventory[-4:]))
    else:
        print("Инвентарь: —")
    print("============================")


# ==========================================
# ДЕЙСТВИЯ
# ==========================================

def add_item(item):
    inventory.append(item)


def add_gold(amount):
    global gold
    gold += amount


def add_xp(amount):
    global xp, level, max_hp, hp
    xp += amount
    safety = 0
    while xp >= level * 10 and safety < 100:
        xp -= level * 10
        level += 1
        max_hp += 10
        hp = max_hp
        safety += 1


def heal(amount):
    global hp
    hp = min(max_hp, hp + amount)


def damage(amount):
    global hp
    hp -= amount
    if hp < 0:
        hp = 0
    return hp <= 0


# ==========================================
# ВВОД
# ==========================================

def ask_choice(max_choice):
    while True:
        s = input("Твой выбор: ").strip()
        if not s:
            sound("error")
            print("Введи число!")
            continue
        try:
            v = int(s)
        except ValueError:
            sound("error")
            print("Введи число!")
            continue
        if 1 <= v <= max_choice:
            return v
        sound("error")
        print(f"Введи число от 1 до {max_choice}")


def ask_yes_no(prompt):
    while True:
        s = input(prompt).strip().lower()
        if s in ("д", "да", "y", "yes"):
            return True
        if s in ("н", "нет", "n", "no"):
            return False
        sound("error")
        print("Ответь 'д' или 'н'.")


# ==========================================
# ПОДВАЛ
# ==========================================

def explore_basement(place_name):
    global strange_key, escape_ready
    show_location("Руины")
    slow_print(f"Ты спускаешься в подвал {place_name}.")

    while True:
        show_status()
        print("1 - Осмотреть полки")
        print("2 - Открыть сундук")
        print("3 - Осмотреть дверь")
        print("4 - Подняться обратно")
        a = ask_choice(4)

        if a == 1:
            if random.random() < 0.4:
                add_item("Факел")
                slow_print("Ты нашёл факел.")
            else:
                slow_print("Ничего интересного.")
            input("Enter...")

        elif a == 2:
            if not can_reward("basement_chest"):
                slow_print("Сундук уже пуст.")
                input("Enter...")
                continue
            mark_reward("basement_chest")
            roll = random.random()
            if roll < 0.2 and not strange_key:
                strange_key = True
                add_item("Странный ключ")
                slow_print("*** В сундуке лежит СТРАННЫЙ КЛЮЧ! ***")
            elif roll < 0.6:
                g = random.randint(30, 100)
                add_gold(g)
                slow_print(f"Ты нашёл золото! +{g}.")
            else:
                damage(random.randint(3, 10))
                slow_print("Из сундука выпрыгнули пауки! -HP.")
            input("Enter...")

        elif a == 3:
            slow_print("В углу массивная железная дверь.")
            if strange_key:
                print("У тебя есть Странный ключ!")
                print("1 - Открыть дверь")
                print("2 - Отойти")
                b = ask_choice(2)
                if b == 1:
                    escape_ready = True
                    slow_print("Ключ повернулся. Дверь открыта. Ты видишь белый свет!")
            else:
                slow_print("Нужен необычный ключ.")
            input("Enter...")

        else:
            break