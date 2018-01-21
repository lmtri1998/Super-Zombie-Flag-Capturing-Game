import pygame

class Flag(pygame.sprite.Sprite):

    def __init__(self, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("flag_sprite.png")
        self.image = pygame.transform.scale(self.image, (34, 34))
        self.rect = self.image.get_rect()
        self.rect.center = position
        self.player = None
        self.init_position = position

    def piked_up_by(self, player):
        self.player = player

    def drop(self):
        self.player = None

    def reset(self):
        self.rect.center = self.init_position
        self.drop()

    def is_carried(self):
        return self.player is not None

    def get_player(self):
        return self.player

    def update(self):
        if not self.player is None:
            self.rect.center = self.player.rect.center
