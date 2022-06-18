import pygame
pygame.init()
# from Enum import Enum, auto


class SuperClass:
    top = "top"
    left = "left"
    right = "right"
    bottom = "bottom"

    def __init__(self, image: pygame.Surface, img_path, x, y):
        self.height = image.get_height()
        self.x = x
        self.y = y
        self.image = image
        self.width = image.get_width()
        self.last_pos = (x, y)
        self.image_path = img_path
        self.rect = pygame.Rect([self.x, self.y, self.width, self.height])

    def draw(self, screen, added_value=0):
        screen.blit(self.image, (self.x + added_value, screen.get_height() - self.y - self.image.get_height()))

    