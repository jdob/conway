from conway import (game, terminal)


if __name__ == '__main__':
    rows, cols = terminal.full_screen_sizes()
    gol = game.random_grid(cols, rows)
    view = terminal.TerminalView(gol)
    view.run()
