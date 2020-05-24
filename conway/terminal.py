import curses

from conway import game


class TerminalView(object):

    def __init__(self, gol) -> None:
        super().__init__()
        self.gol = gol
        self.screen = None

    def run(self):
        self.screen = curses.initscr()
        self.screen.clear()
        self.screen.refresh()

        curses.start_color()
        curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_BLACK)

        curses.curs_set(0)

        try:
            self._run_game()
        except KeyboardInterrupt:
            print('Exiting')

        curses.curs_set(1)
        curses.endwin()

    def _run_game(self):
        n = len(self.gol.grid)
        while True:
            for x in range(n):
                for y in range(n):
                    self._display_glyph(x, y)
            self.screen.refresh()
            self.gol.step()
            curses.napms(100)

    def _display_glyph(self, x, y):
        z = self.gol.grid[x, y]
        if z == game.ON:
            self.screen.addstr(x, y, 'o', curses.color_pair(1))
        else:
            self.screen.addstr(x, y, ' ')
