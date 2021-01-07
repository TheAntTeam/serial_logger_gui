from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import pyqtgraph as pg


class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None):
        #self.setParent(parent) #optional
        fig = Figure(figsize=(5, 5))
        super(MplCanvas, self).__init__(fig)
        self.axes = self.figure.add_subplot(1, 1, 1)
        self.line_temp,   = self.axes.plot([], [], 'r')
        self.line_target, = self.axes.plot([], [], 'b')

    def connect_signal(self, signal):
        pass #not used in Matplot lib canvas at the moment.

    def plot_data(self, x1, y1, x2, y2):
        self.line_temp.set_xdata(x1)
        self.line_temp.set_ydata(y1)
        self.line_target.set_xdata(x2)
        self.line_target.set_ydata(y2)
        min_x = min(self.line_temp.get_xdata())
        max_x = max(self.line_temp.get_xdata())
        min_y = min(min(self.line_temp.get_ydata()), min(self.line_target.get_ydata()))
        max_y = max(max(self.line_temp.get_ydata()), max(self.line_target.get_ydata()))
        min_y = (abs(min_y) / min_y - 0.05) * abs(min_y)
        max_y = (abs(max_y) / max_y + 0.05) * abs(max_y)
        if min_x == max_x:
            max_x = max_x + 1
        if min_y == max_y:
            max_y = max_y + 1
        self.line_temp.axes.set_xlim(min_x, max_x)
        self.line_temp.axes.set_ylim(min_y, max_y)
        self.draw()
        self.flush_events()

    def update_plot(self, x1, y1, x2, y2, signal):
        self.plot_data(x1, y1, x2, y2)


class PyQtGraphCanvas(pg.GraphicsWindow):
    def __init__(self, parent=None, **kargs):
        pg.GraphicsWindow.__init__(self, **kargs)
        # pg.setConfigOptions(useOpenGL=True) #This doesn't seem to change anything
        self.setParent(parent)
        self.pl = self.addPlot()
        self.line_temp = self.pl.plot([], [], pen=pg.mkPen(color='r', width=1))
        self.line_target = self.pl.plot([], [], pen=pg.mkPen(color='b', width=1))
        self.pl.showGrid(x=True, y=True)
        self.pl.disableAutoRange()
        self.x_min = float("inf")
        self.x_max = float("-inf")
        self.y_min = -1
        self.y_max = 300
        self.pl.setXRange(0, 1, padding=0, update=False)
        self.pl.setYRange(self.y_min, self.y_max, padding=0, update=False)

    def connect_signal(self, signal):
        signal.connect(lambda x1, y1, x2, y2: self.plot_data(x1, y1, x2, y2))

    def plot_data(self, x1, y1, x2, y2):
        # self.pl.plot(x1, y1) #direct update, freezes window
        # self.pl.plot(x2, y2) #direct update, freezes window
        min_x = min(min(x1), min(x2))
        max_x = max(max(x1), max(x2))
        if self.x_min > min_x or self.x_max < max_x:
            if self.x_min > min_x:
                self.x_min = min_x
            if self.x_max < max_x:
                max_x = max_x + 10.0
                self.x_max = max_x
            # if min_x == max_x:
            #     max_x = max_x + 1
            self.pl.setXRange(self.x_min, self.x_max, padding=0)#, update=False)

        min_y = min(min(y1), min(y2))
        max_y = max(max(y1), max(y2))
        print(x2[-1])
        print(y2[-1])
        if self.y_min > min_y or self.y_max < max_y:
            if self.y_min > min_y:
                if min_y != 0:
                    min_y = (abs(min_y) / min_y - 0.05) * abs(min_y)
                self.y_min = min_y
            if self.y_max < max_y:
                max_y = (abs(max_y) / max_y + 0.05) * abs(max_y)
                self.y_max = max_y
            self.pl.setYRange(self.y_min, self.y_max, padding=0)#, update=False)

        self.line_temp.setData(x1, y1)
        self.line_target.setData(x2, y2)

    def update_plot(self, x1, y1, x2, y2, signal):
        signal.emit(x1, y1, x2, y2)
        # self.plot_data(x1, y1, x2, y2) #direct update, freezes window


if __name__ == "__main__":
    pass
