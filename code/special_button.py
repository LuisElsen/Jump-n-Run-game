import os
import pygame.font
import Button
from Window import *
from field import Field
from Enemy import *
import json
from pymongo import MongoClient

pygame.init()
BUTTON_DIST = HEIGHT / 10


class Special(Button):
    buttons = []
    info_font = pygame.font.Font(font_name, 40)
    button_font = pygame.font.Font(font_name, 60)
    fp = "Images\\map maker\\special actions"

    @staticmethod
    def create_text(text: str):
        return Special.info_font.render(text, True, white)

    @staticmethod
    def check_valid() -> bool:
        return Field.get_on_map("start") == 1 and Field.get_on_map("end") == 1  # not needed


class LoadSaveSuper(Special):
    map_folder = "Maps"
    new_map = False
    cluster = MongoClient(
        "mongodb+srv://NextTimeBro:LostThePasswordToqu@cluster0.ocuhchc.mongodb.net/?retryWrites=true&w=majority")
    db = cluster["jump_n_run_maps"]
    if os.path.exists("../name.txt"):
        collection = db[open("../name.txt", "r").read()]

    def __init__(self, image: pygame.surface, img_path, x, y, command=None, text=None, num=None, action=None):
        super().__init__(image, img_path, x, y, command=command, text=text, num=num, action=action)
        self.win = None  # window for load and save file
        self.scroll = 0

    def create_existing_maps(self, method):
        buttons = []
        x = self.win.button_dist
        y = x + 100
        for file in self.collection.find():
            text_img = Special.button_font.render(file["name"].split("\\")[1].split(".")[0], True, white)
            button = Button(text_img, False, x, self.win.height - y,
                            command=lambda f=file: method(f["name"].split("\\")[1].split(".")[0]))
            buttons.append(button)
            y += button.height + BUTTON_DIST / 2
        self.win.update_text([])
        self.win.update_buttons(buttons)

    def save_in_loop(self, screen, mx, my, clicked, events, func=None, var=None, scroll=0):
        LoadSaveSuper.update_collection()
        if self.new_map:
            for event in events:
                if event.type == pygame.KEYDOWN:

                    # Check for backspace
                    if event.key == pygame.K_BACKSPACE:

                        # get text input from 0 to -1 i.e. end.
                        var = var[:-1]
                    elif event.key == pygame.K_RETURN:
                        if func(var):
                            continue
                        var = ""
                        self.new_map = False
                        break
                    # Unicode standard is used for string
                    # formation
                    else:
                        var += event.unicode
                self.win.texts[1][0] = Special.create_text(var)
        for event in events:
            # set scroll
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 4:
                    self.scroll -= 50
                elif event.button == 5:
                    self.scroll += 50
        # window actions
        self.win.surface.fill((0, 0, 0))
        x = screen.get_width() / 2 - self.win.surface.get_width() / 2
        y = screen.get_height() / 2 - self.win.surface.get_height() / 2
        if type(self.win) != Window:
            raise TypeError("must use Special.save first")
        else:
            if self.win.draw(screen, (x, y), mx, my, clicked, scroll=self.scroll):
                self.scroll = 0
                self.new_map = False
                return True, var

        return False, var

    @staticmethod
    def update_collection():
        LoadSaveSuper.collection = LoadSaveSuper.db[open("../name.txt", "r").read()]


class Save(LoadSaveSuper):
    existing_maps = False
    map_name = ""

    def map_saver(self, name):
        if Field.get_on_map("end 1") and Field.get_on_map("start 1"):  # checks if savable
            text = ""
            for field in Field.buttons:
                field_name = repr(field)
                if field_name.split("$")[0] != field.path and field_name.split("$")[0] != "clear":
                    # if smth is on that field
                    text += field_name + "\n"
            if text:
                text = {"map": text, "lives": Lives.get_lives(), "name": self.map_folder + "\\" + name + ".json"}
                self.collection.insert_one(text)
            save_msg = Special.create_text("Map saved!")
            self.win.update_text([[save_msg, self.win.centered, self.win.centered]])
            self.new_map = False
        else:
            save_msg = Special.create_text("Missing start or/and end")
            self.win.update_text([[save_msg, self.win.centered, self.win.centered]])
            self.new_map = False

    def save(self):
        width, height = 800, 600
        text = Special.info_font.render("Save as", True, (255, 255, 255))
        texts = [[text, Window.centered, text.get_height()]]
        buttons = []
        buttons = [
            Button(Special.button_font.render("new Map", True, white), None, 0, height / 2 - 50,
                   command=lambda: self.user_input(True, buttons)),
            Button(Special.button_font.render("existing Map", True, white), None, width / 2,
                   height / 2 - 50, command=lambda: self.user_input(False, buttons))
        ]
        self.win = Window((width, height), texts, buttons)
        self.selected = True
        return 2

    def user_input(self, new_map, buttons):
        for button in buttons:
            button.deiconify()

        if new_map:
            self.new_map = True
            if type(self.win) != Window:
                raise TypeError("must use Special.save first")
            else:
                self.win.update_buttons([])

            text = Special.create_text("Enter a name for your map:")
            self.win.update_text([[text, self.win.centered, 0],
                                  [Special.create_text(self.map_name), self.win.centered, self.win.centered]])
        else:
            self.create_existing_maps(self.map_saver)


