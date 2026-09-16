# ==========================================
# endings.py
# Проверка и показ концовок
# ==========================================

import sys
import functions as f


def check_endings():
    if f.escape_ready and f.strange_key:
        return "escape"
    if f.dragon_defeated and f.princess_saved:
        return "savior"
    if f.wolf_friend and f.fairy_friend and f.unicorn_friend:
        return "friend"
    if f.level >= 5 and f.gold >= 3000 \
            and f.dragon_defeated and f.undead_defeated and f.troll_defeated:
        return "legend"
    return None


def show_ending(which):
    sp = f.slow_print
    print()
    print("=====================================")
    print("           ФИНАЛ ИГРЫ")
    print("=====================================")
    print()

    if which == "escape":
        sp("ТЫ ВЫБРАЛСЯ В РЕАЛЬНЫЙ МИР!")
        print()
        sp("Ключ повернулся в замке. Дверь со скрипом открылась —")
        sp("за ней оказался не подвал, а белый коридор.")
        sp("Ты упираешься в знакомую дверь. За ней — твоя комната.")
        sp("На столе лежит тот самый странный ключ.")
        sp("Награда: свобода от иллюзии.")
    elif which == "savior":
        sp("ТЫ — СПАСИТЕЛЬ КОРОЛЕВСТВА!")
        print()
        sp("Дракон повержен. Принцесса спасена.")
        sp("Король вручает тебе ключ от сокровищницы.")
    elif which == "friend":
        sp("ТЫ — ДРУГ ЛЕСА!")
        print()
        sp("Волк идёт рядом, фея кружит над головой,")
        sp("единорог ведёт тебя по тайным тропам.")
    elif which == "legend":
        sp("ТЫ — ЛЕГЕНДАРНЫЙ ГЕРОЙ!")
        print()
        sp("Тролль, призраки, дракон — все пали от твоей руки.")

    print()
    sp("Уровень: " + str(f.level) + " | Опыт: " + str(f.xp) +
       " | Золото: " + str(f.gold))
    sp("День: " + str(f.day))
    print()
    sp("Поздравляем с победой!")
    print()


def show_ending_progress():
    sp = f.slow_print
    print()
    sp("=== ПРОГРЕСС КОНЦОВОК ===")
    sp("0. Побег в реальный мир:")
    sp("   ключ: " + ("v" if f.strange_key else "x"))
    sp("   дверь: " + ("v" if f.escape_ready else "x"))
    sp("1. Спаситель:")
    sp("   дракон: " + ("v" if f.dragon_defeated else "x"))
    sp("   принцесса: " + ("v" if f.princess_saved else "x"))
    sp("2. Друг леса:")
    sp("   волк: " + ("v" if f.wolf_friend else "x") +
       " | фея: " + ("v" if f.fairy_friend else "x") +
       " | единорог: " + ("v" if f.unicorn_friend else "x"))
    sp("3. Легендарный герой:")
    sp("   уровень: " + str(f.level) + " (нужно >= 5)")
    sp("   золото: " + str(f.gold) + " (нужно >= 3000)")
    sp("   дракон: " + ("v" if f.dragon_defeated else "x") +
       " | призраки: " + ("v" if f.undead_defeated else "x") +
       " | тролль: " + ("v" if f.troll_defeated else "x"))
    input("Enter...")