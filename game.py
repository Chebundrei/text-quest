
























import random

import functions as f
import endings as e


NAME_OPTIONS = [
    ("Ростислав", "выигрываете автоматически.",
     {"gold": 500, "hp": 50, "items": ["Рыцарский меч", "Королевский амулет"]}),
    ("Олег", "Проверьте работу Бабурина Андрея.",
     {"gold": 200, "hp": 30, "items": ["Книга", "Книга", "Книга"]}),
    ("Даня", "мы тебя съедим.",
     {"gold": 100, "hp": 1, "items": ["ты бомж"]}),
    ("Аким", "Минусовая однёрка придёт!",
     {"gold": 100, "hp": 20, "items": ["Книга", "Зелье силы"]}),
    ("Инга", "Объяснительная за 7-ми кланчиков ждёт вас.",
     {"gold": 350, "hp": 50, "items": ["Амулет удачи", "ШКОЛА"]}),
    ("Василь", "Найди Бабурина Андрея в ЭЖД.",
     {"gold": 120, "hp": 25, "items": ["Книга", "100 ручек"]}),
    ("Алексей", "Когда будут опыты?",
     {"gold": 350, "hp": 70, "items": ["Магический кристалл"]}),
    ("Артём", "Не грызи ручки.",
     {"gold": 0, "hp": 40, "items": ["Зелье лечения", "Еда"]}),
    ("Ваня", "67.", {"gold": 67, "hp": 67, "items": ["Меч"]}),
    ("Миша", "67.", {"gold": 67, "hp": 67, "items": ["Лук"]}),
    ("Другое", "ок. Идём в лес!", {"gold": 0, "hp": 0, "items": []}),
]


REPLIES = {
    "escape":  "Ты обернулся. Ключ лежит на столе. Никто не знает почему.",
    "savior":  "Королевство ликует. Ты — его новый герой.",
    "friend":  "Лес шумит листвой. Волк, фея и единорог улыбаются тебе.",
    "legend":  "Барды уже слагают новые песни о твоих подвигах.",
    "dungeon_lord": "Глубокие залы признали тебя хозяином.",
    "peaceful": "Ты просто жил. И этого хватило.",
    "lose":    "Тьма смыкается. Может быть, в следующий раз повезёт.",
}


def choose_name():
    print()
    print("=====================================")
    print("         ВЫБЕРИ СВОЁ ИМЯ")
    print("=====================================")
    for i, (name, _p, _b) in enumerate(NAME_OPTIONS, 1):
        print(f"{i} - {name}")
    print("=====================================")
    idx = f.ask_choice(len(NAME_OPTIONS))

    chosen, phrase, bonus = NAME_OPTIONS[idx - 1]

    if chosen == "Другое":
        while True:
            custom = input("Введи своё имя: ").strip()
            if custom:
                break
            f.sound("error")
            print("Имя не может быть пустым.")
        name = custom
        phrase = "Другое — ок. Идём в лес, " + custom + "!"
    else:
        name = chosen

    print()
    f.slow_print("Итак, тебя зовут " + name + ".")
    f.slow_print(phrase)
    return name, bonus


def apply_bonus(bonus):
    g = int(bonus.get("gold", 0))
    h = int(bonus.get("hp", 0))
    if g > 0:
        f.gold += g
    if h > 0:
        f.max_hp += h
        f.hp = f.max_hp
    for it in bonus.get("items", []):
        f.add_item(it)


def show_ending_screen(kind):
    if kind == "lose":
        f.show_location("Поражение")
        f.sound("lose")
        text = "Ты погиб в лесу..."
    else:
        f.show_location("Победа")
        f.sound("win")
        text = e.ending_text(kind)

    f.slow_print(text)
    print()
    print("1 - Ответить")
    f.ask_choice(1)
    f.slow_print(REPLIES.get(kind, ""))
    print()
    print("1 - Играть снова")
    print("2 - Другой персонаж")
    print("3 - Выйти")
    a = f.ask_choice(3)
    return a


# ==========================================
# ЛОКАЦИИ
# ==========================================

