# ==========================================
# functions.py
# Звук, ASCII, общие функции, локации, подвал
# ==========================================

import random
import sys
import time
import os
import struct
import ctypes

# ==========================================
# ЗВУК
# ==========================================

SOUND_DIR = r"C:\Users\cl\Desktop\soundds"
SOUND_TYPING = os.path.join(SOUND_DIR, "typing.wav")
SOUND_ERROR  = os.path.join(SOUND_DIR, "error.wav")
SOUND_LOSE   = os.path.join(SOUND_DIR, "lose.wav")

try:
    print("=== ПРОВЕРКА ЗВУКОВ ===")
    print("Папка:", SOUND_DIR)
    print("Существует:", os.path.isdir(SOUND_DIR))
except Exception:
    pass


def _is_pcm_wav(path):
    try:
        with open(path, "rb") as fp:
            head = fp.read(12)
        return head[:4] == b"RIFF" and head[8:12] == b"WAVE"
    except Exception:
        return False


def _convert_to_pcm_wav(src_path, dst_path):
    try:
        import miniaudio
    except ImportError:
        return False
    try:
        decoded = miniaudio.decode_file(src_path)
        pcm_bytes = decoded.samples.tobytes()
        with open(dst_path, "wb") as fp:
            data_size = len(pcm_bytes)
            byte_rate = decoded.sample_rate * decoded.nchannels * 2
            block_align = decoded.nchannels * 2
            fp.write(b"RIFF")
            fp.write(struct.pack("<I", 36 + data_size))
            fp.write(b"WAVE")
            fp.write(b"fmt ")
            fp.write(struct.pack("<I", 16))
            fp.write(struct.pack("<H", 1))
            fp.write(struct.pack("<H", decoded.nchannels))
            fp.write(struct.pack("<I", decoded.sample_rate))
            fp.write(struct.pack("<I", byte_rate))
            fp.write(struct.pack("<H", block_align))
            fp.write(struct.pack("<H", 16))
            fp.write(b"data")
            fp.write(struct.pack("<I", data_size))
            fp.write(pcm_bytes)
        return True
    except Exception:
        return False


try:
    for _path in (SOUND_TYPING, SOUND_ERROR, SOUND_LOSE):
        if not os.path.exists(_path):
            continue
        if _is_pcm_wav(_path):
            continue
        _tmp = _path + ".pcmtmp"
        if _convert_to_pcm_wav(_path, _tmp):
            try:
                os.replace(_tmp, _path)
            except Exception:
                pass
        else:
            if os.path.exists(_tmp):
                try:
                    os.remove(_tmp)
                except Exception:
                    pass
except Exception as _e:
    print("[SOUND] Ошибка при подготовке звуков:", _e)

_SND_FILENAME  = 0x00020000
_SND_ASYNC     = 0x0001
_SND_LOOP      = 0x0008
_SND_PURGE     = 0x0040
_SND_NODEFAULT = 0x0002

try:
    _winmm = ctypes.windll.winmm
except Exception:
    _winmm = None


def _play(path, loop=False):
    if _winmm is None or not os.path.exists(path):
        return
    flags = _SND_FILENAME | _SND_ASYNC | _SND_NODEFAULT
    if loop:
        flags |= _SND_LOOP
    try:
        _winmm.PlaySoundW(str(path), None, flags)
    except Exception:
        pass


def _stop():
    if _winmm is None:
        return
    try:
        _winmm.PlaySoundW(None, None, _SND_PURGE)
    except Exception:
        pass


def error_sound():
    _play(SOUND_ERROR)


def lose_sound():
    _play(SOUND_LOSE)
    try:
        time.sleep(2.5)
    except Exception:
        pass


def slow_print(text, delay=0.02):
    """text — обязательный аргумент. Проверка на None."""
    if text is None:
        text = ""
    _play(SOUND_TYPING, loop=True)
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        try:
            time.sleep(delay)
        except Exception:
            pass
    print()
    _stop()


