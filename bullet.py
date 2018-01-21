import pygame

FRAME_RATE = 30

SIZE_OF_EXPLOSION = (15, 15)
PISTOL_IMAGE = ""
PISTOL_BULLET_SPEED = 20
PISTOL_DAMGE = 25
PISTOL_BULLET_DISTANCE = 325

SHOTGUN_SPEED = 24
SHOTGUN_DAMGE = 33
SHOTGUN_BULLET_DISTANCE = 60

MACHINEGUN_BULLET_SPEED = 20
MACHINEGUN_DAMGE = 10
MACHINEGUN_BULLET_DISTANCE = 175

SWORD_DAMAGE = 20
SWORD_SPEED = 15
SWORD_ANGLE = 60

COLOR_LIST = [(255, 51, 51), (255, 128, 0), (255, 255, 255), (0, 255, 0), (0, 0, 255), (255, 0, 255), (127, 0, 255)]

class Bullet(pygame.sprite.Sprite):
    def __init__(self):
        raise NotImplementedError

    def update(self):
        raise NotImplementedError

class PistolBullet(Bullet):
    x_vol: int
    y_vol: int
    x: int
    y: int
    damage: int
    distance: int

    def __init__(self, direction, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((5, 5))
        self.image.fill(COLOR_LIST[0])
        self.rect = self.image.get_rect()
        self.rect.centerx = position[0]
        self.rect.centery = position[1]
        self.explosion = False

        self.damage = PISTOL_DAMGE
        self.distance = PISTOL_BULLET_DISTANCE
        self.x_vol = 0
        self.y_vol = 0
        self.frame = 0
        if direction == 0:
            self.x_vol = PISTOL_BULLET_SPEED
        elif direction == 1:
            self.y_vol = PISTOL_BULLET_SPEED
        elif direction == 2:
            self.x_vol = -PISTOL_BULLET_SPEED
        else:
            self.y_vol = -PISTOL_BULLET_SPEED

    def update(self):
        if self.explosion:
            if self.frame == 3:
                self.kill()
            else:
                center = self.rect.center
                self.image = pygame.image.load("explosion/explosion" + str(self.frame) + ".png")
                self.image = pygame.transform.scale(self.image, SIZE_OF_EXPLOSION)
                self.rect = self.image.get_rect()
                self.rect.center = center
                self.frame += 1
        else:
            self.distance -= abs(self.x_vol) + abs(self.y_vol)
            if self.distance < 0:
                self.end()
            self.rect.centerx += self.x_vol
            self.rect.centery += self.y_vol
            self.frame += 1
            self.image.fill(COLOR_LIST[self.frame % len(COLOR_LIST)])

    def collide(self, other):
        if not self.explosion == True:
            other.health -= self.damage
        self.end()


    def end(self):
        if not self.explosion == True:
            self.frame = 0
        self.explosion = True


class ShotGunBullet(Bullet):
    def __init__(self, x_component, y_component, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((5, 5))
        self.image.fill(COLOR_LIST[0])
        self.rect = self.image.get_rect()
        self.rect.centerx = position[0]
        self.rect.centery = position[1]
        self.frame = 0
        self.explosion = False

        self.damage = SHOTGUN_DAMGE
        self.distance = SHOTGUN_BULLET_DISTANCE
        self.x_vol = x_component * SHOTGUN_SPEED
        self.y_vol = y_component * SHOTGUN_SPEED

    def update(self):
        if self.explosion:
            if self.frame == 3:
                self.kill()
            else:
                center = self.rect.center
                self.image = pygame.image.load("explosion/explosion" + str(self.frame) + ".png")
                self.image = pygame.transform.scale(self.image, SIZE_OF_EXPLOSION)
                self.rect = self.image.get_rect()
                self.rect.center = center
                self.frame += 1
        else:
            self.distance -= SHOTGUN_SPEED
            if self.distance < 0:
                self.end()
            self.rect.centerx += self.x_vol
            self.rect.centery += self.y_vol
            self.frame += 1
            self.image.fill(COLOR_LIST[self.frame % len(COLOR_LIST)])

    def collide(self, other):
        # to make sure it only deals the damage once
        if not self.explosion == True:
            other.health -= self.damage
        self.end()

    def end(self):
        if not self.explosion == True:
            self.frame = 0
        self.explosion = True



class MachineGunBullet(Bullet):
    x_vol: int
    y_vol: int
    x: int
    y: int
    damage: int
    distance: int

    def __init__(self, direction, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((5, 5))
        self.image.fill(COLOR_LIST[0])
        self.rect = self.image.get_rect()
        self.rect.centerx = position[0]
        self.rect.centery = position[1]
        self.frame = 0

        self.explosion = False
        self.damage = MACHINEGUN_DAMGE
        self.distance = MACHINEGUN_BULLET_DISTANCE
        self.x_vol = 0
        self.y_vol = 0
        if direction == 0:
            self.x_vol = MACHINEGUN_BULLET_SPEED
        elif direction == 1:
            self.y_vol = MACHINEGUN_BULLET_SPEED
        elif direction == 2:
            self.x_vol = -MACHINEGUN_BULLET_SPEED
        else:
            self.y_vol = -MACHINEGUN_BULLET_SPEED

    def update(self):
        if self.explosion:
            if self.frame == 3:
                self.kill()
            else:
                center = self.rect.center
                self.image = pygame.image.load("explosion/explosion" + str(self.frame) + ".png")
                self.image = pygame.transform.scale(self.image, SIZE_OF_EXPLOSION)
                self.rect = self.image.get_rect()
                self.rect.center = center
                self.frame += 1
        else:
            self.distance -= abs(self.x_vol) + abs(self.y_vol)
            if self.distance < 0:
                self.end()
            self.rect.centerx += self.x_vol
            self.rect.centery += self.y_vol
            self.frame += 1
            self.image.fill(COLOR_LIST[self.frame % len(COLOR_LIST)])


    def collide(self, other):
        # to make sure it only deals damage once
        if not self.explosion == True:
            other.health -= self.damage
        self.end()

    def end(self):
        if not self.explosion == True:
            self.frame = 0
        self.explosion = True




class SwordBlade(pygame.sprite.Sprite):
    def __init__(self, direction, position):
        pygame.sprite.Sprite.__init__(self)
        starting_angles = [-90, 180, 90, 0]
        self.image = pygame.transform.scale(pygame.image.load("sword_sprite.png"), (10, 30))
        self.image = pygame.transform.rotate(self.image, starting_angles[direction] - 45)

        self.rect = self.image.get_rect()
        self.rect.centerx = position[0]
        self.rect.centery = position[1]

        self.damage = SWORD_DAMAGE
        self.angle = SWORD_ANGLE
        self.already_dealt_damage = False

    def update(self):
        if self.angle > 0:
            old_center = self.rect.center
            self.image = pygame.transform.rotate(self.image, SWORD_SPEED)
            self.rect = self.image.get_rect()
            self.rect.center = old_center
            self.angle -= SWORD_SPEED
        if self.angle <= 0:
            self.kill()
        return []

    def collide(self, other):
        if not self.already_dealt_damage:
            other.health -= self.damage
            self.already_dealt_damage = True

    def end(self):
        pass
