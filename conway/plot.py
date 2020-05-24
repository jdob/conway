from matplotlib import (animation, pyplot)


class PlotView(object):

    def __init__(self, gol, update_interval=50) -> None:
        super().__init__()
        self.gol = gol

        self.update_interval = update_interval

    def run(self):
        fig, ax = pyplot.subplots()
        img = ax.imshow(self.gol.grid, interpolation='nearest')

        def update_wrapper(frame_num):
            self.gol.step()
            img.set_data(self.gol.grid)

        ani = animation.FuncAnimation(fig, update_wrapper,
                                      frames=10,
                                      interval=self.update_interval,
                                      save_count=50)
        pyplot.show()
