from superclass import *
FPS = 240


class Obstacle(SuperClass):
    buttons = []
    folder = "Images\\map maker\\normal blocks\\"

    @classmethod
    def from_str(cls, name: list):
        img_path = cls.folder + name[0] + ".png"
        img = pygame.image.load(img_path)
        return cls(img, img_path, int(name[1])*50, int(name[2])*50)

    def action(self):
        pass


class Start(Obstacle):
    folder = "Images\\map maker\\special actions\\"


class UseOneTime(Obstacle):
    folder = "Images\\map maker\\normal blocks\\"
    count_per_num = 30

    def __init__(self, image: pygame.Surface, img_path, x, y):
        self.count = UseOneTime.count_per_num * int(img_path.split()[-1].split(".")[0])
        # by bone image num get the count, depending on how broken the bone is, it changes
        super().__init__(image, img_path, x, y)

    def action(self):
        self.count -= 1
        self.image_path = f"bone {int(self.count/self.count_per_num)+1}.png"
        self.image = pygame.image.load(self.folder + self.image_path)
        if self.count <= 0:
            return True


class End(Obstacle):
    folder = "Images\\map maker\\special actions\\"
