import pygame
from typing import List
from Player import Player
import math

FRAME_RATE = 30
ZOMBIE_VELOCITY = 2
ZOMBIE_DAMAGE = 1
ZOMBIE_HEALTH = 75
DIRECTIONS_STR = ['zombieRight', 'zombieDown', 'zombieLeft', 'zombieUp']
def load_imgage():
    img_set = []
    for i in range(4):
        lst = []
        for j in range(16):
            direection_str = DIRECTIONS_STR[i] + '/skeleton-move_' + str(j) + '.png'
            lst.append(pygame.image.load(direection_str))
        img_set.append(lst)
    return img_set

IMG = load_imgage()

class Zombie(pygame.sprite.Sprite):
    """A Zombie"""

    def __init__(self, player1, player2, position, safe_zone):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("zombieUp/skeleton-move_0.png")
        self.image = pygame.transform.scale(self.image, (34, 34))
        self.image.set_colorkey((255, 255, 255))
        self.safe_zone = safe_zone
        self.rect = self.image.get_rect()

        self.rect.centerx = position[0]
        self.rect.centery = position[1]
        self.spawn_position = position

        self.player1 = player1
        self.player2 = player2

        self.direction = 0
        self.health = ZOMBIE_HEALTH
        self.frame = 0
        self.damage = ZOMBIE_DAMAGE
        self.prev_direction = 0

    def attack(self):
        """Make zombie attack"""
        pass

    def collide(self, other):
        if isinstance(other, Player):
            other.health -= self.damage

    def receive_damage(self):
        """Decrease health"""
        self.health -= 1

    def is_dead(self):
        """Check if the player is dead"""
        return self.health <= 0

    def move(self, zombies):
        """Move the zombie"""
        old_pos = self.rect.center
        destination = self.get_close_position()
        destination_x = destination[0]
        destination_y = destination[1]
        if abs(destination_x - self.rect.centerx) >= \
                abs(destination_y - self.rect.centery):
            if destination_x - self.rect.centerx >= 0:
                self.go_right()
            else:
                self.go_left()
        else:
            if destination_y - self.rect.centery >= 0:
                self.go_down()
            else:
                self.go_up()
        if pygame.sprite.spritecollide(self, self.safe_zone, False):
            self.rect.center = old_pos
        for zombie in pygame.sprite.spritecollide(self, zombies, False):
            if zombie != self:
                self.rect.center = old_pos
                break
    def go_left(self):
        """Go left"""
        self.rect.centerx -= ZOMBIE_VELOCITY
        if self.direction == 2:
            self.frame = (self.frame + 1) % 16
        else:
            self.frame = 0
        self.direction = 2

    def go_right(self):
        """Go right"""
        self.rect.centerx += ZOMBIE_VELOCITY
        if self.direction == 0:
            self.frame = (self.frame + 1) % 16
        else:
            self.frame = 0
        self.direction = 0

    def go_up(self):
        """Go up"""
        self.rect.centery -= ZOMBIE_VELOCITY
        if self.direction == 3:
            self.frame = (self.frame + 1) % 16
        else:
            self.frame = 0
        self.direction = 3

    def go_down(self):
        """Go down"""
        self.rect.centery += ZOMBIE_VELOCITY
        if self.direction == 1:
            self.frame = (self.frame + 1) % 16
        else:
            self.frame = 0
        self.direction = 1

    def get_close_position(self):
        """Get the closest player position"""
        player1_dst = math.sqrt(((self.player1.rect.centerx - self.rect.centerx)
                                ** 2 + (self.player1.rect.centery -
                                       self.rect.centery)**2))
        player2_dst = math.sqrt(((self.player2.rect.centerx - self.rect.centerx)
                                ** 2) + ((self.player2.rect.centery -
                                       self.rect.centery)**2))
        if player1_dst >= player2_dst:
            return self.player2.rect.center
        else:
            return self.player1.rect.center

    def update(self):
        """Update the image"""
        self.change_image(self.direction, self.frame)

    def change_image(self, direction, frame):
        """Update the image"""
        old_pos = self.rect.center
        #direction_str = direction + '/skeleton-move_' + str(frame) + '.png'
        # self.image = pygame.image.load(direction_str)
        self.image = IMG[direction][frame]
        self.image = pygame.transform.scale(self.image, (34, 34))
        self.image.set_colorkey((255, 255, 255))

        self.rect = self.image.get_rect()
        self.rect.center = old_pos

