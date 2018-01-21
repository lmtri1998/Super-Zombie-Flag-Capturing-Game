import pygame

class Boundary(pygame.sprite.Sprite):
    def __init__(self, position, color, size):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface(size)
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.center = position
        self.color = color

    def make_invisible(self):
        self.image.set_colorkey(self.color)


class StatBar(Boundary):

    max_stat: int
    curr_stat: int
    max_length: int
    max_width: int
    x: int
    y: int

    def __init__(self, position, color, size, max_stat):
        Boundary.__init__(self, position, color, size)
        self.moving_direction = 0 # 0: right to left; 1: left to right
        self.max_stat = max_stat
        self.curr_stat = max_stat
        self.max_length = size[0]
        self.max_width = size[1]
        self.x, self.y = self.rect.topleft
        self.color = color
        self.init_position = position

    def set_reversed_direction(self):
        if self.moving_direction == 0:
            self.moving_direction = 1
        else:
            self.moving_direction = 0

    def set_curr_stat(self, stat):
        if stat < 0:
            self.curr_stat = 0
        else:
            self.curr_stat = stat
        self.decrease()

    def set_max_stat(self, stat):
        self.max_stat = stat

    def decrease(self):
        length = round(self.max_length * (self.curr_stat / self.max_stat))
        self.image = pygame.Surface((length, self.max_width))
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        if self.moving_direction == 0:
            self.rect.topleft = (self.x, self.y)
        else:
            self.rect.topright = (self.x + self.max_length, self.y)

    def get_full_bar(self, color):
        return Boundary(self.init_position, color, (self.max_length, self.max_width))

