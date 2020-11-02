from qtpy.QtCore import QRunnable, Slot

# Custom imports #
from serial_channel import SerialChannel


class SerialWorker(QRunnable):
    """Serial Worker thread"""
    serial_ch = SerialChannel()

    def __init__(self, serial_rx_queue, text_field, *args, **kwargs):
        super(SerialWorker, self).__init__()
        self.args = args                    # Unused at the moment
        self.kwargs = kwargs                # Unused at the moment
        self.is_paused = True               # Running status of the thread
        self.no_serial_worker = True        # It checks that thread is created once
        self.close_it = False               # It is used to demand closure to runner
        self.serialQueue = serial_rx_queue  # FIFO RX Queue to pass data to view thread
        self.text_out = text_field

    def get_port_list(self):
        """Return serial port list."""
        return self.serial_ch.get_available_ports()

    def open_port(self, port):
        """Open passed serial port."""
        # print("Open " + port)
        self.text_out.append("Opening " + port)
        try:
            self.serial_ch.open(port)
        except IOError:
            # print("COM port already in use.")
            self.text_out.append("COM port already in use.")

    def close_port(self):
        """Pause the thread from reading the serial port and close it.
           The closing of the serial port is demanded to the runner
           function to avoid side effects."""
        # print("Close " + self.serial_ch.active_port.name)
        self.text_out.append("Closing " + self.serial_ch.active_port.name)
        self.is_paused = True
        self.close_it = True

    @Slot()
    def run(self):
        """Serial Worker Runner function."""
        # print("Init Serial Worker Thread")
        # self.text_out.append("Init Serial Worker Thread")
        residual_string = ""
        while True:
            if self.is_paused:
                if self.close_it:
                    self.serial_ch.close()
                    self.close_it = False
                    residual_string = ""
            else:
                if self.serial_ch.active_port_is_open():
                    bytes_to_read = self.serial_ch.active_port.in_waiting  # Checking data byte size
                    if bytes_to_read:
                        data_out = self.serial_ch.active_port.read(bytes_to_read)
                        if data_out:
                            # print("data in: ")
                            # print(data_out.decode("utf-8", "ignore"))
                            residual_string = residual_string + data_out.decode("utf-8", "ignore")
                            # print("Residual string: ")
                            # print(residual_string)
                            res_split = residual_string.splitlines(True)
                            # print("Res split: ")
                            # print(res_split)
                            residual_string = ""
                            while res_split:
                                element = res_split.pop(0)
                                if '\n' in element:
                                    self.serialQueue.put(element)
                                else:
                                    residual_string = element
                            # print("Final residual string: ")
                            # print(residual_string)

    def thread_is_started(self):
        """This function is to ensure to create the serial
           worker thread just one time."""
        self.no_serial_worker = False

    def pause_it(self):
        """Pause thread from reading from serial port."""
        self.is_paused = True

    def revive_it(self):
        """Restart the thread reading from serial port."""
        self.is_paused = False
