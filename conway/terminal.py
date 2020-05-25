import curses

from conway import game

FULL_SCREEN_WIDTH_PADDING = 4
FULL_SCREEN_HEIGHT_PADDING = 4


class TerminalView(object):

    def __init__(self, gol, update_interval=500) -> None:
        super().__init__()
        self.gol = gol
        self.screen = None
        self.x_offset = 0
        self.y_offset = 0
        self.update_interval = update_interval

    def run(self):
        self.screen = curses.initscr()
        self.screen.clear()
        self.screen.refresh()

        # Color setup
        curses.start_color()
        curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_CYAN, curses.COLOR_BLACK)

        # General curses settings
        curses.curs_set(0)

        self._calculate_offsets()
        self._flush_terminal()

        try:
            self._run_game()
        except:
            pass

        curses.curs_set(1)
        curses.endwin()

    def _run_game(self):
        while True:
            for y in range(self.gol.height):
                for x in range(self.gol.width):
                    self._display_glyph(x, y)
            self._display_status()
            self.screen.refresh()
            self.gol.step()
            curses.napms(self.update_interval)

    def _display_glyph(self, x, y):
        z = self.gol.grid[y, x]

        if z == game.ALIVE:
            glyph = 'o'
            color = curses.color_pair(1) | curses.A_BOLD
        elif z == game.NEW:
            glyph = 'o'
            color = curses.color_pair(1) | curses.A_BOLD
        elif z == game.KILLED:
            glyph = ' '
            color = curses.color_pair(2)
        else:
            glyph = ' '
            color = curses.color_pair(1)

        self.screen.addstr(y + self.y_offset, x + self.x_offset,
                           glyph, color)

    def _display_status(self):
        status = 'Step: %d' % self.gol.step_count
        self.screen.addstr((self.gol.height + self.y_offset + 1), self.x_offset, status)

    def _calculate_offsets(self):
        num_rows, num_cols = self.screen.getmaxyx()

        self.x_offset = int((num_cols - self.gol.width) / 2) - 1
        self.y_offset = int((num_rows - self.gol.height) / 2) - 1

    def _flush_terminal(self):
        """Fill the terminal with empty spaces to initialize the canvas"""
        num_rows, num_cols = self.screen.getmaxyx()
        for y in range(num_rows - 1):
            for x in range(num_cols - 1):
                self.screen.addstr(y, x, ' ', curses.color_pair(1))


def full_screen_sizes():
    screen = curses.initscr()
    num_rows, num_cols = screen.getmaxyx()

    full_rows = num_rows - (2 * FULL_SCREEN_HEIGHT_PADDING)
    full_cols = num_cols - (2 * FULL_SCREEN_WIDTH_PADDING)

    return full_rows, full_cols
