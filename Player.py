import pygame
from weapon import Pistol, ShotGun, MachineGun, Sword
from typing import List

FRAME_RATE = 30
PLAYER_VELOCITY = 5
FLASH_TIME = 60
DIRECTIONS_STR = ['characterRight', 'characterDown', 'characterLeft', 'characterUp']
MAX_HP = 100

class TempBlock(pygame.sprite.Sprite):
    def __init__(self, position, size):
        self.image = pygame.Surface(size)
        self.rect = self.image.get_rect()
        self.rect.center = position

class Player(pygame.sprite.Sprite):
    """Player for the game"""
    health: int
    x: int
    y: int
    weapon: 'Weapon'
    direction: int
    spawn_position: int

    def __init__(self, position):
        pygame.sprite.Sprite.__init__(self)
        self.weapon = Sword(self)
        # self.image = pygame.image.load("player_sprite.png").subsurface(29, 29,
        #                                                                56, 70)
        # self.image = pygame.Surface((35, 35))
        # # self.image.fill((255, 255, 0))
        self.image = pygame.image.load("ShotGun/characterRight/survivor-move (1).png")
        self.image = pygame.transform.scale(self.image, (32, 32))
        self.rect = self.image.get_rect()
        self.respawn_flash_countdown = 0
        self.rect.center = position
        self.rect.centerx = position[0]
        self.rect.centery = position[1]
        self.spawn_position = position
        self.direction = 0
        self.health = MAX_HP
        self.frame = 0
        self.prev_direction = 0
        self.velocity = PLAYER_VELOCITY

    def attack(self) -> List[pygame.sprite.Sprite]:
        """Make player attack"""
        sprite_list = self.weapon.attack()
        return sprite_list

    def switch_weapon(self, new_weapon):
        """Switch weapon"""
        self.weapon = new_weapon

    def go_left(self):
        """Go left"""
        self.rect.centerx -= self.velocity
        if self.direction == 2:
            self.frame = (self.frame + 1) % 19
        else:
            self.frame = 0
            self.prev_direction = self.direction
        self.direction = 2

    def go_right(self):
        """Go right"""
        self.rect.centerx += self.velocity
        if self.direction == 0:
            self.frame = (self.frame + 1) % 19
        else:
            self.frame = 0
            self.prev_direction = self.direction
        self.direction = 0

    def go_up(self):
        """Go up"""
        self.rect.centery -= self.velocity
        if self.direction == 3:
            self.frame = (self.frame + 1) % 19
        else:
            self.frame = 0
            self.prev_direction = self.direction
        self.direction = 3

    def go_down(self):
        """Go down"""
        self.rect.centery += self.velocity
        if self.direction == 1:
            self.frame = (self.frame + 1) % 19
        else:
            self.frame = 0
            self.prev_direction = self.direction
        self.direction = 1

    def receive_damage(self):
        """Decrease health"""
        self.health -= 1

    def is_dead(self):
        """Check if the player is dead"""
        return self.health <= 0

    def respawn(self):
        self.health = 100
        self.rect.center = self.spawn_position
        self.respawn_flash_countdown = FLASH_TIME
        self.velocity = PLAYER_VELOCITY

    def update(self):
        """Update the image"""
        self.change_image(DIRECTIONS_STR[self.direction], self.frame)

    def change_image(self, direction, frame):
        """Update the image"""
        if self.respawn_flash_countdown > 0:
            self.respawn_flash_countdown -= 1
            if self.respawn_flash_countdown % 30 < 5:
                old_pos = self.rect.center
                direction_str = "Transparent.png"
                self.image = pygame.image.load(direction_str)
                self.image = pygame.transform.scale(self.image, (32, 32))
                self.rect = self.image.get_rect()
                self.rect.center = old_pos
                return

        old_pos = self.rect.center
        # direction_str = str(self.weapon) + '/' + direction + '/survivor-move_handgun_' + str(frame) + '.png'
        direction_str = self.weapon.__str__() + '/' + direction + '/survivor-move (' + str(frame+1) + ').png'
        self.image = pygame.image.load(direction_str)
        self.image = pygame.transform.scale(self.image, (32, 32))
        # self.image.set_colorkey((255, 255, 255))

        self.rect = self.image.get_rect()
        self.rect.center = old_pos