def loc_forest():
    while True:
        f.show_location("Лес")
        f.show_status()
        print("=== ЛЕС ===")
        print("1 - В чащу")
        print("2 - Собрать травы")
        print("3 - К ручью")
        print("4 - К дубу")
        print("5 - Найти замок")
        print("6 - Назад")
        a = f.ask_choice(6)

        if a == 1:
            if not f.wolf_friend:
                f.damage(random.randint(10, 25))
                f.slow_print(f"Волк напал! HP: {f.hp}")
                print("1 - Погладить волка")
                print("2 - Убежать")
                b = f.ask_choice(2)
                if b == 1:
                    f.wolf_friend = True
                    f.add_item("Друг-волк")
                    f.slow_print("Волк стал твоим другом!")
            else:
                f.heal(20)
                f.slow_print("Волк рад тебе! +20 HP.")

        elif a == 2:
            if not f.can_reward("herbs"):
                f.slow_print("Здесь больше нечего собирать.")
            else:
                f.mark_reward("herbs")
                f.add_item("Трава")
                f.heal(5)
                f.add_xp(2)
                f.slow_print("Ты собрал травы. +5 HP, +2 опыта.")

        elif a == 3:
            if not f.can_reward("stream"):
                f.slow_print("В ручье больше нет рыбы.")
            else:
                f.mark_reward("stream")
                f.add_item("Свежая рыба")
                f.heal(10)
                f.slow_print("Ты поймал рыбу. +10 HP.")

        elif a == 4:
            if not f.can_reward("oak"):
                f.slow_print("Дупло пустое.")
            else:
                f.mark_reward("oak")
                g = random.randint(30, 90)
                f.add_gold(g)
                f.slow_print(f"В дупле дуба — золото! +{g}.")

        elif a == 5:
            f.castle_found = True
            f.add_xp(10)
            f.slow_print("С холма виден замок!")

        else:
            return

        input("Enter...")
        if f.hp <= 0:
            return


def loc_swamp():
    while True:
        f.show_location("Болото")
        f.show_status()
        print("1 - Искать клад")
        print("2 - К хижине ведьмы")
        print("3 - Назад")
        a = f.ask_choice(3)

        if a == 1:
            if not f.can_reward("swamp"):
                f.slow_print("Болото больше ничего не отдаёт.")
            else:
                f.mark_reward("swamp")
                roll = random.random()
                if roll < 0.2 and not f.strange_key:
                    f.strange_key = True
                    f.add_item("Странный ключ")
                    f.slow_print("Ты нашёл СТРАННЫЙ КЛЮЧ!")
                elif roll < 0.6:
                    g = random.randint(30, 100)
                    f.add_gold(g)
                    f.slow_print(f"Ты нашёл золото! +{g}.")
                else:
                    f.damage(random.randint(5, 15))
                    f.slow_print("Змея укусила! -HP.")

        elif a == 2:
            if not f.can_reward("swamp_hut"):
                f.slow_print("Ведьма больше ничего не даёт.")
            elif f.gold >= 30:
                f.gold -= 30
                f.mark_reward("swamp_hut")
                f.add_item("Болотный амулет")
                f.slow_print("Ведьма дала амулет за 30 золота.")
            else:
                f.slow_print("Нужно 30 золота.")

        else:
            return

        input("Enter...")
        if f.hp <= 0:
            return


def loc_village():
    while True:
        f.show_location("Деревня")
        f.show_status()
        print("=== ДЕРЕВНЯ ===")
        print("1 - К замку")
        print("2 - К троллю")
        print("3 - Кузница")
        print("4 - Таверна")
        print("5 - Подвал старосты")
        print("6 - Назад")
        a = f.ask_choice(6)

        if a == 1:
            return "castle"

        elif a == 2:
            if f.troll_defeated:
                f.slow_print("Тролль уже побеждён.")
            elif random.random() < 0.6:
                f.add_gold(150)
                f.troll_defeated = True
                f.add_xp(40)
                f.slow_print("Ты победил тролля! +150 золота.")
            else:
                f.damage(40)
                f.slow_print("Тролль ранил тебя! -40 HP.")

        elif a == 3:
            if not f.can_reward("smithy"):
                f.slow_print("Кузнец больше не кует для тебя.")
            elif f.gold >= 100:
                f.gold -= 100
                f.mark_reward("smithy")
                f.add_item("Меч")
                f.slow_print("Кузнец дал тебе меч. -100 золота.")
            else:
                f.slow_print("Нужно 100 золота.")

        elif a == 4:
            f.heal(30)
            f.day += 1
            f.slow_print(f"Ты отдохнул. +30 HP. День {f.day}.")

        elif a == 5:
            f.explore_basement("дома старосты")

        else:
            return "cross"

        input("Enter...")
        if f.hp <= 0:
            return "die"


