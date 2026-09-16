# ==========================================
# game.py
# Основной файл. Каждая локация — своя функция.
# Переходы между локациями — через вызовы функций (косвенная рекурсия).
# ==========================================

import sys
import time
import random

import functions as f
from functions import (
    slow_print, get_choice, show_health_line, show_location_image,
    show_status, show_inventory, add_item, add_gold, add_xp, heal,
    take_damage, shop, use_item, explore_basement, error_sound,
    ask_yes_no, reset_state,
)
from endings import check_endings, show_ending, show_ending_progress


# ==========================================
# ВЫБОР ИМЕНИ
# ==========================================

NAME_OPTIONS = [
    ("Ростислав", "выигрываете автоматически.",
     {"gold": 500, "hp": 50, "xp": 30,
      "items": ["Рыцарский меч", "Королевский амулет"], "flags": {}}),
    ("Олег", "Проверьте работу Бабурина Андрея.",
     {"gold": 200, "hp": 30, "xp": 20, "items": ["Книга"] * 3, "flags": {}}),
    ("Даня", "мы тебя съедим.",
     {"gold": 100, "hp": 1, "xp": 0, "items": ["ты бомж"], "flags": {}}),
    ("Аким", "Минусовая однёрка придёт!",
     {"gold": 100, "hp": 20, "xp": 40, "items": ["Книга", "Зелье силы"], "flags": {}}),
    ("Инга", "Объяснительная за 7-ми кланчиков ждёт вас.",
     {"gold": 350, "hp": 50, "xp": 10,
      "items": ["Амулет удачи", "Зелье лечения", "ШКОЛА"], "flags": {}}),
    ("Василь", "Найди Бабурина Андрея в ЭЖД.",
     {"gold": 120, "hp": 25, "xp": 15,
      "items": ["Книга", "100 ручек"], "flags": {}}),
    ("Алексей", "Когда будут опыты?",
     {"gold": 350, "hp": 70, "xp": 60,
      "items": ["Магический кристалл", "Зелье силы"], "flags": {}}),
    ("Артём", "Не грызи ручки.",
     {"gold": 0, "hp": 40, "xp": 20, "items": ["Зелье лечения", "Еда"], "flags": {}}),
    ("Ваня", "67.", {"gold": 67, "hp": 67, "xp": 67, "items": ["Меч"], "flags": {}}),
    ("Миша", "67.", {"gold": 67, "hp": 67, "xp": 67, "items": ["Лук"], "flags": {}}),
    ("Другое", "ок. Идём в лес!", {"gold": 0, "hp": 0, "xp": 0, "items": [], "flags": {}}),
]


def apply_bonuses(name, bonus):
    global _f_note
    print()
    print("---- СТАРТОВЫЕ БОНУСЫ ----")
    g = int(bonus.get("gold", 0)); h = int(bonus.get("hp", 0)); x = int(bonus.get("xp", 0))

    if g > 0:
        f.gold += g
        print("+ " + str(g) + " золота")
    if h > 0:
        f.max_hp += h
        f.hp = f.max_hp
        print("+ " + str(h) + " HP")
    if x > 0:
        f.xp += x
        safety = 0
        while f.xp >= f.level * 10 and safety < 1000:
            f.xp -= f.level * 10
            f.level += 1
            f.max_hp += 10
            f.hp = f.max_hp
            safety += 1
        print("+ " + str(x) + " опыта (уровень " + str(f.level) + ")")
    for it in bonus.get("items", []):
        f.inventory.append(it)
        print("+ предмет: " + it)
    print("--------------------------")


def choose_name():
    print()
    print("=====================================")
    print("         ВЫБЕРИ СВОЁ ИМЯ")
    print("=====================================")
    for i, (name, _p, _b) in enumerate(NAME_OPTIONS, 1):
        print(str(i) + " - " + name)
    print("=====================================")

    while True:
        try:
            idx = int(input("Твой выбор (1-" + str(len(NAME_OPTIONS)) + "): "))
            if 1 <= idx <= len(NAME_OPTIONS):
                break
            error_sound()
            print("Введи число от 1 до " + str(len(NAME_OPTIONS)))
        except ValueError:
            error_sound()
            print("Введи число!")

    chosen_name, chosen_phrase, bonus = NAME_OPTIONS[idx - 1]

    if chosen_name == "Другое":
        name = input("Введи своё имя: ").strip() or "Путник"
        phrase = "Другое — ок. Идём в лес, " + name + "!"
    else:
        name = chosen_name
        phrase = chosen_phrase

    print()
    slow_print("Итак, тебя зовут " + name + ".")
    slow_print(phrase)
    apply_bonuses(name, bonus)
    print("...")
    time.sleep(5)
    return name, bonus


