import pygame
from bullet import PistolBullet, ShotGunBullet, MachineGunBullet, SwordBlade
FRAME_RATE = 30

PISTOL_BULLET_COUNT = 10
PISTOL_RELOAD_TIME= 15

SHOTGUN_BULLET_COUNT = 5
SHOTGUN_RELOAD_TIME = 30

MACHINEGUN_BULLET_COUNT = 100
MACHINEGUN_RELOAD_TIME = 20
MACHINEGUN_BULLETS_PER_SHOT = 5

SWORD_RECHARGE_TIME = 15
class Weapon():

    owner: 'Player'
    bullet_count: int
    def __init__(self):
        raise NotImplementedError

    def attack(self):
        raise NotImplementedError

    def still_available(self) -> bool:
        raise NotImplementedError

    def update(self):
        if self.reload_time != 0:
            self.reload_time -= 1
        return []


class Pistol(Weapon):
    owner: 'Player'
    bullet: 'Bullet'
    bullet_count: int
    reload_time: int

    def __init__(self, owner):
        self.owner = owner
        self.bullet = PistolBullet
        self.bullet_count = PISTOL_BULLET_COUNT
        self.reload_time = 0

    def attack(self):
        if self.reload_time == 0:
            self.bullet_count -= 1
            self.reload_time = PISTOL_RELOAD_TIME
            return [self.bullet(self.owner.direction, self.owner.rect.center)]
        return []

    def still_available(self):
        return self.bullet_count != 0

    def update(self):
        if self.reload_time != 0:
            self.reload_time -= 1
        return []

    def __str__(self):
        return "Pistol"


class ShotGun(Weapon):
    def __init__(self, owner):
        self.owner = owner
        self.bullet = ShotGunBullet
        self.bullet_count = SHOTGUN_BULLET_COUNT
        self.reload_time = 0

    def attack(self):
        if self.reload_time == 0:
            self.bullet_count -= 1
            self.reload_time = SHOTGUN_RELOAD_TIME
            if self.owner.direction == 0:
                bullets = [self.bullet(1, 0, self.owner.rect.center),
                           self.bullet(1, 0.2, self.owner.rect.center),
                           self.bullet(1, -0.2, self.owner.rect.center)]
            elif self.owner.direction == 1:
                bullets = [self.bullet(0, 1, self.owner.rect.center),
                           self.bullet(0.2, 1, self.owner.rect.center),
                           self.bullet(-0.2, 1, self.owner.rect.center)]
            elif self.owner.direction == 2:
                bullets = [self.bullet(-1, 0, self.owner.rect.center),
                           self.bullet(-1, 0.2, self.owner.rect.center),
                           self.bullet(-1, -0.2, self.owner.rect.center)]
            else:
                bullets = [self.bullet(0, -1, self.owner.rect.center),
                           self.bullet(0.2, -1, self.owner.rect.center),
                           self.bullet(-0.2, -1, self.owner.rect.center)]
            return bullets


        return []

    def still_available(self):
        return self.bullet_count != 0

    def update(self):
        if self.reload_time != 0:
            self.reload_time -= 1
        return []

    def __str__(self):
        return "ShotGun"

class MachineGun(Weapon):

    def __init__(self, owner):
        self.owner = owner
        self.bullet = MachineGunBullet
        self.bullet_count = MACHINEGUN_BULLET_COUNT
        self.reload_time = 0
        self.bullet_left = 0

    def attack(self):
        if self.bullet_left > 0:
            self.bullet_left -= 1
            return [self.bullet(self.owner.direction, self.owner.rect.center)]
        elif self.reload_time == 0:
            self.bullet_left = MACHINEGUN_BULLETS_PER_SHOT - 1
            self.reload_time = MACHINEGUN_RELOAD_TIME
            return [self.bullet(self.owner.direction, self.owner.rect.center)]
        else:
            return []

    def update(self):
        if self.reload_time != 0:
            self.reload_time -= 1
        if self.bullet_left > 0:
            return [self.attack()]
        else:
            return []

    def still_available(self):
        return self.bullet_count != 0

    def __str__(self):
        return "MachineGun"

class Sword(Weapon):
    def __init__(self, owner):
        self.owner = owner
        self.sword = SwordBlade
        self.recharge_time = 0

    def attack(self):

        if self.recharge_time == 0:
            self.recharge_time = SWORD_RECHARGE_TIME

            if self.owner.direction == 0:
                position = self.owner.rect.midright
            elif self.owner.direction == 1:
                position = self.owner.rect.midbottom
            elif self.owner.direction == 2:
                position = self.owner.rect.midleft
            else:
                position = self.owner.rect.midtop
            return [self.sword(self.owner.direction, position)]
        else:
            return []

    def update(self):
        if self.recharge_time != 0:
            self.recharge_time -= 1

        return []

    def still_available(self):
        return True

    def __str__(self):
        return "Sword"
