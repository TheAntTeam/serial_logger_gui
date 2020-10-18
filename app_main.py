import sys
# from PyQt5 import QtWidgets, uic
import matplotlib.pyplot as plt

import os
# Choose 'pyqt5' or 'pyside2'
os.environ['QT_API'] = 'pyside2'
# Imports from pyside2 #
from qtpy import QtGui, QtWidgets, QtCore, uic
from qtpy.QtCore import QThreadPool, QTimer
from queue import Queue

# Custom imports #
from serial_thread import SerialWorker
from view_thread import ViewWorker


class MainWindow(QtWidgets.QMainWindow):
    serialRxQu = Queue()                   # serial FIFO RX Queue
    serialWo = SerialWorker(serialRxQu)    # serial Worker Thread

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Momentarily choose to load the ui from file for flexibility during
        # development, eventually it could be converted in a .py if stable.
        uic.loadUi("test_serial.ui", self)
        self.refreshButton.clicked.connect(self.handle_refresh_button)
        self.connectButton.clicked.connect(self.handle_connect_button)
        self.disconnectButton.clicked.connect(self.handle_disconnect_button)

        # Temporarily create the figure here and pass it to the view thread.
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.autoscale()
        line1,  = ax.plot([], [])
        fig.show()

        # Visualization Worker Thread, started as soon as
        # the thread pool is started.
        self.viewWo = ViewWorker(self.serialRxQu, fig, line1)

        self.threadpool = QThreadPool()
        self.threadpool.start(self.viewWo)

    def handle_refresh_button(self):
        """Get list of serial ports available."""
        ls = self.serialWo.get_port_list()
        if ls:
            print(ls)
            self.serialPortsComboBox.clear()
            self.serialPortsComboBox.addItems(ls)
        else:
            print('No serial ports available.')
            self.serialPortsComboBox.clear()

    def handle_connect_button(self):
        """Connect button opens the selected serial port and
           creates the serial worker thread. If the thread was
           already created previously and paused, it revives it."""
        print(self.serialPortsComboBox.currentText())
        self.serialWo.open_port(self.serialPortsComboBox.currentText())
        if self.serialWo.no_serial_worker:
            self.serialWo.revive_it()
            self.threadpool.start(self.serialWo)
            self.serialWo.thread_is_started()
        if self.serialWo.is_paused:
            self.serialWo.revive_it()

    def handle_disconnect_button(self):
        """Disconnect button closes the serial port."""
        self.serialWo.close_port()

    # Debug function
    # def text_changed(self):
    #     print("Text changed:")
    #     print(self.serialPortsComboBox.currentText())
    #     self.serialWo.set_actual_port(self.serialPortsComboBox.currentText())


app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()
