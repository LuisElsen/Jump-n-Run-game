import os

from Window import *
from field import Field

pygame.init()
BUTTON_DIST = HEIGHT / 10


class Special(Button):
    buttons = []
    info_font = pygame.font.Font(font_name, 40)
    button_font = pygame.font.Font(font_name, 60)
    new_map = False
    existing_maps = False
    map_name = ""
    map_folder = "Maps"
    main_menu = None

    def __init__(self, image: pygame.surface, img_path, x, y, command=None, text=None, num=None):
        super().__init__(image, img_path, x, y, command=command, text=text, num=num)
        self.win = None  # window for load and save file
        self.scroll = 0

    # special methods
    # save button methods
    def map_saver(self, name):
        if Field.get_on_map("end 1") and Field.get_on_map("start 1"):
            text = ""
            with open(self.map_folder + "/" + name + ".txt", "w") as f:
                for field in Field.buttons:
                    field_name = repr(field)
                    if field_name.split("$")[0] != field.path and field_name.split("$")[0] != "clear":
                        text += field_name + "\n"
                if text:
                    f.write(text)
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

    def save_in_loop(self, screen, mx, my, clicked, events, scroll=0):
        if self.new_map:
            for event in events:
                if event.type == pygame.KEYDOWN:

                    # Check for backspace
                    if event.key == pygame.K_BACKSPACE:

                        # get text input from 0 to -1 i.e. end.
                        Special.map_name = Special.map_name[:-1]
                    elif event.key == pygame.K_RETURN:
                        self.map_saver(Special.map_name)
                        Special.map_name = ""
                        break
                    # Unicode standard is used for string
                    # formation
                    else:
                        Special.map_name += event.unicode
                self.win.texts[1][0] = Special.create_text(Special.map_name)
        for event in events:
            # set scroll
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 4:
                    self.scroll += 50
                elif event.button == 5:
                    self.scroll -= 50
        # window actions
        self.win.surface.fill((0, 0, 0))
        x = screen.get_width() / 2 - self.win.surface.get_width() / 2
        y = screen.get_height() / 2 - self.win.surface.get_height() / 2
        if type(self.win) != Window:
            raise TypeError("must use Special.save first")
        else:
            if self.win.draw(screen, (x, y), mx, my, clicked, scroll=self.scroll):
                self.scroll = 0
                return True

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
            self.create_existing_maps(True)

    def start_end(self):
        rv = None
        self.num = 1 - Field.get_on_map(self.image_path)
        if self.num:
            rv = self.select_obstacle()
        self.set_text(self.text_str.split()[0] + " " + str(1 - Field.get_on_map(self.image_path)), True)
        return rv

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def create_text(text: str):
        return Special.info_font.render(text, True, white)

    def clear(self):
        self.selected = True
        return True

    @staticmethod
    def check_valid() -> bool:
        return Field.get_on_map("start") == 1 and Field.get_on_map("end")

    def create_existing_maps(self, save):
        buttons = []
        x = self.win.button_dist
        y = x
        for file in os.listdir(self.map_folder):
            text_img = Special.button_font.render(file.split(".")[0], True, white)
            #  at the save Button
            if save:
                button = Button(text_img, False, x, self.win.height - y,
                                command=lambda f=file: self.map_saver(f.split(".")[0]))
                buttons.append(button)
            # at the file load button
            else:
                button = Button(text_img, False, x, self.win.height - y, command=lambda f=file: self.load_file(f))
                buttons.append(button)
            y += button.height + BUTTON_DIST/2
        self.win.update_text([])
        self.win.update_buttons(buttons)

    # file load methods
    def load_file(self, file):
        text = self.load_only(self.map_folder + "/" + file)
        Field.set_fields(text, special_dict, Special)
        return self.win.stop

    @staticmethod
    def load_only(location):  # formatting the map that's passed with location
        with open(location, "r") as f:
            text = f.read()
            text = text.split("\n")
            for i in range(len(text)):
                if text[i]:
                    t = text[i].split("$")
                    t[1] = int(t[1])
                    t[2] = int(t[2])
                    text[i] = t
                else:
                    text.remove(text[i])
        return text

    def file_load_window(self):
        self.win = Window((800, 600), [], [])
        self.create_existing_maps(False)
        text = Special.create_text("Select a map:")
        self.win.update_text([[text, self.win.centered, 0]])
        return 2

    @staticmethod
    def go_to_main_menu(_):
        Special.main_menu()


special_dict = {
        "clear": Special.clear,
        "save": Special.save,
        "start": Special.start_end,
        "end": Special.start_end,
        "load file": Special.file_load_window,
        "main menu": Special.go_to_main_menu,
    }
