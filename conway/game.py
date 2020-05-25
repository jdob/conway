import numpy

ALIVE = 1
DEAD = 0
NEW = 2
KILLED = 3


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
                current = self.grid[y, x]

                # At this iteration, treat these as alive or dead
                if current == NEW:
                    current = ALIVE
                    new_grid[y, x] = ALIVE
                elif current == KILLED:
                    current = DEAD
                    new_grid[y, x] = DEAD

                if current == ALIVE:
                    if (neighbors < 2) or (neighbors > 3):
                        new_grid[y, x] = KILLED
                else:
                    if neighbors == 3:
                        new_grid[y, x] = NEW

        self.grid[:] = new_grid[:]

    def print_grid(self):
        for y in range(self.height):
            row = ''
            for x in range(self.width):
                row += '%d ' % self.grid[y, x]
            print(row)

    @staticmethod
    def is_on(value):
        return value == ALIVE or value == NEW

    @staticmethod
    def is_off(value):
        return value == DEAD or value == KILLED

    def _count_neighbors(self, x, y):
        def value_of(vy, vx):
            z = self.grid[vy, vx]
            if self.is_on(z):
                return 1
            else:
                return 0

        total = value_of((y - 1) % self.height, x) + \
                value_of((y + 1) % self.height, x) + \
                value_of(y, (x - 1) % self.width) + \
                value_of(y, (x + 1) % self.width) + \
                value_of((y - 1) % self.height, (x - 1) % self.width) + \
                value_of((y + 1) % self.height, (x - 1) % self.width) + \
                value_of((y - 1) % self.height, (x + 1) % self.width) + \
                value_of((y + 1) % self.height, (x + 1) % self.width)
        return total


def random_grid(width, height):
    grid = numpy.random.choice([ALIVE, DEAD], width * height, p=[0.2, 0.8]).reshape(height, width)
    gol = GameOfLife(grid)
    return gol
