import numpy

ALIVE = 1
DEAD = 0
NEW = 2
KILLED = 3


class GameOfLife(object):

    def __init__(self, starting_grid) -> None:
        super().__init__()

        self._grid = starting_grid.copy()
        self._width = len(self._grid[0])
        self._height = len(self._grid)
        self._step_count = 0

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    @property
    def step_count(self):
        return self._step_count

    def value(self, x, y):
        return self._grid[y, x]

    def step(self):
        new_grid = self._grid.copy()

        for y in range(self._height):
            for x in range(self._width):
                neighbors = self._count_neighbors(x, y)
                current = self._grid[y, x]

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

        self._step_count += 1
        self._grid[:] = new_grid[:]

    def print_grid(self):
        for y in range(self._height):
            row = ''
            for x in range(self._width):
                row += '%d ' % self._grid[y, x]
            print(row)

    @staticmethod
    def is_on(value):
        return value == ALIVE or value == NEW

    @staticmethod
    def is_off(value):
        return value == DEAD or value == KILLED

    def _count_neighbors(self, x, y):
        def value_of(vy, vx):
            z = self._grid[vy, vx]
            if self.is_on(z):
                return 1
            else:
                return 0

        total = value_of((y - 1) % self._height, x) + \
                value_of((y + 1) % self._height, x) + \
                value_of(y, (x - 1) % self._width) + \
                value_of(y, (x + 1) % self._width) + \
                value_of((y - 1) % self._height, (x - 1) % self._width) + \
                value_of((y + 1) % self._height, (x - 1) % self._width) + \
                value_of((y - 1) % self._height, (x + 1) % self._width) + \
                value_of((y + 1) % self._height, (x + 1) % self._width)
        return total


def random_grid(width, height):
    grid = numpy.random.choice([ALIVE, DEAD], width * height, p=[0.2, 0.8]).reshape(height, width)
    gol = GameOfLife(grid)
    return gol
