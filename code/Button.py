import pygame
from pygame.locals import *
import time
font_name = None
white = (255, 255, 255)

pygame.init()

# set size
info = pygame.display.Info()
WIDTH = info.current_w
HEIGHT = info.current_h
MENU_BAR = WIDTH / 4
SWIPE_BUTTONS = WIDTH / 30
screen = pygame.display.set_mode((WIDTH, HEIGHT))
del info


def timer(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        rv = func(*args, **kwargs)
        print(func, ": ", 1 / (time.time() - start))
        return rv
    return wrapper


class Button:
    buttons = []
    font = pygame.font.Font(font_name, 20)
    centered = "centered"
    fp = "Images\\map maker\\normal blocks"

    def __init__(self, image: pygame.surface, img_path, x, y, command=None, text=None, num=None, action=None):
        self.action = action
        self.image = image  # blitted img
        self.image_path = img_path  # img file path
        self.width = image.get_width()  # width and height of img
        self.height = image.get_height()
        self.x = x  # pos on the surface
        self.y = y
        self.show = True  # activate / deactivate button
        self.command = command  # command when button is clicked
        self.selected = False  # For drawing on field only 1 selected
        self.text = None  # text surface for special w/ text
        self.add_x = 0  # bc of text changed x and y
        self.add_y = 0
        self.num = num  # for special w/ num (start and end) type int
        self.text_str = text  # text str for special
        if text:
            if self.num:
                self.text_str = text + " " + str(num)
                self.set_text(self.text_str, False)
            else:
                self.set_text(text, False)

    def set_text(self, text, existing: bool):
        self.text = Button.font.render(text, True, (0, 0, 0))
        if not existing:
            self.height += self.text.get_height()
            self.add_y = self.text.get_height()
            self.add_x = -(self.text.get_width() - self.width) / 2
        if self.text.get_width() > self.width:
            self.add_x = -(self.text.get_width() - self.width) / 2
            self.width = self.text.get_width()

    def deiconify(self):
        self.show = False

    def draw(self, screen: pygame.Surface, mouse_x, mouse_y, clicked, add_x=0, biggest=0, add_y=0):
        mouse_y = screen.get_height() - mouse_y
        if self.show:
            if self.selected:
                self.draw_only(screen, self.image, (mouse_x - self.width / 2, mouse_y - self.height / 2 + add_y))
            elif self.text:
                self.draw_only(screen, self.text, (self.x + self.add_x, self.y + add_y))
                self.draw_only(screen, self.image, (self.x, self.y + self.add_y + add_y))
            else:
                try:
                    if add_x <= self.repr_x <= biggest:
                        self.draw_only(screen, self.image, (self.x - add_x * 50, self.y + add_y))
                except AttributeError:
                    self.draw_only(screen, self.image, (self.x, self.y + add_y))
            if clicked:
                if self.command:
                    try:
                        if add_x <= self.repr_x <= biggest:
                            if self.x - add_x * 50 < mouse_x < self.x - add_x * 50 + self.width and \
                                    self.y + add_y < mouse_y < self.y + add_y + self.height:
                                return self.command()
                    except AttributeError:
                        if self.x < mouse_x < self.x + self.width and self.y + add_y < mouse_y < self.y + add_y + self.height:
                            return self.command()
                        elif self.selected:
                            return self.command()

    @staticmethod
    def draw_only(screen, image, pos):
        screen.blit(image, (pos[0], screen.get_height() - pos[1] - image.get_height()))

    def update_command(self, command):
        self.command = command

    def select_obstacle(self):
        self.selected = True
        return 1

    @classmethod
    def show_unusual(cls, mode: bool):
        for button in cls.buttons:
            if button.command != button.select_obstacle:
                button.show = mode

    @staticmethod
    def unselect_obstacle(buttons: list):
        for button in buttons:
            button.selected = False

    @classmethod
    def get_instance(cls, img_path):
        for instance in cls.buttons:
            if instance.image_path:
                if instance.image_path.split()[0] == img_path.split()[0]:
                    return instance

    @staticmethod
    def create_text(text, x, y):
        Button.buttons.append(Button(*Button.create_text_only(text, x, y)))

    @staticmethod
    def create_text_only(text, x, y):
        text_img = Button.font.render(text, True, white)
        if x == Button.centered:
            x = WIDTH / 2 - text_img.get_width() / 2
        if y == Button.centered:
            y = HEIGHT / 2 - text_img.get_height() / 2
        return text_img, False, x, y

    @staticmethod
    def set_description(text):
        img = Button.font.render(text, True, white)
        return Button(img, False, WIDTH/2-img.get_width()/2, HEIGHT-img.get_height())

    def run_action(self, field):
        if self.action:
            return self.action(field)

    @classmethod
    def set_shown(cls, mode: bool):
        for button in cls.buttons:
            button.show = mode

    def __repr__(self):
        return self.image_path
