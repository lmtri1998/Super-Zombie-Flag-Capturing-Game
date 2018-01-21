import pygame
from typing import List
import random

NORMAL_TILE = pygame.image.load("04muroverde.jpg")
SPECIAL_TILE = pygame.image.load("04multia.jpg")
SAFE_GRID_TILE = pygame.image.load("trak2_plate2a.png")

class Grid(pygame.sprite.Sprite):
    def __init__(self, position, color, size=(36, 36), is_safe_grid=False):
        pygame.sprite.Sprite.__init__(self)
        # self.image = pygame.Surface(size)
        # self.image.fill(color)
        if is_safe_grid is True:
            self.image = SAFE_GRID_TILE
        else:
            rand_num = random.randint(0, 10)
            if rand_num == 0 or rand_num == 1 or rand_num == 2:
                self.image = SPECIAL_TILE
            else:
                self.image = NORMAL_TILE
        self.image = pygame.transform.scale(self.image, (36, 36))
        self.rect = self.image.get_rect()
        self.rect.center = position


    def set_type(self):
        pass

    def get_center(self):
        return self.rect.center


class Boundary(pygame.sprite.Sprite):
    def __init__(self, position, color, size):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface(size)
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.center = position


class Obsticle(Grid):

    def __init__(self, position):
        Grid.__init__(self, position,color=(255, 255, 255))
        self.image = pygame.image.load("trak2_wall3d.png")
        self.image = pygame.transform.scale(self.image, (36, 36))


class Wall:

    width: int
    height: int
    sprites: List[Obsticle]

    def __init__(self, shape):
        self.obsticles = shape
        self.width = 0
        self.height = 0
        for item in shape:
            self.width = max(self.width, item[0])
            self.height = max(self.height, item[1])

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    def get_obsticle(self, init_position, size: int):
        sprite = []
        x = init_position[0]
        y = init_position[1]

        for item in self.obsticles:
            v_x, v_y = item[0], item[1]
            sprite.append(Obsticle((x + v_x*size, y + v_y*size)))

        return sprite


