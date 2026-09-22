
























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
    if f.undead_defeated and f.troll_defeated and f.gold >= 1500:
        return "dungeon_lord"
    if f.gold >= 500 and f.day >= 10 and not f.dragon_defeated:
        return "peaceful"
    return None


def ending_text(which):
    if which == "escape":
        return ("ТЫ ВЫБРАЛСЯ В РЕАЛЬНЫЙ МИР!\n"
                "Ключ открыл дверь в белый коридор.\n"
                "Ты дома. Лесное приключение было сном?")
    if which == "savior":
        return ("ТЫ СПАСИТЕЛЬ КОРОЛЕВСТВА!\n"
                "Дракон побеждён, принцесса спасена.\n"
                "Король дарует тебе титул.")
    if which == "friend":
        return ("ТЫ ДРУГ ЛЕСА!\n"
                "Волк, фея и единорог — твои спутники.\n"
                "Лес признал тебя своим.")
    if which == "legend":
        return ("ТЫ ЛЕГЕНДАРНЫЙ ГЕРОЙ!\n"
                "Тролль, призраки и дракон пали.\n"
                "Сундуки ломятся от золота.")
    if which == "dungeon_lord":
        return ("ТЫ ЛОРД ПОДЗЕМЕЛИЙ!\n"
                "Призраки и тролль повержены.\n"
                "Ты правишь глубокими залами.")
    if which == "peaceful":
        return ("ТЫ МИРНЫЙ ЖИТЕЛЬ!\n"
                "Много дней ты спокойно жил в лесу,\n"
                "собирая золото без сражений.")
    return ""


def show_progress():
    print()
    print("=== ПРОГРЕСС КОНЦОВОК ===")
    print("1. Побег:")
    print("   ключ " + ("v" if f.strange_key else "x") +
          "  дверь " + ("v" if f.escape_ready else "x"))
    print("2. Спаситель:")
    print("   дракон " + ("v" if f.dragon_defeated else "x") +
          "  принцесса " + ("v" if f.princess_saved else "x"))
    print("3. Друг леса:")
    print("   волк " + ("v" if f.wolf_friend else "x") +
          "  фея " + ("v" if f.fairy_friend else "x") +
          "  единорог " + ("v" if f.unicorn_friend else "x"))
    print("4. Легендарный герой:")
    print("   ур." + str(f.level) + "  зол." + str(f.gold) +
          "  дракон " + ("v" if f.dragon_defeated else "x") +
          "  призраки " + ("v" if f.undead_defeated else "x") +
          "  тролль " + ("v" if f.troll_defeated else "x"))
    print("5. Лорд подземелий:")
    print("   призраки " + ("v" if f.undead_defeated else "x") +
          "  тролль " + ("v" if f.troll_defeated else "x") +
          "  зол." + str(f.gold))
    print("6. Мирный житель:")
    print("   день " + str(f.day) + "  зол." + str(f.gold) +
          "  дракон " + ("x" if not f.dragon_defeated else "v"))
    input("Enter...")