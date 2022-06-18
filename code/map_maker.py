import sys

from field import Arrows
from special_button import *
import os


buttons_fp = "Images/map images"
special_fp = "Images/special buttons"
if config:
    buttons_fp = config + "/Images/map images"
    special_fp = config + "/Images/special buttons"


def create_left_right_buttons():
    directory = "Images/other"
    if config:
        directory = config + "/Images/other"
    left_img = pygame.image.load(directory + "/" + "left.png")
    right_img = pygame.image.load(directory + "/" + "right.png")
    left = Arrows(left_img, MENU_BAR+5)
    left.command = left.move_map_left
    Arrows.buttons.append(left)
    right = Arrows(right_img, WIDTH-right_img.get_width())
    right.command = right.move_map_right
    Arrows.buttons.append(right)


def create_buttons(fp_directory, special: bool, reverse: bool, in_menu=None, add_x=0):
    fp_list = os.listdir(fp_directory)
    x = BUTTON_DIST + add_x
    if reverse:
        y = HEIGHT - BUTTON_DIST
    else:
        y = BUTTON_DIST
    for fp in fp_list:
        text = None
        if special:
            text = fp.split(".")[0]  # remove .png

        img_fp = fp.split(".")[0]  # remove .png
        if in_menu:
            image = in_menu[1].render(text, True, white)
        else:
            image = pygame.image.load(fp_directory + "/" + fp)
        if special:
            try:
                num = int(text.split()[1])
                text = text.split()[0]
                button = Special(image, img_fp, x, y, text=text, num=num)
            except IndexError:
                button = Special(image, img_fp, x, y, text=text)
            except ValueError:
                button = Special(image, img_fp, x, y, text=text)
        else:
            button = Button(image, img_fp, x, y, text=text)

        x += button.width + BUTTON_DIST

        if x + image.get_width() > MENU_BAR:
            if reverse:
                y -= BUTTON_DIST + button.height
            else:
                y += BUTTON_DIST + button.height

            x = BUTTON_DIST
        if special:
            Special.buttons.append(button)
        else:
            Button.buttons.append(button)
        if special:
            if in_menu:
                button.update_command(lambda: in_menu[0](text))
                button.num = int(text.split()[1])
            else:
                button.update_command(
                    lambda t=text, b=button, *args, **kwargs: special_dict[t](b, *args, **kwargs))
        else:
            button.update_command(button.select_obstacle)


def menu_loop(scrollable, all_buttons):
    clicked = False
    add_y = 0
    while True:
        screen.fill((0, 100, 0))

        # events
        mx, my = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    clicked = True
            if scrollable:
                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 4:
                        add_y += 50
                    elif event.button == 5:
                        add_y -= 50

        for button in all_buttons:
            if button.draw(screen, mx, my, clicked, add_y=add_y):
                return

        pygame.display.update()


def map_maker(commands):
    Special.main_menu = commands["main menu"]
    Button.buttons = []
    Special.buttons = []
    Field.buttons = []
    Arrows.buttons = []

    # sidebar buttons
    create_buttons(buttons_fp, False, True)
    create_buttons(special_fp, True, False)
    # arrow buttons
    create_left_right_buttons()
    all_buttons = Button.buttons + Special.buttons + Arrows.buttons
    save_loop = False
    # create mat to draw
    Field.create_fields()

    while True:
        events = pygame.event.get()
        selected = [button for button in all_buttons if button.selected]
        if not save_loop:
            screen.fill((66, 116, 224))
        pygame.draw.line(screen, (255, 255, 255), (MENU_BAR, 0), (MENU_BAR, HEIGHT), 5)
        # events
        mx, my = pygame.mouse.get_pos()
        clicked = False
        pressed, _, _ = pygame.mouse.get_pressed(3)

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    clicked = True
            if event.type == pygame.QUIT:
                sys.exit()

        if not save_loop:
            for button in all_buttons:
                rv = button.draw(screen, mx, my, clicked)
                if rv:
                    Button.unselect_obstacle(all_buttons)
                    button.selected = True
                    save_loop = False
                if rv == 2:
                    selected = [button for button in all_buttons if button.selected]
                    button.command()
                    save_loop = True
                    Field.update_selected(None)
        if not save_loop:
            if selected:
                Field.update_selected(selected[0])
            for field in Field.buttons:
                field.draw(screen, mx, my, pressed, Arrows.smallest, Field.buttons[-1].repr_x - Arrows.biggest)

        if save_loop:
            if selected:
                if selected[0].save_in_loop(screen, mx, my, clicked, events):
                    save_loop = False
                    selected[0].selected = False

        pygame.display.update()


