from game import *


def menu():
    Button.buttons.clear()
    Special.buttons = []
    Field.buttons = []
    Arrows.buttons = []

    scrollable = create_menu("Images/Main menu")
    all_buttons = Button.buttons + Special.buttons + Arrows.buttons
    menu_loop(scrollable, all_buttons)


# all the main functions for the different parts of the program
commands = {
    "Map Maker": lambda: map_maker(commands),
    "play": lambda: game_menu(commands),
    "main menu": menu,
}


def create_menu(directory):
    scroll = False
    fp_list = os.listdir(directory)
    x = BUTTON_DIST
    y = x
    Button.font = pygame.font.Font(font_name, 100)
    for fp in fp_list:
        text = fp.split(".")[0]  # remove .png
        image = pygame.image.load(directory + "/" + fp)
        image_y = HEIGHT - 2 * BUTTON_DIST
        image = pygame.transform.scale(image, [image.get_width()*image_y/image.get_height(), image_y])
        button = Button(image, fp, x, y, text=text)
        button.command = commands[text]
        Button.buttons.append(button)
        x += image.get_width()
        if x > WIDTH:
            x = BUTTON_DIST
            y += image.get_height() + BUTTON_DIST
            scroll = True
    Button.font = pygame.font.Font(font_name, 20)
    return scroll


if __name__ == '__main__':
    menu()
