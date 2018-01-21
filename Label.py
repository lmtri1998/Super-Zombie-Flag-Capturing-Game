import pygame

class Label(pygame.sprite.Sprite):

    msg: str
    position: str

    def __init__(self, font_size, position):
        pygame.sprite.Sprite.__init__(self)
        self.position = position
        self.font = pygame.font.Font("28_Days_Later.ttf", font_size)
        self.msg = ""
        self.image = self.font.render(self.msg, 1, (0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.center = position
        self.color = (0, 0, 0)

    def set_color(self, color):
        self.color = color

    def set_position(self, position):
        self.rect.center = position

    def set_msg(self, msg: str):
        self.msg = msg
        self.image = self.font.render(self.msg, 1, self.color)
        self.image.get_rect()
        self.rect.center = self.position


class Timer(Label):

    minute: int
    second: int
    frame_rate: int

    def __init__(self, font_size, position, minute, second, frame_rate):
        Label.__init__(self, font_size, position)
        self.frame_rate = frame_rate
        self.minute, self.second = self.convert(minute, second)

    def convert(self, minute, second):
        minute += int(second / 60)
        second = (second % 60) * self.frame_rate

        return minute, second

    def get_real_second(self):
        return int(self.second / 30)

    def time_up(self):
        return self.minute <= 0 and self.get_real_second() <= 0

    def update(self):
        if self.second < 0:
            self.minute -= 1
            self.second = 60 * self.frame_rate

        if self.minute < 10:
            real_minure = "0" + str(self.minute)
        else:
            real_minure = str(self.minute)
        if int(self.second / 30) < 10:
            real_second = "0" + str(int(self.second / 30))
        else:
            real_second = str(int(self.second / 30))

        time_string = "%s  %s" %(real_minure, real_second)
        self.set_msg(time_string)
        self.second -= 1

class TempLabel(Label):

    def __init__(self, font_size, position, real_time, frame_rate, color=(0, 255, 0)):
        Label.__init__(self, font_size, position)
        self.frame_time = real_time * frame_rate
        self.set_color(color)

    def update(self):
        self.frame_time -= 1
        if self.frame_time < 0:
            self.kill()


class Pointer(Label):

    def __init__(self, font_size, positions, values):
        Label.__init__(self, font_size, positions[0])
        self.positions = positions
        self.values = values
        self.index = 0
        self.set_msg("*")

    def move_next(self):
        if self.index == len(self.positions)-1:
            self.index = 0
        else:
            self.index += 1

        self.rect.center = self.positions[self.index]

    def move_previous(self):
        if self.index == 0:
            self.index = len(self.positions)-1
        else:
            self.index -= 1

        self.rect.center = self.positions[self.index]

    def get_value(self):
        return self.values[self.index]

