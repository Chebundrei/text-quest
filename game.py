# ==========================================
# ==========================================
# ==========================================
# ==========================================
# ==========================================
# ==========================================
# ==========================================
# ==========================================
# ==========================================
# ==========================================
# ==========================================
# ==========================================
# ==========================================
# ==========================================
# ==========================================
# ==========================================
# ==========================================
# ==========================================
# ==========================================
# ==========================================
# ==========================================
# ==========================================
# ==========================================
# ==========================================
# ==========================================
# ==========================================

import random
import sys
import os
import time

import functions as f
from functions import (
    show_health_line, show_location_image, show_status, show_inventory,
    get_choice, add_item, add_gold, add_xp, heal, take_damage,
    shop, use_item, slow_print, explore_basement,
    error_sound,
)

from endings import check_endings, show_ending, show_ending_progress


NAME_OPTIONS = [
    ("Ростислав", "выигрываете автоматически. Но если очень хочешь поиграть -- смотри ниже",
     {"gold": 500, "hp": 50, "xp": 30,
      "items": ["Рыцарский меч", "Королевский амулет"],
      "flags": {"auto_win": True}}),
    ("Олег", "Проверьте экзаменационную работу Бабурина Андрея с летней сессии 2026",
     {"gold": 200, "hp": 30, "xp": 20,
      "items": ["Книга"] * 3,
      "flags": {"exam_pass": True}}),
    ("Даня", "мы тебя съедим.",
     {"gold": 100, "hp": 1, "xp": 0,
      "items": ["ты бомж"],
      "flags": {"cannibal_snack": True}}),
    ("Аким", "Минусовая однёрка пийдёт! Попробуй не отправить меня в 105.",
     {"gold": 100, "hp": 20, "xp": 40,
      "items": ["Книга", "Зелье силы"],
      "flags": {"lazy_smart": True}}),
    ("Инга", "Вам предстоит написать обьяснительную на следующий учебный день в школе, в 105, на тему: 'Новые способы замучать всех кроме 7-ми кланчиков'",
     {"gold": 350, "hp": 50, "xp": 10,
      "items": ["Амулет удачи", "Зелье лечения", "Зелье лечения",
                "Кристалл", "ШКОЛА"],
      "flags": {"director": True}}),
    ("Василь", "Самый важный квэст - найди Бабурина Андрея в ЭЖД",
     {"gold": 120, "hp": 25, "xp": 15,
      "items": ["Книга", "Свиток", "Факел", "100 ручек"],
      "flags": {"pen_seeker": True}}),
    ("Алексей", "Алексей Геннадьевич, когда будут опыты?",
     {"gold": 350, "hp": 70, "xp": 60,
      "items": ["Магический кристалл", "Зелье силы",
                "Зелье скорости", "Антидот"],
      "flags": {"scientist": True}}),
    ("Артём", "Артём, не грызи ручки.",
     {"gold": 0, "hp": 40, "xp": 20,
      "items": ["Зелье лечения", "Еда"],
      "flags": {"pen_biter": True}}),
    ("Ваня", "67.",
     {"gold": 67, "hp": 67, "xp": 67,
      "items": ["Меч", "Броня"],
      "flags": {"sixty_seven": True}}),
    ("Миша", "67.",
     {"gold": 67, "hp": 67, "xp": 67,
      "items": ["Лук", "Стрелы", "Стрелы"],
      "flags": {"sixty_seven": True}}),
    ("Другое", "ок. Идём в лес!",
     {"gold": 0, "hp": 0, "xp": 0, "items": [], "flags": {}}),
]


def reset_game_state():
    """Сбрасывает все игровые переменные к стартовым значениям."""
    f.inventory = []
    f.hp = random.randint(90, 130)
    f.max_hp = f.hp
    f.gold = random.randint(80, 200)
    f.xp = 0
    f.level = 1
    f.day = 1

    f.castle_found = False
    f.wolf_friend = False
    f.troll_defeated = False
    f.witch_met = False
    f.dragon_defeated = False
    f.undead_defeated = False
    f.fairy_friend = False
    f.unicorn_friend = False
    f.princess_saved = False

    f.strange_key = False
    f.escape_ready = False


