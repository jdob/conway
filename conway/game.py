import numpy


ON = 1
OFF = 0


class GameOfLife(object):

    def __init__(self, starting_grid) -> None:
        super().__init__()
        self.grid = starting_grid.copy()

    def step(self):
        new_grid = self.grid.copy()

        for x in range(len(self.grid)):
            for y in range(len(self.grid)):
                neighbors = self._count_neighbors(x, y)
                if self.grid[x, y] == ON:
                    if (neighbors < 2) or (neighbors > 3):
                        new_grid[x, y] = OFF
                else:
                    if neighbors == 3:
                        new_grid[x, y] = ON

        self.grid[:] = new_grid[:]

    def _count_neighbors(self, x, y):
        n = len(self.grid)
        total = self.grid[(x-1)%n, y] +\
                self.grid[(x+1)%n, y] +\
                self.grid[x, (y-1)%n] +\
                self.grid[x, (y+1)%n] +\
                self.grid[(x-1)%n, (y-1)%n] +\
                self.grid[(x+1)%n, (y-1)%n] +\
                self.grid[(x-1)%n, (y+1)%n] +\
                self.grid[(x+1)%n, (y+1)%n]
        return total

    def print_grid(self):
        for y in range(len(self.grid)):
            row = ''
            for x in range(len(self.grid)):
                row += '%d ' % self.grid[x, y]
            print(row)


def random_grid(size):
    grid = numpy.random.choice([ON, OFF], size*size, p=[0.2, 0.8]).reshape(size, size)
    gol = GameOfLife(grid)
    return gol