# ==========================================
# ЛОКАЦИИ (каждая — своя функция)
# Переходы — через вызовы функций.
# ==========================================

def loc_forest(player_name):
    show_location_image("Лес")
    while True:
        show_health_line()
        slow_print("=== ЛЕС ===")
        slow_print("1 - К ручью")
        slow_print("2 - На холм")
        slow_print("3 - В чащу")
        slow_print("4 - К дубу")
        slow_print("5 - К озеру")
        slow_print("6 - К пасеке")
        slow_print("7 - В деревню")
        slow_print("8 - К болоту")
        slow_print("9 - Назад на развилку")
        a = get_choice(9)
        if a == 1:
            add_item("Свежая рыба")
        elif a == 2:
            f.castle_found = True
            add_xp(15)
            slow_print("Ты видишь замок!")
        elif a == 3:
            if f.wolf_friend:
                heal(random.randint(20, 40))
            else:
                take_damage(random.randint(20, 40))
                if ask_yes_no("Погладить волка? (д/н): "):
                    f.wolf_friend = True
                    add_item("Друг-волк")
        elif a == 4:
            slow_print("1 - Залезть  2 - Дупло  3 - Отдохнуть")
            b = get_choice(3)
            if b == 1: add_xp(10)
            elif b == 2: add_gold(random.randint(100, 300))
            else: heal(25)
        elif a == 5:
            heal(30); add_item("Жемчужина")
        elif a == 6:
            add_item("Мёд")
        elif a == 7:
            return loc_village(player_name)
        elif a == 8:
            return loc_swamp(player_name)
        else:
            return loc_crossroads(player_name)
        input("Enter...")


def loc_swamp(player_name):
    show_location_image("Болото")
    while True:
        show_health_line()
        take_damage(random.randint(2, 5))
        slow_print("=== БОЛОТО ===")
        slow_print("1 - К хижине ведьмы")
        slow_print("2 - Крикнуть")
        slow_print("3 - Искать тропу")
        slow_print("4 - В деревню")
        slow_print("5 - В лес")
        slow_print("6 - Назад на развилку")
        a = get_choice(6)
        if a == 1:
            if f.gold >= 30 and ask_yes_no("Ведьма просит 30 золота. Отдать? (д/н): "):
                f.gold -= 30
                add_item("Болотный амулет")
                f.witch_met = True
        elif a == 2:
            add_item("Еда")
        elif a == 3:
            add_gold(random.randint(50, 150))
            add_xp(random.randint(5, 15))
        elif a == 4:
            return loc_village(player_name)
        elif a == 5:
            return loc_forest(player_name)
        else:
            return loc_crossroads(player_name)
        input("Enter...")


def loc_village(player_name):
    show_location_image("Деревня")
    while True:
        show_health_line()
        slow_print("=== ДЕРЕВНЯ ===")
        slow_print("1 - Подземелье (тролль)")
        slow_print("2 - Таверна")
        slow_print("3 - Рынок")
        slow_print("4 - Дом старосты")
        slow_print("5 - Храм")
        slow_print("6 - Подвал дома старосты")
        slow_print("7 - В лес")
        slow_print("8 - К болоту")
        slow_print("9 - Назад на развилку")
        a = get_choice(9)
        if a == 1:
            if not f.troll_defeated:
                slow_print("1 - Сражаться  2 - Договориться")
                if get_choice(2) == 1:
                    add_gold(random.randint(200, 500))
                    add_item("Трофей тролля"); add_xp(40)
                else:
                    add_gold(random.randint(100, 300)); add_xp(25)
                f.troll_defeated = True
        elif a == 2:
            return loc_tavern(player_name)
        elif a == 3:
            shop()
        elif a == 4:
            return loc_mayor_house(player_name)
        elif a == 5:
            return loc_temple(player_name)
        elif a == 6:
            explore_basement("дома старосты")
        elif a == 7:
            return loc_forest(player_name)
        elif a == 8:
            return loc_swamp(player_name)
        else:
            return loc_crossroads(player_name)
        input("Enter...")


