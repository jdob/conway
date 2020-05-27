import numpy
import sys


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
        self._current_alive = 0
        self._max_alive = 0
        self._min_alive = sys.maxsize
        self._total_created = 0
        self._total_killed = 0
        self._at_equilibrium = False

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    @property
    def step_count(self):
        return self._step_count

    @property
    def alive_count(self):
        return self._current_alive

    @property
    def created_count(self):
        return self._total_created

    @property
    def killed_count(self):
        return self._total_killed

    @property
    def max_alive(self):
        return self._max_alive

    @property
    def min_alive(self):
        return self._min_alive

    @property
    def at_equilibrium(self):
        return self._at_equilibrium

    def value(self, x, y):
        return self._grid[y, x]

    def step(self):
        new_grid = self._grid.copy()

        # Reset current alive counter and recalculate each time
        previous_alive = self._current_alive
        self._current_alive = 0

        for y in range(self._height):
            for x in range(self._width):
                neighbors = self._count_neighbors(x, y)
                current = self._grid[y, x]

                # At this iteration, treat these as alive or dead
                if current == NEW:
                    current = ALIVE
                elif current == KILLED:
                    current = DEAD

                if current == ALIVE:
                    if (neighbors < 2) or (neighbors > 3):
                        current = KILLED
                        self._total_killed += 1
                else:
                    if neighbors == 3:
                        current = NEW
                        self._total_created += 1

                if current == ALIVE or current == NEW:
                    self._current_alive += 1

                new_grid[y, x] = current

        self._step_count += 1

        # Equilibrium check
        if (previous_alive == self._current_alive) and (self._grid == new_grid).all():
            self._at_equilibrium = True

        # Stats updating
        self._max_alive = max(self._max_alive, self._current_alive)
        self._min_alive = min(self._min_alive, self._current_alive)

        # Replace the old grid with the grid from this iteration
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


def random_grid(width, height, percent_alive):
    return numpy.random.choice([ALIVE, DEAD], width * height,
                               p=[percent_alive, (1 - percent_alive)]).reshape(height, width)