def loc_castle():
    while True:
        f.show_location("Замок")
        f.show_status()
        print("=== ЗАМОК ===")
        print("1 - К дракону")
        print("2 - В тронный зал")
        print("3 - Библиотека")
        print("4 - Подвал замка")
        print("5 - Назад")
        a = f.ask_choice(5)

        if a == 1:
            return "dragon"
        elif a == 2:
            if not f.dragon_defeated:
                f.slow_print("Сначала убей дракона!")
            elif not f.princess_saved:
                f.princess_saved = True
                f.add_gold(500)
                f.add_xp(50)
                f.slow_print("Ты спас принцессу! +500 золота.")
            else:
                f.slow_print("Принцесса уже спасена.")
        elif a == 3:
            if not f.can_reward("library"):
                f.slow_print("Ты уже прочитал все редкие книги.")
            else:
                f.mark_reward("library")
                f.add_xp(20)
                f.add_item("Книга")
                f.slow_print("Прочитал книги. +20 опыта, книга.")
        elif a == 4:
            f.explore_basement("замка")
        else:
            return "village"
        input("Enter...")


def loc_dragon():
    while True:
        f.show_location("Драконье логово")
        f.show_status()
        print("1 - Сражаться")
        print("2 - Договориться")
        print("3 - Убежать")
        a = f.ask_choice(3)

        if a == 1:
            if f.dragon_defeated:
                f.slow_print("Дракон уже повержен.")
            elif random.random() < 0.5:
                f.dragon_defeated = True
                f.add_gold(1000)
                f.add_xp(80)
                f.slow_print("Дракон повержен! +1000 золота.")
            else:
                f.damage(50)
                f.slow_print("Дракон обжёг тебя! -50 HP.")
        elif a == 2:
            if f.dragon_defeated:
                f.slow_print("Дракон уже покинул логово.")
            else:
                f.add_gold(400)
                f.dragon_defeated = True
                f.slow_print("Дракон согласился на мир. +400 золота.")
        else:
            return "castle"

        input("Enter...")
        if f.hp <= 0:
            return "die"


def loc_cemetery():
    while True:
        f.show_location("Кладбище")
        f.show_status()
        print("1 - Склеп")
        print("2 - Призраки")
        print("3 - Назад")
        a = f.ask_choice(3)
        if a == 1:
            if not f.can_reward("crypt"):
                f.slow_print("Склеп пуст.")
            else:
                f.mark_reward("crypt")
                g = random.randint(100, 400)
                f.add_gold(g)
                f.slow_print(f"В склепе — золото! +{g}.")
        elif a == 2:
            if f.undead_defeated:
                f.slow_print("Призраки уже развеяны.")
            elif random.random() < 0.6:
                f.undead_defeated = True
                f.add_xp(30)
                f.slow_print("Ты развеял призраков! +30 опыта.")
            else:
                f.damage(30)
                f.slow_print("Призраки ранили! -30 HP.")
        else:
            return
        input("Enter...")
        if f.hp <= 0:
            return


def loc_ruins():
    while True:
        f.show_location("Руины")
        f.show_status()
        print("1 - Алтарь")
        print("2 - Сокровищница")
        print("3 - Назад")
        a = f.ask_choice(3)
        if a == 1:
            if not f.can_reward("altar"):
                f.slow_print("Алтарь уже не отвечает.")
            else:
                f.mark_reward("altar")
                f.add_item("Магический артефакт")
                f.add_xp(40)
                f.slow_print("Ты нашёл артефакт! +40 опыта.")
        elif a == 2:
            if not f.can_reward("ruins_treasure"):
                f.slow_print("Сокровищница руин пуста.")
            else:
                f.mark_reward("ruins_treasure")
                g = random.randint(500, 1500)
                f.add_gold(g)
                f.slow_print(f"Ты нашёл сокровищницу руин! +{g}.")
        else:
            return
        input("Enter...")


def loc_fairy():
    while True:
        f.show_location("Лес фей")
        f.show_status()
        print("1 - Найти фею")
        print("2 - Собрать пыльцу")
        print("3 - Назад")
        a = f.ask_choice(3)
        if a == 1:
            if f.fairy_friend:
                f.slow_print("Фея уже подружилась с тобой.")
            else:
                f.fairy_friend = True
                f.add_item("Дар феи")
                f.add_xp(30)
                f.slow_print("Фея стала твоим другом! +30 опыта.")
        elif a == 2:
            if not f.can_reward("fairy_dust"):
                f.slow_print("Пыльцы больше нет.")
            else:
                f.mark_reward("fairy_dust")
                f.add_item("Волшебная пыльца")
                f.heal(10)
                f.slow_print("Ты собрал пыльцу. +10 HP.")
        else:
            return
        input("Enter...")


