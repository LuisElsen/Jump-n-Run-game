from superclass import *
from Obstacle import End
from Button import timer


class Player(SuperClass):
    JUMP_POWER = 3.2
    SPEED = 1.7
    GRAVITY = -0.045
    on_ground = False

    def __init__(self, image: pygame.Surface, img_path, x, y):
        super().__init__(image, img_path, x, y)
        self.power = 0
        self.jumping = False
        self.last_x = x
        self.last_y = y

    def jump(self):
        if not self.jumping:
            self.jumping = True
            self.power = Player.JUMP_POWER

    def move(self, direction):
        self.x += self.SPEED * direction

    # main player function including obstacle collision
    def draw_player(self, screen: pygame.Surface, obstacles: list, movement):
        self.set_last()
        self.add_gravity()
        for obstacle in obstacles:
            if type(obstacle) == End:
                if self.top_collision(obstacle):
                    return False, True
            coll = self.top_bottom_collision(obstacle)
            if coll:
                if self.handle_top_bottom(coll, obstacle):
                    obstacles.remove(obstacle)
        on_ground = Player.on_ground
        Player.on_ground = False
        if any(movement):
            left, right = movement
            if left:
                self.move(-1)
            if right:
                self.move(1)

        for obstacle in obstacles:
            if type(obstacle) == End:
                if self.top_collision(obstacle):
                    return on_ground, 1
                elif self.y <= 0:
                    return on_ground, 2
            coll = self.left_right_collision(obstacle)
            if coll:
                self.handle_left_right(coll)
        self.draw(screen)
        return on_ground, False

    def add_gravity(self):
        self.power += Player.GRAVITY
        self.y += self.power

    def top_bottom_collision(self, other):
        if pygame.Rect.colliderect(pygame.Rect([self.x, self.y, self.width, self.height]), other.rect):
            if self.last_y + self.height < other.y:
                return self.bottom

            if self.last_y >= other.y + other.height + self.GRAVITY:
                return self.top

        return False

    def left_right_collision(self, other):
        if pygame.Rect.colliderect(pygame.Rect([self.x, self.y, self.width, self.height]), other.rect):
            if self.last_x >= other.x + other.width:
                return self.right

            if self.last_x < other.x:
                return self.left

        return False

    def top_collision(self, other):
        if self.top_bottom_collision(other) == self.top:
            return True

    def handle_top_bottom(self, side, obstacle):
        if side == self.top:
            self.power = 0
            self.y = self.last_y
            self.jumping = False
            Player.on_ground = True
            return obstacle.action()
        elif side == self.bottom:
            self.power = 0
            self.y = obstacle.y - self.height

    def handle_left_right(self, side):
        if side == self.right or side == self.left:
            self.x = self.last_x

    def set_last(self):
        self.last_x = self.x
        self.last_y = self.y

    def __repr__(self):
        return f"x = {self.x}, y = {self.y}"