# ==========================================
# СОСТОЯНИЕ ИГРЫ
# ==========================================

inventory = []
hp = random.randint(90, 130)
max_hp = hp
gold = random.randint(80, 200)
xp = 0
level = 1
day = 1

castle_found = False
wolf_friend = False
troll_defeated = False
witch_met = False
dragon_defeated = False
undead_defeated = False
fairy_friend = False
unicorn_friend = False
princess_saved = False
strange_key = False
escape_ready = False

items_prices = {
    "Еда": 10, "Меч": 50, "Броня": 100, "Зелье лечения": 30,
    "Амулет": 40, "Факел": 5, "Верёвка": 15, "Карта": 25,
    "Лук": 60, "Стрелы": 20, "Щит": 80, "Шлем": 70,
    "Сапоги": 45, "Плащ": 55, "Кольцо": 90, "Свиток": 35,
    "Книга": 65, "Кристалл": 150, "Жемчужина": 250,
    "Зелье силы": 60, "Зелье скорости": 70, "Антидот": 40,
    "Странный ключ": 9999, "ты бомж": 1, "ШКОЛА": 99999,
    "100 ручек": 100, "Рыцарский меч": 500,
    "Королевский амулет": 800, "Магический кристалл": 400,
    "Драгоценный камень": 300,
}


def reset_state():
    global inventory, hp, max_hp, gold, xp, level, day
    global castle_found, wolf_friend, troll_defeated, witch_met
    global dragon_defeated, undead_defeated, fairy_friend, unicorn_friend
    global princess_saved, strange_key, escape_ready

    inventory = []
    hp = random.randint(90, 130)
    max_hp = hp
    gold = random.randint(80, 200)
    xp = 0
    level = 1
    day = 1
    castle_found = False
    wolf_friend = False
    troll_defeated = False
    witch_met = False
    dragon_defeated = False
    undead_defeated = False
    fairy_friend = False
    unicorn_friend = False
    princess_saved = False
    strange_key = False
    escape_ready = False


# ==========================================
# ИГРОВЫЕ ДЕЙСТВИЯ
# ==========================================

def show_health_line():
    global hp, max_hp
    bar_len = 20
    try:
        filled = int((hp / max_hp) * bar_len)
    except Exception:
        filled = 0
    filled = max(0, min(filled, bar_len))
    bar = "|" * filled + "." * (bar_len - filled)
    print("")
    print("========= ЗДОРОВЬЕ =========")
    print("  " + str(hp) + "/" + str(max_hp) + "  [" + bar + "]")
    print("============================")


def add_item(item):
    inventory.append(item)
    slow_print("[ПОДСКАЗКА] Получен предмет: " + item)


def add_gold(amount):
    global gold
    gold += amount
    slow_print("[ПОДСКАЗКА] +" + str(amount) + " золота (Всего: " + str(gold) + ")")


def add_xp(amount):
    global xp, level, max_hp, hp
    xp += amount
    slow_print("[ПОДСКАЗКА] +" + str(amount) + " опыта!")
    safety = 0
    while xp >= level * 10 and safety < 1000:
        xp -= level * 10
        level += 1
        max_hp += 10
        hp = max_hp
        safety += 1
        slow_print("[ПОДСКАЗКА] УРОВЕНЬ ПОВЫШЕН! Теперь ты уровня " + str(level))
        slow_print("[ПОДСКАЗКА] Максимум здоровья: " + str(max_hp))


def heal(amount):
    global hp, max_hp
    hp += amount
    if hp > max_hp:
        hp = max_hp
    slow_print("[ПОДСКАЗКА] Восстановлено " + str(amount) + " здоровья!")


def take_damage(amount):
    global hp
    hp -= amount
    if hp < 0:
        hp = 0
    slow_print("[ПОДСКАЗКА] Получено " + str(amount) + " урона!")
    if hp <= 0:
        lose_sound()
        slow_print("ТЫ УМЕР!")
        slow_print("Уровень: " + str(level) + " | Опыт: " + str(xp) + " | Золото: " + str(gold))
        slow_print("Игра окончена.")
        raise SystemExit(0)