def loc_unicorns():
    while True:
        f.show_location("Долина единорогов")
        f.show_status()
        print("1 - Подружиться")
        print("2 - Взять рог")
        print("3 - Назад")
        a = f.ask_choice(3)
        if a == 1:
            if f.unicorn_friend:
                f.slow_print("Единорог уже твой друг.")
            else:
                f.unicorn_friend = True
                f.add_xp(30)
                f.slow_print("Единорог стал твоим другом!")
        elif a == 2:
            if not f.can_reward("unicorn_horn"):
                f.slow_print("Второй рог брать нельзя.")
            else:
                f.mark_reward("unicorn_horn")
                f.add_item("Рог единорога")
                f.add_gold(300)
                f.slow_print("Ты взял рог. +300 золота.")
        else:
            return
        input("Enter...")


# ==========================================
# ИНВЕНТАРЬ
# ==========================================

def show_inventory():
    f.show_status()
    if not f.inventory:
        f.slow_print("Инвентарь пуст.")
        return

    print("Что использовать?")
    for i, item in enumerate(f.inventory, 1):
        print(f"{i} - {item}")
    print(f"{len(f.inventory)+1} - отмена")
    a = f.ask_choice(len(f.inventory) + 1)
    if a == len(f.inventory) + 1:
        return

    item = f.inventory[a - 1]

    if item in ("Трава", "Свежая рыба", "Еда", "Зелье лечения"):
        f.heal(20)
        f.inventory.remove(item)
        f.slow_print("Ты использовал " + item + ". +20 HP.")
    elif item == "ШКОЛА":
        f.inventory.remove(item)
        f.add_item("10000 объяснительных")
        f.slow_print("Ты обменял ШКОЛУ на 10000 объяснительных!")
    elif item == "10000 объяснительных":
        if not f.can_reward("recycle"):
            f.slow_print("Макулатурщик сказал: «Больше не принимаю».")
        else:
            f.mark_reward("recycle")
            f.inventory.remove(item)
            f.add_gold(100)
            f.slow_print("Сдал 10000 объяснительных. +100 золота.")
    elif item == "Странный ключ":
        f.slow_print("Найди запертую дверь в подвале.")
    else:
        f.slow_print("Ты не знаешь, как использовать " + item)


# ==========================================
# ГЛАВНЫЙ ЦИКЛ
# ==========================================

def play_session(player_name):
    f.slow_print("Ты просыпаешься на развилке лесной тропы, " + player_name + ".")
    f.slow_print("Вокруг тёмный лес. Где-то воет волк.")
    input("Enter...")

    while True:
        ending = e.check_endings()
        if ending:
            return show_ending_screen(ending)

        if f.hp <= 0:
            return show_ending_screen("lose")

        f.show_location("Развилка")
        f.show_status()
        print("=== РАЗВИЛКА ===")
        print("1 - Лес")
        print("2 - Деревня")
        print("3 - Болото")
        print("4 - Кладбище")
        print("5 - Руины")
        print("6 - Лес фей")
        print("7 - Долина единорогов")
        print("8 - Инвентарь")
        print("9 - Прогресс концовок")
        print("10 - Отдохнуть")
        a = f.ask_choice(10)

        if a == 1:
            loc_forest()
        elif a == 2:
            nxt = loc_village()
            if nxt == "castle":
                nxt2 = loc_castle()
                if nxt2 == "dragon":
                    loc_dragon()
        elif a == 3:
            loc_swamp()
        elif a == 4:
            loc_cemetery()
        elif a == 5:
            loc_ruins()
        elif a == 6:
            loc_fairy()
        elif a == 7:
            loc_unicorns()
        elif a == 8:
            show_inventory()
            input("Enter...")
        elif a == 9:
            e.show_progress()
        elif a == 10:
            f.heal(25)
            f.day += 1
            f.slow_print(f"Ты отдохнул. +25 HP. День {f.day}.")
            input("Enter...")


def main():
    print("================================")
    print("       ЛЕСНОЕ ПРИКЛЮЧЕНИЕ")
    print("================================")

    current_name = None
    current_bonus = None

    while True:
        if current_name is None:
            f.reset_state()
            current_name, current_bonus = choose_name()
        else:
            f.reset_state()
            print()
            print("Ты снова играешь за " + current_name.upper())
            input("Enter...")

        apply_bonus(current_bonus)
        answer = play_session(current_name)

        if answer == 1:
            continue
        elif answer == 2:
            current_name = None
            current_bonus = None
        else:
            print("Спасибо за игру!")
            return


if __name__ == "__main__":
    main()