def choose_name():
    print()
    print("=====================================")
    print("         ВЫБЕРИ СВОЁ ИМЯ")
    print("=====================================")
    for i, (name, _phrase, _bonus) in enumerate(NAME_OPTIONS, 1):
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
        name = input("Введи своё имя: ").strip()
        if name == "":
            name = "Путник"
        phrase = "Другое — ок. Идём в лес, " + name + "!"
    else:
        name = chosen_name
        phrase = chosen_phrase

    print()
    slow_print("Итак, тебя зовут " + name + ".")
    slow_print(phrase)

    apply_bonuses(name, bonus)

    print()
    print("...")
    time.sleep(5)

    return name, bonus


def apply_bonuses(name, bonus):
    print()
    print("-------------------------------------")
    print("     СТАРТОВЫЕ БОНУСЫ")
    print("-------------------------------------")

    gold_b = int(bonus.get("gold", 0))
    hp_b   = int(bonus.get("hp", 0))
    xp_b   = int(bonus.get("xp", 0))

    if gold_b > 0:
        f.gold += gold_b
        print("+ " + str(gold_b) + " золота")

    if hp_b > 0:
        f.max_hp += hp_b
        f.hp = f.max_hp
        print("+ " + str(hp_b) + " к максимуму здоровья")

    if xp_b > 0:
        f.xp += xp_b
        safety = 0
        while f.xp >= f.level * 10 and safety < 1000:
            f.xp -= f.level * 10
            f.level += 1
            f.max_hp += 10
            f.hp = f.max_hp
            safety += 1
        print("+ " + str(xp_b) + " опыта (уровень " + str(f.level) + ")")

    for item in bonus.get("items", []):
        f.inventory.append(item)
        print("+ предмет: " + item)

    flags = bonus.get("flags", {})

    if flags.get("auto_win"):
        print()
        print(">>> БОНУС РОСТИСЛАВА: победа засчитается автоматически.")
    if flags.get("exam_pass"):
        print()
        print(">>> ОЛЕГ: экзамен сдан, оценка в кармане.")
    if flags.get("cannibal_snack"):
        print()
        print(">>> ДАНЯ: враги боятся тебя съесть.")
        print("    Но у тебя 1 HP и ты бомж. Держись!")
    if flags.get("lazy_smart"):
        print()
        print(">>> РОМАН: дз меньше, знаний больше. +1 опыт за действие.")
    if flags.get("director"):
        print()
        print(">>> ИНГА — ДИРЕКТОР ЛЕСА.")
        print("    Правила объяснительных отменены.")
    if flags.get("pen_seeker"):
        print()
        print(">>> ВАСИЛЬ: ручка найдена.")
    if flags.get("scientist"):
        print()
        print(">>> АЛЕКСЕЙ — ГЛАВНЫЙ УЧЁНЫЙ. Опыты удаются.")
    if flags.get("pen_biter"):
        print()
        print(">>> АРТЁМ: ручки целы, зубы здоровы.")
    if flags.get("sixty_seven"):
        print()
        print(">>> 67 — СЧАСТЛИВОЕ ЧИСЛО.")

    print("-------------------------------------")


# ==========================================
# ОДНА ПАРТИЯ
# ==========================================

