# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'temperature_target_graph.ui'
##
## Created by: Qt User Interface Compiler version 5.15.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from canvas import MplCanvas


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1066, 644)
        self.actionSave = QAction(MainWindow)
        self.actionSave.setObjectName(u"actionSave")
        self.actionClassic = QAction(MainWindow)
        self.actionClassic.setObjectName(u"actionClassic")
        self.actionFusion = QAction(MainWindow)
        self.actionFusion.setObjectName(u"actionFusion")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayoutWidget = QWidget(self.centralwidget)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(10, 10, 181, 161))
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.serialPortsComboBox = QComboBox(self.verticalLayoutWidget)
        self.serialPortsComboBox.setObjectName(u"serialPortsComboBox")

        self.horizontalLayout.addWidget(self.serialPortsComboBox)

        self.label = QLabel(self.verticalLayoutWidget)
        self.label.setObjectName(u"label")

        self.horizontalLayout.addWidget(self.label)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.refreshButton = QPushButton(self.verticalLayoutWidget)
        self.refreshButton.setObjectName(u"refreshButton")
        self.refreshButton.setCheckable(True)

        self.verticalLayout.addWidget(self.refreshButton)

        self.connectButton = QPushButton(self.verticalLayoutWidget)
        self.connectButton.setObjectName(u"connectButton")

        self.verticalLayout.addWidget(self.connectButton)

        self.disconnectButton = QPushButton(self.verticalLayoutWidget)
        self.disconnectButton.setObjectName(u"disconnectButton")

        self.verticalLayout.addWidget(self.disconnectButton)

        self.scrollArea = QScrollArea(self.centralwidget)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setGeometry(QRect(10, 180, 181, 421))
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 179, 419))
        self.textEdit = QTextEdit(self.scrollAreaWidgetContents)
        self.textEdit.setObjectName(u"textEdit")
        self.textEdit.setEnabled(True)
        self.textEdit.setGeometry(QRect(0, 0, 181, 421))
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.splitter = QSplitter(self.centralwidget)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setGeometry(QRect(0, 0, 0, 0))
        self.splitter.setOrientation(Qt.Vertical)
        self.widget = QWidget(self.centralwidget)
        self.widget.setObjectName(u"widget")
        self.widget.setGeometry(QRect(330, 90, 120, 80))
        self.gridLayoutWidget = QWidget(self.centralwidget)
        self.gridLayoutWidget.setObjectName(u"gridLayoutWidget")
        self.gridLayoutWidget.setGeometry(QRect(200, 60, 851, 541))
        self.canvasGridLayout = QGridLayout(self.gridLayoutWidget)
        self.canvasGridLayout.setObjectName(u"canvasGridLayout")
        self.canvasGridLayout.setContentsMargins(0, 0, 0, 0)
        self.canvas = MplCanvas(self.gridLayoutWidget)
        self.canvas.setObjectName(u"canvas")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(60)
        sizePolicy.setVerticalStretch(40)
        sizePolicy.setHeightForWidth(self.canvas.sizePolicy().hasHeightForWidth())
        self.canvas.setSizePolicy(sizePolicy)

        self.canvasGridLayout.addWidget(self.canvas, 0, 0, 1, 1)

        self.layoutWidget = QWidget(self.centralwidget)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(201, 9, 851, 51))
        self.gridLayout_2 = QGridLayout(self.layoutWidget)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.label_8 = QLabel(self.layoutWidget)
        self.label_8.setObjectName(u"label_8")
        font = QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_8.setFont(font)
        self.label_8.setAlignment(Qt.AlignCenter)

        self.gridLayout_2.addWidget(self.label_8, 0, 2, 1, 1)

        self.actual_time_label = QLabel(self.layoutWidget)
        self.actual_time_label.setObjectName(u"actual_time_label")
        self.actual_time_label.setFont(font)
        self.actual_time_label.setAlignment(Qt.AlignCenter)

        self.gridLayout_2.addWidget(self.actual_time_label, 1, 1, 1, 1)

        self.label_2 = QLabel(self.layoutWidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setFont(font)
        self.label_2.setAlignment(Qt.AlignCenter)

        self.gridLayout_2.addWidget(self.label_2, 0, 0, 1, 1)

        self.actual_target_label = QLabel(self.layoutWidget)
        self.actual_target_label.setObjectName(u"actual_target_label")
        self.actual_target_label.setFont(font)
        self.actual_target_label.setAlignment(Qt.AlignCenter)

        self.gridLayout_2.addWidget(self.actual_target_label, 1, 2, 1, 1)

        self.actual_temp_label = QLabel(self.layoutWidget)
        self.actual_temp_label.setObjectName(u"actual_temp_label")
        self.actual_temp_label.setFont(font)
        self.actual_temp_label.setAlignment(Qt.AlignCenter)

        self.gridLayout_2.addWidget(self.actual_temp_label, 1, 0, 1, 1)

        self.label_7 = QLabel(self.layoutWidget)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setFont(font)
        self.label_7.setAlignment(Qt.AlignCenter)

        self.gridLayout_2.addWidget(self.label_7, 0, 1, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1066, 21))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuStyle = QMenu(self.menubar)
        self.menuStyle.setObjectName(u"menuStyle")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuStyle.menuAction())
        self.menuFile.addAction(self.actionSave)
        self.menuStyle.addAction(self.actionClassic)
        self.menuStyle.addAction(self.actionFusion)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.actionSave.setText(QCoreApplication.translate("MainWindow", u"Save", None))
#if QT_CONFIG(shortcut)
        self.actionSave.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+S", None))
#endif // QT_CONFIG(shortcut)
        self.actionClassic.setText(QCoreApplication.translate("MainWindow", u"Classic", None))
        self.actionFusion.setText(QCoreApplication.translate("MainWindow", u"Fusion", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Serial Port", None))
#if QT_CONFIG(tooltip)
        self.refreshButton.setToolTip(QCoreApplication.translate("MainWindow", u"Refresh serial port list.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(statustip)
        self.refreshButton.setStatusTip(QCoreApplication.translate("MainWindow", u"Refresh serial port list.", None))
#endif // QT_CONFIG(statustip)
        self.refreshButton.setText(QCoreApplication.translate("MainWindow", u"Refresh", None))
#if QT_CONFIG(tooltip)
        self.connectButton.setToolTip(QCoreApplication.translate("MainWindow", u"Connect to selected serial port.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(statustip)
        self.connectButton.setStatusTip(QCoreApplication.translate("MainWindow", u"Connect to selected serial port.", None))
#endif // QT_CONFIG(statustip)
        self.connectButton.setText(QCoreApplication.translate("MainWindow", u"Connect", None))
#if QT_CONFIG(tooltip)
        self.disconnectButton.setToolTip(QCoreApplication.translate("MainWindow", u"Disconnect the serial port.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(statustip)
        self.disconnectButton.setStatusTip(QCoreApplication.translate("MainWindow", u"Disconnect the serial port.", None))
#endif // QT_CONFIG(statustip)
        self.disconnectButton.setText(QCoreApplication.translate("MainWindow", u"Disconnect", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"Target Temperature [C]", None))
        self.actual_time_label.setText("")
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Temperature [C]", None))
        self.actual_target_label.setText("")
        self.actual_temp_label.setText("")
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"Time [s]", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.menuStyle.setTitle(QCoreApplication.translate("MainWindow", u"Style", None))
    # retranslateUi