def show_status(player_name):
    show_health_line()
    slow_print("Уровень: " + str(level) + " | Опыт: " + str(xp) + " | Золото: " + str(gold))
    slow_print("День: " + str(day))


def show_inventory():
    show_health_line()
    slow_print("ТВОЙ ИНВЕНТАРЬ:")
    if len(inventory) == 0:
        slow_print("Пока пусто")
    else:
        for i, item in enumerate(inventory, 1):
            price = items_prices.get(item, random.randint(5, 100))
            slow_print(str(i) + " - " + item + " (цена: " + str(price) + ")")


def ask_yes_no(prompt):
    """Читает ответ д/н. Всё, кроме 'д'/'да', считается 'нет'."""
    ans = input(prompt).strip().lower()
    return ans in ("д", "да", "y", "yes")


def use_item():
    global escape_ready, strange_key
    if len(inventory) == 0:
        slow_print("Инвентарь пуст!")
        return
    slow_print("Что использовать?")
    for i, item in enumerate(inventory, 1):
        slow_print(str(i) + " - " + item)
    slow_print(str(len(inventory) + 1) + " - отмена")

    while True:
        try:
            idx = int(input("Твой выбор: "))
        except ValueError:
            error_sound()
            slow_print("Введи число!")
            continue
        if idx < 1 or idx > len(inventory) + 1:
            error_sound()
            slow_print("Введи число от 1 до " + str(len(inventory) + 1))
            continue
        break

    if idx == len(inventory) + 1:
        slow_print("Отмена.")
        return

    item = inventory[idx - 1]

    if item in ("Еда", "Свежая рыба", "Мёд"):
        heal(random.randint(10, 25))
        inventory.remove(item)
    elif item == "Целебная трава":
        heal(random.randint(10, 20))
        inventory.remove(item)
    elif item == "Целебная вода":
        heal(random.randint(20, 35))
        inventory.remove(item)
    elif item == "Зелье лечения":
        heal(random.randint(30, 50))
        inventory.remove(item)
    elif item == "Зелье силы":
        add_xp(random.randint(10, 20))
        inventory.remove(item)
    elif item == "Зелье скорости":
        heal(15)
        add_xp(10)
        inventory.remove(item)
    elif item in ("Меч", "Старый меч", "Древний меч", "Рыцарский меч"):
        if item == "Рыцарский меч":
            slow_print("Ты сжимаешь Рыцарский меч.")
            slow_print("Он сияет золотом. Чувствуешь себя непобедимым.")
        else:
            slow_print("Ты берёшь в руки " + item + " — теперь сильнее в бою!")
    elif item in ("Броня", "Старая броня"):
        slow_print("Ты надел " + item + " — теперь защищён!")
    elif item in ("Амулет", "Амулет удачи", "Болотный амулет"):
        slow_print("Ты надел " + item + " — удача с тобой!")
    elif item == "Друг-волк":
        slow_print("Волк охраняет тебя!")
    elif item == "Странный ключ":
        slow_print("Ключ холодный на ощупь. Он явно от какой-то двери...")
        slow_print("Найди запертую дверь в одном из подвалов.")
    elif item == "ты бомж":
        slow_print("Ты бомж. Все смотрят на тебя с жалостью.")
        slow_print("Но тебе нечего терять — вперёд, к приключениям!")
    elif item == "ШКОЛА":
        slow_print("Ты достаёшь ШКОЛУ.")
        slow_print("Директор Инга лично подписывает тебе пропуск от всех проблем.")
        slow_print("Все контрольные отменены, объяснительные — тоже.")
        slow_print("Мир трещит по швам...")
        escape_ready = True
        strange_key = True
        slow_print("(Ты готов покинуть иллюзию — иди на развилку)")
    elif item == "100 ручек":
        slow_print("Ты высыпаешь 100 ручек на пол.")
        slow_print("Василь бы позавидовал. Теперь писать есть чем.")
        slow_print("Ты получаешь +5 опыта.")
        add_xp(5)
        inventory.remove(item)
    elif item == "Книга":
        slow_print("Ты читаешь книгу. +3 опыта.")
        add_xp(3)
        inventory.remove(item)
    elif item == "Королевский амулет":
        slow_print("Королевский амулет теплеет.")
    elif item == "Магический кристалл":
        slow_print("Кристалл светится. +10 опыта.")
        add_xp(10)
        inventory.remove(item)
    elif item == "Драгоценный камень":
        slow_print("Драгоценный камень переливается.")
    else:
        slow_print("Ты не знаешь, как использовать " + item)


