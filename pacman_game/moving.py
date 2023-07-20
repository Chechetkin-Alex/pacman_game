from being import Being


class Moving(Being):
    speed = 1500
    allowed_directions = [False, False, False, False]
    direction = [0, 0, 0, 0]  # left up right down

    def __init__(self, var):
        super().__init__(var)

    def set_allowed_directions(self, allowed_directions):
        if not self.coord.in_cell_x():
            self.allowed_directions = [True, False, True, False]
        elif not self.coord.in_cell_y():
            self.allowed_directions = [False, True, False, True]
        else:
            self.allowed_directions = allowed_directions

    def set_direction(self, direction):
        if direction == -1:
            return True
        if self.allowed_directions[direction]:
            self.direction = [0, 0, 0, 0]
            self.direction[direction] = 1
            return True
        return False

    def set_speed(self, speed):
        self.speed = speed

    def move(self):
        for i in range(4):
            if not self.allowed_directions[i]:
                self.direction[i] = 0
        if self.direction[0]:
            self.coord.increment(-1, 0)
        if self.direction[1]:
            self.coord.increment(0, -1)
        if self.direction[2]:
            self.coord.increment(1, 0)
        if self.direction[3]:
            self.coord.increment(0, 1)
        if self.coord.x == -10 * self.coord.cell_size:
            self.coord.set(self.var.num_cols * self.coord.cell_size * 10 - 1, self.coord.y)
        if self.coord.x == self.var.num_cols * self.coord.cell_size * 10:
            self.coord.set(-10 * self.coord.cell_size + 1, self.coord.y)
        if self.coord.y == -10 * self.coord.cell_size:
            self.coord.set(self.coord.x, self.var.num_rows * self.coord.cell_size * 10 - 1)
        if self.coord.y == self.var.num_rows * self.coord.cell_size * 10:
            self.coord.set(self.coord.x, -10 * self.coord.cell_size + 1)
