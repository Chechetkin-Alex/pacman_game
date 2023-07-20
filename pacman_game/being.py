class Coord:
    x = 0
    y = 0
    cell_size = 20

    def __init__(self, coord, cell_size, is_cell=False):
        if is_cell:
            self.x = coord[0] * 10 * cell_size
            self.y = coord[1] * 10 * cell_size
        else:
            self.x, self.y = coord
        self.cell_size = cell_size

    def normal(self):
        return self.x, self.y

    def px(self, half_cell_incr_x=0, half_cell_incr_y=0, shift=0):
        return (self.x // 10 + self.cell_size // 2 * half_cell_incr_x + shift,
                self.y // 10 + self.cell_size // 2 * half_cell_incr_y + shift)

    def cell(self, incr_x=0, incr_y=0):
        return self.x // 10 // self.cell_size + incr_x, self.y // 10 // self.cell_size + incr_y

    def in_cell_x(self):
        return self.x % (self.cell_size * 10) == 0

    def in_cell_y(self):
        return self.y % (self.cell_size * 10) == 0

    def in_cell(self):
        return self.in_cell_x() and self.in_cell_y()

    def set(self, x, y, is_cell=False):
        if is_cell:
            self.x = x * self.cell_size * 10
            self.y = y * self.cell_size * 10
        else:
            self.x = x
            self.y = y

    def increment(self, x, y):
        self.x += x
        self.y += y

    def diff(self, other):
        return (self.cell()[0] - other.cell()[0]) ** 2 + (self.cell()[1] - other.cell()[1]) ** 2

    def mid(self, other):
        if other is None:
            return self.cell()
        return (self.cell()[0] + other.cell()[0]) // 2, (self.cell()[1] + other.cell()[1]) // 2

    def new(self, x, y):
        return Coord((x, y), self.cell_size, is_cell=True)


class Being:
    coord = object()
    var = object()
    view_size = 26

    def __init__(self, var):
        self.coord = Coord((0, 0), 0)
        self.var = var
