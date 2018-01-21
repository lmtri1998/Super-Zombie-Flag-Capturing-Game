import pygame
from Player import Player
from weapon import Pistol, ShotGun, MachineGun, Sword
from typing import List, Tuple
import random

BOX_IMAGE = "box.png"
HEAL = [10, 25, 40, 75]
WEAPONS = [Pistol, ShotGun, MachineGun, Sword]


class Box(pygame.sprite.Sprite):
    """Item box"""
    position: Tuple

    def __init__(self, position):

        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(BOX_IMAGE)
        self.image = pygame.transform.scale(self.image, (34, 34))
        self.rect = self.image.get_rect()
        self.rect.center = position
        self.rect.centerx = position[0]
        self.rect.centery = position[1]

    def collide(self, other):
        """Collsion detection"""
        raise NotImplementedError


class HealthBox(Box):
    """Health Box"""
    heal_amount: int

    def __init__(self, position):
        Box.__init__(self, position)
        self.heal_amount = random.choice(HEAL)

    def collide(self, other):
        """Collision detection"""
        other.health = other.health + self.heal_amount
        if other.health > 100:
            other.health = 100
        self.kill()

    def __str__(self):
        return "Heal"


class WeaponBox(Box):
    """Weapon Box"""
    weapon: 'Weapon'

    def __init__(self, position):
        Box.__init__(self, position)
        self.weapon = random.choice(WEAPONS)

    def collide(self, other):
        """Collision detection"""
        other.weapon = self.weapon(other)
        self.kill()

    def __str__(self):
        return self.weapon.__str__(self.weapon)
