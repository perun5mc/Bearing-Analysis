from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QComboBox, QMainWindow, QFileDialog, QMessageBox

import pyqtgraph as pg
from pyqtgraph.console import ConsoleWidget
from pyqtgraph.dockarea.Dock import Dock
from pyqtgraph.dockarea.DockArea import DockArea
from pyqtgraph.Qt import QtWidgets

import os
import shutil
import json

from scripts.fft_acc_z import generate_fft_plot as generate_acc
from scripts.fft_vel_z import generate_fft_plot as generate_vel
from scripts.fft_env_acc_z import generate_fft_plot as generate_env_acc
from scripts.fft_env_vel_z import generate_fft_plot as generate_env_vel
from scripts.createGraph import createGraph

from scripts.acc_z_spec import generate_spec_plot as generate_acc_spec
from scripts.vel_z_spec import generate_spec_plot as generate_vel_spec
from scripts.env_acc_z_spec import generate_spec_plot as generate_env_acc_spec
from scripts.env_vel_z_spec import generate_spec_plot as generate_env_vel_spec
from scripts.createHeatmap import createHeatmap


# customowa klasa pozwalająca na to, aby dropdown lista miała checkboxy (znalazłem to na internecie, trochę pozmieniałem)
class CheckableComboBox(QComboBox):
    sig = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self._changed = False
        self.view().pressed.connect(self.handleItemPressed)
        self.currentIndexChanged.connect(self.onChange) # wywołuje się przy kliknięciu dolnego elementu listy

    def setItemChecked(self, index, checked=False):
        item = self.model().item(index, self.modelColumn())
        if index != 0:
            if checked:
                item.setCheckState(Qt.Checked)
            else:
                item.setCheckState(Qt.Unchecked)
        else:
            self.view().setRowHidden(0, True) # pierwszy row jest zawsze ukryty

    def handleItemPressed(self, index):
        item = self.model().itemFromIndex(index)
        if item.checkState() == Qt.Checked:
            item.setCheckState(Qt.Unchecked)
        else:
            item.setCheckState(Qt.Checked)
        self._changed = True

    def hidePopup(self):
        if not self._changed:
            super().hidePopup()
            self.sig.emit("hide")
        self.setCurrentIndex(0)
        self._changed = False

    def itemChecked(self, index):
        item = self.model().item(index, self.modelColumn())
        return item.checkState() == Qt.Checked

    def onChange(self):
        self.setCurrentIndex(0) # sprawia, że text dropdown listy zawsze jest ustawiony na wartość pierwszego elementu 

