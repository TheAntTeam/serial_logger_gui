import sys
import common_environ_set  # This is where I stored the environment variable selecting pyside2
from qtpy import QtWidgets, uic
from qtpy.QtCore import QThreadPool, Signal
from queue import Queue
from qtpy.QtWidgets import QMainWindow, QActionGroup
""" Custom imports """
from serial_thread import SerialWorker
from view_thread import ViewWorker
from style_manager import StyleManager
from temperature_target_graph import Ui_MainWindow


""" The Following class is just used to load the UI instead of using the generated Ui_MainWindow.  *** 
*** If you want to use it uncomment it. You don't need to comment the import of the UI_MainWindow. """
# class Ui_MainWindow(object):
#     def setupUi(self, MainWindow):
#         uic.loadUi("temperature_target_graph.ui", self)


class MainWindow(QMainWindow, Ui_MainWindow):
    serialRxQu = Queue()                   # serial FIFO RX Queue
    serialWo = ""
    signal = Signal(object, object, object, object)
    termination_signal = False

    def __init__(self, *args, **kwargs):
        Ui_MainWindow.__init__(self)
        QMainWindow.__init__(self)

        # Initialize UI
        self.setupUi(self)
        self.refreshButton.clicked.connect(self.handle_refresh_button)
        self.connectButton.clicked.connect(self.handle_connect_button)
        self.disconnectButton.clicked.connect(self.handle_disconnect_button)
        self.actionSave.triggered.connect(self.save_file)
        self.style_group = QActionGroup(self)
        self.palette_group = QActionGroup(self)
        self.palette_group.setExclusive(False)
        style_man.add_styles_to_menu(self, self.menuStyle, self.style_group, self.palette_group)
        self.style_group.triggered.connect(self.select_style)
        self.palette_group.triggered.connect(self.select_palette)

        # self.signal.connect(lambda x1, y1, x2, y2: self.canvas.plot_data(x1, y1, x2, y2))
        self.canvas.connect_signal(self.signal)

        # Visualization Worker Thread, started as soon as the thread pool is started. Pass the figure to plot on.
        self.viewWo = ViewWorker(self.serialRxQu,
                                 self.canvas,
                                 self.signal,
                                 self.actual_temp_label,
                                 self.actual_time_label,
                                 self.actual_target_label,
                                 self.textEdit)
        # serial Worker Thread
        self.serialWo = SerialWorker(self.serialRxQu, self.textEdit)

        self.threadpool = QThreadPool()
        self.threadpool.start(self.viewWo)

    def set_finish_signal(self):
        self.viewWo.terminate_thread()
        self.serialWo.terminate_thread()

    def closeEvent(self, event):
        self.set_finish_signal()
        app.exit(0)

    def handle_refresh_button(self):
        """Get list of serial ports available."""
        ls = self.serialWo.get_port_list()
        if ls:
            # print(ls)
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
        if self.serialWo.open_port(self.serialPortsComboBox.currentText()):
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
        save_file_path = QtWidgets.QFileDialog.getSaveFileName(self, self.tr("Save Values in a Comma Separated Value file"),
                                                                     self.tr("."),
                                                                     self.tr("CSV (*.csv)"))
        # print(save_file_path)
        self.textEdit.append("Saving file: ")
        self.textEdit.append(save_file_path[0])
        if save_file_path[0] != "":
            self.viewWo.save_csv_file(save_file_path[0])

    def select_style(self):
        style_man.change_style(self.style_group.checkedAction().text())

    def select_palette(self):
        style_man.set_palette()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    style_man = StyleManager(app)
    window = MainWindow()
    style_man.set_default_style()
    style_man.set_default_palette()
    window.show()
    sys.exit(app.exec_())