def loc_tavern(player_name):
    show_location_image("Таверна")
    while True:
        show_health_line()
        slow_print("=== ТАВЕРНА ===")
        slow_print("1 - Общий зал (отдохнуть)")
        slow_print("2 - Кухня (еда)")
        slow_print("3 - Комнаты наверху")
        slow_print("4 - Подвал таверны")
        slow_print("5 - Выйти")
        t = get_choice(5)
        if t == 1:
            heal(random.randint(10, 20)); add_xp(10)
        elif t == 2:
            add_item("Еда")
        elif t == 3:
            slow_print("1 - Первая  2 - Вторая  3 - Третья  4 - Назад")
            r = get_choice(4)
            if r == 1:
                add_gold(random.randint(10, 50))
            elif r == 2:
                if random.random() < 0.3: add_item("Кольцо")
            elif r == 3:
                if random.random() < 0.25: add_item("Свиток"); add_xp(15)
        elif t == 4:
            explore_basement("таверны")
        else:
            return loc_village(player_name)
        input("Enter...")


def loc_mayor_house(player_name):
    show_location_image("Деревня")
    slow_print("Ты входишь в дом старосты.")
    while True:
        show_health_line()
        slow_print("1 - Поговорить  2 - Спальня  3 - Кухня  4 - Кабинет  5 - Выйти")
        h = get_choice(5)
        if h == 1:
            add_gold(random.randint(50, 150))
        elif h == 2:
            if random.random() < 0.4: add_item("Амулет удачи")
        elif h == 3:
            add_item("Еда")
        elif h == 4:
            if random.random() < 0.5: add_item("Карта"); add_xp(10)
        else:
            return loc_village(player_name)
        input("Enter...")


def loc_temple(player_name):
    show_location_image("Храм")
    while True:
        show_health_line()
        slow_print("1 - Помолиться  2 - Пожертвовать  3 - Ризница  4 - Выйти")
        h = get_choice(4)
        if h == 1:
            heal(25); add_item("Святая вода")
        elif h == 2:
            if f.gold >= 20:
                f.gold -= 20; add_xp(20)
            else:
                slow_print("Недостаточно золота.")
        elif h == 3:
            if random.random() < 0.4: add_item("Древний свиток")
        else:
            return loc_village(player_name)
        input("Enter...")


def loc_castle(player_name):
    show_location_image("Замок")
    if not f.castle_found:
        slow_print("Сначала найди замок с холма.")
        return loc_crossroads(player_name)
    while True:
        show_health_line()
        slow_print("1 - Тронный зал  2 - Библиотека  3 - Подвал замка")
        slow_print("4 - Башня  5 - Сад  6 - Назад на развилку")
        a = get_choice(6)
        if a == 1:
            if not f.dragon_defeated:
                slow_print("Сначала убей дракона.")
            elif not f.princess_saved:
                slow_print("Принцесса спасена!")
                add_xp(50); add_gold(random.randint(500, 1500))
                add_item("Королевский амулет")
                f.princess_saved = True
        elif a == 2:
            add_xp(20)
            if random.random() < 0.5: add_item("Книга")
        elif a == 3:
            explore_basement("замка")
        elif a == 4:
            add_item("Магический кристалл")
        elif a == 5:
            heal(30); add_item("Редкое растение")
        else:
            return loc_crossroads(player_name)
        input("Enter...")


def loc_mountains(player_name):
    show_location_image("Горы")
    while True:
        show_health_line()
        take_damage(random.randint(2, 5))
        slow_print("1 - Вершина  2 - Пещера  3 - Озеро  4 - К морю  5 - Назад")
        a = get_choice(5)
        if a == 1:
            add_xp(20); add_gold(random.randint(20, 100))
        elif a == 2:
            add_gold(random.randint(200, 800)); add_item("Горные сокровища")
        elif a == 3:
            heal(30)
        elif a == 4:
            return loc_sea(player_name)
        else:
            return loc_crossroads(player_name)
        input("Enter...")


def loc_sea(player_name):
    show_location_image("Море")
    while True:
        show_health_line()
        slow_print("1 - Поплавать  2 - Сокровища  3 - Лодка  4 - В замок  5 - Назад")
        a = get_choice(5)
        if a == 1:
            heal(15)
        elif a == 2:
            add_item("Пиратская карта")
        elif a == 3:
            add_item("Свежая рыба"); heal(15)
        elif a == 4:
            return loc_castle(player_name)
        else:
            return loc_crossroads(player_name)
        input("Enter...")


def loc_cave(player_name):
    show_location_image("Пещера")
    while True:
        show_health_line()
        slow_print("1 - Вглубь  2 - Руда  3 - Озеро  4 - Рисунки  5 - Назад")
        a = get_choice(5)
        if a == 1:
            add_gold(random.randint(300, 800))
        elif a == 2:
            add_item("Редкая руда"); add_gold(random.randint(50, 200))
        elif a == 3:
            heal(30)
        elif a == 4:
            add_xp(20)
        else:
            return loc_crossroads(player_name)
        input("Enter...")


