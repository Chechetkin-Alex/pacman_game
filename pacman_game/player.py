from moving import Moving
import pygame


class Player(Moving):
    index = 0
    counter = 0
    skins = []
    angry_skins = []
    lives = 3
    how_angry = 0
    score = 0
    new_direction = 0
    new_direction_timeout = 0

    def __init__(self, index, filepath_skin, filepath_angry_skin):
        super().__init__(object())
        self.index = index
        for path in filepath_skin:
            self.skins += [pygame.transform.scale(pygame.image.load(path),
                                                  (self.view_size, self.view_size))]
        for angry_path in filepath_angry_skin:
            self.angry_skins += [pygame.transform.scale(pygame.image.load(angry_path),
                                                        (self.view_size, self.view_size))]

    def set_var(self, var):
        self.var = var
        self.coord.cell_size = self.var.cell_size

    def move_to(self, coord):
        self.coord.set(coord[0], coord[1], is_cell=True)

    def set_direction_with_timeout(self, direction):
        self.new_direction = direction
        self.new_direction_timeout = self.speed * self.var.fps // 3

    def move(self):
        if self.new_direction_timeout > 0:
            self.new_direction_timeout -= 1
            if self.set_direction(self.new_direction):
                self.new_direction_timeout = 0
        if self.how_angry > 0:
            self.how_angry -= 1
        if self.how_angry == 1:
            return 1
        super().move()

    def set_angry(self):
        self.how_angry = self.speed * 5

    def meet_ghost(self, ghost):
        if self.how_angry > 0:
            ghost.go_home()
            return 0  # angry

        self.lives -= 1
        if self.lives == 0:
            return 1  # restart level
        else:
            return 2  # death

    def draw(self):
        coord = self.coord.px(shift=(self.coord.cell_size - self.view_size) // 2)

        self.counter += 1
        if self.counter == len(self.skins) * 5:
            self.counter = 0

        if self.how_angry > 0:
            skin = self.angry_skins[self.counter // 5]
        else:
            skin = self.skins[self.counter // 5]

        self.var.screen.blit(skin, coord)
