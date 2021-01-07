from qtpy.QtCore import QRunnable, Slot, QFile, QIODevice, QTextStream
import re


class ViewWorker(QRunnable):
    """View Worker thread"""
    def __init__(self, serial_rx_queue, canvas, signal, actual_temp_label, actual_time_label, actual_target_label, text_field, *args, **kwargs):
        super(ViewWorker, self).__init__()
        self.args = args
        self.kwargs = kwargs
        self.serialQueue = serial_rx_queue
        self.canvas = canvas
        self.signal = signal
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
                        matcher_str = "^[0-9]+.?[0-9]*[eE]?[+]?[0-9]*,[0-9]+.?[0-9]*,[0-9]+.?[0-9]*,[0-9]+.?[0-9]*"
                        if re.match(matcher_str, element):
                            [time, temp, target, duty_cycle] = element.split(",")
                            time_sec = float(time) / 1000
                            """ This check is added to make the graph more robust to wrongly formed strings.        ###
                            ### As an example the first value could be truncated, also if it is a number.           ### 
                            ### It's not comprehensive of all the checks possible, but for our scopes this will do. """
                            if (time_sec > 0) and ((not time_ls) or (time_sec > time_ls[-1])):
                                temp_c = float(temp)
                                target_c = float(target)
                                time_ls.append(time_sec)
                                temp_ls.append(temp_c)
                                target_ls.append(target_c)
                                self.time_label.setText(format(time_sec, '.1f'))
                                self.temp_label.setText(format(temp_c, '.2f'))  # Set the label with a float with 2 decimals
                                self.target_label.setText(format(target_c, '.2f'))
                                self.canvas.update_plot(time_ls, temp_ls, time_ls, target_ls, self.signal)
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


if __name__ == "__main__":
    pass
