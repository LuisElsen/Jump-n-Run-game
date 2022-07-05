from Button import *


class Field(Button):
    path = "Images/field.png"
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
                if type(Field.selected_button.num) == int:  # set start end buttons cmd
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
                return True

    def reset(self):
        if type(self.img_num) == int:
            self.cls.num += 1  # for start and end button
            self.image = Field.image
            self.image_path = Field.path
        else:
            self.image = Field.image
            self.image_path = Field.path

    @staticmethod
    def update_selected(new):
        Field.selected_button = new

    @staticmethod
    def get_on_map(img_name) -> int:
        count = 0
        for field in Field.buttons:
            if field.image_path == img_name:
                count += 1
        return count

    @staticmethod
    def set_fields(new, special_dict, special_cls, enemy_cls):
        for n in new:
            field = Field.get_instance((int(n[1]), int(n[2].split("-")[0])))
            while not field:
                Field.add_line()
                field = Field.get_instance((int(n[1]), int(n[2].split("-")[0])))
            if field:
                if n[0].split()[0] in special_dict:
                    new_button = special_cls.get_instance(n[0])
                    Field.update_selected(new_button)
                    field.command()
                elif len(n[2].split("-")) == 2:  # cannon
                    new_button = enemy_cls.get_instance(n[0])
                    Field.update_selected(new_button)
                    field.create_cannon(field)
                    field = Cannon.get_instance((field.repr_x, field.repr_y))
                    field.change_direction(int(n[2].split("-")[1]))
                else:
                    new_button = Button.get_instance(n[0])
                    Field.update_selected(new_button)
                    field.command()

    @classmethod  # dann field.selected neuer button und self.command beim richtigen field
    def get_instance(cls, pos):
        for instance in cls.buttons:
            if instance.repr_x == pos[0] and instance.repr_y == pos[1]:
                return instance

    @staticmethod
    def create_cannon(self):
        self = Cannon(self.repr_x, self.repr_y)
        self.command()
        Field.buttons[Field.buttons.index(Field.get_instance((self.repr_x, self.repr_y)))] = self
        # replace filed where cannon is w/ the instance of cannon cls
        description = Button.set_description(
            "use the arrow keys on your keyboard to change the direction where the cannon shoots")
        return description, self.cannon_method

    def __repr__(self):
        return f"{self.image_path}${self.repr_x}${self.repr_y}"


class Cannon(Field):
    up = 0
    left = 1
    down = 2
    right = 3

    def __init__(self, x: int, y: int):
        super().__init__(x, y)
        self.rotation = Cannon.right

    def change_direction(self, direction: int):
        if self.rotation == Cannon.left:
            self.image = pygame.transform.flip(self.image, False, True)
        if direction - self.rotation > 0:
            self.image = pygame.transform.rotate(self.image, 90*(direction - self.rotation))
            self.rotation = direction
        else:
            direction += 4
            self.image = pygame.transform.rotate(self.image, 90 * (direction - self.rotation))
            direction -= 4
            self.rotation = direction
        if direction == Cannon.left:
            self.image = pygame.transform.flip(self.image, False, True)

    def cannon_method(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.change_direction(Cannon.up)
                elif event.key == pygame.K_LEFT:
                    self.change_direction(Cannon.left)
                elif event.key == pygame.K_RIGHT:
                    self.change_direction(Cannon.right)
                elif event.key == pygame.K_DOWN:
                    self.change_direction(Cannon.down)

    def __repr__(self):
        return f"{self.image_path}${self.repr_x}${self.repr_y}-{self.rotation}"


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