def play_session(player_name):
    """Одна полная партия. Возвращает True если игрок умер/финал достигнут."""
    slow_print("Ты просыпаешься на развилке лесной тропы, " + player_name + ".")
    slow_print("Ты не помнишь, как здесь оказался.")
    slow_print("Вокруг тебя — тёмный лес.")
    slow_print("Где-то вдалеке воет волк.")
    slow_print("Говорят, из этого мира можно выбраться... если найти особый ключ.")
    slow_print("Куда пойдёшь?")
    input("Нажми Enter...")

    current_location = "Развилка"

    while True:

        show_location_image(current_location)

        print("")
        print("================================")
        print("ТЫ НА РАЗВИЛКЕ, " + player_name.upper())
        print("================================")
        show_status()

        ending = check_endings()
        if ending:
            show_ending(ending)
            return True

        if random.random() < 0.2:
            slow_print("[СЛУЧАЙНОЕ СОБЫТИЕ]")
            e = random.randint(1, 12)
            if e == 1:
                slow_print("Пошёл дождь. Ты промок.")
                take_damage(random.randint(1, 5))
            elif e == 2:
                slow_print("Ты нашёл монету!")
                add_gold(random.randint(1, 30))
            elif e == 3:
                slow_print("Ты споткнулся и упал.")
                take_damage(random.randint(1, 5))
            elif e == 4:
                slow_print("Птица села на плечо.")
                add_xp(random.randint(1, 5))
            elif e == 5:
                slow_print("Ничего не произошло.")
            elif e == 6:
                slow_print("Ты нашёл целебную траву!")
                add_item("Целебная трава")
            elif e == 7:
                slow_print("Напала дикая собака!")
                take_damage(random.randint(3, 10))
            elif e == 8:
                slow_print("Бродячий торговец прошёл мимо.")
            elif e == 9:
                slow_print("Ты нашёл обрывок карты.")
                add_item("Обрывок карты")
            elif e == 10:
                slow_print("Ты нашёл странный гриб.")
                if random.random() < 0.5:
                    take_damage(random.randint(5, 15))
                else:
                    heal(random.randint(5, 15))
            elif e == 11:
                slow_print("Ты нашёл кошелёк с золотом!")
                add_gold(random.randint(20, 100))
            elif e == 12:
                slow_print("На тебя напали разбойники!")
                take_damage(random.randint(5, 15))

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
        slow_print("10 - Вулкан")
        slow_print("11 - Шахта")
        slow_print("12 - Корабль")
        slow_print("13 - Пиратская пещера")
        slow_print("14 - Драконье логово")
        slow_print("15 - Лес фей")
        slow_print("16 - Долина единорогов")
        slow_print("17 - Логово волков")
        slow_print("18 - Заброшенная деревня")
        slow_print("19 - Охотничий лагерь")
        slow_print("20 - Башня")
        slow_print("21 - Сад")
        slow_print("22 - Старый дуб")
        slow_print("23 - Ручей")
        slow_print("24 - Водопад")
        slow_print("25 - Инвентарь")
        slow_print("26 - Использовать предмет")
        slow_print("27 - Отдохнуть")
        slow_print("28 - Проверить прогресс концовок")

        choice = get_choice(28)

        if choice == 1:
            current_location = "Болото"
            show_location_image(current_location)
            while True:
                show_health_line()
                take_damage(random.randint(2, 5))
                slow_print("1 - К хижине ведьмы")
                slow_print("2 - Крикнуть")
                slow_print("3 - Искать тропу")
                slow_print("4 - В деревню")
                slow_print("5 - В лес")
                slow_print("6 - Назад")
                a = get_choice(6)
                if a == 1:
                    if f.gold >= 30 and input("Ведьма просит 30 золота. Отдать? (д/н): ").lower() == "д":
                        f.gold -= 30
                        add_item("Болотный амулет")
                        f.witch_met = True
                elif a == 2:
                    add_item("Еда")
                elif a == 3:
                    add_gold(random.randint(50, 150))
                    add_xp(random.randint(5, 15))
                elif a == 4:
                    current_location = "Деревня"; break
                elif a == 5:
                    current_location = "Лес"; break
                else:
                    current_location = "Развилка"; break
                input("Enter...")

        elif choice == 2:
            current_location = "Деревня"
            show_location_image(current_location)
            while True:
                show_health_line()
                slow_print("1 - Подземелье (тролль)")
                slow_print("2 - Таверна")
                slow_print("3 - Рынок")
                slow_print("4 - Староста (дом)")
                slow_print("5 - Храм")
                slow_print("6 - Кузница")
                slow_print("7 - Подвал старосты")
                slow_print("8 - В лес")
                slow_print("9 - К болоту")
                slow_print("10 - Назад")
                a = get_choice(10)
                if a == 1:
                    if not f.troll_defeated:
                        slow_print("1 - Сражаться  2 - Договориться")
                        if get_choice(2) == 1:
                            add_gold(random.randint(200, 500))
                            add_item("Трофей тролля")
                            add_xp(40)
                        else:
                            add_gold(random.randint(100, 300))
                            add_xp(25)
                        f.troll_defeated = True
                elif a == 2:
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
                            heal(random.randint(10, 20))
                            add_xp(10)
                        elif t == 2:
                            add_item("Еда")
                        elif t == 3:
                            show_location_image("Комната")
                            slow_print("Ты поднимаешься в комнаты наверху.")
                            slow_print("1 - Заглянуть в первую комнату")
                            slow_print("2 - Заглянуть во вторую комнату")
                            slow_print("3 - Заглянуть в третью комнату")
                            slow_print("4 - Спуститься обратно")
                            r = get_choice(4)
                            if r == 1:
                                slow_print("Пустая комната. Ты находишь несколько монет.")
                                add_gold(random.randint(10, 50))
                            elif r == 2:
                                slow_print("Комната с сундуком.")
                                if random.random() < 0.3:
                                    add_item("Кольцо")
                                else:
                                    slow_print("Сундук пуст.")
                            elif r == 3:
                                slow_print("Таинственная комната.")
                                if random.random() < 0.25:
                                    add_item("Свиток")
                                    add_xp(15)
                                else:
                                    slow_print("Ничего примечательного.")
                            input("Enter...")
                        elif t == 4:
                            explore_basement("таверны")
                        else:
                            break
                        input("Enter...")
                elif a == 3:
                    shop()
                elif a == 4:
                    show_location_image("Деревня")
                    slow_print("Ты входишь в дом старосты.")
                    while True:
                        show_health_line()
                        slow_print("=== ДОМ СТАРОСТЫ ===")
                        slow_print("1 - Поговорить со старостой")
                        slow_print("2 - Спальня")
                        slow_print("3 - Кухня")
                        slow_print("4 - Кабинет")
                        slow_print("5 - Выйти")
                        h = get_choice(5)
                        if h == 1:
                            add_gold(random.randint(50, 150))
                            slow_print("Староста благодарит тебя за добрые дела.")
                        elif h == 2:
                            slow_print("Ты осматриваешь спальню.")
                            if random.random() < 0.4:
                                add_item("Амулет удачи")
                            else:
                                slow_print("Только пыль и старая одежда.")
                        elif h == 3:
                            slow_print("На кухне пахнет хлебом.")
                            add_item("Еда")
                        elif h == 4:
                            slow_print("В кабинете — старые бумаги и карты.")
                            if random.random() < 0.5:
                                add_item("Карта")
                                add_xp(10)
                            else:
                                slow_print("Бумаги истлели от времени.")
                        else:
                            break
                        input("Enter...")
                elif a == 5:
                    show_location_image("Храм")
                    while True:
                        show_health_line()
                        slow_print("=== ХРАМ ===")
                        slow_print("1 - Помолиться (исцеление)")
                        slow_print("2 - Алтарь (пожертвование)")
                        slow_print("3 - Ризница")
                        slow_print("4 - Выйти")
                        h = get_choice(4)
                        if h == 1:
                            heal(25)
                            add_item("Святая вода")
                        elif h == 2:
                            if f.gold >= 20:
                                f.gold -= 20
                                add_xp(20)
                                slow_print("Ты пожертвовал 20 золота. Чувствуешь благословение.")
                            else:
                                slow_print("Недостаточно золота.")
                        elif h == 3:
                            slow_print("В ризнице — старые свитки.")
                            if random.random() < 0.4:
                                add_item("Древний свиток")
                            else:
                                slow_print("Полки пусты.")
                        else:
                            break
                        input("Enter...")
                elif a == 6:
                    if f.gold >= 50:
                        f.gold -= 50
                        add_item("Меч")
                elif a == 7:
                    explore_basement("дома старосты")
                elif a == 8:
                    current_location = "Лес"; break
                elif a == 9:
                    current_location = "Болото"; break
                else:
                    current_location = "Развилка"; break
                input("Enter...")

        elif choice == 3:
            current_location = "Лес"
            show_location_image(current_location)
            while True:
                show_health_line()
                slow_print("1 - К ручью")
                slow_print("2 - На холм")
                slow_print("3 - В чащу")
                slow_print("4 - К дубу")
                slow_print("5 - К озеру")
                slow_print("6 - К пасеке")
                slow_print("7 - В деревню")
                slow_print("8 - К болоту")
                slow_print("9 - Назад")
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
                        if input("Погладить волка? (д/н): ").lower() == "д":
                            f.wolf_friend = True
                            add_item("Друг-волк")
                elif a == 4:
                    slow_print("1 - Залезть  2 - Дупло  3 - Отдохнуть")
                    b = get_choice(3)
                    if b == 1: add_xp(10)
                    elif b == 2: add_gold(random.randint(100, 300))
                    else: heal(25)
                elif a == 5:
                    heal(30)
                    add_item("Жемчужина")
                elif a == 6:
                    add_item("Мёд")
                elif a == 7:
                    current_location = "Деревня"; break
                elif a == 8:
                    current_location = "Болото"; break
                else:
                    current_location = "Развилка"; break
                input("Enter...")

        elif choice == 4:
            current_location = "Горы"
            show_location_image(current_location)
            while True:
                show_health_line()
                take_damage(random.randint(2, 5))
                slow_print("1 - Вершина")
                slow_print("2 - Пещера")
                slow_print("3 - Горцы")
                slow_print("4 - Озеро")
                slow_print("5 - Самоцветы")
                slow_print("6 - В лес")
                slow_print("7 - К морю")
                slow_print("8 - Назад")
                a = get_choice(8)
                if a == 1:
                    add_xp(20); add_gold(random.randint(20, 100))
                elif a == 2:
                    add_gold(random.randint(200, 800))
                    add_item("Горные сокровища")
                elif a == 3:
                    add_item("Еда"); heal(20)
                elif a == 4:
                    heal(30)
                elif a == 5:
                    add_item("Самоцвет")
                    add_gold(random.randint(50, 200))
                elif a == 6:
                    current_location = "Лес"; break
                elif a == 7:
                    current_location = "Море"; break
                else:
                    current_location = "Развилка"; break
                input("Enter...")

        elif choice == 5:
            current_location = "Море"
            show_location_image(current_location)
            while True:
                show_health_line()
                slow_print("1 - Поплавать")
                slow_print("2 - Сокровища")
                slow_print("3 - Рыбаки")
                slow_print("4 - Лодка")
                slow_print("5 - Пиратский корабль")
                slow_print("6 - В горы")
                slow_print("7 - В замок")
                slow_print("8 - Назад")
                a = get_choice(8)
                if a == 1:
                    heal(15)
                elif a == 2:
                    add_item("Пиратская карта")
                elif a == 3:
                    add_gold(random.randint(50, 150))
                elif a == 4:
                    add_item("Свежая рыба"); heal(15)
                elif a == 5:
                    add_gold(random.randint(200, 600))
                    add_item("Пиратское золото")
                elif a == 6:
                    current_location = "Горы"; break
                elif a == 7:
                    current_location = "Замок"; break
                else:
                    current_location = "Развилка"; break
                input("Enter...")

        elif choice == 6:
            current_location = "Замок"
            show_location_image(current_location)
            while True:
                show_health_line()
                if not f.castle_found:
                    slow_print("Сначала найди замок с холма.")
                    break
                slow_print("1 - Войти (тронный зал)")
                slow_print("2 - Библиотека")
                slow_print("3 - Спальня принцессы")
                slow_print("4 - Стража")
                slow_print("5 - Подземелье")
                slow_print("6 - Подвал замка")
                slow_print("7 - Башня")
                slow_print("8 - Сад")
                slow_print("9 - К морю")
                slow_print("10 - Назад")
                a = get_choice(10)
                if a == 1:
                    if not f.dragon_defeated:
                        slow_print("Стражник качает головой:")
                        slow_print("«Принцессу похитил дракон. Сначала убей дракона».")
                    else:
                        if not f.princess_saved:
                            slow_print("Ты входишь в тронный зал.")
                            slow_print("Принцесса благодарит тебя за спасение!")
                            add_xp(50)
                            add_gold(random.randint(500, 1500))
                            add_item("Королевский амулет")
                            f.princess_saved = True
                elif a == 2:
                    slow_print("=== БИБЛИОТЕКА ЗАМКА ===")
                    slow_print("Полки ломятся от древних книг.")
                    slow_print("1 - Читать книги (опыт)")
                    slow_print("2 - Искать редкий том")
                    slow_print("3 - Выйти")
                    b = get_choice(3)
                    if b == 1:
                        add_xp(20)
                    elif b == 2:
                        if random.random() < 0.5:
                            add_item("Книга")
                        else:
                            slow_print("Только пыль и старые фолианты.")
                    input("Enter...")
                elif a == 3:
                    slow_print("Ты заходишь в спальню принцессы.")
                    if f.princess_saved:
                        slow_print("Принцесса рада тебя видеть!")
                        heal(30)
                    else:
                        slow_print("Комната заперта, принцессы нет.")
                    input("Enter...")
                elif a == 4:
                    add_item("Ключ от тронного зала")
                elif a == 5:
                    add_gold(random.randint(500, 1500))
                elif a == 6:
                    explore_basement("замка")
                elif a == 7:
                    slow_print("1 - Вдаль  2 - Сокровища  3 - Кристалл")
                    b = get_choice(3)
                    if b == 1: add_xp(10)
                    elif b == 2: add_gold(random.randint(100, 400))
                    else: add_item("Магический кристалл")
                elif a == 8:
                    heal(30)
                    add_item("Редкое растение")
                elif a == 9:
                    current_location = "Море"; break
                else:
                    current_location = "Развилка"; break
                input("Enter...")

        elif choice == 7:
            current_location = "Пещера"
            show_location_image(current_location)
            while True:
                show_health_line()
                slow_print("1 - Вглубь")
                slow_print("2 - Руда")
                slow_print("3 - Озеро")
                slow_print("4 - Рисунки")
                slow_print("5 - Назад")
                a = get_choice(5)
                if a == 1:
                    add_gold(random.randint(300, 800))
                elif a == 2:
                    add_item("Редкая руда")
                    add_gold(random.randint(50, 200))
                elif a == 3:
                    heal(30)
                elif a == 4:
                    add_xp(20)
                else:
                    current_location = "Развилка"; break
                input("Enter...")

        elif choice == 8:
            current_location = "Кладбище"
            show_location_image(current_location)
            while True:
                show_health_line()
                slow_print("1 - Могилы")
                slow_print("2 - Склеп")
                slow_print("3 - Призраки")
                slow_print("4 - Часовня")
                slow_print("5 - Назад")
                a = get_choice(5)
                if a == 1:
                    add_gold(random.randint(10, 50))
                elif a == 2:
                    add_gold(random.randint(100, 400))
                elif a == 3:
                    add_xp(30)
                    f.undead_defeated = True
                elif a == 4:
                    heal(30)
                else:
                    current_location = "Развилка"; break
                input("Enter...")

        elif choice == 9:
            current_location = "Руины"
            show_location_image(current_location)
            while True:
                show_health_line()
                slow_print("1 - Алтарь")
                slow_print("2 - Сокровищница")
                slow_print("3 - Библиотека")
                slow_print("4 - Ловушки")
                slow_print("5 - Подвал руин")
                slow_print("6 - Назад")
                a = get_choice(6)
                if a == 1:
                    add_item("Магический артефакт")
                elif a == 2:
                    add_gold(random.randint(500, 1500))
                elif a == 3:
                    add_xp(40)
                elif a == 4:
                    take_damage(random.randint(10, 30))
                elif a == 5:
                    explore_basement("руин")
                else:
                    current_location = "Развилка"; break
                input("Enter...")

        elif choice == 10:
            current_location = "Вулкан"
            show_location_image(current_location)
            while True:
                show_health_line()
                take_damage(random.randint(5, 15))
                slow_print("1 - Кратер")
                slow_print("2 - Обсидиан")
                slow_print("3 - Лавовая пещера")
                slow_print("4 - Назад")
                a = get_choice(4)
                if a == 1:
                    add_xp(20)
                elif a == 2:
                    add_item("Обсидиан")
                    add_gold(random.randint(50, 150))
                elif a == 3:
                    add_gold(random.randint(300, 1000))
                else:
                    current_location = "Развилка"; break
                input("Enter...")

        elif choice == 11:
            current_location = "Шахта"
            show_location_image(current_location)
            while True:
                show_health_line()
                slow_print("1 - Копать")
                slow_print("2 - Золото")
                slow_print("3 - Выход")
                slow_print("4 - Назад")
                a = get_choice(4)
                if a == 1:
                    add_item("Редкая руда")
                elif a == 2:
                    add_gold(random.randint(200, 700))
                elif a == 3:
                    slow_print("Ты выбрался!")
                else:
                    current_location = "Развилка"; break
                input("Enter...")

        elif choice == 12:
            current_location = "Корабль"
            show_location_image(current_location)
            while True:
                show_health_line()
                slow_print("1 - Плыть")
                slow_print("2 - Трюм")
                slow_print("3 - Капитан")
                slow_print("4 - Назад")
                a = get_choice(4)
                if a == 1:
                    add_xp(15)
                elif a == 2:
                    add_gold(random.randint(100, 500))
                elif a == 3:
                    add_gold(random.randint(300, 900))
                else:
                    current_location = "Развилка"; break
                input("Enter...")

        elif choice == 13:
            current_location = "Пиратская пещера"
            show_location_image(current_location)
            while True:
                show_health_line()
                slow_print("1 - Сокровища")
                slow_print("2 - Карта")
                slow_print("3 - Ловушки")
                slow_print("4 - Назад")
                a = get_choice(4)
                if a == 1:
                    add_gold(random.randint(500, 2000))
                elif a == 2:
                    add_item("Пиратская карта")
                elif a == 3:
                    take_damage(random.randint(10, 30))
                else:
                    current_location = "Развилка"; break
                input("Enter...")

        elif choice == 14:
            current_location = "Драконье логово"
            show_location_image(current_location)
            while True:
                show_health_line()
                if f.dragon_defeated:
                    slow_print("Дракон побеждён.")
                    break
                slow_print("1 - Сражаться")
                slow_print("2 - Договориться")
                slow_print("3 - Украсть")
                slow_print("4 - Назад")
                a = get_choice(4)
                if a == 1:
                    if random.random() < 0.5:
                        add_gold(random.randint(1000, 3000))
                        add_item("Драконья чешуя")
                        f.dragon_defeated = True
                        slow_print("Дракон повержен!")
                    else:
                        take_damage(40)
                elif a == 2:
                    add_gold(random.randint(500, 1500))
                    f.dragon_defeated = True
                    slow_print("Дракон согласился на мир.")
                elif a == 3:
                    add_gold(random.randint(2000, 5000))
                    f.dragon_defeated = True
                    slow_print("Ты украл сокровище и сбежал!")
                else:
                    current_location = "Развилка"; break
                input("Enter...")

        elif choice == 15:
            current_location = "Лес фей"
            show_location_image(current_location)
            while True:
                show_health_line()
                slow_print("1 - Отдохнуть")
                slow_print("2 - Пыльца")
                slow_print("3 - Фея")
                slow_print("4 - Назад")
                a = get_choice(4)
                if a == 1:
                    heal(35)
                elif a == 2:
                    add_item("Волшебная пыльца")
                elif a == 3:
                    f.fairy_friend = True
                    add_xp(30)
                    slow_print("Фея стала твоим другом!")
                else:
                    current_location = "Развилка"; break
                input("Enter...")

        elif choice == 16:
            current_location = "Долина единорогов"
            show_location_image(current_location)
            while True:
                show_health_line()
                slow_print("1 - Отдохнуть")
                slow_print("2 - Рог")
                slow_print("3 - Погладить")
                slow_print("4 - Назад")
                a = get_choice(4)
                if a == 1:
                    heal(45)
                elif a == 2:
                    add_item("Рог единорога")
                elif a == 3:
                    f.unicorn_friend = True
                    add_xp(20)
                    slow_print("Единорог стал твоим другом!")
                else:
                    current_location = "Развилка"; break
                input("Enter...")

        elif choice == 17:
            current_location = "Логово волков"
            show_location_image(current_location)
            while True:
                show_health_line()
                if f.wolf_friend:
                    heal(45)
                    slow_print("Волки рады тебе!")
                else:
                    take_damage(random.randint(20, 50))
                slow_print("1 - Назад")
                if get_choice(1) == 1:
                    current_location = "Развилка"; break
                input("Enter...")

        elif choice == 18:
            current_location = "Заброшенная деревня"
            show_location_image(current_location)
            while True:
                show_health_line()
                slow_print("1 - Церковь")
                slow_print("2 - Дом старосты")
                slow_print("3 - Колодец")
                slow_print("4 - Подвал дома старосты")
                slow_print("5 - Назад")
                a = get_choice(5)
                if a == 1:
                    add_item("Древний свиток")
                elif a == 2:
                    add_item("Старая карта")
                    add_gold(random.randint(100, 300))
                elif a == 3:
                    add_item("Древний меч")
                elif a == 4:
                    explore_basement("заброшенного дома")
                else:
                    current_location = "Развилка"; break
                input("Enter...")

        elif choice == 19:
            current_location = "Охотничий лагерь"
            show_location_image(current_location)
            while True:
                show_health_line()
                slow_print("1 - Поговорить")
                slow_print("2 - Еда")
                slow_print("3 - Оружие")
                slow_print("4 - Охота")
                slow_print("5 - Назад")
                a = get_choice(5)
                if a == 1:
                    add_xp(10)
                elif a == 2:
                    add_item("Еда")
                elif a == 3:
                    add_item("Лук и стрелы")
                elif a == 4:
                    add_item("Шкура зверя")
                else:
                    current_location = "Развилка"; break
                input("Enter...")

        elif choice == 20:
            current_location = "Башня"
            show_location_image(current_location)
            while True:
                show_health_line()
                slow_print("1 - Вдаль")
                slow_print("2 - Сокровища")
                slow_print("3 - Кристалл")
                slow_print("4 - Назад")
                a = get_choice(4)
                if a == 1:
                    add_xp(10)
                elif a == 2:
                    add_gold(random.randint(100, 400))
                elif a == 3:
                    add_item("Магический кристалл")
                else:
                    current_location = "Развилка"; break
                input("Enter...")

        elif choice == 21:
            current_location = "Сад"
            show_location_image(current_location)
            while True:
                show_health_line()
                slow_print("1 - Погулять")
                slow_print("2 - Растения")
                slow_print("3 - Фонтан")
                slow_print("4 - Назад")
                a = get_choice(4)
                if a == 1:
                    heal(15)
                elif a == 2:
                    add_item("Редкое растение")
                elif a == 3:
                    heal(30)
                else:
                    current_location = "Развилка"; break
                input("Enter...")

        elif choice == 22:
            current_location = "Старый дуб"
            show_location_image(current_location)
            while True:
                show_health_line()
                slow_print("1 - Залезть")
                slow_print("2 - Дупло")
                slow_print("3 - Отдохнуть")
                slow_print("4 - Назад")
                a = get_choice(4)
                if a == 1:
                    add_xp(10)
                elif a == 2:
                    add_gold(random.randint(100, 300))
                elif a == 3:
                    heal(25)
                else:
                    current_location = "Развилка"; break
                input("Enter...")

        elif choice == 23:
            current_location = "Ручей"
            show_location_image(current_location)
            while True:
                show_health_line()
                slow_print("1 - Рыба")
                slow_print("2 - Напиться")
                slow_print("3 - Водопад")
                slow_print("4 - Назад")
                a = get_choice(4)
                if a == 1:
                    add_item("Свежая рыба")
                elif a == 2:
                    heal(10)
                elif a == 3:
                    add_gold(random.randint(200, 600))
                else:
                    current_location = "Развилка"; break
                input("Enter...")

        elif choice == 24:
            current_location = "Водопад"
            show_location_image(current_location)
            while True:
                show_health_line()
                slow_print("1 - Искупаться")
                slow_print("2 - Пещера")
                slow_print("3 - Вода")
                slow_print("4 - Назад")
                a = get_choice(4)
                if a == 1:
                    heal(25)
                elif a == 2:
                    add_gold(random.randint(200, 600))
                elif a == 3:
                    add_item("Целебная вода")
                else:
                    current_location = "Развилка"; break
                input("Enter...")

        elif choice == 25:
            show_inventory()
            input("Enter...")

        elif choice == 26:
            use_item()
            input("Enter...")

        elif choice == 27:
            slow_print("Ты отдыхаешь на развилке.")
            heal(25)
            f.day += 1
            slow_print("Наступил день " + str(f.day))
            add_xp(3)
            input("Enter...")

        elif choice == 28:
            show_ending_progress()


# ==========================================
# ГЛАВНЫЙ ЦИКЛ (запуск партий)
# ==========================================

print("================================")
print("       ЛЕСНОЕ ПРИКЛЮЧЕНИЕ")
print("================================")

current_name = None
current_bonus = None

while True:
    if current_name is None:
        # Первая партия или игрок выбрал нового персонажа
        reset_game_state()
        current_name, current_bonus = choose_name()
    else:
        # Продолжаем тем же персонажем — сбрасываем состояние,
        # но заново применяем его бонусы
        reset_game_state()
        print()
        print("=====================================")
        print("  ТЫ СНОВА ИГРАЕШЬ ЗА " + current_name.upper())
        print("=====================================")
        apply_bonuses(current_name, current_bonus)
        print()
        input("Нажми Enter, чтобы начать заново...")

    # одна полная партия
    play_session(current_name)

    # после финала — спросить, что делать дальше
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
        # оставляем current_name как есть — цикл перезапустит его
        continue
    elif ans == 2:
        current_name = None
        current_bonus = None
        continue
    else:
        slow_print("Спасибо за игру! До встречи в лесу.")
        break