class LoadFile(LoadSaveSuper):
    def load_file(self, file):  # actual file loader
        for field in Field.buttons:
            field.reset()
        text = self.load_only(self.map_folder + "\\" + file + ".json")
        Lives.lives = text["lives"]
        Field.set_fields(text["map"], special_dict, Special, Enemy)
        return self.win.stop

    @staticmethod
    def load_only(location):  # formatting the map that's passed with location
        text = LoadSaveSuper.collection.find({"name": location})[0]
        text["map"] = text["map"].split("\n")
        for i in range(len(text["map"])):
                if text["map"][i]:
                    text["map"][i] = text["map"][i].split("$")
                else:
                    text["map"].pop(i)
        return text

    def file_load_window(self):
        self.win = Window((800, 600), [], [])
        self.create_existing_maps(self.load_file)
        text = Special.create_text("Select a map:")
        self.win.update_text([[text, self.win.centered, 0]])
        return 2


class StartEnd(Special):
    # this method is called when u click the start or end button
    def start_end(self):
        rv = None
        self.num = 1 - Field.get_on_map(self.image_path)
        if self.num:
            rv = self.select_obstacle()
        self.set_text(self.text_str.split()[0] + " " + str(1 - Field.get_on_map(self.image_path)), True)
        return rv

    # this method updates the text od start and end button
    def update_text(self):
        self.set_text(self.text_str.split()[0] + " " + str(self.num), True)


class Lives(LoadSaveSuper):
    lives = 3

    # this method is executed when the life button is clicked and sets up the window
    def setup_window(self):
        width, height = 800, 600
        self.win = Window((width, height), [], [])
        text = Special.info_font.render("Enter the number of hearts you want to have", True, white)
        texts = [[text, Window.centered, text.get_height()],
                 [Special.create_text(str(self.lives)), self.win.centered, self.win.centered]]
        self.win.update_text(texts)
        self.selected = True
        self.new_map = True
        return 2

    # this method is run constantly when lives is selected
    def set_lives(self, lives):
        try:
            lives = int(lives)
            Lives.lives = lives
            self.win.update_buttons([])
            self.win.update_text([[Special.create_text("lives set"), Button.centered, Button.centered]])
            self.new_map = False
            return True
        except ValueError:
            self.win.update_text([self.win.texts[0], self.win.texts[1],
                                  [Special.info_font.render("Enter a number", True, (255, 0, 0)), Button.centered,
                                   self.win.get_height() - Special.info_font.get_height()]])
            return True

    @staticmethod
    def get_lives():
        return Lives.lives


class Delete(LoadSaveSuper):
    def setup_window(self):
        width, height = 800, 600
        self.win = Window((width, height), [], [])
        self.create_existing_maps(self.user_check)
        text = Special.button_font.render("Select a map you want to delete:", True, white)
        texts = [[text, Window.centered, text.get_height()]]
        self.win.update_text(texts)
        return 2

    def user_check(self, name):
        text = Special.info_font.render("do you really want to delete " + name, True, (255, 255, 255))
        Button.font = pygame.font.Font(font_name, 100)
        buttons = [
            Button(*Button.create_text_only("yes", 0, self.win.get_height() / 2 - 50),
                   command=lambda n=name: self.delete_file(n)),
            Button(*Button.create_text_only("no", self.win.get_width() / 2, self.win.get_height() / 2 - 50),
                   command=self.setup_window)
        ]
        Button.font = pygame.font.Font(font_name, 20)
        self.win.update_text([[text, Button.centered, 0]])
        self.win.update_buttons(buttons)

    def delete_file(self, name):
        self.collection.delete_one({"name": name})
        self.win.update_buttons([])
        self.win.update_text(
            [[Special.info_font.render("Map deleted!", True, white), Window.centered, Window.centered]])


class Clear(Special):
    def clear(self):
        self.selected = True
        return True


class MainMenu(Special):
    main_menu = None

    @staticmethod
    def go_to_main_menu(_):
        MainMenu.main_menu()


special_dict = {
    "clear": Clear.clear,
    "save": Save.save,
    "start": StartEnd.start_end,
    "end": StartEnd.start_end,
    "load file": LoadFile.file_load_window,
    "main menu": MainMenu.go_to_main_menu,
    "delete file": Delete.setup_window,
    "lives": Lives.setup_window,
}