def loc_cemetery(player_name):
    show_location_image("Кладбище")
    while True:
        show_health_line()
        slow_print("1 - Могилы  2 - Склеп  3 - Призраки  4 - Часовня  5 - Назад")
        a = get_choice(5)
        if a == 1:
            add_gold(random.randint(10, 50))
        elif a == 2:
            add_gold(random.randint(100, 400))
        elif a == 3:
            add_xp(30); f.undead_defeated = True
        elif a == 4:
            heal(30)
        else:
            return loc_crossroads(player_name)
        input("Enter...")


def loc_ruins(player_name):
    show_location_image("Руины")
    while True:
        show_health_line()
        slow_print("1 - Алтарь  2 - Сокровищница  3 - Библиотека  4 - Подвал руин  5 - Назад")
        a = get_choice(5)
        if a == 1:
            add_item("Магический артефакт")
        elif a == 2:
            add_gold(random.randint(500, 1500))
        elif a == 3:
            add_xp(40)
        elif a == 4:
            explore_basement("руин")
        else:
            return loc_crossroads(player_name)
        input("Enter...")


def loc_dragon(player_name):
    show_location_image("Драконье логово")
    while True:
        show_health_line()
        if f.dragon_defeated:
            slow_print("Дракон побеждён.")
            return loc_crossroads(player_name)
        slow_print("1 - Сражаться  2 - Договориться  3 - Украсть  4 - Назад")
        a = get_choice(4)
        if a == 1:
            if random.random() < 0.5:
                add_gold(random.randint(1000, 3000))
                add_item("Драконья чешуя")
                f.dragon_defeated = True
            else:
                take_damage(40)
        elif a == 2:
            add_gold(random.randint(500, 1500))
            f.dragon_defeated = True
        elif a == 3:
            add_gold(random.randint(2000, 5000))
            f.dragon_defeated = True
        else:
            return loc_crossroads(player_name)
        input("Enter...")


def loc_fairy(player_name):
    show_location_image("Лес фей")
    while True:
        show_health_line()
        slow_print("1 - Отдохнуть  2 - Пыльца  3 - Фея  4 - Назад")
        a = get_choice(4)
        if a == 1:
            heal(35)
        elif a == 2:
            add_item("Волшебная пыльца")
        elif a == 3:
            f.fairy_friend = True; add_xp(30)
        else:
            return loc_crossroads(player_name)
        input("Enter...")


def loc_unicorns(player_name):
    show_location_image("Долина единорогов")
    while True:
        show_health_line()
        slow_print("1 - Отдохнуть  2 - Рог  3 - Погладить  4 - Назад")
        a = get_choice(4)
        if a == 1:
            heal(45)
        elif a == 2:
            add_item("Рог единорога")
        elif a == 3:
            f.unicorn_friend = True; add_xp(20)
        else:
            return loc_crossroads(player_name)
        input("Enter...")


def loc_wolves(player_name):
    show_location_image("Логово волков")
    show_health_line()
    if f.wolf_friend:
        heal(45); slow_print("Волки рады тебе!")
    else:
        take_damage(random.randint(20, 50))
    slow_print("1 - Назад")
    get_choice(1)
    return loc_crossroads(player_name)


def loc_abandoned_village(player_name):
    show_location_image("Заброшенная деревня")
    while True:
        show_health_line()
        slow_print("1 - Церковь  2 - Дом старосты  3 - Колодец  4 - Подвал  5 - Назад")
        a = get_choice(5)
        if a == 1:
            add_item("Древний свиток")
        elif a == 2:
            add_item("Старая карта"); add_gold(random.randint(100, 300))
        elif a == 3:
            add_item("Древний меч")
        elif a == 4:
            explore_basement("заброшенного дома")
        else:
            return loc_crossroads(player_name)
        input("Enter...")


# ==========================================
# РАЗВИЛКА — ГЛАВНЫЙ УЗЕЛ
# ==========================================

