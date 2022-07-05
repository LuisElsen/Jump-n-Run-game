from Button import *
import pygame.surface


class Window:
    x_button = pygame.image.load("Images/delete.png")
    centered = "centered"
    stop = "stop"

    def __init__(self, size, texts: list, buttons: list):
        self.surface = pygame.surface.Surface(size)
        self.width = size[0]
        self.height = size[1]
        self.x_button = Button(self.x_button, "Images/delete.png", self.width - self.x_button.get_width(),
                               self.height - self.x_button.get_height(), command=self.delete)
        self.buttons = buttons
        self.texts = texts
        self.button_dist = self.height / 10
        # center window texts
        for text in self.texts:
            if text[1] == Window.centered:
                text[1] = int(self.get_width() / 2 - text[0].get_width() / 2)
            if text[2] == Window.centered:
                text[2] = int(self.get_width() / 2 - text[0].get_width() / 2)

    def draw(self, screen, pos, mx, my, clicked, scroll=0):
        mouse_x = mx - pos[0]
        mouse_y = my - pos[1]
        for text in self.texts:
            self.surface.blit(text[0], (text[1], text[2] - scroll))

        rv = self.x_button.draw(self.surface, mouse_x, mouse_y, clicked)

        for button in self.buttons:
            if button.draw(self.surface, mouse_x, mouse_y, clicked, add_y=scroll) == Window.stop:
                rv = True

        screen.blit(self.surface, pos)
        return rv

    def get_width(self):
        return self.surface.get_width()

    def get_height(self):
        return self.surface.get_height()

    def delete(self):
        return True

    def update_text(self, new: list):
        for text in new:
            if text[1] == Window.centered:
                text[1] = int(self.get_width() / 2 - text[0].get_width() / 2)
            if text[2] == Window.centered:
                text[2] = int(self.get_width() / 2 - text[0].get_width() / 2)
        self.texts = new

    def update_buttons(self, new: list):
        self.buttons = new
