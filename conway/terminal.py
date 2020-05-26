import curses

from conway import game

FULL_SCREEN_WIDTH_PADDING = 4
FULL_SCREEN_HEIGHT_PADDING = 4


class TerminalView(object):

    def __init__(self, gol, update_interval=500,
                 alive_glyph=None, new_glyph=None,
                 dead_glyph=None, killed_glyph=None) -> None:
        super().__init__()
        self.gol = gol
        self.update_interval = update_interval

        self._screen = None
        self._x_offset = 0
        self._y_offset = 0

        self._alive_glyph = alive_glyph or '●'
        self._new_gyph = new_glyph or '●'
        self._dead_glyph = dead_glyph or ' '
        self._killed_glyph = killed_glyph or ' '

    def run(self):
        self._screen = curses.initscr()
        self._screen.clear()
        self._screen.refresh()

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
        except KeyboardInterrupt:
            pass

        curses.curs_set(1)
        curses.endwin()

    def _run_game(self):
        while True:
            for y in range(self.gol.height):
                for x in range(self.gol.width):
                    self._display_glyph(x, y)
            self.gol.step()
            self._display_status()
            self._screen.refresh()
            curses.napms(self.update_interval)

    def _display_glyph(self, x, y):
        z = self.gol.value(x, y)

        if z == game.ALIVE:
            glyph = self._alive_glyph
            color = curses.color_pair(1) | curses.A_BOLD
        elif z == game.NEW:
            glyph = self._new_gyph
            color = curses.color_pair(1) | curses.A_BOLD
        elif z == game.KILLED:
            glyph = self._killed_glyph
            color = curses.color_pair(2)
        else:
            glyph = self._dead_glyph
            color = curses.color_pair(1)

        self._screen.addstr(y + self._y_offset, x + self._x_offset,
                            glyph, color)

    def _display_status(self):
        status = 'Generation: %d   Alive: %d   Total Created: %d   Total Killed: %d' % \
                 (self.gol.step_count, self.gol.alive_count, self.gol.created_count, self.gol.killed_count)

        s_gen = 'Generation: %d  ' % self.gol.step_count
        s_alive = 'Alive: %d  ' % self.gol.alive_count
        s_created = 'Created: %d  ' % self.gol.created_count
        s_killed = 'Killed: %d  ' % self.gol.killed_count

        all_lines = ['']
        for i in [s_gen, s_alive, s_created, s_killed]:
            if (len(i) + len(all_lines[-1:][0])) <= self.gol.width:
                add_to_me = all_lines.pop(-1) + i
                all_lines.append(add_to_me)
            else:
                all_lines.append(i)

        for n, i in enumerate(all_lines):
            self._screen.addstr((self.gol.height + self._y_offset + n + 1), self._x_offset, i)

    def _calculate_offsets(self):
        num_rows, num_cols = self._screen.getmaxyx()

        self._x_offset = int((num_cols - self.gol.width) / 2) - 1
        self._y_offset = int((num_rows - self.gol.height) / 2) - 1

    def _flush_terminal(self):
        """Fill the terminal with empty spaces to initialize the canvas"""
        num_rows, num_cols = self._screen.getmaxyx()
        for y in range(num_rows - 1):
            for x in range(num_cols - 1):
                self._screen.addstr(y, x, ' ', curses.color_pair(1))


def full_screen_sizes():
    screen = curses.initscr()
    num_rows, num_cols = screen.getmaxyx()

    full_rows = num_rows - (2 * FULL_SCREEN_HEIGHT_PADDING)
    full_cols = num_cols - (2 * FULL_SCREEN_WIDTH_PADDING)

    return full_rows, full_cols
