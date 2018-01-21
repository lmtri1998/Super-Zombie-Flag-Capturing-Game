import pygame

CaptureFlag_DESCRIPTION = "Capture the flag a number of times to win!"

class Goal:

    def __init__(self, players):
        self.players = players

    def check_for_win(self):
        raise NotImplementedError

class CaptureFlag(Goal):

    def __init__(self, players, zones, flag, num_round):
        Goal.__init__(self, players)
        self.score = [0, 0]
        self.num_round = num_round
        self.wining_player = None
        self.flag = flag
        self.zones = zones
        self.players_grp = pygame.sprite.Group(players)
        self.screen_pause = False

    def check_for_win(self):
        is_reset = False
        if self.players[0].rect.colliderect(self.zones[0].rect):
            if self.flag.get_player() == self.players[0]:
                self.score[0] += 1
                is_reset = True
        elif self.players[1].rect.colliderect(self.zones[1].rect):
            if self.flag.get_player() == self.players[1]:
                self.score[1] += 1
                is_reset = True

        if is_reset:
            self.screen_pause = True
            if 2 == self.score[0]:
                self.wining_player = self.players[0]
                return True
            elif 2 == self.score[1]:
                self.wining_player = self.players[1]
                return True

            self.flag.reset()

            for p in self.players:
                p.respawn()
        if not self.flag.is_carried():
            for p in pygame.sprite.spritecollide(self.flag, self.players_grp, False):
                self.flag.piked_up_by(p)
                p.velocity -= 2

    def get_wining_player(self):
        return self.wining_player

    def get_wining_msg(self):
        for i in range(len(self.players)):
            if self.players[i] == self.wining_player:
                return "Player " + str(i+1) + " Wins"
        return "OOps"
