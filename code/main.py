from game import *
import tkinter


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
        image = pygame.transform.scale(image, [image.get_width() * image_y / image.get_height(), image_y])
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
    if os.path.exists("../name.txt"):
        menu()
    else:
        win = tkinter.Tk()
        tkinter.Label(win, text="tell us your name").grid(row=0, column=0)
        box = tkinter.Entry(win)
        box.grid(row=1, column=0)
        tkinter.Button(win, text="Submit", command=lambda: (
            open("../name.txt", "w").write(box.get()), tkinter.Label(text="you can close this window now")
            .grid(row=3, column=0))).grid(row=2, column=0)

        win.mainloop()
