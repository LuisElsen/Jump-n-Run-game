from Button import *


class Field(Button):
    path = "Images/field.png"
    if config:
        path = config + "/" + path
    image = pygame.image.load(path)
    size = image.get_width()
    selected_button = None
    change = True
    buttons = []

    def __init__(self, x: int, y: int):
        self.repr_x = x
        self.repr_y = y
        self.img_num = None
        self.cls = None
        super().__init__(self.image, self.path, x * self.size + MENU_BAR + SWIPE_BUTTONS, y * self.size, self.command)

    @staticmethod
    def add_line():
        x = Field.buttons[-1].repr_x
        y = Field.buttons[-1].repr_y
        for i in range(y + 1):
            Field.buttons.append(Field(x + 1, i))

    @staticmethod
    def create_fields():
        y_fields = int(HEIGHT / Field.size)
        x_fields = int((WIDTH - MENU_BAR - 2 * SWIPE_BUTTONS) / Field.size)
        Field.buttons = [Field(x, y) for x in range(x_fields) for y in range(y_fields)]

    def command(self):
        if Field.change:
            if Field.selected_button:
                if type(Field.selected_button.num) == int:
                    if Field.selected_button.num != 0:
                        Field.selected_button.num -= 1
                        self.image = Field.selected_button.image
                        self.image_path = Field.selected_button.image_path
                        self.img_num = Field.selected_button.num
                        self.cls = Field.selected_button
                else:
                    if type(self.img_num) == int:
                        self.cls.num += 1  # for start and end button
                        self.image = Field.selected_button.image
                        self.image_path = Field.selected_button.image_path
                    else:
                        self.image = Field.selected_button.image
                        self.image_path = Field.selected_button.image_path

    @staticmethod
    def update_selected(new):
        Field.selected_button = new

    @staticmethod
    def get_on_map(img_name) -> int:
        count = 0
        for field in Field.buttons:
            print(field.image_path)
            if field.image_path == img_name:
                count += 1
        return count

    @staticmethod
    def set_fields(new, special_dict, special_cls):
        for n in new:
            field = Field.get_instance((n[1], n[2]))
            if field:
                if n[0].split()[0] in special_dict:
                    new_button = special_cls.get_instance(n[0])
                    Field.update_selected(new_button)
                    field.command()
                else:
                    new_button = Button.get_instance(n[0])
                    Field.update_selected(new_button)
                    field.command()

    @classmethod  # dann field.selected neuer button und self.command beim richtigen field
    def get_instance(cls, pos):
        for instance in cls.buttons:
            if instance.repr_x == pos[0] and instance.repr_y == pos[1]:
                return instance

    def __repr__(self):
        return f"{self.image_path}${self.repr_x}${self.repr_y}"


class Arrows(Button):
    smallest = 0
    biggest = 0
    buttons = []

    def __init__(self, image, x, command=None):
        super().__init__(image, False, x, HEIGHT / 2 - image.get_height() / 2, command)

    def move_map_left(self):
        if self.smallest > 0:
            Arrows.smallest -= 1
            Arrows.biggest += 1

    def move_map_right(self):
        if self.biggest == 0:
            Field.add_line()
            Arrows.smallest += 1
        else:
            Arrows.smallest += 1
            Arrows.biggest -= 1
