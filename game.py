import tkinter as tk
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


class Quest:
    def __init__(self, root):
        self.root = root
        self.root.title("Лесное приключение — 2D")
        self.root.attributes("-fullscreen", True)
        self.root.configure(bg="#1a2b1a")
        self.root.bind("<Escape>", self.toggle_fullscreen)

        self.screen_w = self.root.winfo_screenwidth()
        self.screen_h = self.root.winfo_screenheight()

        self.player_name = None
        self.player_bonus = None

        canvas_h = self.screen_h - 260

        self.canvas = tk.Canvas(root,
                                width=self.screen_w,
                                height=canvas_h,
                                bg="#0f1e0f",
                                highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        self.text = tk.Label(root, text="", font=("Consolas", 16),
                             fg="#e8e8c8", bg="#1a2b1a",
                             justify="left", anchor="nw",
                             wraplength=self.screen_w - 40)
        self.text.place(x=20, y=self.screen_h - 260,
                        width=self.screen_w - 40, height=100)

        self.hp_label = tk.Label(root, text="",
                                 font=("Consolas", 14, "bold"),
                                 fg="#88ff88", bg="#1a2b1a", anchor="w")
        self.hp_label.place(x=20, y=self.screen_h - 155)

        self.gold_label = tk.Label(root, text="",
                                   font=("Consolas", 14, "bold"),
                                   fg="#ffd166", bg="#1a2b1a", anchor="w")
        self.gold_label.place(x=500, y=self.screen_h - 155)

        self.inv_label = tk.Label(root, text="",
                                  font=("Consolas", 12),
                                  fg="#c8c8ff", bg="#1a2b1a", anchor="w")
        self.inv_label.place(x=1000, y=self.screen_h - 155)

        self.buttons = tk.Frame(root, bg="#1a2b1a")
        self.buttons.place(x=20, y=self.screen_h - 130,
                           width=self.screen_w - 40, height=120)

        self._btn_count = 0
        self.show_name_choice()

    # -------- fullscreen --------

    def toggle_fullscreen(self, event=None):
        try:
            self.root.attributes("-fullscreen",
                                 not self.root.attributes("-fullscreen"))
        except Exception:
            pass

    # -------- служебное --------

    def refresh(self):
        bar = max(0, min(20, int(f.hp / f.max_hp * 20)))
        hp_bar = "[" + "|" * bar + "." * (20 - bar) + "]"
        self.hp_label.config(text=f"HP {f.hp}/{f.max_hp} {hp_bar}")
        need = f.level * 10
        self.gold_label.config(
            text=f"Золото: {f.gold}   День: {f.day}   Ур.{f.level} "
                 f"(опыт {f.xp}/{need})")
        inv = ", ".join(f.inventory[-4:]) if f.inventory else "—"
        self.inv_label.config(text="Инвентарь: " + inv)

    def clear_buttons(self):
        for w in self.buttons.winfo_children():
            w.destroy()
        self._btn_count = 0

    def make_button(self, label, cmd, width=18):
        cols = 6
        r = self._btn_count // cols
        c = self._btn_count % cols
        self._btn_count += 1

        b = tk.Button(self.buttons, text=label,
                      font=("Consolas", 12, "bold"),
                      bg="#2e4a2e", fg="#e8e8c8",
                      activebackground="#4a7a4a",
                      activeforeground="#ffffff",
                      relief="raised", bd=3,
                      width=width, height=2, command=cmd)
        b.grid(row=r, column=c, padx=4, pady=4, sticky="nsew")
        self.buttons.grid_columnconfigure(c, weight=1)
        return b

    def set_text(self, s):
        self.text.config(text=s)

    # -------- выбор имени --------

    def show_name_choice(self):
        f.draw_location(self.canvas, "cross")
        self.set_text("Выбери персонажа — нажми кнопку.")
        self.refresh()
        self.clear_buttons()

        for i, (name, _p, _b) in enumerate(NAME_OPTIONS):
            self.make_button(name,
                             lambda idx=i: self.pick_name(idx),
                             width=15)

    def pick_name(self, idx):
        f.click()
        name, phrase, bonus = NAME_OPTIONS[idx]

        if name == "Другое":
            self.set_text("Введи своё имя в консоли...")
            self.root.update()
            try:
                custom = input("Введи своё имя: ").strip()
            except Exception:
                custom = ""
            if not custom:
                custom = "Путник"
            self.player_name = custom
            self.player_bonus = bonus
            self.show_intro(phrase.replace(name, custom))
        else:
            self.player_name = name
            self.player_bonus = bonus
            self.show_intro(phrase)

    def show_intro(self, phrase):
        f.reset_state()
        self.apply_bonus(self.player_bonus)

        self.set_text(f"Итак, тебя зовут {self.player_name}.\n{phrase}")
        self.refresh()
        self.clear_buttons()
        self.make_button("Начать приключение", self.start_game)

    def apply_bonus(self, bonus):
        g = int(bonus.get("gold", 0))
        h = int(bonus.get("hp", 0))
        if g > 0:
            f.gold += g
        if h > 0:
            f.max_hp += h
            f.hp = f.max_hp
        for it in bonus.get("items", []):
            f.add_item(it)

    def start_game(self):
        f.click()
        self.show_crossroads()

    # -------- смерть / конец --------

    def check_death(self):
        if f.hp <= 0:
            f.draw_location(self.canvas, "lose")
            f.lose()
            self.set_text("Ты погиб в лесу...")
            self.clear_buttons()
            self.make_button("Начать заново", self.restart)
            self.make_button("Другой персонаж", self.show_name_choice)
            self.make_button("Выйти", self.root.destroy)
            return True
        return False

    def check_end(self):
        end = e.check_endings()
        if end is None:
            return False
        f.draw_location(self.canvas, "win")
        f.win()
        self.set_text(e.ending_text(end))
        self.clear_buttons()
        self.make_button("Играть снова", self.restart)
        self.make_button("Другой персонаж", self.show_name_choice)
        self.make_button("Выйти", self.root.destroy)
        return True

    def restart(self):
        f.click()
        f.reset_state()
        self.apply_bonus(self.player_bonus)
        self.refresh()
        self.show_crossroads()

    # -------- ШКОЛА / макулатура --------

    def exchange_school(self):
        if "ШКОЛА" not in f.inventory:
            self.set_text("У тебя нет ШКОЛЫ для обмена.")
            self.clear_buttons()
            self.make_button("Назад", self.show_inventory)
            return
        f.inventory.remove("ШКОЛА")
        f.add_item("10000 объяснительных")
        self.set_text("Ты обменял ШКОЛУ на 10000 объяснительных!")
        self.clear_buttons()
        self.make_button("Назад", self.show_inventory)
        self.refresh()

    def recycle_notes(self):
        if "10000 объяснительных" not in f.inventory:
            self.set_text("Нет объяснительных для сдачи.")
            self.clear_buttons()
            self.make_button("Назад", self.show_inventory)
            return
        if not f.can_reward("recycle"):
            self.set_text("Макулатурщик сказал: «Больше не принимаю».")
            self.clear_buttons()
            self.make_button("Назад", self.show_inventory)
            return
        f.mark_reward("recycle")
        f.inventory.remove("10000 объяснительных")
        f.add_gold(100)
        self.set_text("Ты сдал 10000 объяснительных в макулатуру!\n"
                      "+100 золота.")
        self.clear_buttons()
        self.make_button("Назад", self.show_inventory)
        self.refresh()

    # -------- развилка --------

    def show_crossroads(self):
        f.draw_location(self.canvas, "cross")
        self.set_text(f"Ты на развилке, {self.player_name}. Куда пойдёшь?")
        self.refresh()
        self.clear_buttons()
        self.make_button("Лес", self.show_forest)
        self.make_button("Деревня", self.show_village)
        self.make_button("Болото", self.show_swamp)
        self.make_button("Горы", self.show_mountains)
        self.make_button("Море", self.show_sea)
        self.make_button("Кладбище", self.show_cemetery)
        self.make_button("Руины", self.show_ruins)
        self.make_button("Лес фей", self.show_fairy)
        self.make_button("Единороги", self.show_unicorns)
        self.make_button("Инвентарь", self.show_inventory)
        self.make_button("Отдохнуть", self.rest)

    # -------- лес --------

    def show_forest(self):
        f.click()
        f.draw_location(self.canvas, "forest")
        self.set_text("Тёмный лес. Слышен вой волка.")
        self.clear_buttons()
        self.make_button("В чащу", self.forest_thicket)
        self.make_button("Собрать травы", self.forest_herbs)
        self.make_button("К ручью", self.forest_stream)
        self.make_button("К дубу", self.forest_oak)
        self.make_button("Найти замок", self.forest_hill)
        self.make_button("Назад", self.show_crossroads)

    def forest_thicket(self):
        f.click()
        if not f.wolf_friend:
            f.damage(random.randint(10, 25))
            self.set_text(f"Волк напал! HP: {f.hp}")
            self.clear_buttons()
            self.make_button("Погладить волка", self.befriend_wolf)
            self.make_button("Убежать", self.show_forest)
        else:
            f.heal(20)
            self.set_text("Волк рад тебе! +20 HP.")
            self.clear_buttons()
            self.make_button("Дальше", self.show_forest)
        self.refresh()
        self.check_death()

    def befriend_wolf(self):
        f.click()
        f.wolf_friend = True
        f.add_item("Друг-волк")
        self.set_text("Волк стал твоим другом!")
        self.clear_buttons()
        self.make_button("Дальше", self.show_forest)
        self.refresh()
        self.check_end()

    def forest_herbs(self):
        f.click()
        if not f.can_reward("herbs"):
            self.set_text("Здесь больше нечего собирать.")
            self.clear_buttons()
            self.make_button("Назад", self.show_forest)
            return
        f.mark_reward("herbs")
        f.add_item("Трава")
        f.heal(5)
        f.add_xp(2)
        self.set_text("Ты собрал травы. +5 HP, +2 опыта.")
        self.clear_buttons()
        self.make_button("Ещё", self.forest_herbs)
        self.make_button("Назад", self.show_forest)
        self.refresh()

    def forest_stream(self):
        f.click()
        if not f.can_reward("stream"):
            self.set_text("В ручье больше нет рыбы.")
            self.clear_buttons()
            self.make_button("Назад", self.show_forest)
            return
        f.mark_reward("stream")
        f.add_item("Свежая рыба")
        f.heal(10)
        self.set_text("Ты поймал рыбу. +10 HP.")
        self.clear_buttons()
        self.make_button("Ещё", self.forest_stream)
        self.make_button("Назад", self.show_forest)
        self.refresh()

    def forest_oak(self):
        f.click()
        if not f.can_reward("oak"):
            self.set_text("Дупло пустое.")
            self.clear_buttons()
            self.make_button("Назад", self.show_forest)
            return
        f.mark_reward("oak")
        f.add_gold(random.randint(30, 90))
        self.set_text("В дупле дуба — золото!")
        self.clear_buttons()
        self.make_button("Назад", self.show_forest)
        self.refresh()

    def forest_hill(self):
        f.click()
        f.castle_found = True
        f.add_xp(10)
        self.set_text("С холма виден замок!")
        self.clear_buttons()
        self.make_button("В деревню", self.show_village)
        self.make_button("Назад", self.show_forest)
        self.refresh()

    # -------- деревня --------

    def show_village(self):
        f.click()
        f.draw_location(self.canvas, "village")
        self.set_text("Деревня. В центре — замок на холме.")
        self.clear_buttons()
        self.make_button("К замку", self.show_castle)
        self.make_button("К троллю", self.fight_troll)
        self.make_button("Кузница", self.smithy)
        self.make_button("Таверна", self.tavern)
        self.make_button("Храм", self.temple)
        self.make_button("Назад", self.show_crossroads)

    def fight_troll(self):
        f.click()
        if f.troll_defeated:
            self.set_text("Тролль уже побеждён.")
        elif random.random() < 0.6:
            f.add_gold(150)
            f.troll_defeated = True
            f.add_xp(40)
            self.set_text("Ты победил тролля! +150 золота.")
        else:
            f.damage(40)
            self.set_text("Тролль ранил тебя! -40 HP.")
        self.clear_buttons()
        self.make_button("Назад", self.show_village)
        self.refresh()
        self.check_death()
        self.check_end()

    def smithy(self):
        f.click()
        if not f.can_reward("smithy"):
            self.set_text("Кузнец больше не кует для тебя.")
            self.clear_buttons()
            self.make_button("Назад", self.show_village)
            return
        if f.gold >= 100:
            f.gold -= 100
            f.mark_reward("smithy")
            f.add_item("Меч")
            self.set_text("Кузнец дал тебе меч. -100 золота.")
        else:
            self.set_text("Нужно 100 золота.")
        self.clear_buttons()
        self.make_button("Назад", self.show_village)
        self.refresh()

    def tavern(self):
        f.click()
        f.heal(30)
        f.day += 1
        self.set_text("Ты отдохнул. +30 HP, новый день.")
        self.clear_buttons()
        self.make_button("Назад", self.show_village)
        self.refresh()
        self.check_end()

    def temple(self):
        f.click()
        if not f.can_reward("temple"):
            self.set_text("Храм больше не даёт благословения.")
            self.clear_buttons()
            self.make_button("Назад", self.show_village)
            return
        f.mark_reward("temple")
        f.heal(20)
        f.add_item("Святая вода")
        self.set_text("Ты помолился. +20 HP, святая вода.")
        self.clear_buttons()
        self.make_button("Назад", self.show_village)
        self.refresh()

    # -------- замок --------

    def show_castle(self):
        f.click()
        f.draw_location(self.canvas, "castle")
        self.set_text("Замок. Стражник: «Спаси принцессу!»")
        self.clear_buttons()
        self.make_button("К дракону", self.show_dragon)
        self.make_button("В тронный зал", self.throne_room)
        self.make_button("Библиотека", self.library)
        self.make_button("Подвал замка", self.castle_basement)
        self.make_button("Назад", self.show_village)

    def throne_room(self):
        f.click()
        if not f.dragon_defeated:
            self.set_text("Сначала убей дракона!")
        elif not f.princess_saved:
            f.princess_saved = True
            f.add_gold(500)
            f.add_xp(50)
            self.set_text("Ты спас принцессу! +500 золота.")
        else:
            self.set_text("Принцесса уже спасена.")
        self.clear_buttons()
        self.make_button("Назад", self.show_castle)
        self.refresh()
        self.check_end()

    def library(self):
        f.click()
        if not f.can_reward("library"):
            self.set_text("Ты уже прочитал все редкие книги.")
            self.clear_buttons()
            self.make_button("Назад", self.show_castle)
            return
        f.mark_reward("library")
        f.add_xp(20)
        f.add_item("Книга")
        self.set_text("Прочитал книги. +20 опыта, книга.")
        self.clear_buttons()
        self.make_button("Назад", self.show_castle)
        self.refresh()

    def castle_basement(self):
        f.click()
        if not f.can_reward("castle_basement"):
            self.set_text("Подвал замка обыскан.")
            self.clear_buttons()
            self.make_button("Назад", self.show_castle)
            return
        f.mark_reward("castle_basement")
        f.add_gold(random.randint(200, 600))
        self.set_text("В подвале замка — сундук с золотом.")
        self.clear_buttons()
        self.make_button("Назад", self.show_castle)
        self.refresh()
        self.check_end()

    def show_dragon(self):
        f.click()
        f.draw_location(self.canvas, "dragon")
        self.set_text("Логово дракона. Он смотрит на тебя.")
        self.clear_buttons()
        self.make_button("Сражаться", self.fight_dragon)
        self.make_button("Договориться", self.dragon_talk)
        self.make_button("Убежать", self.show_castle)

    def fight_dragon(self):
        f.click()
        if f.dragon_defeated:
            self.set_text("Дракон уже повержен.")
        elif random.random() < 0.5:
            f.dragon_defeated = True
            f.add_gold(1000)
            f.add_xp(80)
            self.set_text("Дракон повержен! +1000 золота.")
        else:
            f.damage(50)
            self.set_text("Дракон обжёг тебя! -50 HP.")
        self.clear_buttons()
        self.make_button("Назад", self.show_castle)
        self.refresh()
        self.check_death()
        self.check_end()

    def dragon_talk(self):
        f.click()
        if f.dragon_defeated:
            self.set_text("Дракон уже покинул логово.")
        else:
            f.add_gold(400)
            f.dragon_defeated = True
            self.set_text("Дракон согласился на мир. +400 золота.")
        self.clear_buttons()
        self.make_button("Назад", self.show_castle)
        self.refresh()
        self.check_end()

    # -------- болото --------

    def show_swamp(self):
        f.click()
        f.draw_location(self.canvas, "swamp")
        self.set_text("Болото. Пахнет сыростью.")
        self.clear_buttons()
        self.make_button("Искать клад", self.swamp_treasure)
        self.make_button("К хижине", self.swamp_hut)
        self.make_button("Назад", self.show_crossroads)

    def swamp_treasure(self):
        f.click()
        if not f.can_reward("swamp"):
            self.set_text("Болото больше ничего не отдаёт.")
            self.clear_buttons()
            self.make_button("Назад", self.show_swamp)
            return
        f.mark_reward("swamp")
        roll = random.random()
        if roll < 0.2 and not f.strange_key:
            f.strange_key = True
            f.add_item("Странный ключ")
            self.set_text("Ты нашёл СТРАННЫЙ КЛЮЧ!")
        elif roll < 0.6:
            gain = random.randint(30, 100)
            f.add_gold(gain)
            self.set_text(f"Ты нашёл золото! +{gain}.")
        else:
            f.damage(random.randint(5, 15))
            self.set_text("Змея укусила! -HP.")
        self.clear_buttons()
        self.make_button("Ещё", self.swamp_treasure)
        self.make_button("Назад", self.show_swamp)
        self.refresh()
        self.check_death()
        self.check_end()

    def swamp_hut(self):
        f.click()
        if not f.can_reward("swamp_hut"):
            self.set_text("Ведьма больше ничего не даёт.")
            self.clear_buttons()
            self.make_button("Назад", self.show_swamp)
            return
        if f.gold >= 30:
            f.gold -= 30
            f.mark_reward("swamp_hut")
            f.add_item("Болотный амулет")
            self.set_text("Ведьма дала амулет за 30 золота.")
        else:
            self.set_text("Нужно 30 золота.")
        self.clear_buttons()
        self.make_button("Назад", self.show_swamp)
        self.refresh()

    # -------- горы --------

    def show_mountains(self):
        f.click()
        f.draw_location(self.canvas, "mountains")
        self.set_text("Горы. Ветер, снег, где-то блестит золото.")
        self.clear_buttons()
        self.make_button("Вершина", self.mountain_top)
        self.make_button("Пещера", self.mountain_cave)
        self.make_button("Назад", self.show_crossroads)

    def mountain_top(self):
        f.click()
        if not f.can_reward("mountain_top"):
            self.set_text("Ты уже покорил эту вершину.")
            self.clear_buttons()
            self.make_button("Назад", self.show_mountains)
            return
        f.mark_reward("mountain_top")
        f.add_xp(20)
        f.add_gold(100)
        self.set_text("Ты взошёл на вершину. +100 золота, +20 опыта.")
        self.clear_buttons()
        self.make_button("Назад", self.show_mountains)
        self.refresh()

    def mountain_cave(self):
        f.click()
        if not f.can_reward("mountain_cave"):
            self.set_text("Пещера пуста.")
            self.clear_buttons()
            self.make_button("Назад", self.show_mountains)
            return
        f.mark_reward("mountain_cave")
        f.add_gold(random.randint(200, 800))
        self.set_text("В пещере ты нашёл сокровища!")
        self.clear_buttons()
        self.make_button("Назад", self.show_mountains)
        self.refresh()
        self.check_end()

    # -------- море --------

    def show_sea(self):
        f.click()
        f.draw_location(self.canvas, "sea")
        self.set_text("Море. Шум волн, крики чаек.")
        self.clear_buttons()
        self.make_button("Поплавать", self.sea_swim)
        self.make_button("Сокровища", self.sea_treasure)
        self.make_button("Назад", self.show_crossroads)

    def sea_swim(self):
        f.click()
        if not f.can_reward("sea_swim"):
            self.set_text("Ты уже накупался вдоволь.")
            self.clear_buttons()
            self.make_button("Назад", self.show_sea)
            return
        f.mark_reward("sea_swim")
        f.heal(15)
        self.set_text("Ты поплавал. +15 HP.")
        self.clear_buttons()
        self.make_button("Назад", self.show_sea)
        self.refresh()

    def sea_treasure(self):
        f.click()
        if not f.can_reward("sea_treasure"):
            self.set_text("Больше сокровищ на дне нет.")
            self.clear_buttons()
            self.make_button("Назад", self.show_sea)
            return
        f.mark_reward("sea_treasure")
        f.add_gold(random.randint(200, 600))
        self.set_text("Ты нашёл затонувшее сокровище!")
        self.clear_buttons()
        self.make_button("Назад", self.show_sea)
        self.refresh()
        self.check_end()

    # -------- кладбище --------

    def show_cemetery(self):
        f.click()
        f.draw_location(self.canvas, "cemetery")
        self.set_text("Кладбище. Тихо. Только вороны.")
        self.clear_buttons()
        self.make_button("Склеп", self.crypt)
        self.make_button("Призраки", self.ghosts)
        self.make_button("Назад", self.show_crossroads)

    def crypt(self):
        f.click()
        if not f.can_reward("crypt"):
            self.set_text("Склеп пуст.")
            self.clear_buttons()
            self.make_button("Назад", self.show_cemetery)
            return
        f.mark_reward("crypt")
        f.add_gold(random.randint(100, 400))
        self.set_text("В склепе — золото.")
        self.clear_buttons()
        self.make_button("Назад", self.show_cemetery)
        self.refresh()

    def ghosts(self):
        f.click()
        if f.undead_defeated:
            self.set_text("Призраки уже развеяны.")
        elif random.random() < 0.6:
            f.undead_defeated = True
            f.add_xp(30)
            self.set_text("Ты развеял призраков! +30 опыта.")
        else:
            f.damage(30)
            self.set_text("Призраки ранили! -30 HP.")
        self.clear_buttons()
        self.make_button("Назад", self.show_cemetery)
        self.refresh()
        self.check_death()
        self.check_end()

    # -------- руины --------

    def show_ruins(self):
        f.click()
        f.draw_location(self.canvas, "ruins")
        self.set_text("Древние руины. Пахнет магией.")
        self.clear_buttons()
        self.make_button("Алтарь", self.altar)
        self.make_button("Сокровищница", self.ruins_treasure)
        self.make_button("Назад", self.show_crossroads)

    def altar(self):
        f.click()
        if not f.can_reward("altar"):
            self.set_text("Алтарь уже не отвечает.")
            self.clear_buttons()
            self.make_button("Назад", self.show_ruins)
            return
        f.mark_reward("altar")
        f.add_item("Магический артефакт")
        f.add_xp(40)
        self.set_text("Ты нашёл артефакт! +40 опыта.")
        self.clear_buttons()
        self.make_button("Назад", self.show_ruins)
        self.refresh()

    def ruins_treasure(self):
        f.click()
        if not f.can_reward("ruins_treasure"):
            self.set_text("Сокровищница руин пуста.")
            self.clear_buttons()
            self.make_button("Назад", self.show_ruins)
            return
        f.mark_reward("ruins_treasure")
        f.add_gold(random.randint(500, 1500))
        self.set_text("Ты нашёл сокровищницу руин!")
        self.clear_buttons()
        self.make_button("Назад", self.show_ruins)
        self.refresh()
        self.check_end()

    # -------- фея --------

    def show_fairy(self):
        f.click()
        f.draw_location(self.canvas, "forest")
        self.set_text("Лес фей. В воздухе блестит пыльца.")
        self.clear_buttons()
        self.make_button("Найти фею", self.find_fairy)
        self.make_button("Собрать пыльцу", self.fairy_dust)
        self.make_button("Назад", self.show_crossroads)

    def find_fairy(self):
        f.click()
        if f.fairy_friend:
            self.set_text("Фея уже подружилась с тобой.")
        else:
            f.fairy_friend = True
            f.add_item("Дар феи")
            f.add_xp(30)
            self.set_text("Фея стала твоим другом! +30 опыта.")
        self.clear_buttons()
        self.make_button("Назад", self.show_fairy)
        self.refresh()
        self.check_end()

    def fairy_dust(self):
        f.click()
        if not f.can_reward("fairy_dust"):
            self.set_text("Пыльцы больше нет.")
            self.clear_buttons()
            self.make_button("Назад", self.show_fairy)
            return
        f.mark_reward("fairy_dust")
        f.add_item("Волшебная пыльца")
        f.heal(10)
        self.set_text("Ты собрал пыльцу. +10 HP.")
        self.clear_buttons()
        self.make_button("Назад", self.show_fairy)
        self.refresh()

    # -------- единороги --------

    def show_unicorns(self):
        f.click()
        f.draw_location(self.canvas, "forest")
        self.set_text("Долина единорогов. Радуга и тишина.")
        self.clear_buttons()
        self.make_button("Подружиться", self.befriend_unicorn)
        self.make_button("Взять рог", self.unicorn_horn)
        self.make_button("Назад", self.show_crossroads)

    def befriend_unicorn(self):
        f.click()
        if f.unicorn_friend:
            self.set_text("Единорог уже твой друг.")
        else:
            f.unicorn_friend = True
            f.add_xp(30)
            self.set_text("Единорог стал твоим другом!")
        self.clear_buttons()
        self.make_button("Назад", self.show_unicorns)
        self.refresh()
        self.check_end()

    def unicorn_horn(self):
        f.click()
        if not f.can_reward("unicorn_horn"):
            self.set_text("Второй рог брать нельзя.")
            self.clear_buttons()
            self.make_button("Назад", self.show_unicorns)
            return
        f.mark_reward("unicorn_horn")
        f.add_item("Рог единорога")
        f.add_gold(300)
        self.set_text("Ты взял рог. +300 золота.")
        self.clear_buttons()
        self.make_button("Назад", self.show_unicorns)
        self.refresh()
        self.check_end()

    # -------- отдых / инвентарь --------

    def rest(self):
        f.click()
        f.heal(25)
        f.day += 1
        self.set_text(f"Ты отдохнул. +25 HP. День {f.day}.")
        self.clear_buttons()
        self.make_button("Назад", self.show_crossroads)
        self.refresh()
        self.check_end()

    def show_inventory(self):
        f.click()
        f.draw_location(self.canvas, "forest")
        if f.inventory:
            self.set_text("Инвентарь:\n" +
                          "\n".join("• " + x for x in f.inventory))
        else:
            self.set_text("Инвентарь пуст.")

        self.clear_buttons()

        if "ШКОЛА" in f.inventory:
            self.make_button("Обменять ШКОЛУ", self.exchange_school)
        if "10000 объяснительных" in f.inventory:
            self.make_button("Сдать в макулатуру", self.recycle_notes)

        self.make_button("Прогресс", self.show_progress)
        self.make_button("Сменить персонажа", self.show_name_choice)
        self.make_button("Назад", self.show_crossroads)

    def show_progress(self):
        f.click()
        self.set_text(e.show_progress())
        self.clear_buttons()
        self.make_button("Назад", self.show_inventory)


if __name__ == "__main__":
    root = tk.Tk()
    Quest(root)
    root.mainloop()