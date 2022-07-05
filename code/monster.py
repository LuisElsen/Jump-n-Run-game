from Obstacle import *
from Button import HEIGHT


# base class of monster, behaves like an obstacle, but runs constantly the action, which does as default nothing
class Monster(Obstacle):
    folder = "Images\\map maker\\Enemies\\"


class StraightCannon(Monster):
    interval = 2  # in seconds
    count = interval * FPS
    balls = []
    up = 0
    left = 1
    down = 2
    right = 3

    def __init__(self, image: pygame.Surface, img_path, x, y):
        super().__init__(image, img_path, x, y)
        self.__rotation = CannonBall.right

    def set_rotation(self, direction: int):
        if self.__rotation == StraightCannon.left:
            self.image = pygame.transform.flip(self.image, False, True)
        if direction - self.__rotation > 0:
            self.image = pygame.transform.rotate(self.image, 90*(direction - self.__rotation))
            self.__rotation = direction
        else:
            direction += 4
            self.image = pygame.transform.rotate(self.image, 90 * (direction - self.__rotation))
            direction -= 4
            self.__rotation = direction
        if direction == StraightCannon.left:
            self.image = pygame.transform.flip(self.image, False, True)

    @classmethod
    def from_str(cls, name: list):
        help_list = [name[0], name[1], name[2].split("-")[0]]
        instance = super().from_str(help_list)
        instance.set_rotation(int(name[2].split("-")[1]))
        return instance

    @classmethod
    def reset_count(cls):
        cls.count = cls.interval * FPS

    @staticmethod
    def draw_balls(screen, player, add):
        rv = False
        for ball in StraightCannon.balls:
            if ball.draw(screen, player, add):
                rv = True
        return rv

    def action(self):
        self.count -= 1
        if self.count <= 0:
            self.count = StraightCannon.count
            self.shoot_ball()

    def shoot_ball(self):
        if self.__rotation == self.right:
            StraightCannon.balls.append(CannonBall(self.x + self.width - 10, HEIGHT - (self.y + self.width / 2 + 5),
                                                   self.__rotation))
        if self.__rotation == self.left:
            StraightCannon.balls.append(CannonBall(self.x + 10, HEIGHT - (self.y + self.width / 2 + 5),
                                                   self.__rotation))
        if self.__rotation == self.up:
            StraightCannon.balls.append(CannonBall(self.x + 20, HEIGHT - (self.y + self.width / 2 + 15),
                                                   self.__rotation))
        if self.__rotation == self.down:
            StraightCannon.balls.append(CannonBall(self.x + 30, HEIGHT - (self.y + self.width / 2 - 15),
                                                   self.__rotation))


class CannonBall:
    speed = 2.5  # speed in px per iteration
    up = 0
    left = 1
    down = 2
    right = 3
    radius = 9

    def __init__(self, x, y, direction):
        self.direction = direction
        self.x = x
        self.y = y
        self.has_hit = False

    def draw(self, screen, player, add):
        self.move()
        self.draw_only(screen, add)
        return self.collision(player)

    def move(self):
        if self.direction == CannonBall.up:
            self.y -= CannonBall.speed
        elif self.direction == CannonBall.down:
            self.y += CannonBall.speed
        elif self.direction == CannonBall.left:
            self.x -= CannonBall.speed
        else:
            self.x += CannonBall.speed

    def draw_only(self, screen, add):
        pygame.draw.circle(screen, (0, 0, 0), (self.x - add, self.y), CannonBall.radius)

    def collision(self, player):
        if not self.has_hit:
            if pygame.Rect.colliderect(
                    pygame.Rect([self.x - self.radius, self.y - self.radius, 2 * self.radius, 2 * self.radius]),
                    pygame.Rect([player.x, HEIGHT-player.y, player.width, -player.height])):
                self.has_hit = True
                return True
