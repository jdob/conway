from conway import (game, plot, terminal)


if __name__ == '__main__':
    gol = game.random_grid(40)
    # view = plot.PlotView(gol)

    view = terminal.TerminalView(gol)
    view.run()