def loc_crossroads(player_name):
    # проверяем финал
    ending = check_endings()
    if ending:
        show_ending(ending)
        raise SystemExit(0)

    show_location_image("Развилка")
    print("")
    print("================================")
    print("ТЫ НА РАЗВИЛКЕ, " + player_name.upper())
    print("================================")
    show_status(player_name)

    if random.random() < 0.2:
        slow_print("[СЛУЧАЙНОЕ СОБЫТИЕ]")
        e = random.randint(1, 12)
        if e == 1:
            slow_print("Дождь."); take_damage(random.randint(1, 5))
        elif e == 2:
            slow_print("Нашёл монету!"); add_gold(random.randint(1, 30))
        elif e == 3:
            slow_print("Споткнулся."); take_damage(random.randint(1, 5))
        elif e == 4:
            slow_print("Птица."); add_xp(random.randint(1, 5))
        elif e == 6:
            slow_print("Трава."); add_item("Целебная трава")
        elif e == 7:
            slow_print("Собака!"); take_damage(random.randint(3, 10))
        elif e == 11:
            slow_print("Кошелёк!"); add_gold(random.randint(20, 100))
        elif e == 12:
            slow_print("Разбойники!"); take_damage(random.randint(5, 15))

    print("")
    slow_print("1 - Болото")
    slow_print("2 - Деревня")
    slow_print("3 - Лес")
    slow_print("4 - Горы")
    slow_print("5 - Море")
    slow_print("6 - Замок")
    slow_print("7 - Пещеры")
    slow_print("8 - Кладбище")
    slow_print("9 - Руины")
    slow_print("10 - Драконье логово")
    slow_print("11 - Лес фей")
    slow_print("12 - Долина единорогов")
    slow_print("13 - Логово волков")
    slow_print("14 - Заброшенная деревня")
    slow_print("15 - Инвентарь")
    slow_print("16 - Использовать предмет")
    slow_print("17 - Отдохнуть")
    slow_print("18 - Прогресс концовок")

    choice = get_choice(18)

    if choice == 1:
        return loc_swamp(player_name)
    elif choice == 2:
        return loc_village(player_name)
    elif choice == 3:
        return loc_forest(player_name)
    elif choice == 4:
        return loc_mountains(player_name)
    elif choice == 5:
        return loc_sea(player_name)
    elif choice == 6:
        return loc_castle(player_name)
    elif choice == 7:
        return loc_cave(player_name)
    elif choice == 8:
        return loc_cemetery(player_name)
    elif choice == 9:
        return loc_ruins(player_name)
    elif choice == 10:
        return loc_dragon(player_name)
    elif choice == 11:
        return loc_fairy(player_name)
    elif choice == 12:
        return loc_unicorns(player_name)
    elif choice == 13:
        return loc_wolves(player_name)
    elif choice == 14:
        return loc_abandoned_village(player_name)
    elif choice == 15:
        show_inventory()
        input("Enter...")
        return loc_crossroads(player_name)
    elif choice == 16:
        use_item()
        input("Enter...")
        return loc_crossroads(player_name)
    elif choice == 17:
        slow_print("Ты отдыхаешь.")
        heal(25)
        f.day += 1
        slow_print("Наступил день " + str(f.day))
        add_xp(3)
        input("Enter...")
        return loc_crossroads(player_name)
    elif choice == 18:
        show_ending_progress()
        return loc_crossroads(player_name)
    else:
        return loc_crossroads(player_name)


# ==========================================
# ОДНА ПАРТИЯ
# ==========================================

def play_session(player_name):
    slow_print("Ты просыпаешься на развилке лесной тропы, " + player_name + ".")
    slow_print("Ты не помнишь, как здесь оказался.")
    slow_print("Куда пойдёшь?")
    input("Нажми Enter...")
    # Косвенная рекурсия: развилка → локации → развилка ...
    loc_crossroads(player_name)


# ==========================================
# ГЛАВНЫЙ ЦИКЛ
# ==========================================

print("================================")
print("       ЛЕСНОЕ ПРИКЛЮЧЕНИЕ")
print("================================")

current_name = None
current_bonus = None

while True:
    if current_name is None:
        reset_state()
        current_name, current_bonus = choose_name()
    else:
        reset_state()
        print()
        print("Ты снова играешь за " + current_name.upper())
        apply_bonuses(current_name, current_bonus)
        input("Нажми Enter, чтобы начать заново...")

    try:
        play_session(current_name)
    except SystemExit:
        pass

    print()
    print("=====================================")
    print("         ЧТО ДАЛЬШЕ?")
    print("=====================================")
    print("1 - Играть снова за " + current_name)
    print("2 - Выбрать другого персонажа")
    print("3 - Выйти из игры")
    print("=====================================")

    while True:
        try:
            ans = int(input("Твой выбор: "))
            if ans in (1, 2, 3):
                break
            print("Введи 1, 2 или 3")
        except ValueError:
            error_sound()
            print("Введи число!")

    if ans == 1:
        continue
    elif ans == 2:
        current_name = None
        current_bonus = None
        continue
    else:
        slow_print("Спасибо за игру! До встречи в лесу.")
        break