def shop():
    global gold
    shop_items = [
        ("Еда", 10), ("Меч", 50), ("Броня", 100),
        ("Зелье лечения", 30), ("Зелье силы", 60), ("Зелье скорости", 70),
        ("Антидот", 40), ("Амулет", 40), ("Факел", 5),
        ("Верёвка", 15), ("Карта", 25), ("Лук", 60),
        ("Стрелы", 20), ("Щит", 80), ("Шлем", 70),
        ("Сапоги", 45), ("Плащ", 55), ("Кольцо", 90),
        ("Свиток", 35), ("Книга", 65), ("Кристалл", 150)
    ]
    while True:
        show_health_line()
        slow_print("=== МАГАЗИН ===")
        slow_print("Золото: " + str(gold))
        for i, (item, price) in enumerate(shop_items, 1):
            slow_print(str(i) + " - " + item + " (" + str(price) + ")")
        slow_print(str(len(shop_items) + 1) + " - выйти")

        while True:
            try:
                idx = int(input("Твой выбор: "))
            except ValueError:
                error_sound()
                slow_print("Введи число!")
                continue
            if idx < 1 or idx > len(shop_items) + 1:
                error_sound()
                slow_print("Введи число от 1 до " + str(len(shop_items) + 1))
                continue
            break

        if idx == len(shop_items) + 1:
            break
        item, price = shop_items[idx - 1]
        if gold >= price:
            gold -= price
            add_item(item)
        else:
            error_sound()
            slow_print("Недостаточно золота!")


def get_choice(max_choice):
    while True:
        try:
            c = int(input("Твой выбор: "))
            if 1 <= c <= max_choice:
                return c
            error_sound()
            slow_print("Введи число от 1 до " + str(max_choice))
        except ValueError:
            error_sound()
            slow_print("Введи число!")


# ==========================================
# ASCII-КАРТИНКИ
# ==========================================

ASCII_ART = {
"Развилка": "\n   РАЗВИЛКА (тропа расходится в три стороны)\n",
"Болото": "\n   ~~~ БОЛОТО ~~~\n",
"Деревня": "\n   [деревня]  домики, дым из труб\n",
"Лес": "\n   /\\/\\/\\ ЛЕС /\\/\\/\\\n",
"Горы": "\n   /\\ ГОРЫ /\\\n",
"Море": "\n   ~~~~ МОРЕ ~~~~\n",
"Замок": "\n   [ЗАМОК]  с башнями\n",
"Пещера": "\n   (ПЕЩЕРА) тёмный вход\n",
"Кладбище": "\n   + + КЛАДБИЩЕ + +\n",
"Вулкан": "\n   /\\ ВУЛКАН /\\  дым\n",
"Руины": "\n   _ _ РУИНЫ _ _\n",
"Шахта": "\n   [ШАХТА] вход в гору\n",
"Корабль": "\n   <> КОРАБЛЬ <>\n",
"Пиратская пещера": "\n   X X ПИРАТСКАЯ ПЕЩЕРА\n",
"Драконье логово": "\n   (ДРАКОН) кости, золото\n",
"Лес фей": "\n   * . * ЛЕС ФЕЙ * . *\n",
"Долина единорогов": "\n   (ЕДИНОРОГ) радуга\n",
"Логово волков": "\n   V V ЛОГОВО ВОЛКОВ\n",
"Заброшенная деревня": "\n   [] [] ЗАБРОШЕННАЯ ДЕРЕВНЯ\n",
"Охотничий лагерь": "\n   /\ ОХОТНИЧИЙ ЛАГЕРЬ\n",
"Башня": "\n   |_| БАШНЯ |_|\n",
"Сад": "\n   @ @ САД @ @\n",
"Старый дуб": "\n   ~ ДУБ ~\n",
"Ручей": "\n   ~~ РУЧЕЙ ~~\n",
"Водопад": "\n   || ВОДОПАД ||\n",
"Таверна": "\n   [ТАВЕРНА]\n",
"Рынок": "\n   [РЫНОК]\n",
"Храм": "\n   /\\ ХРАМ /\\\n",
"Подвал": "\n   [ПОДВАЛ] темно\n",
"Комната": "\n   [КОМНАТА]\n",
"Сокровищница": "\n   $ $ СОКРОВИЩНИЦА $ $\n",
}


