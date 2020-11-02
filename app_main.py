import sys
import os
# Choose 'pyqt5' or 'pyside2'
os.environ['QT_API'] = 'pyside2'
# Imports from qtpy #
from qtpy import QtWidgets, uic
from qtpy.QtCore import QThreadPool, QFile, QIODevice, QTextStream
from queue import Queue
from qtpy.QtWidgets import QMainWindow
# Custom imports #
from serial_thread import SerialWorker
from view_thread import ViewWorker


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        # Momentarily choose to load the ui from file for flexibility during
        # development, eventually it could be converted in a .py if stable.
        uic.loadUi("temperature_target_graph.ui", self)


class MainWindow(QMainWindow, Ui_MainWindow):
    serialRxQu = Queue()                   # serial FIFO RX Queue
    serialWo = ""

    def __init__(self, *args, **kwargs):
        Ui_MainWindow.__init__(self)
        QMainWindow.__init__(self)

        # Initialize UI
        self.setupUi(self)
        self.refreshButton.clicked.connect(self.handle_refresh_button)
        self.connectButton.clicked.connect(self.handle_connect_button)
        self.disconnectButton.clicked.connect(self.handle_disconnect_button)
        self.actionSave.triggered.connect(self.save_file)

        axes = self.canvas.figure.add_subplot(1, 1, 1)
        line_temp,   = axes.plot([], [], 'r')
        line_target, = axes.plot([], [], 'b')

        # Visualization Worker Thread, started as soon as the thread pool is started. Pass the figure to plot on.
        self.viewWo = ViewWorker(self.serialRxQu, self.canvas.figure, line_temp, line_target,
                                 self.actual_temp_label,
                                 self.actual_time_label,
                                 self.actual_target_label,
                                 self.textEdit)
        # serial Worker Thread
        self.serialWo = SerialWorker(self.serialRxQu, self.textEdit)

        self.threadpool = QThreadPool()
        self.threadpool.start(self.viewWo)

    def handle_refresh_button(self):
        """Get list of serial ports available."""
        ls = self.serialWo.get_port_list()
        if ls:
            #print(ls)
            self.textEdit.append("Listing serial ports: ")
            self.textEdit.append(str(ls))
            self.serialPortsComboBox.clear()
            self.serialPortsComboBox.addItems(ls)
        else:
            # print('No serial ports available.')
            self.textEdit.append('No serial ports available.')
            self.serialPortsComboBox.clear()

    def handle_connect_button(self):
        """Connect button opens the selected serial port and
           creates the serial worker thread. If the thread was
           already created previously and paused, it revives it."""
        # print(self.serialPortsComboBox.currentText())
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

    def save_file(self):
        save_file_path = QtWidgets.QFileDialog.getSaveFileName(self, self.tr("Load Image"),
                                                                     self.tr("~/Desktop/"),
                                                                     self.tr("CSV (*.csv)"))
        # print(save_file_path)
        self.textEdit.append("Saving file: ")
        self.textEdit.append(save_file_path[0])
        if save_file_path[0] != "":
            self.viewWo.save_csv_file(save_file_path[0])


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()
