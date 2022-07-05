from monster import *


class Player(SuperClass):
    JUMP_POWER = 3.2
    SPEED = 1.7
    GRAVITY = -0.045
    on_ground = False
    heart_img = pygame.image.load("Images/heart.png")
    hit_points = 3

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
    def draw_player(self, screen: pygame.Surface, obstacles: list, movement, add):
        self.set_last()
        self.add_gravity()
        on_ground, rv = self.complete_collision(obstacles, movement)
        if StraightCannon.draw_balls(screen, self, self.x - add):
            Player.hit_points -= 1
        self.draw_hearts(screen)
        self.draw(screen, self.x - add)
        if Player.hit_points <= 0:
            return on_ground, 2
        return on_ground, rv

    def complete_collision(self, obstacles, movement):
        for obstacle in obstacles:
            if issubclass(type(obstacle), Monster):
                if obstacle.action():
                    obstacles.remove(obstacle)
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
            if not issubclass(type(obstacle), Monster):
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

    def draw_hearts(self, screen):
        add_x = 0
        space = 5
        for _ in range(self.hit_points):
            screen.blit(Player.heart_img, (0 + add_x, 0))
            add_x += space+Player.heart_img.get_width()

    def __repr__(self):
        return f"x = {self.x}, y = {self.y}"
