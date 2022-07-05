"""import pygame
import time
img = pygame.image.load("Images/player.png")
screen = pygame.display.set_mode()
while True:
    screen.fill((0, 0, 0))
    screen.blit(img, (screen.get_width()/2, screen.get_height()/2))
    pygame.display.update()
    img = pygame.transform.rotate(img, 90)
    time.sleep(1)"""
import json
with open("Maps\\jsonfile.json", "r") as f:
    print(json.load(f))