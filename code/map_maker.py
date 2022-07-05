import sys

import pygame.font

from special_button import *
import os
from selected_methods import *

dir_path = "Images/map maker"
get_class = {
    "clear": Clear,
    "save": Save,
    "start": StartEnd,
    "end": StartEnd,
    "load": LoadFile,
    "main": MainMenu,
    "delete": Delete,
    "lives": Lives,
}


def create_left_right_buttons():
    directory = "Images/other"
    left_img = pygame.image.load(directory + "/" + "left.png")
    right_img = pygame.image.load(directory + "/" + "right.png")
    left = Arrows(left_img, MENU_BAR + 5)
    left.command = left.move_map_left
    Arrows.buttons.append(left)
    right = Arrows(right_img, WIDTH - right_img.get_width())
    right.command = right.move_map_right
    Arrows.buttons.append(right)


def show_directory(cls, others):
    cls.set_shown(True)
    [other.set_shown(False) for other in others]
    Button.show_unusual(True)


def create_buttons(fp_directory, cls, reverse: bool, in_menu=None, add_x=0):
    fp_list = os.listdir(fp_directory)
    x = BUTTON_DIST + add_x
    if reverse:
        y = HEIGHT - BUTTON_DIST
    else:
        y = BUTTON_DIST
    for fp in fp_list:
        text = None
        if cls == Special:
            text = fp.split(".")[0]  # remove .png

        img_fp = fp.split(".")[0]  # remove .png
        if img_fp in selected_methods:
            action = selected_methods[img_fp]
        else:
            action = False
        if in_menu:
            image = in_menu[1].render(text, True, white)
        else:
            image = pygame.image.load(fp_directory + "/" + fp)
        if cls == Special:
            cls = get_class[text.split()[0]]  # sum ting wong
            try:
                num = int(text.split()[1])
                text = text.split()[0]
                button = cls(image, img_fp, x, y, text=text, num=num, action=action)
            except IndexError:
                button = cls(image, img_fp, x, y, text=text, action=action)
            except ValueError:
                button = cls(image, img_fp, x, y, text=text, action=action)
            finally:
                cls = Special
        else:
            button = cls(image, img_fp, x, y, text=text, action=action)

        x += button.width + BUTTON_DIST

        if x + image.get_width() > MENU_BAR:
            if reverse:
                y -= BUTTON_DIST + button.height
            else:
                y += BUTTON_DIST + button.height

            x = BUTTON_DIST
        button.show = False
        cls.buttons.append(button)
        if cls == Special:
            if in_menu:
                button.update_command(lambda: in_menu[0](text))
                button.num = int(text.split()[1])
            else:
                button.update_command(
                    lambda t=text, b=button, *args, **kwargs: special_dict[t](b, *args, **kwargs))
        else:
            button.update_command(button.select_obstacle)


def create_directories(path):
    x = BUTTON_DIST
    y = HEIGHT - BUTTON_DIST
    Button.font = pygame.font.Font(font_name, 30)
    for text in os.listdir(path):
        if Special.fp.split("\\")[-1] == text:
            cls = Special
            others = Enemy, Button
        elif Enemy.fp.split("\\")[-1] == text:
            cls = Enemy
            others = Special, Button
        else:
            cls = Button
            others = Enemy, Special

        def command(cls=cls, others=others):
            cls.set_shown(True)
            [other.set_shown(False) for other in others]
            button.show_unusual(True)

        button = Button(*Button.create_text_only(text, x, y),
                        command=lambda cls=cls, others=others: command(cls, others))
        Button.buttons.append(button)

        x += button.width + BUTTON_DIST
        if x + button.width > MENU_BAR:
            y -= BUTTON_DIST + button.height
            x = BUTTON_DIST
    Button.font = pygame.font.Font(font_name, 20)


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
    # reset the board
    MainMenu.main_menu = commands["main menu"]
    Arrows.buttons.clear()
    Special.buttons.clear()
    Button.buttons.clear()
    Field.buttons.clear()

    # sidebar buttons
    create_directories(dir_path)
    create_buttons(Button.fp, Button, False)
    create_buttons(Special.fp, Special, False)
    create_buttons(Enemy.fp, Enemy, False)
    show_directory(Special, (Enemy, Button))
    # arrow buttons
    create_left_right_buttons()
    save_loop = False  # for the window of the save loop
    # create mat to draw
    Field.create_fields()
    description = None
    selected_method = None
    while True:
        all_buttons = Button.buttons + Special.buttons + Arrows.buttons + Enemy.buttons
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
                if type(button) == StartEnd:
                    button.update_text()
        if not save_loop:
            if selected:
                Field.update_selected(selected[0])
            for field in Field.buttons:
                if field.draw(screen, mx, my, pressed, Arrows.smallest, Field.buttons[-1].repr_x - Arrows.biggest):
                    rv = Field.selected_button.run_action(field)
                    if rv:
                        description, selected_method = rv
                    else:
                        description, selected_method = None, None

        if save_loop:
            if selected:
                if type(selected[0]) == Save:
                    stop, Save.map_name = selected[0].save_in_loop(screen, mx, my, clicked, events, selected[0].map_saver,
                                                                   var=Save.map_name)
                    if stop:
                        save_loop = False
                        selected[0].selected = False
                elif type(selected[0]) == Lives:
                    stop, Lives.lives = selected[0].save_in_loop(screen, mx, my, clicked, events,
                                                                 selected[0].set_lives, var=str(Lives.lives))
                    if stop:
                        save_loop = False
                        selected[0].selected = False
                else:
                    stop, _ = selected[0].save_in_loop(screen, mx, my, clicked, events)
                    if stop:
                        save_loop = False
                        selected[0].selected = False
        if description:
            description.draw(screen, mx, my, clicked)

        if selected_method:
            rv = selected_method(events)
            if rv:
                description = rv

        pygame.display.update()
