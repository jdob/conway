import curses

from conway import game


class TerminalView(object):

    def __init__(self, gol) -> None:
        super().__init__()
        self.gol = gol
        self.screen = None
        self.x_offset = 0
        self.y_offset = 0

    def run(self):
        self.screen = curses.initscr()
        self.screen.clear()
        self.screen.refresh()

        # Color setup
        curses.start_color()
        curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_BLACK)

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
            self.screen.refresh()
            self.gol.step()
            curses.napms(100)

    def _display_glyph(self, x, y):
        z = self.gol.grid[y, x]
        if z == game.ON:
            self.screen.addstr(y + self.y_offset, x + self.x_offset,
                               'o', curses.color_pair(1) | curses.A_BOLD)
        else:
            self.screen.addstr(y + self.y_offset, x + self.x_offset,
                               ' ')

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