def show_location_image(location_name):
    art = ASCII_ART.get(location_name)
    if art:
        print(art)


# ==========================================
# ПОДВАЛ (исправлен баг с slow_print)
# ==========================================

def explore_basement(place_name):
    global strange_key, escape_ready
    show_location_image("Подвал")
    slow_print("Ты спускаешься в подвал " + place_name + ".")

    while True:
        show_health_line()
        slow_print("1 - Осмотреть полки")
        slow_print("2 - Открыть сундук")
        slow_print("3 - Пройти вглубь (сокровищница)")
        slow_print("4 - Подняться обратно")
        a = get_choice(4)

        if a == 1:
            slow_print("Ты находишь старые вещи и хлам.")
            if random.random() < 0.4:
                add_item("Факел")
            elif random.random() < 0.3:
                add_gold(random.randint(5, 30))
            else:
                slow_print("Ничего интересного.")
            input("Enter...")

        elif a == 2:
            slow_print("Ты открываешь старый сундук...")
            roll = random.random()
            if roll < 0.20:
                if not strange_key:
                    strange_key = True
                    add_item("Странный ключ")
                    slow_print("*** В сундуке лежит СТРАННЫЙ КЛЮЧ! ***")
                else:
                    slow_print("Ключа тут больше нет.")
            elif roll < 0.5:
                add_gold(random.randint(50, 200))
            elif roll < 0.7:
                slow_print("Из сундука выпрыгивают пауки!")
                take_damage(random.randint(3, 8))
            else:
                slow_print("Сундук пуст.")
            input("Enter...")

        elif a == 3:
            show_location_image("Сокровищница")
            slow_print("Ты входишь в сокровищницу.")
            slow_print("1 - Взять золото")
            slow_print("2 - Обыскать всё")
            slow_print("3 - Осмотреть дверь")
            slow_print("4 - Назад")
            b = get_choice(4)
            if b == 1:
                add_gold(random.randint(100, 500))
            elif b == 2:
                add_gold(random.randint(300, 900))
                if random.random() < 0.2 and not strange_key:
                    strange_key = True
                    add_item("Странный ключ")
                    slow_print("*** Ты нашёл СТРАННЫЙ КЛЮЧ среди сокровищ! ***")
                elif random.random() < 0.3:
                    add_item("Драгоценный камень")
            elif b == 3:
                slow_print("В углу — массивная железная дверь.")
                slow_print("Замок необычной формы.")
                if strange_key:
                    slow_print()  # ИСПРАВЛЕНО: пустой вызов заменён
                    slow_print("У тебя есть Странный ключ!")
                    slow_print("1 - Попробовать открыть дверь")
                    slow_print("2 - Отойти")
                    if get_choice(2) == 1:
                        escape_ready = True
                        slow_print("Ключ с щелчком вошёл в замок!")
                        slow_print("Дверь медленно открылась...")
                        slow_print("За ней — яркий белый свет.")
                else:
                    slow_print("Нужен необычный ключ.")
            input("Enter...")

        else:
            break