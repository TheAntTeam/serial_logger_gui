from qtpy.QtCore import QRunnable, Slot, QFile, QIODevice, QTextStream
import re


class ViewWorker(QRunnable):
    """View Worker thread"""
    def __init__(self, serial_rx_queue, fig, line_temp, line_target, actual_temp_label, actual_time_label, actual_target_label, text_field, *args, **kwargs):
        super(ViewWorker, self).__init__()
        self.args = args
        self.kwargs = kwargs
        self.serialQueue = serial_rx_queue
        self.fi = fig
        self.lin = line_temp
        self.lin_target = line_target
        self.temp_label = actual_temp_label
        self.time_label = actual_time_label
        self.target_label = actual_target_label
        self.save_file = False
        self.save_filename = ""
        self.text_out = text_field  # Gui text field where events are logged

    def save_csv_file(self, file_name):
        """Save csv file."""
        self.save_filename = file_name
        self.save_file = True

    @Slot()
    def run(self):
        # print("Init View Worker Thread")
        # self.text_out.append("Init View Worker Thread")
        time_ls = []
        temp_ls = []
        target_ls = []
        duty_cycle_ls = []

        while True:
            if not self.serialQueue.empty():
                try:
                    element = self.serialQueue.get(block=False)
                    if element:
                        matcher_str = "^[0-9]*.?[0-9]*,[0-9]*.?[0-9]*,[0-9]*.?[0-9]*,[0-9]*.?[0-9]*"
                        if re.match(matcher_str, element):
                            [time, temp, target, duty_cycle] = element.split(",")
                            time_sec = float(time) / 1000
                            temp_c = float(temp)
                            target_c = float(target)
                            time_ls.append(time_sec)
                            temp_ls.append(temp_c)
                            target_ls.append(target_c)
                            self.lin.set_xdata(time_ls)
                            self.lin.set_ydata(temp_ls)
                            self.lin_target.set_xdata(time_ls)
                            self.lin_target.set_ydata(target_ls)
                            self.time_label.setText(format(time_sec, '.1f'))
                            self.temp_label.setText(format(temp_c, '.2f'))  # Set the label with a float with 2 decimals
                            self.target_label.setText(format(target_c, '.2f'))
                            min_x = min(self.lin.get_xdata())
                            max_x = max(self.lin.get_xdata())
                            min_y = min(min(self.lin.get_ydata()), min(self.lin_target.get_ydata()))
                            max_y = max(max(self.lin.get_ydata()), max(self.lin_target.get_ydata()))
                            min_y = (abs(min_y) / min_y - 0.05) * abs(min_y)
                            max_y = (abs(max_y) / max_y + 0.05) * abs(max_y)
                            if min_x == max_x:
                                max_x = max_x + 1
                            if min_y == max_y:
                                max_y = max_y + 1
                            self.lin.axes.set_xlim(min_x, max_x)
                            self.lin.axes.set_ylim(min_y, max_y)
                            self.fi.canvas.draw()
                            self.fi.canvas.flush_events()
                except BlockingIOError:
                    pass

            if self.save_file:
                f = QFile(self.save_filename)
                try:
                    f.open(QIODevice.WriteOnly)
                    if time_ls:
                        for i in range(0, len(time_ls)):
                            QTextStream(f) << '{0}, {1}, {2}\n'.format(time_ls[i], temp_ls[i], target_ls[i])
                    f.close()
                except FileNotFoundError:
                    # print("File not found or not accessible")
                    self.text_out.append("File not found or not accessible")
                self.save_file = False
