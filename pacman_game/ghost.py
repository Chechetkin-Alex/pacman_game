from random import randint
from moving import Moving
import pygame


class Ghost(Moving):
    NAMES = ["Blinky", "Clyde", "Inky", "Pinky"]
    name = ""
    skins = []
    counter = 0
    eaten_skin = object()
    is_eaten = 0
    when_leave = 0
    start_coord = object()
    leave_after_start = 0
    is_blind = False
    speed_multiplier = 10

    def __init__(self, var, start_coord, name):
        super().__init__(var)
        self.coord.cell_size = self.var.cell_size
        self.start_coord = self.coord.new(start_coord[0], start_coord[1])
        self.name = name
        self.skins = [pygame.transform.scale(pygame.image.load(f"Assets/ghosts/{name + str(i + 1)}.png"),
                                             (self.view_size, self.view_size)) for i in range(6)]
        self.eaten_skin = pygame.transform.scale(pygame.image.load(f"Assets/ghosts/eaten.png"),
                                                 (self.view_size, self.view_size))
        self.speed = 1000
        self.leave_after_start = self.NAMES.index(name) * self.speed

    def go_to_start(self):
        self.coord.set(self.start_coord.x, self.start_coord.y)

    def get_target(self, blinky_coord, players):
        self.is_blind = False
        if self.is_eaten:
            if self.start_coord.normal() == self.coord.normal() and self.is_eaten == 1:
                self.when_leave = self.speed * 20
                self.is_eaten = 2
            return (self.start_coord.cell(),)
        if self.name == self.NAMES[3]:
            ans = []
            for player in players:
                if player.how_angry == 0:
                    if player.direction[0]:
                        ans += [player.coord.cell(-4, 0)]
                    elif player.direction[1]:
                        ans += [player.coord.cell(0, -4)]
                    elif player.direction[2]:
                        ans += [player.coord.cell(4, 0)]
                    elif player.direction[3]:
                        ans += [player.coord.cell(0, 4)]
                    else:
                        ans += [player.coord.cell()]
            return ans
        if self.name == self.NAMES[1]:
            return [player.coord.mid(blinky_coord) for player in players if player.how_angry == 0]
        if self.name == self.NAMES[2]:
            ans = []
            for player in players:
                if self.coord.diff(player.coord) > 16:
                    ans += [player.coord.cell()]
            if not ans:
                self.speed_multiplier = 2
                return [self.start_coord.cell()]
            self.speed_multiplier = 10
            return ans
        return [player.coord.cell() for player in players if player.how_angry == 0]

    def set_blind(self):
        self.is_blind = True

    def go_home(self):
        self.is_eaten = 1

    def move(self):
        if self.when_leave > 0:
            self.counter = 300
            self.when_leave -= 1
            if self.when_leave == 0:
                self.is_eaten = 0
        else:
            self.counter += 1
            if self.counter == 600:
                self.counter = 0
            super().move()

    def get_speed(self):
        if self.is_eaten:
            return self.speed * 5
        if self.is_blind:
            return self.speed // 5
        return self.speed // 10 * self.speed_multiplier

    def set_direction(self, direction):
        if super().set_direction(direction):
            return
        while not super().set_direction(randint(0, 3)):
            pass

    def draw(self):
        if self.is_eaten:
            skin = self.eaten_skin
        else:
            skin = self.skins[self.counter // 100]
        coord = self.coord.px(shift=(self.coord.cell_size - self.view_size) // 2)
        if self.direction[0]:
            self.var.screen.blit(pygame.transform.flip(skin, True, False), coord)
        elif self.direction[1]:
            self.var.screen.blit(pygame.transform.rotate(skin, 90), coord)
        elif self.direction[3]:
            self.var.screen.blit(pygame.transform.rotate(skin, -90), coord)
        else:
            self.var.screen.blit(skin, coord)