# klasa z oknem Options utworzona w pełni przez QtDesigner
class Ui_Options(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(250, 200)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QtCore.QSize(250, 200))
        MainWindow.setMaximumSize(QtCore.QSize(250, 200))
        MainWindow.setStyleSheet("background: #140546;")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.lbl_speed = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Nirmala UI")
        font.setPointSize(12)
        self.lbl_speed.setFont(font)
        self.lbl_speed.setStyleSheet("color: white;")
        self.lbl_speed.setObjectName("lbl_speed")
        self.horizontalLayout_4.addWidget(self.lbl_speed)
        self.inp_speed = QtWidgets.QSpinBox(self.centralwidget)
        self.inp_speed.setMinimumSize(QtCore.QSize(100, 0))
        self.inp_speed.setMaximumSize(QtCore.QSize(500000, 50))
        font = QtGui.QFont()
        font.setFamily("Nirmala UI")
        font.setPointSize(12)
        self.inp_speed.setFont(font)
        self.inp_speed.setStyleSheet("QSpinBox {\n"
                                     "    color: white;\n"
                                     "    padding: 5px;\n"
                                     "    border-radius: 10px;\n"
                                     "    background-color: #240388;\n"
                                     "}\n"
                                     "QMenu::item:enabled {"
                                     "color: white;"
                                     "}"
                                     "QMenu::item:enabled:selected {"
                                     "color: cornflowerblue;"
                                     "}"
                                     "")
        self.inp_speed.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.inp_speed.setMinimum(0)
        self.inp_speed.setMaximum(999999)
        self.inp_speed.setProperty("value", 60)
        self.inp_speed.setObjectName("inp_speed")
        self.horizontalLayout_4.addWidget(self.inp_speed)
        self.horizontalLayout_4.setStretch(1, 2)
        self.horizontalLayout_2.addLayout(self.horizontalLayout_4)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.lbl_harmonics = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Nirmala UI")
        font.setPointSize(12)
        self.lbl_harmonics.setFont(font)
        self.lbl_harmonics.setStyleSheet("color: white;")
        self.lbl_harmonics.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.lbl_harmonics.setObjectName("lbl_harmonics")
        self.horizontalLayout_3.addWidget(self.lbl_harmonics)
        self.inp_harmonics = QtWidgets.QSpinBox(self.centralwidget)
        self.inp_harmonics.setMinimumSize(QtCore.QSize(100, 0))
        self.inp_harmonics.setMaximumSize(QtCore.QSize(50000, 50))
        font = QtGui.QFont()
        font.setFamily("Nirmala UI")
        font.setPointSize(12)
        self.inp_harmonics.setFont(font)
        self.inp_harmonics.setStyleSheet("QSpinBox {\n"
                                         "    color: white;\n"
                                         "    padding: 5px;\n"
                                         "    border-radius: 10px;\n"
                                         "    background-color: #240388;\n"
                                         "}\n"
                                         "QMenu::item:enabled {"
                                         "color: white;"
                                         "}"
                                         "QMenu::item:enabled:selected {"
                                         "color: cornflowerblue;"
                                         "}"
                                         "")
        self.inp_harmonics.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.inp_harmonics.setSpecialValueText("")
        self.inp_harmonics.setMaximum(99999)
        self.inp_harmonics.setObjectName("inp_harmonics")
        self.horizontalLayout_3.addWidget(self.inp_harmonics)
        self.horizontalLayout_3.setStretch(1, 2)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.drop_modes = CheckableComboBox()
        self.drop_modes.setMinimumSize(QtCore.QSize(120, 25))
        self.drop_modes.setMaximumSize(QtCore.QSize(50000, 25))
        font = QtGui.QFont()
        font.setFamily("Nirmala UI")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        font.setKerning(True)
        self.drop_modes.setFont(font)
        self.drop_modes.setStyleSheet("QComboBox {\n"
                                      "    color: white;\n"
                                      "    padding-left: 10px;\n"
                                      "    border-radius: 10px;\n"
                                      "    background-color: #240388;\n"
                                      "}\n"
                                      "\n"
                                      "QComboBox QAbstractItemView {\n"
                                      "    selection-background-color: #240388;\n"
                                      "}\n"
                                      "\n"
                                      "QListView {\n"
                                      "    color: white;\n"
                                      "    border-radius: 0px;\n"
                                      "    padding: 5px;\n"
                                      "    font-size: 15px;\n"
                                      "}\n"
                                      "\n"
                                      "QComboBox::drop-down {\n"
                                      "    image: url(./img/arrow.png);\n"
                                      "    width: 22px;\n"
                                      "    padding-right: 5px;\n"
                                      "    height: 28px;\n"
                                      "    border-top-right-radius: 5px;\n"
                                      "    border-bottom-right-radius: 5px;\n"
                                      "}")
        self.drop_modes.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToContents)
        self.drop_modes.setObjectName("drop_modes")
        self.drop_modes.addItem("")
        self.drop_modes.addItem("")
        self.drop_modes.addItem("")
        self.drop_modes.addItem("")
        self.drop_modes.addItem("")
        self.drop_modes.addItem("")
        self.drop_modes.setItemChecked(0, False)
        self.drop_modes.setItemChecked(1, False)
        self.drop_modes.setItemChecked(2, False)
        self.drop_modes.setItemChecked(3, False)
        self.drop_modes.setItemChecked(4, False)
        self.drop_modes.setItemChecked(5, False)
        self.verticalLayout_2.addWidget(self.drop_modes)
        self.drop_bearings = CheckableComboBox()
        self.drop_bearings.setMinimumSize(QtCore.QSize(120, 25))
        self.drop_bearings.setMaximumSize(QtCore.QSize(50000, 25))
        font = QtGui.QFont()
        font.setFamily("Nirmala UI")
        font.setPointSize(12)
        self.drop_bearings.setFont(font)
        self.drop_bearings.setStyleSheet("QComboBox {\n"
                                         "    color: white;\n"
                                         "    padding-left: 10px;\n"
                                         "    border-radius: 10px;\n"
                                         "    background-color: #240388;\n"
                                         "}\n"
                                         "\n"
                                         "QComboBox QAbstractItemView {\n"
                                         "    selection-background-color: #240388;\n"
                                         "}\n"
                                         "\n"
                                         "QListView {\n"
                                         "    color: white;\n"
                                         "    border-radius: 0px;\n"
                                         "    padding: 5px;\n"
                                         "    font-size: 15px;\n"
                                         "}\n"
                                         "\n"
                                         "QComboBox::drop-down {\n"
                                         "    image: url(./img/arrow.png);\n"
                                         "    width: 22px;\n"
                                         "    padding-right: 5px;\n"
                                         "    height: 28px;\n"
                                         "    border-top-right-radius: 5px;\n"
                                         "    border-bottom-right-radius: 5px;\n"
                                         "}")
        self.drop_bearings.setEditable(False)
        self.drop_bearings.setDuplicatesEnabled(True)
        self.drop_bearings.setFrame(True)
        self.drop_bearings.setObjectName("drop_bearings")
        self.verticalLayout_2.addWidget(self.drop_bearings)
        self.checkBox = QtWidgets.QCheckBox(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Nirmala UI")
        font.setPointSize(12)
        self.checkBox.setFont(font)
        self.checkBox.setFocusPolicy(QtCore.Qt.NoFocus)
        self.checkBox.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.checkBox.setStyleSheet(":enabled {\n"
                                    "    background: none;\n"
                                    "    border-radius: 10px;\n"
                                    "    color: white;\n"
                                    "    height: 25px;\n"
                                    "    padding-left: 10px;\n"
                                    "}\n"
                                    "\n"
                                    ":hover {\n"
                                    "    background: #453083;\n"
                                    "}")
        self.checkBox.setChecked(False)
        self.checkBox.setTristate(False)
        self.checkBox.setObjectName("checkBox")
        self.verticalLayout_2.addWidget(self.checkBox)
        self.verticalLayout.addLayout(self.verticalLayout_2)
        self.horizontalLayout_5.addLayout(self.verticalLayout)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Options"))
        MainWindow.setWindowIcon(QtGui.QIcon('./img/icon.png'))
        self.lbl_speed.setText(_translate("MainWindow", "Speed (Hz): "))
        self.lbl_harmonics.setText(_translate("MainWindow", "Harmonics: "))
        self.drop_modes.setItemText(0, _translate("MainWindow", "Choose modes: "))
        self.drop_modes.setItemText(1, _translate("MainWindow", "Roller"))
        self.drop_modes.setItemText(2, _translate("MainWindow", "Inner Race"))
        self.drop_modes.setItemText(3, _translate("MainWindow", "Outer Race"))
        self.drop_modes.setItemText(4, _translate("MainWindow", "Cage"))
        self.drop_modes.setItemText(5, _translate("MainWindow", "Shaft"))
        self.checkBox.setText(_translate("MainWindow", "  To Log"))


class Ui_MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("Graphs")
        MainWindow.resize(1500, 1000)
        MainWindow.setStyleSheet("background: #474C5C;")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        MainWindow.setCentralWidget(self.centralwidget)
        self.dockWidget = QtWidgets.QDockWidget(MainWindow)
        self.dockWidget.setTitleBarWidget(QtWidgets.QWidget())
        self.dockWidget.setMinimumSize(QtCore.QSize(1194, 150))
        self.dockWidget.setMaximumSize(QtCore.QSize(524287, 150))
        self.dockWidget.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.dockWidget.setStyleSheet("background: #0C0032;\n"
                                      "padding: 5px;\n"
                                      "margin: 0px;")
        self.dockWidget.setFloating(False)
        self.dockWidget.setFeatures(QtWidgets.QDockWidget.DockWidgetFloatable | QtWidgets.QDockWidget.DockWidgetMovable)
        self.dockWidget.setWindowTitle("")
        self.dockWidget.setObjectName("dockWidget")
        self.dockWidgetContents = QtWidgets.QWidget()
        self.dockWidgetContents.setObjectName("dockWidgetContents")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.dockWidgetContents)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem = QtWidgets.QSpacerItem(92, 20, QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.btn_addFile = QtWidgets.QPushButton(self.dockWidgetContents)
        self.btn_addFile.setMinimumSize(QtCore.QSize(180, 50))
        font = QtGui.QFont()
        font.setFamily("Nirmala UI")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.btn_addFile.setFont(font)
        self.btn_addFile.setStyleSheet(":enabled {\n"
                                       "    background: none;\n"
                                       "    border-radius: 15px;\n"
                                       "    color: white;\n"
                                       "}\n"
                                       "\n"
                                       ":hover {\n"
                                       "    background: #453083;\n"
                                       "}")
        self.btn_addFile.setObjectName("btn_addFile")
        self.horizontalLayout_2.addWidget(self.btn_addFile)
        spacerItem1 = QtWidgets.QSpacerItem(80, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setSpacing(6)
        self.gridLayout.setObjectName("gridLayout")
        self.btn_vel1 = QtWidgets.QPushButton(self.dockWidgetContents)
        self.btn_vel1.setMinimumSize(QtCore.QSize(180, 50))
        self.btn_vel1.setMaximumSize(QtCore.QSize(200, 50))
        font = QtGui.QFont()
        font.setFamily("Nirmala UI")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.btn_vel1.setFont(font)
        self.btn_vel1.setStyleSheet(":enabled {\n"
                                    "    background: none;\n"
                                    "    border-radius: 15px;\n"
                                    "    color: white;\n"
                                    "}\n"
                                    "\n"
                                    ":hover {\n"
                                    "    background: #453083;\n"
                                    "}")
        self.btn_vel1.setObjectName("btn_vel1")
        self.gridLayout.addWidget(self.btn_vel1, 0, 1, 1, 1, QtCore.Qt.AlignVCenter)
        self.btn_acc2 = QtWidgets.QPushButton(self.dockWidgetContents)
        self.btn_acc2.setMinimumSize(QtCore.QSize(180, 50))
        self.btn_acc2.setMaximumSize(QtCore.QSize(200, 50))
        font = QtGui.QFont()
        font.setFamily("Nirmala UI")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.btn_acc2.setFont(font)
        self.btn_acc2.setStyleSheet(":enabled {\n"
                                    "    background: none;\n"
                                    "    border-radius: 15px;\n"
                                    "    color: white;\n"
                                    "}\n"
                                    "\n"
                                    ":hover {\n"
                                    "    background: #453083;\n"
                                    "}")
        self.btn_acc2.setObjectName("btn_acc2")
        self.gridLayout.addWidget(self.btn_acc2, 1, 0, 1, 1)
        self.btn_envAcc2 = QtWidgets.QPushButton(self.dockWidgetContents)
        self.btn_envAcc2.setMinimumSize(QtCore.QSize(180, 50))
        self.btn_envAcc2.setMaximumSize(QtCore.QSize(200, 50))
        font = QtGui.QFont()
        font.setFamily("Nirmala UI")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.btn_envAcc2.setFont(font)
        self.btn_envAcc2.setStyleSheet(":enabled {\n"
                                       "    background: none;\n"
                                       "    border-radius: 15px;\n"
                                       "    color: white;\n"
                                       "}\n"
                                       "\n"
                                       ":hover {\n"
                                       "    background: #453083;\n"
                                       "}")
        self.btn_envAcc2.setObjectName("btn_envAcc2")
        self.gridLayout.addWidget(self.btn_envAcc2, 1, 2, 1, 1)
        self.btn_acc1 = QtWidgets.QPushButton(self.dockWidgetContents)
        self.btn_acc1.setMinimumSize(QtCore.QSize(180, 50))
        self.btn_acc1.setMaximumSize(QtCore.QSize(200, 50))
        font = QtGui.QFont()
        font.setFamily("Nirmala UI")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.btn_acc1.setFont(font)
        self.btn_acc1.setStyleSheet(":enabled {\n"
                                    "    background: none;\n"
                                    "    border-radius: 15px;\n"
                                    "    color: white;\n"
                                    "}\n"
                                    "\n"
                                    ":hover {\n"
                                    "    background: #453083;\n"
                                    "}")
        self.btn_acc1.setObjectName("btn_acc1")
        self.gridLayout.addWidget(self.btn_acc1, 0, 0, 1, 1)
        self.btn_vel2 = QtWidgets.QPushButton(self.dockWidgetContents)
        self.btn_vel2.setMinimumSize(QtCore.QSize(180, 50))
        self.btn_vel2.setMaximumSize(QtCore.QSize(200, 50))
        font = QtGui.QFont()
        font.setFamily("Nirmala UI")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.btn_vel2.setFont(font)
        self.btn_vel2.setStyleSheet(":enabled {\n"
                                    "    background: none;\n"
                                    "    border-radius: 15px;\n"
                                    "    color: white;\n"
                                    "}\n"
                                    "\n"
                                    ":hover {\n"
                                    "    background: #453083;\n"
                                    "}")
        self.btn_vel2.setObjectName("btn_vel2")
        self.gridLayout.addWidget(self.btn_vel2, 1, 1, 1, 1)
        self.btn_envVel1 = QtWidgets.QPushButton(self.dockWidgetContents)
        self.btn_envVel1.setMinimumSize(QtCore.QSize(180, 50))
        self.btn_envVel1.setMaximumSize(QtCore.QSize(200, 50))
        font = QtGui.QFont()
        font.setFamily("Nirmala UI")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.btn_envVel1.setFont(font)
        self.btn_envVel1.setStyleSheet(":enabled {\n"
                                       "    background: none;\n"
                                       "    border-radius: 15px;\n"
                                       "    color: white;\n"
                                       "}\n"
                                       "\n"
                                       ":hover {\n"
                                       "    background: #453083;\n"
                                       "}")
        self.btn_envVel1.setObjectName("btn_envVel1")
        self.gridLayout.addWidget(self.btn_envVel1, 0, 3, 1, 1)
        self.btn_envAcc1 = QtWidgets.QPushButton(self.dockWidgetContents)
        self.btn_envAcc1.setMinimumSize(QtCore.QSize(180, 50))
        self.btn_envAcc1.setMaximumSize(QtCore.QSize(200, 50))
        font = QtGui.QFont()
        font.setFamily("Nirmala UI")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.btn_envAcc1.setFont(font)
        self.btn_envAcc1.setStyleSheet(":enabled {\n"
                                       "    background: none;\n"
                                       "    border-radius: 15px;\n"
                                       "    color: white;\n"
                                       "}\n"
                                       "\n"
                                       ":hover {\n"
                                       "    background: #453083;\n"
                                       "}")
        self.btn_envAcc1.setObjectName("btn_envAcc1")
        self.gridLayout.addWidget(self.btn_envAcc1, 0, 2, 1, 1)
        self.btn_envVel2 = QtWidgets.QPushButton(self.dockWidgetContents)
        self.btn_envVel2.setMinimumSize(QtCore.QSize(180, 50))
        self.btn_envVel2.setMaximumSize(QtCore.QSize(200, 50))
        font = QtGui.QFont()
        font.setFamily("Nirmala UI")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.btn_envVel2.setFont(font)
        self.btn_envVel2.setStyleSheet(":enabled {\n"
                                       "    background: none;\n"
                                       "    border-radius: 15px;\n"
                                       "    color: white;\n"
                                       "}\n"
                                       "\n"
                                       ":hover {\n"
                                       "    background: #453083;\n"
                                       "}")
        self.btn_envVel2.setObjectName("btn_envVel2")
        self.gridLayout.addWidget(self.btn_envVel2, 1, 3, 1, 1)
        self.horizontalLayout_2.addLayout(self.gridLayout)
        spacerItem2 = QtWidgets.QSpacerItem(80, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        self.btn_options = QtWidgets.QPushButton(self.dockWidgetContents)
        self.btn_options.setMinimumSize(QtCore.QSize(180, 50))
        font = QtGui.QFont()
        font.setFamily("Nirmala UI")
        font.setPointSize(12)
        self.btn_options.setFont(font)
        self.btn_options.setStyleSheet(":enabled {\n"
                                       "    background: none;\n"
                                       "    border-radius: 15px;\n"
                                       "    color: white;\n"
                                       "}\n"
                                       "\n"
                                       ":hover {\n"
                                       "    background: #453083;\n"
                                       "}")
        self.btn_options.setObjectName("btn_log")
        self.horizontalLayout_2.addWidget(self.btn_options)
        spacerItem3 = QtWidgets.QSpacerItem(92, 20, QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem3)
        self.horizontalLayout_2.setStretch(3, 1)
        self.horizontalLayout_3.addLayout(self.horizontalLayout_2)
        self.dockWidget.setWidget(self.dockWidgetContents)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(4), self.dockWidget)
        self.dockWidget_2 = QtWidgets.QDockWidget(MainWindow)
        self.dockWidget_2.setTitleBarWidget(QtWidgets.QWidget())
        self.dockWidget_2.setStyleSheet("margin-top: 10px;")
        self.dockWidget_2.setObjectName("dockWidget_2")
        self.dockWidgetContents_2 = QtWidgets.QWidget()
        self.dockWidgetContents_2.setObjectName("dockWidgetContents_2")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.dockWidgetContents_2)
        self.verticalLayout.setContentsMargins(10, 0, 0, 10)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.widget_2 = QtWidgets.QWidget(self.dockWidgetContents_2)
        self.widget_2.setMinimumSize(QtCore.QSize(300, 200))
        self.widget_2.setMaximumSize(QtCore.QSize(10000, 16777215))
        self.widget_2.setStyleSheet("background: #0C0032;\n"
                                    "border-radius: 20px;")
        self.widget_2.setObjectName("widget_2")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.widget_2)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.lbl_files = QtWidgets.QLabel(self.widget_2)
        font = QtGui.QFont()
        font.setFamily("Nirmala UI")
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.lbl_files.setFont(font)
        self.lbl_files.setStyleSheet("color: white")
        self.lbl_files.setObjectName("lbl_files")
        self.verticalLayout_3.addWidget(self.lbl_files, 0, QtCore.Qt.AlignHCenter)
        self.list_files = QtWidgets.QListWidget(self.widget_2)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.list_files.setFont(font)
        self.list_files.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.list_files.setFocusPolicy(QtCore.Qt.NoFocus)
        self.list_files.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.list_files.setStyleSheet(u":enabled {\n"
                                      "	color: white;\n"
                                      "}\n"
                                      "\n"
                                      "QListView::item {\n"
                                      "	padding: 5px;\n"
                                      "	border-radius: 15px;\n"
                                      "	margin-bottom: 5px;\n"
                                      "}\n"
                                      "\n"
                                      "QListView::item:hover {\n"
                                      "	background-color: #0F135E;\n"
                                      "}\n"
                                      "\n"
                                      "QListView::item:selected{\n"
                                      "background-color: #453083;\n"
                                      "color: white;\n"
                                      "}\n"
                                      "\n"
                                      "QScrollBar:vertical {\n"
                                      "	border: none;\n"
                                      "    background: rgb(45, 45, 68);\n"
                                      "    width: 14px;\n"
                                      "    margin: 15px 0 15px 0;\n"
                                      "	border-radius: 0px;\n"
                                      " }\n"
                                      "\n"
                                      "/*  HANDLE BAR VERTICAL */\n"
                                      "QScrollBar::handle:vertical {	\n"
                                      "	background-color: rgb(80, 80, 122);\n"
                                      "	min-height: 30px;\n"
                                      "}\n"
                                      "QScrollBar::handle:vertical:hover{	\n"
                                      "	background-color: #9898E8;\n"
                                      "}\n"
                                      "\n"
                                      "/* BTN TOP - SCROLLBAR */\n"
                                      "QScrollBar::sub-line:vertical {\n"
                                      "	border: none;\n"
                                      "	background-color: rgb(59, 59, 90);\n"
                                      "	height: 15px;\n"
                                      "	border-top-left-radius: 7px;\n"
                                      "	border-top-right-radius: 7px;\n"
                                      "	subcontrol-position: top;\n"
                                      "	subcontrol-origin: margin;\n"
                                      "}\n"
                                      "QScrollBar::sub-line:vertical:hover {	\n"
                                      "	"
                                      "background-color: #7878B8;\n"
                                      "}\n"
                                      "\n"
                                      "/* BTN BOTTOM - SCROLLBAR */\n"
                                      "QScrollBar::add-line:vertical {\n"
                                      "	border: none;\n"
                                      "	background-color: rgb(59, 59, 90);\n"
                                      "	height: 15px;\n"
                                      "	border-bottom-left-radius: 7px;\n"
                                      "	border-bottom-right-radius: 7px;\n"
                                      "	subcontrol-position: bottom;\n"
                                      "	subcontrol-origin: margin;\n"
                                      "}\n"
                                      "QScrollBar::add-line:vertical:hover {	\n"
                                      "	background-color: #7878B8;\n"
                                      "}\n"
                                      "\n"
                                      "/* RESET ARROW */\n"
                                      "QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {\n"
                                      "	background: none;\n"
                                      "}\n"
                                      "QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {\n"
                                      "	background: none;\n"
                                      "}\n"
                                      "QScrollBar:horizontal {\n"
                                      "	border: none;\n"
                                      "    background: rgb(45, 45, 68);\n"
                                      "    height: 14px;\n"
                                      "    margin: 0 15px 0 15px;\n"
                                      "	border-radius: 0px;\n"
                                      " }\n"
                                      "/*  HANDLE BAR VERTICAL */\n"
                                      "QScrollBar::handle:horizontal {	\n"
                                      "	background-color: rgb(80, 80, 122);\n"
                                      "	min-width: 30px;\n"
                                      "}\n"
                                      "QScrollBar::handle:horizontal:hover{	\n"
                                      ""
                                      "	background-color: #9898E8;\n"
                                      "}\n"
                                      "/* BTN TOP - SCROLLBAR */\n"
                                      "QScrollBar::sub-line:horizontal {\n"
                                      "	border: none;\n"
                                      "	background-color: rgb(59, 59, 90);\n"
                                      "	width: 15px;\n"
                                      "	border-top-left-radius: 7px;\n"
                                      "	border-bottom-left-radius: 7px;\n"
                                      "	subcontrol-position: left;\n"
                                      "	subcontrol-origin: margin;\n"
                                      "}\n"
                                      "QScrollBar::sub-line:horizontal:hover {	\n"
                                      "	background-color: #7878B8;\n"
                                      "}\n"
                                      "/* BTN BOTTOM - SCROLLBAR */\n"
                                      "QScrollBar::add-line:horizontal {\n"
                                      "	border: none;\n"
                                      "	background-color: rgb(59, 59, 90);\n"
                                      "	width: 15px;\n"
                                      "	border-top-right-radius: 7px;\n"
                                      "	border-bottom-right-radius: 7px;\n"
                                      "	subcontrol-position: right;\n"
                                      "	subcontrol-origin: margin;\n"
                                      "}\n"
                                      "QScrollBar::add-line:horizontal:hover {	\n"
                                      "	background-color: #7878B8;\n"
                                      "}\n"
                                      "/* RESET ARROW */\n"
                                      "QScrollBar::right-arrow:horizontal, QScrollBar::left-arrow:horizontal {\n"
                                      "	background: none;\n"
                                      "}\n"
                                      "QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizonal {\n"
                                      "	background: none;\n"
                                      "}\n")
        self.list_files.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.list_files.setLineWidth(2)
        self.list_files.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.list_files.setProperty("showDropIndicator", False)
        self.list_files.setDragEnabled(False)
        self.list_files.setDefaultDropAction(QtCore.Qt.IgnoreAction)
        self.list_files.setAlternatingRowColors(False)
        self.list_files.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)  # do zmiany!!!
        self.list_files.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.list_files.setTextElideMode(QtCore.Qt.ElideNone)
        self.list_files.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerItem)
        self.list_files.setMovement(QtWidgets.QListView.Static)
        self.list_files.setProperty("isWrapping", False)
        self.list_files.setResizeMode(QtWidgets.QListView.Adjust)
        self.list_files.setLayoutMode(QtWidgets.QListView.SinglePass)
        self.list_files.setViewMode(QtWidgets.QListView.ListMode)
        self.list_files.setModelColumn(0)
        self.list_files.setWordWrap(True)
        self.list_files.setObjectName("list_files")
        # item = QtWidgets.QListWidgetItem()
        # item.setTextAlignment(QtCore.Qt.AlignCenter)
        # font = QtGui.QFont()
        # font.setFamily("Nirmala UI")
        # item.setFont(font)
        # item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsEnabled)
        # self.list_files.addItem(item)
        # item = QtWidgets.QListWidgetItem()
        # item.setTextAlignment(QtCore.Qt.AlignCenter)
        # font = QtGui.QFont()
        # font.setFamily("Nirmala UI")
        # item.setFont(font)
        # item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEnabled)
        # self.list_files.addItem(item)
        self.verticalLayout_3.addWidget(self.list_files)
        self.verticalLayout_4.addLayout(self.verticalLayout_3)
        self.verticalLayout.addWidget(self.widget_2)
        self.dockWidget_2.setWidget(self.dockWidgetContents_2)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(1), self.dockWidget_2)
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 1488, 21))
        self.menuBar.setStyleSheet(":enabled {\n"
                                   "color: white;\n"
                                   "}\n"
                                   "\n"
                                   "QMenuBar::item:selected {\n"
                                   "background-color: #0F135E;\n"
                                   "}\n"
                                   "\n"
                                   "QMenu::item::selected {\n"
                                   "     background-color: #0F135E;\n"
                                   "}\n"
                                   "")
        self.menuBar.setObjectName("menuBar")
        self.menuPlik = QtWidgets.QMenu(self.menuBar)
        self.menuPlik.setObjectName("menuPlik")
        self.menuOkno = QtWidgets.QMenu(self.menuBar)
        self.menuOkno.setObjectName("menuOkno")
        MainWindow.setMenuBar(self.menuBar)
        self.action_Dodaj_plik = QtWidgets.QAction(MainWindow)
        self.action_Dodaj_plik.setObjectName("action_Dodaj_plik")
        self.action_Zapisz = QtWidgets.QAction(MainWindow)
        self.action_Zapisz.setObjectName("action_Zapisz")
        self.action_Wczytaj = QtWidgets.QAction(MainWindow)
        self.action_Wczytaj.setObjectName("action_Wczytaj")
        self.menuPlik.addAction(self.action_Dodaj_plik)
        self.menuOkno.addAction(self.action_Zapisz)
        self.menuOkno.addAction(self.action_Wczytaj)
        self.menuBar.addAction(self.menuPlik.menuAction())
        self.menuBar.addAction(self.menuOkno.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.options_win = QtWidgets.QMainWindow()
        self.options = Ui_Options()
        self.options.setupUi(self.options_win)

        # tworzy nowe okno i dodaje do niego area dla docków
        self.win = MainWindow
        self.area = DockArea()
        self.win.setCentralWidget(self.area)

        # domyślne ustawienia dla prędkości, harmonicsow, toLog itp
        self.speed = 60
        self.harmonics = 0
        self.toLog = False

        self.btn_options.clicked.connect(self.openWindow) # otwiera okno opcji przy kliknięciu buttona

        self.list_files.itemSelectionChanged.connect(self.itemChanged) # wywołuje się jak zaznaczymy lub odznaczymy coś z listy

        self.options.drop_bearings.currentTextChanged.connect(self.bearingsUpdated) # wywołuje się przy updacie dropdown listy bearingów
        self.options.drop_modes.currentTextChanged.connect(self.modesUpdated) # # wywołuje się przy updacie dropdown listy modów

        self.options_win.hide() # chowa okno opcji
        
        # ustawia domyślną ścieżkę wyszukiwania na ''. Jak dodaje się plik, ta ścieżka się zmienia
        # dialog można otworzyć albo buttonem, albo z dropdown menu
        self.defaultBrowsePath = ''
        self.btn_addFile.clicked.connect(self.browsefiles)
        self.action_Dodaj_plik.triggered.connect(self.browsefiles)

        # wywołuje funkcje jak zmienia się ustawienia
        self.options.inp_speed.textChanged.connect(self.speedChanged)
        self.options.inp_harmonics.textChanged.connect(self.harmonicsChanged)
        self.options.checkBox.stateChanged.connect(self.logChanged)

        self.openWindowsDict = {}
        
        # tworzy słownik z buttonami i dodaje wartości odpowienim buttonom
        self.btnDict = {}
        self.btnDict[self.btn_acc1.text()] = [False, 0]
        self.btnDict[self.btn_acc2.text()] = [False, 0]
        self.btnDict[self.btn_vel1.text()] = [False, 0]
        self.btnDict[self.btn_vel2.text()] = [False, 0]
        self.btnDict[self.btn_envVel1.text()] = [False, 0]
        self.btnDict[self.btn_envVel2.text()] = [False, 0]
        self.btnDict[self.btn_envAcc1.text()] = [False, 0]
        self.btnDict[self.btn_envAcc2.text()] = [False, 0]
        self.btn_acc1.clicked.connect(lambda: self.btnClick(self.btn_acc1, True))
        self.btn_acc2.clicked.connect(lambda: self.btnClick(self.btn_acc2, True))
        self.btn_vel1.clicked.connect(lambda: self.btnClick(self.btn_vel1, True))
        self.btn_vel2.clicked.connect(lambda: self.btnClick(self.btn_vel2, True))
        self.btn_envAcc1.clicked.connect(lambda: self.btnClick(self.btn_envAcc1, True))
        self.btn_envAcc2.clicked.connect(lambda: self.btnClick(self.btn_envAcc2, True))
        self.btn_envVel1.clicked.connect(lambda: self.btnClick(self.btn_envVel1, True))
        self.btn_envVel2.clicked.connect(lambda: self.btnClick(self.btn_envVel2, True))

        try:
            stateFile = open('data/state.json')
            self.state = json.load(stateFile)
        except Exception:
            self.state = None
        self.action_Zapisz.triggered.connect(self.saveState)
        self.action_Wczytaj.triggered.connect(self.loadState)

        self.bearing_file_path = "data/bearings.json"

        self.bearingsList = []
        self.setNewBearings()

        self.prev_selectedBearings = []
        self.selectedBearings = []

        self.prev_selectedModes = []
        self.selectedModes = []

        self.selectedFiles = []
        self.names = []

        # zmienne wykorzystywane do zapisywania widgetów dodawanych do docków
        self.currentWidgetsACC = []
        self.currentWidgetsVEL = []
        self.currentWidgetsENV_ACC = []
        self.currentWidgetsENV_VEL = []

        self.currentWidgetsACC_SPEC = []
        self.currentWidgetsVEL_SPEC = []
        self.currentWidgetsENV_ACC_SPEC = []
        self.currentWidgetsENV_VEL_SPEC = []

        # wywołuje się kiedy otrzyma sygnał "hide" od któregoś z dropdown menu
        self.options.drop_bearings.sig.connect(self.dropBearingsClosed)
        self.options.drop_modes.sig.connect(self.dropModesClosed)

        self.addFiles()

    def dropBearingsClosed(self): # funkcja która jest wywoływana przy zamknięciu menu bearings
        if self.prev_selectedBearings != self.selectedBearings: # wywołuje się tylko jeśli użytkownik dokonał jakichś zmian
            self.updateGraphs(False)
            self.prev_selectedBearings = self.selectedBearings

    def dropModesClosed(self): # funkcja która jest wywoływana przy zamknięciu menu modes
        if self.prev_selectedModes != self.selectedModes: # wywołuje się tylko jeśli użytkownik dokonał jakichś zmian
            self.updateGraphs(False)
            self.prev_selectedModes = self.selectedModes

    def openWindow(self): # funkcja wywołuje się po kliknięciu guzika Options i otwiera menu opcji
        self.options_win.hide()
        self.options_win.show()
        self.options_win.showNormal() # wyciąga okno jeśli jest zminimalizowane
        x = MainWindow.geometry().x()
        y = MainWindow.geometry().y()
        widthMain = MainWindow.geometry().width()
        heightMain = MainWindow.geometry().height()
        widthSub = self.options_win.width()
        heightSub = self.options_win.height()
        self.options_win.setGeometry(int(x + (widthMain / 2) - (widthSub / 2)),
                                     int(y + (heightMain / 2) - (heightSub / 2)), 0, 0) # ustawia okno na środku głównego okna aplikacji (odrobinka matematyki))
        self.setNewBearings()

    def closeEvent(self, event): # event wywołuje się przy zamknięciu aplikacji
        self.options_win.close() # zamyka okno opcji jeśli jest otwarte

    def addFiles(self): # wczytuje listę plików na podstawie ścieżek zapisanych w pliku ./data/filepaths.json
        self.list_files.clear()
        try: # próbuje załadować jsona
            paths = open('./data/filepaths.json')
            filepaths = json.load(paths)
        except Exception: # jeśli dostajemy błąd (bo np. plik jest pusty), to ustawiamy listę plików na pustą
            filepaths = []
        newPaths = filepaths.copy()

        if len(newPaths) > 0:
            for i in range(len(filepaths)): # pętla usuwa z jsona ścieżki do plików, które nie istnieją
                if not os.path.exists(filepaths[i]):
                    newPaths.remove(filepaths[i])

        if newPaths != filepaths: # jeśli funkcja powyżej dokonała jakiejś zmiany, to zapisuje nową listę plików do jsona
            with open('./data/filepaths.json', 'w') as file:
                json.dump(newPaths, file)
                file.close()

        for filepath in newPaths:
            filename = str(os.path.basename(filepath)) # dodaje do listy tylko nazwy plików
            item = QtWidgets.QListWidgetItem()
            item.setTextAlignment(QtCore.Qt.AlignLeft)
            font = QtGui.QFont()
            font.setFamily("Nirmala UI")
            item.setFont(font)
            item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
            item.setText(filename)
            item.setData(Qt.UserRole, filepath) # dla każdego z elementów listy ustawia jego dane na ścieżkę do pliku
            self.list_files.addItem(item)

    def itemChanged(self): # funkcja wywołuje się po zaznaczeniu nowego pliku
        items = self.list_files.selectedItems()
        list = []
        for item in items:
            list.append(item.data(Qt.UserRole))
        self.selectedFiles = list # do listy selectedFiles dodaje ścieżki zaznaczonych plików

        self.names = []
        for filepath in self.selectedFiles:
            filename = os.path.basename(filepath)
            name = str(filename.split(".")[0]).split("_")[0]
            self.names.append(name) # ustawia zmiennej names odpowiednie nazwy, które będą wykorzystane przy labelach w wykresach

        self.updateGraphs(False) # wywołuje update graphów

    def setNewBearings(self): # ładuje listę bearingów z pliku ./data/bearings.json. Wywołuje się po otworzeniu okna Options
        bearing_file = open(self.bearing_file_path)
        bearings_file_data = json.load(bearing_file)
        bearing_data = bearings_file_data["bearings"]
        bearings_list = list(bearing_data.keys())

        if self.bearingsList != bearings_list: # ustawia nowe bearingi pod warunkiem że plik został edytowany
            self.options.drop_bearings.clear()
            self.options.drop_bearings.addItem("Choose bearings:")
            self.options.drop_bearings.view().setRowHidden(0, True)

            for item in bearings_list:
                self.options.drop_bearings.addItem(item)

            for i in range(len(bearings_list)):
                self.options.drop_bearings.setItemChecked(i + 1, False)

            self.bearingsList = bearings_list
            self.harmonicsChanged()
            self.options.inp_harmonics.setValue(0)
            self.updateGraphs(False)

    def bearingsUpdated(self): # wywołuje się po zaznaczeniu/odznaczeniu bearingów i zapisuje zaznaczone bearingi do listy. Wykorzystują to skrypty przy generowaniu wykresów
        tempList = []
        for i in range(1, self.options.drop_bearings.count()):
            if self.options.drop_bearings.itemChecked(i):
                tempList.append(i - 1)
        self.selectedBearings = tempList
        print(f"Selected bearings: {self.selectedBearings}")

    def modesUpdated(self): # identyczna sytuacja jak powyżej
        modes = ['roll', 'inner', 'outer', 'cage', 'shaft']
        tempList = []
        for i in range(1, self.options.drop_modes.count()):
            if self.options.drop_modes.itemChecked(i):
                tempList.append(modes[i - 1])
        self.selectedModes = tempList
        print(f"Selected modes: {self.selectedModes}")

    def browsefiles(self): # pozwala wybrać i dodać nowe pliki do programu.
        fname = QFileDialog.getOpenFileNames(None, 'Open files', self.defaultBrowsePath, 'JSON files (*.json)') # otwiera okno dialogowe i pozwala zaznaczyć tylko pliki json
        if len(fname[0]) > 0: # jeśli wybrano jakiś plik, to dodaje je do jsona
            try:
                paths = open('./data/filepaths.json')
                filepaths = json.load(paths)
            except Exception:
                filepaths = []
            for file in fname[0]:
                filepath = str(file).replace("/", "\\")
                filename = str(os.path.basename(filepath))
                self.defaultBrowsePath = filepath.replace(filename, "")
                if not filepaths.__contains__(filepath): # pomija istniejące już pliki
                    filepaths.append(filepath)
            with open('./data/filepaths.json', 'w') as file:
                json.dump(filepaths, file) # zapisuje jsona
                file.close()

            self.addFiles() # aktualizuje listę plików

    def speedChanged(self): # wywołuje się po zmianie prędkości
        self.speed = int(self.options.inp_speed.value()) # zapisuje prędkość do pliku
        self.updateGraphs(False) # aktualizuje graph

    def harmonicsChanged(self): # analogicznie jak powyżej
        self.harmonics = int(self.options.inp_harmonics.value())
        self.updateGraphs(False)

    def logChanged(self): # analogicznie jak powyżej tylko że przechowuje wartość True/False
        self.toLog = self.options.checkBox.isChecked()
        self.updateGraphs(False)

    # btn to po prostu button który został kliknięty, a realClick określa czy to rzeczywiście użytkownik kliknął guzik, czy kliknięcie zostało wywołane przez skrypt
    def btnClick(self, btn, realClick): # wywołuje się po kliknięciu buttona
        if self.btnDict[btn.text()][0]:
            self.btnDict[btn.text()][0] = False
            btn.setStyleSheet(":enabled {\n"
                              "    background: none;\n"
                              "    border-radius: 15px;\n"
                              "    color: white;\n"
                              "}\n"
                              "\n"
                              ":hover {\n"
                              "    background: #453083;\n"
                              "}")
            if realClick:
                self.openWindowsDict[btn.text()].close()
                self.openWindowsDict[btn.text()] = None
                print(self.openWindowsDict[btn.text()])
        else:
            if realClick:
                self.btnDict[btn.text()][0] = True
                btn.setStyleSheet(":enabled {\n"
                                  "    background: #453083;\n"
                                  "    border-radius: 15px;\n"
                                  "    color: white;\n"
                                  "}\n"
                                  "\n"
                                  ":hover {\n"
                                  "    background: #342463;\n"
                                  "}")
                dock = Dock(f"{btn.text()}", closable=True, autoOrientation=False) # tworzy nowego docka
                dock.sigClosed.connect(lambda: self.btnClick(btn, False)) # przy zamknięciu docka emitowane jest kliknięcie buttona
                self.openWindowsDict[btn.text()] = dock # dodaje docka do listy docków
                self.area.addDock(dock, 'top') # dodaje docka do area
                self.updateGraphs(btn.text()) # wywołuje update graphów
        print(f"{btn.text()}: {self.btnDict[btn.text()]}")
        print(self.openWindowsDict.values())

    def saveState(self): # zapisuje stan układu docków do pliku ./data./state.json
        self.state = self.area.saveState()
        with open('data/state.json', 'w') as file:
            json.dump(self.state, file)
            file.close()

    def loadState(self): # ładuje stan układu docków z pliku ./data./state.json
        if self.state:
            self.area.restoreState(self.state, missing='ignore')
            print(self.state)
        else:
            msg = QMessageBox()
            msg.setText(f"No state to load.")
            msg.setWindowTitle("Error!")
            msg.setIcon(QMessageBox.Information)
            msg.exec_()


    # dodaje nowe okno z odpowiednimi graphami lub heatmapami
    def updateGraphs(self, add): # add oznacza, że dodaje nowe okno. Kiedy to się dzieje, to nie odświeża pozostałych okien
        openDocks = list(self.openWindowsDict.values()) # tworzy listę otwartych docków
        if len(openDocks) > 0:
            for item in openDocks:
                if item:
                    title = item.title()
                    if title == "ACC - Z":
                        if not add or add == 'ACC - Z':
                            for widget in self.currentWidgetsACC:
                                try:
                                    widget.deleteLater() # czasami ta funkcja daje komunikat o błędzie, który zatrzymuje program ale nie powoduje problemów. except - pass rozwiązuje ten problem
                                except:
                                    print("ERRORRRR")
                                    pass
                            self.currentWidgetsACC = []
                            if len(self.selectedFiles) > 0:
                                values = []
                                print(self.selectedFiles)
                                for i in range(len(self.selectedFiles)):  # ta pętla tworzy wykres dla każdego z plików
                                    filepath = self.selectedFiles[i]
                                    try:
                                        values.append(
                                            generate_acc(self.speed, 1, self.selectedBearings, self.selectedModes,
                                                            filepath)) # generuje wartości na podstawie danych zawartych w plikach
                                    except: # jeżeli wystąpi błąd przy generowaniu to oznacza to, że w pliku zawarte są niepoprawne dane
                                        msg = QMessageBox()
                                        msg.setText(f"File {filepath} is invalid.")
                                        msg.setWindowTitle("Error!")
                                        msg.setIcon(QMessageBox.Information)
                                        msg.exec_()
                                        self.addFiles() # ta funkcja odznacza wszystkie zaznaczone pliki, więc jej tu użyłem
                                                        # lepszym rozwiązaniem byłoby odznaczenie tylko i wyłącznie uszkodzonego/niewłaściwego pliku
                                        return
                                widget = createGraph(values, self.names, self.harmonics, "ACC") # tworzy graphy na podstawie wygenerowanych danych
                                self.currentWidgetsACC.append(widget) # dodaje utworzony powyżej widget do listy widgetów. Robi to po to, by później mógł je usunąć
                                self.openWindowsDict[title].addWidget(widget) # dodaje widget do docka
                    # działa to analogicznie dla pozostałych
                    if title == "VEL - Z":
                        if not add or add == 'VEL - Z':
                            for widget in self.currentWidgetsVEL:
                                try:
                                    widget.deleteLater()
                                except:
                                    print("ERRORRRR")
                                    pass
                            self.currentWidgetsVEL = []
                            if len(self.selectedFiles) > 0:
                                values = []
                                print(self.selectedFiles)
                                for i in range(len(self.selectedFiles)):
                                    filepath = self.selectedFiles[i]
                                    try:
                                        values.append(
                                            generate_vel(self.speed, 1, self.selectedBearings, self.selectedModes,
                                                            filepath))
                                    except:
                                        msg = QMessageBox()
                                        msg.setText(f"File {filepath} is invalid.")
                                        msg.setWindowTitle("Error!")
                                        msg.setIcon(QMessageBox.Information)
                                        msg.exec_()
                                        self.addFiles()
                                        return
                                widget = createGraph(values, self.names, self.harmonics, "VEL")
                                self.currentWidgetsVEL.append(widget)
                                self.openWindowsDict[title].addWidget(widget)
                    if title == "ENV - ACC - Z":
                        if not add or add == 'ENV - ACC - Z':
                            for widget in self.currentWidgetsENV_ACC:
                                try:
                                    widget.deleteLater()
                                except:
                                    print("ERRORRRR")
                                    pass
                            self.currentWidgetsENV_ACC = []
                            if len(self.selectedFiles) > 0:
                                values = []
                                print(self.selectedFiles)
                                for i in range(len(self.selectedFiles)):
                                    filepath = self.selectedFiles[i]
                                    try:
                                        values.append(
                                            generate_env_acc(self.speed, 1, self.selectedBearings, self.selectedModes,
                                                            filepath))
                                    except:
                                        msg = QMessageBox()
                                        msg.setText(f"File {filepath} is invalid.")
                                        msg.setWindowTitle("Error!")
                                        msg.setIcon(QMessageBox.Information)
                                        msg.exec_()
                                        self.addFiles()
                                        return
                                widget = createGraph(values, self.names, self.harmonics, "ACC")
                                self.currentWidgetsENV_ACC.append(widget)
                                self.openWindowsDict[title].addWidget(widget)
                    if title == "ENV - VEL - Z":
                        if not add or add == 'ENV - VEL - Z':
                            for widget in self.currentWidgetsENV_VEL:
                                try:
                                    widget.deleteLater()
                                except:
                                    print("ERRORRRR")
                                    pass
                            self.currentWidgetsENV_VEL = []
                            if len(self.selectedFiles) > 0:
                                values = []
                                print(self.selectedFiles)
                                for i in range(len(self.selectedFiles)):
                                    filepath = self.selectedFiles[i]
                                    try:
                                        values.append(
                                            generate_env_vel(self.speed, 1, self.selectedBearings, self.selectedModes,
                                                            filepath))
                                    except:
                                        msg = QMessageBox()
                                        msg.setText(f"File {filepath} is invalid.")
                                        msg.setWindowTitle("Error!")
                                        msg.setIcon(QMessageBox.Information)
                                        msg.exec_()
                                        self.addFiles()
                                        return
                                widget = createGraph(values, self.names, self.harmonics, "VEL")
                                self.currentWidgetsENV_VEL.append(widget)
                                self.openWindowsDict[title].addWidget(widget)
                    # spec - skrót od spectogram - tak naprawdę jest to hitmapa
                    # jedyna różnica jest taka, że tworzy on tylko i wyłącznie jeden spektogram z ostatnio wybranego pliku
                    # nie tworzy wielu spektogramów z wielu plików
                    if title == "ACC - Z - SPEC":
                        if not add or add == 'ACC - Z - SPEC':
                            for widget in self.currentWidgetsACC_SPEC:
                                try:
                                    widget.deleteLater()
                                except:
                                    print("ERRORRRR")
                                    pass
                            self.currentWidgetsACC_SPEC = []
                            if len(self.selectedFiles) > 0:
                                filepath = self.selectedFiles[len(self.selectedFiles) - 1]
                                try:
                                    value = generate_acc_spec(filepath, self.toLog)
                                except:
                                    msg = QMessageBox()
                                    msg.setText(f"File {filepath} is invalid.")
                                    msg.setWindowTitle("Error!")
                                    msg.setIcon(QMessageBox.Information)
                                    msg.exec_()
                                    self.addFiles()
                                    return
                                widget = createHeatmap(value)
                                self.currentWidgetsACC_SPEC.append(widget)
                                self.openWindowsDict[title].addWidget(widget)
                    if title == "VEL - Z - SPEC":
                        if not add or add == 'VEL - Z - SPEC':
                            for widget in self.currentWidgetsVEL_SPEC:
                                try:
                                    widget.deleteLater()
                                except:
                                    print("ERRORRRR")
                                    pass
                            self.currentWidgetsVEL_SPEC = []
                            if len(self.selectedFiles) > 0:
                                filepath = self.selectedFiles[len(self.selectedFiles) - 1]
                                try:
                                    value = generate_vel_spec(filepath, self.toLog)
                                except:
                                    msg = QMessageBox()
                                    msg.setText(f"File {filepath} is invalid.")
                                    msg.setWindowTitle("Error!")
                                    msg.setIcon(QMessageBox.Information)
                                    msg.exec_()
                                    self.addFiles()
                                    return
                                widget = createHeatmap(value)
                                self.currentWidgetsVEL_SPEC.append(widget)
                                self.openWindowsDict[title].addWidget(widget)
                    if title == "ENV - ACC - Z - SPEC":
                        if not add or add == 'ENV - ACC - Z - SPEC':
                            for widget in self.currentWidgetsENV_ACC_SPEC:
                                try:
                                    widget.deleteLater()
                                except:
                                    print("ERRORRRR")
                                    pass
                            self.currentWidgetsENV_ACC_SPEC = []
                            if len(self.selectedFiles) > 0:
                                filepath = self.selectedFiles[len(self.selectedFiles) - 1]
                                try:
                                    value = generate_env_acc_spec(filepath, self.toLog)
                                except:
                                    msg = QMessageBox()
                                    msg.setText(f"File {filepath} is invalid.")
                                    msg.setWindowTitle("Error!")
                                    msg.setIcon(QMessageBox.Information)
                                    msg.exec_()
                                    self.addFiles()
                                    return
                                widget = createHeatmap(value)
                                self.currentWidgetsENV_ACC_SPEC.append(widget)
                                self.openWindowsDict[title].addWidget(widget)
                    if title == "ENV - VEL - Z - SPEC":
                        if not add or add == 'ENV - VEL - Z - SPEC':
                            for widget in self.currentWidgetsENV_VEL_SPEC:
                                try:
                                    widget.deleteLater()
                                except:
                                    print("ERRORRRR")
                                    pass
                            self.currentWidgetsENV_VEL_SPEC = []
                            if len(self.selectedFiles) > 0:
                                filepath = self.selectedFiles[len(self.selectedFiles) - 1]
                                try:
                                    value = generate_env_vel_spec(filepath, self.toLog)
                                except:
                                    msg = QMessageBox()
                                    msg.setText(f"File {filepath} is invalid.")
                                    msg.setWindowTitle("Error!")
                                    msg.setIcon(QMessageBox.Information)
                                    msg.exec_()
                                    self.addFiles()
                                    return
                                widget = createHeatmap(value)
                                self.currentWidgetsENV_VEL_SPEC.append(widget)
                                self.openWindowsDict[title].addWidget(widget)
                                widget = createHeatmap(value)

    # funkcja utworzona przez QtDesigner - ustawia takie rzeczy jak tekst widgetow itp
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Graphs"))
        MainWindow.setWindowIcon(QtGui.QIcon('./img/icon.png'))
        self.btn_addFile.setText(_translate("MainWindow", "Add files"))
        self.btn_vel1.setText(_translate("MainWindow", "VEL - Z"))
        self.btn_acc2.setText(_translate("MainWindow", "ACC - Z - SPEC"))
        self.btn_envAcc2.setText(_translate("MainWindow", "ENV - ACC - Z - SPEC"))
        self.btn_acc1.setText(_translate("MainWindow", "ACC - Z"))
        self.btn_vel2.setText(_translate("MainWindow", "VEL - Z - SPEC"))
        self.btn_envVel1.setText(_translate("MainWindow", "ENV - VEL - Z"))
        self.btn_envAcc1.setText(_translate("MainWindow", "ENV - ACC - Z"))
        self.btn_envVel2.setText(_translate("MainWindow", "ENV - VEL - Z - SPEC"))
        self.btn_options.setText(_translate("MainWindow", "Options"))
        self.lbl_files.setText(_translate("MainWindow", "Available files:"))
        self.list_files.setSortingEnabled(False)
        __sortingEnabled = self.list_files.isSortingEnabled()
        self.list_files.setSortingEnabled(False)
        self.list_files.setSortingEnabled(__sortingEnabled)
        self.menuPlik.setTitle(_translate("MainWindow", "Files"))
        self.menuOkno.setTitle(_translate("MainWindow", "Docks"))
        self.action_Dodaj_plik.setText(_translate("MainWindow", "Add file"))
        self.action_Zapisz.setText(_translate("MainWindow", "Save state"))
        self.action_Wczytaj.setText(_translate("MainWindow", "Load state"))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    app.setApplicationName("Graphs") # ustawia nazwę aplikacji (wyświetla się jako nazwa okna kiedy dock jest w stanie float)
    MainWindow = Ui_MainWindow()
    MainWindow.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
