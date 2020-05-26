import argparse
from functools import update_wrapper

from conway import (game, terminal)


def parse_arguments():
    parser = argparse.ArgumentParser()

    # Game Settings
    parser.add_argument('--cols', '-c', dest='width', action='store')
    parser.add_argument('--rows', '-r', dest='height', action='store')
    parser.add_argument('--fullscreen', '-f', dest='fullscreen', action='store_true')
    parser.add_argument('--percent-alive', '-a', dest='percent_alive', action='store')

    # Terminal Settings
    parser.add_argument('--interval', '-i', dest='update_interval', action='store',
                        help='Interval in ms between steps')

    return parser.parse_args()


if __name__ == '__main__':

    args = parse_arguments()

    # Initialize the game
    width = args.width or 78
    height = args.height or 40
    percent_alive = args.percent_alive or .2

    if args.fullscreen:
        height, width = terminal.full_screen_sizes()

    grid = game.random_grid(int(width), int(height), float(percent_alive))
    gol = game.GameOfLife(grid)

    # Initialize the view
    interval = args.update_interval or 500
    view = terminal.TerminalView(gol, update_interval=int(interval))

    # Start the simulation
    view.run()
