import pdb
from Obstacle import *
import pygame.font
import sys

from map_maker import *
import player as play
FPS = 240
TIME_PER_ITERATION = 1/FPS


def load_map(name):
    def configuration(n):
        if config:
            return config + "/Maps/" + n
        else:
            return "Maps/" + n

    name = configuration(name)

    text = Special.load_only(name)
    for t in text:
        if t[0] == "start 1":
            Obstacle.buttons.append(Start.from_str(t))
        elif t[0] == "end 1":
            Obstacle.buttons.append(End.from_str(t))
        elif t[0].startswith("bone"):
            Obstacle.buttons.append(UseOneTime.from_str(t))
        else:
            Obstacle.buttons.append(Obstacle.from_str(t))


def game_menu(main_menu=None):
    if main_menu:
        Special.main_menu = main_menu["main menu"]
    Obstacle.buttons.clear()
    UseOneTime.buttons.clear()
    Start.buttons.clear()
    End.buttons.clear()
    Button.buttons = []
    scroll = False
    Button.font = pygame.font.Font(font_name, 150)
    if config:
        paths = os.listdir(config + "/" + Special.map_folder)
    else:
        paths = os.listdir(Special.map_folder)
    x = BUTTON_DIST
    y = x
    Button.create_text("choose a Map", Button.centered, HEIGHT - Button.font.get_height())
    Button.buttons.append(
        Button(*Button.create_text_only("Main Menu", Button.centered, HEIGHT - 2 * Button.font.get_height()),
               command=lambda: (Button.buttons.clear(), Special.go_to_main_menu(None))))

    for path in paths:
        text = path.split(".")[0]
        image = Button.font.render(text, True, white)
        Button.buttons.append(Button(image, path, x, y, command=lambda fp=path: game(fp, main_menu)))
        x += image.get_width() + BUTTON_DIST
        if x + image.get_width() + BUTTON_DIST > WIDTH:
            x = BUTTON_DIST
            y += image.get_height() + BUTTON_DIST
            if y > HEIGHT - 2 * Button.font.get_height():
                scroll = True
    Button.font = pygame.font.Font(font_name, 20)
    menu_loop(scroll, Button.buttons)


def get_player_spawn():
    for obstacle in Obstacle.buttons:
        if obstacle.image_path.split("\\")[-1] == "start 1.png":
            return obstacle.x, obstacle.y + obstacle.height + 5
    raise BaseException("no start on the map")


def game(map_name, commands):
    load_map(map_name)

    # player
    if config:
        img_path = config + "/" + "Images/player.png"
    else:
        img_path = "Images/player.png"
    player_img = pygame.image.load(img_path)
    cords = get_player_spawn()
    player = play.Player(player_img, img_path, *cords)
    can_jump = False
    while True:
        start = time.time()
        screen.fill((66, 116, 224))
        if pygame.key.get_pressed()[pygame.K_UP]:
            if can_jump:
                player.jump()
        # events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        # movement
        movement = pygame.key.get_pressed()[pygame.K_LEFT], pygame.key.get_pressed()[pygame.K_RIGHT]

        can_jump, rv = player.draw_player(screen, Obstacle.buttons, movement)
        if rv:
            break
        for obstacle in Obstacle.buttons:
            obstacle.draw(screen)

        required_time = time.time()-start
        if required_time < TIME_PER_ITERATION:
            time.sleep(TIME_PER_ITERATION-required_time)

        pygame.display.update()
    if rv == 1:
        after_game()
    else:
        Obstacle.buttons.clear()
        UseOneTime.buttons.clear()
        Start.buttons.clear()
        End.buttons.clear()
        Button.buttons = []
        game(map_name, commands)


def after_game():
    Button.buttons = []
    Button.font = pygame.font.Font(font_name, 100)
    Button.create_text("You Won", Button.centered, HEIGHT / 4 * 3)
    Button.buttons.append(
        Button(*Button.create_text_only("Go Back", Button.centered, HEIGHT / 4), command=game_menu))
    Button.font = pygame.font.Font(font_name, 20)
    menu_loop(False, Button.buttons)
