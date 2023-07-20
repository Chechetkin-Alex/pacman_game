import math
import pygame

from being import Being


class Point(Being):
    command = object()
    category = 0
    # ordinary points will not leave
    will_leave = False
    time_to_leave = 0

    def __init__(self, var, category, coord):
        super().__init__(var)
        self.category = category
        self.coord.cell_size = self.var.cell_size
        self.coord.set(coord[0], coord[1], is_cell=True)

    def get_eaten(self):
        pass

    def draw(self):
        if self.category == 1:
            pygame.draw.circle(self.var.screen, "white",
                               self.coord.px(1, 1), 3)
        if self.category == 2:
            radius = abs(math.sin(pygame.time.get_ticks() / 800)) * 4 + 3
            pygame.draw.circle(self.var.screen, "orange",
                               self.coord.px(1, 1), radius)
