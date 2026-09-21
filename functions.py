import os
import random
import winsound


SOUND_DIR = r"C:\Users\cl\Desktop\soundds"
SND_CLICK = os.path.join(SOUND_DIR, "click.wav")
SND_ERROR = os.path.join(SOUND_DIR, "error.wav")
SND_LOSE  = os.path.join(SOUND_DIR, "lose.wav")
SND_WIN   = os.path.join(SOUND_DIR, "win.wav")


def _play(path):
    if not os.path.exists(path):
        return
    try:
        winsound.PlaySound(path, winsound.SND_FILENAME | winsound.SND_ASYNC)
    except Exception:
        pass


def click():
    _play(SND_CLICK)


def error():
    _play(SND_ERROR)


def lose():
    _play(SND_LOSE)


def win():
    _play(SND_WIN)


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


def draw_location(canvas, kind):
    canvas.delete("all")
    c = canvas
    if kind == "cross":
        c.create_oval(380, 120, 520, 260,
                      fill="#1e3a1e", outline="#88ff88", width=3)
        c.create_text(450, 190, text="РАЗВИЛКА",
                      fill="#e8e8c8", font=("Consolas", 16, "bold"))
        c.create_line(450, 260, 250, 340, fill="#a08050", width=6)
        c.create_line(450, 260, 450, 340, fill="#a08050", width=6)
        c.create_line(450, 260, 650, 340, fill="#a08050", width=6)
        c.create_text(250, 355, text="Лес",
                      fill="#c8ffc8", font=("Consolas", 11))
        c.create_text(450, 355, text="Деревня",
                      fill="#c8ffc8", font=("Consolas", 11))
        c.create_text(650, 355, text="Болото",
                      fill="#c8ffc8", font=("Consolas", 11))
    elif kind == "forest":
        for x in range(60, 880, 90):
            c.create_rectangle(x, 200, x + 18, 320,
                               fill="#5a3a1a", outline="")
            c.create_polygon(x - 25, 200, x + 45, 200, x + 10, 130,
                             fill="#1e5a1e", outline="#2e7a2e", width=2)
        c.create_text(450, 60, text="ЛЕС",
                      fill="#e8e8c8", font=("Consolas", 20, "bold"))
    elif kind == "village":
        for x in (200, 400, 600):
            c.create_rectangle(x, 200, x + 130, 300,
                               fill="#7a5a3a", outline="#3a2a1a", width=2)
            c.create_polygon(x - 10, 200, x + 70, 140, x + 140, 200,
                             fill="#8b3a1a", outline="#3a1a0a", width=2)
            c.create_rectangle(x + 50, 250, x + 80, 300, fill="#3a2a1a")
        c.create_text(450, 60, text="ДЕРЕВНЯ",
                      fill="#e8e8c8", font=("Consolas", 20, "bold"))
    elif kind == "swamp":
        c.create_rectangle(0, 250, 900, 380, fill="#2a4a3a", outline="")
        for x in range(40, 900, 100):
            c.create_oval(x, 270, x + 80, 310,
                          fill="#3a6a4a", outline="#1e3a2a")
        c.create_text(450, 60, text="БОЛОТО",
                      fill="#e8e8c8", font=("Consolas", 20, "bold"))
    elif kind == "castle":
        c.create_rectangle(250, 150, 650, 320,
                           fill="#6a6a7a", outline="#3a3a4a", width=3)
        c.create_rectangle(200, 120, 280, 320,
                           fill="#8a8a9a", outline="#3a3a4a", width=3)
        c.create_rectangle(620, 120, 700, 320,
                           fill="#8a8a9a", outline="#3a3a4a", width=3)
        c.create_polygon(200, 120, 240, 70, 280, 120, fill="#8b3a1a")
        c.create_polygon(620, 120, 660, 70, 700, 120, fill="#8b3a1a")
        c.create_rectangle(420, 240, 480, 320, fill="#3a2a1a")
        c.create_text(450, 60, text="ЗАМОК",
                      fill="#e8e8c8", font=("Consolas", 20, "bold"))
    elif kind == "dragon":
        c.create_oval(330, 100, 570, 280,
                      fill="#5a1a1a", outline="#ff4444", width=4)
        c.create_text(450, 180, text="ДРАКОН",
                      fill="#ffcccc", font=("Consolas", 22, "bold"))
        c.create_polygon(350, 130, 300, 80, 380, 110,
                         fill="#7a2a2a", outline="#ff4444")
        c.create_polygon(550, 130, 600, 80, 520, 110,
                         fill="#7a2a2a", outline="#ff4444")
    elif kind == "cemetery":
        c.create_rectangle(0, 300, 900, 380, fill="#1a1a2a", outline="")
        for x in range(80, 880, 120):
            c.create_rectangle(x, 220, x + 60, 300,
                               fill="#4a4a5a", outline="#2a2a3a", width=2)
            c.create_line(x + 30, 220, x + 30, 200,
                          fill="#8a8a9a", width=3)
            c.create_line(x + 20, 200, x + 40, 200,
                          fill="#8a8a9a", width=3)
        c.create_text(450, 60, text="КЛАДБИЩЕ",
                      fill="#c8c8d8", font=("Consolas", 20, "bold"))
    elif kind == "sea":
        c.create_rectangle(0, 0, 900, 380, fill="#0a2a4a", outline="")
        for y in range(120, 380, 40):
            c.create_line(0, y, 900, y, fill="#1a4a7a", width=3)
        c.create_text(450, 60, text="МОРЕ",
                      fill="#c8e8ff", font=("Consolas", 20, "bold"))
    elif kind == "mountains":
        c.create_polygon(100, 340, 300, 80, 500, 340,
                         fill="#4a4a5a", outline="#2a2a3a", width=3)
        c.create_polygon(400, 340, 600, 120, 800, 340,
                         fill="#5a5a6a", outline="#2a2a3a", width=3)
        c.create_text(450, 60, text="ГОРЫ",
                      fill="#e8e8c8", font=("Consolas", 20, "bold"))
    elif kind == "ruins":
        for x in (150, 350, 550, 750):
            c.create_rectangle(x, 200, x + 60, 340,
                               fill="#7a6a5a", outline="#3a2a1a", width=2)
            c.create_line(x, 200, x + 60, 200, fill="#3a2a1a", width=2)
        c.create_text(450, 60, text="РУИНЫ",
                      fill="#e8e8c8", font=("Consolas", 20, "bold"))
    elif kind == "win":
        for _ in range(80):
            x = random.randint(0, 900)
            y = random.randint(0, 380)
            col = random.choice(["#ffd166", "#88ff88",
                                 "#88ccff", "#ff8888", "#ff88ff"])
            c.create_oval(x, y, x + 10, y + 10, fill=col, outline="")
        c.create_text(450, 180, text="ПОБЕДА!",
                      fill="#ffd166", font=("Consolas", 40, "bold"))
    elif kind == "lose":
        c.create_rectangle(0, 0, 900, 380, fill="#2a0a0a", outline="")
        c.create_text(450, 190, text="ТЫ ПРОИГРАЛ",
                      fill="#ff4444", font=("Consolas", 36, "bold"))