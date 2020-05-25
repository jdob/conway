from conway import (game, terminal)


if __name__ == '__main__':
    gol = game.random_grid(40)
    view = terminal.TerminalView(gol)
    view.run()
