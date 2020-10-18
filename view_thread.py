from qtpy.QtCore import QRunnable, Slot
import re


class ViewWorker(QRunnable):
    """View Worker thread"""
    def __init__(self, serial_rx_queue, fig, line1, *args, **kwargs):
        super(ViewWorker, self).__init__()
        self.args = args
        self.kwargs = kwargs
        self.serialQueue = serial_rx_queue
        self.fi = fig
        self.lin = line1

    @Slot()
    def run(self):
        print("Init View Worker Thread")
        residual_string = ""
        time_ls = []
        temp_ls = []
        target_ls = []
        duty_cycle_ls = []

        while True:
            if not self.serialQueue.empty():
                try:
                    residual_string = residual_string + self.serialQueue.get(block=False)
                    # print(residual_string) #debug
                except BlockingIOError:
                    pass
            if residual_string:
                res_split = residual_string.splitlines()
                if res_split:
                    # print(res_split) #debug
                    matcher_str = "^[0-9]*.?[0-9]*,[0-9]*.?[0-9]*,[0-9]*.?[0-9]*,[0-9]*.?[0-9]*"
                    while res_split:
                        element = res_split.pop(0)
                        if re.match(matcher_str, element):
                            [time, temp, target, duty_cycle] = element.split(",")
                            time_ls.append(float(time) + 1)
                            temp_ls.append(float(temp))
                            self.lin.set_ydata(temp_ls)
                            self.lin.set_xdata(time_ls)
                            min_x = min(self.lin.get_xdata())
                            max_x = max(self.lin.get_xdata())
                            min_y = min(self.lin.get_ydata())
                            max_y = max(self.lin.get_ydata())
                            if min_x == max_x:
                                max_x = max_x + 1
                            if min_y == max_y:
                                max_y = max_y + 1
                            self.lin.axes.set_xlim(min_x, max_x)
                            self.lin.axes.set_ylim(min_y, max_y)
                            self.fi.canvas.draw()
                            self.fi.canvas.flush_events()
                        else:
                            ''' Catch the residual part of the string and the 
                                next part of the string will be attached to it. '''
                            residual_string = element
