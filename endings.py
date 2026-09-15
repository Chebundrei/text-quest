# ==========================================
# endings.py
# Проверка и показ концовок
# ==========================================

import sys
import functions as _f


def check_endings():
    if _f.escape_ready and _f.strange_key:
        return "escape"
    if _f.dragon_defeated and _f.princess_saved:
        return "savior"
    if _f.wolf_friend and _f.fairy_friend and _f.unicorn_friend:
        return "friend"
    if _f.level >= 5 and _f.gold >= 3000 \
            and _f.dragon_defeated and _f.undead_defeated and _f.troll_defeated:
        return "legend"
    return None


def show_ending(which):
    sp = _f.slow_print
    print()
    print("=====================================")
    print("           ФИНАЛ ИГРЫ")
    print("=====================================")
    print()

    if which == "escape":
        sp("ТЫ ВЫБРАЛСЯ В РЕАЛЬНЫЙ МИР!")
        print()
        sp("Ключ повернулся в замке. Дверь со скрипом открылась —")
        sp("и за ней оказался вовсе не подвал, а белый коридор.")
        sp("Ты идёшь по нему всё дальше и дальше,")
        sp("пока не упираешься в знакомую дверь.")
        sp("За ней — твоя комната. Ты дома.")
        print()
        sp("Лесное приключение было сном. Или нет?")
        sp("На столе лежит тот самый странный ключ.")
        print()
        sp("Награда: свобода от иллюзии.")
    elif which == "savior":
        sp("ТЫ — СПАСИТЕЛЬ КОРОЛЕВСТВА!")
        print()
        sp("Дракон повержен. Принцесса спасена.")
        sp("Ты стоишь на балконе замка, а внизу ликует народ.")
        sp("Король вручает тебе ключ от сокровищницы.")
        sp("Твоё имя войдёт в легенды на века.")
    elif which == "friend":
        sp("ТЫ — ДРУГ ЛЕСА!")
        print()
        sp("Волк идёт рядом, фея кружит над головой,")
        sp("единорог ведёт тебя по тайным тропам.")
        sp("Лес признал тебя своим. Ни одно зло")
        sp("не посмеет войти в эти чащи.")
    elif which == "legend":
        sp("ТЫ — ЛЕГЕНДАРНЫЙ ГЕРОЙ!")
        print()
        sp("Тролль, призраки, дракон — все пали от твоей руки.")
        sp("Твои сундуки ломятся от золота,")
        sp("а барды поют о тебе в каждой таверне.")

    print()
    sp("Уровень: " + str(_f.level) + " | Опыт: " + str(_f.xp) +
       " | Золото: " + str(_f.gold))
    sp("День: " + str(_f.day))
    print()
    sp("Поздравляем с победой!")
    print()
    input("Нажми Enter, чтобы выйти...")
    sys.exit()


def show_ending_progress():
    sp = _f.slow_print
    print()
    sp("=== ПРОГРЕСС КОНЦОВОК ===")
    print()
    sp("0. Побег в реальный мир:")
    sp("   Странный ключ найден: " + ("v" if _f.strange_key else "x"))
    sp("   Запертая дверь найдена: " + ("v" if _f.escape_ready else "x"))
    sp("   (ключ ищи в подвалах, шанс 20% в сундуке)")
    print()
    sp("1. Спаситель королевства:")
    sp("   дракон побеждён: " + ("v" if _f.dragon_defeated else "x"))
    sp("   принцесса спасена: " + ("v" if _f.princess_saved else "x"))
    print()
    sp("2. Друг леса:")
    sp("   волк: " + ("v" if _f.wolf_friend else "x") +
       " | фея: " + ("v" if _f.fairy_friend else "x") +
       " | единорог: " + ("v" if _f.unicorn_friend else "x"))
    print()
    sp("3. Легендарный герой:")
    sp("   уровень >= 5: " + ("v" if _f.level >= 5 else "x") +
       " (сейчас " + str(_f.level) + ")")
    sp("   золото >= 3000: " + ("v" if _f.gold >= 3000 else "x") +
       " (сейчас " + str(_f.gold) + ")")
    sp("   дракон: " + ("v" if _f.dragon_defeated else "x") +
       " | призраки: " + ("v" if _f.undead_defeated else "x") +
       " | тролль: " + ("v" if _f.troll_defeated else "x"))
    input("Enter...")