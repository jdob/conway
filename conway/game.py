import numpy

ON = 1
OFF = 0


class GameOfLife(object):

    def __init__(self, starting_grid) -> None:
        super().__init__()
        self.grid = starting_grid.copy()

        self.width = len(self.grid[0])
        self.height = len(self.grid)

    def step(self):
        new_grid = self.grid.copy()

        for y in range(self.height):
            for x in range(self.width):
                neighbors = self._count_neighbors(x, y)
                if self.grid[y, x] == ON:
                    if (neighbors < 2) or (neighbors > 3):
                        new_grid[y, x] = OFF
                else:
                    if neighbors == 3:
                        new_grid[y, x] = ON

        self.grid[:] = new_grid[:]

    def _count_neighbors(self, x, y):
        total = self.grid[(y - 1) % self.height, x] + \
                self.grid[(y + 1) % self.height, x] + \
                self.grid[y, (x - 1) % self.width] + \
                self.grid[y, (x + 1) % self.width] + \
                self.grid[(y - 1) % self.height, (x - 1) % self.width] + \
                self.grid[(y + 1) % self.height, (x - 1) % self.width] + \
                self.grid[(y - 1) % self.height, (x + 1) % self.width] + \
                self.grid[(y + 1) % self.height, (x + 1) % self.width]
        return total

    def print_grid(self):
        for y in range(self.height):
            row = ''
            for x in range(self.width):
                row += '%d ' % self.grid[y, x]
            print(row)


def random_grid(width, height):
    grid = numpy.random.choice([ON, OFF], width * height, p=[0.2, 0.8]).reshape(height, width)
    gol = GameOfLife(grid)
    return gol
