# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_desig_v0_9.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(620, 460)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QtCore.QSize(620, 460))
        MainWindow.setMaximumSize(QtCore.QSize(620, 460))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        MainWindow.setFont(font)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(0, 60, 611, 361))
        self.tabWidget.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.layoutWidget = QtWidgets.QWidget(self.tab)
        self.layoutWidget.setGeometry(QtCore.QRect(530, 10, 77, 311))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.pushButton_1 = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_1.setObjectName("pushButton_1")
        self.verticalLayout_4.addWidget(self.pushButton_1)
        self.pushButton_2 = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_2.setObjectName("pushButton_2")
        self.verticalLayout_4.addWidget(self.pushButton_2)
        self.pushButton_3 = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_3.setObjectName("pushButton_3")
        self.verticalLayout_4.addWidget(self.pushButton_3)
        self.pushButton_4 = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_4.setObjectName("pushButton_4")
        self.verticalLayout_4.addWidget(self.pushButton_4)
        self.pushButton_5 = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_5.setObjectName("pushButton_5")
        self.verticalLayout_4.addWidget(self.pushButton_5)
        self.pushButton_6 = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_6.setObjectName("pushButton_6")
        self.verticalLayout_4.addWidget(self.pushButton_6)
        self.pushButton_7 = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_7.setObjectName("pushButton_7")
        self.verticalLayout_4.addWidget(self.pushButton_7)
        self.pushButton_8 = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_8.setObjectName("pushButton_8")
        self.verticalLayout_4.addWidget(self.pushButton_8)
        self.layoutWidget1 = QtWidgets.QWidget(self.tab)
        self.layoutWidget1.setGeometry(QtCore.QRect(466, 10, 51, 321))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.layoutWidget1)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.lineEdit = QtWidgets.QLineEdit(self.layoutWidget1)
        self.lineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit.setObjectName("lineEdit")
        self.verticalLayout_3.addWidget(self.lineEdit)
        self.lineEdit_2 = QtWidgets.QLineEdit(self.layoutWidget1)
        self.lineEdit_2.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.verticalLayout_3.addWidget(self.lineEdit_2)
        self.lineEdit_3 = QtWidgets.QLineEdit(self.layoutWidget1)
        self.lineEdit_3.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.verticalLayout_3.addWidget(self.lineEdit_3)
        self.lineEdit_4 = QtWidgets.QLineEdit(self.layoutWidget1)
        self.lineEdit_4.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.verticalLayout_3.addWidget(self.lineEdit_4)
        self.lineEdit_5 = QtWidgets.QLineEdit(self.layoutWidget1)
        self.lineEdit_5.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_5.setObjectName("lineEdit_5")
        self.verticalLayout_3.addWidget(self.lineEdit_5)
        self.lineEdit_6 = QtWidgets.QLineEdit(self.layoutWidget1)
        self.lineEdit_6.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_6.setObjectName("lineEdit_6")
        self.verticalLayout_3.addWidget(self.lineEdit_6)
        self.lineEdit_7 = QtWidgets.QLineEdit(self.layoutWidget1)
        self.lineEdit_7.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_7.setObjectName("lineEdit_7")
        self.verticalLayout_3.addWidget(self.lineEdit_7)
        self.lineEdit_8 = QtWidgets.QLineEdit(self.layoutWidget1)
        self.lineEdit_8.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_8.setObjectName("lineEdit_8")
        self.verticalLayout_3.addWidget(self.lineEdit_8)
        self.layoutWidget2 = QtWidgets.QWidget(self.tab)
        self.layoutWidget2.setGeometry(QtCore.QRect(70, 10, 391, 311))
        self.layoutWidget2.setObjectName("layoutWidget2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.layoutWidget2)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.servoSlider1 = QtWidgets.QSlider(self.layoutWidget2)
        self.servoSlider1.setMinimum(-120)
        self.servoSlider1.setMaximum(120)
        self.servoSlider1.setPageStep(15)
        self.servoSlider1.setProperty("value", 0)
        self.servoSlider1.setSliderPosition(0)
        self.servoSlider1.setOrientation(QtCore.Qt.Horizontal)
        self.servoSlider1.setTickPosition(QtWidgets.QSlider.TicksAbove)
        self.servoSlider1.setObjectName("servoSlider1")
        self.verticalLayout_2.addWidget(self.servoSlider1)
        self.servoSlider2 = QtWidgets.QSlider(self.layoutWidget2)
        self.servoSlider2.setMinimum(-60)
        self.servoSlider2.setMaximum(120)
        self.servoSlider2.setProperty("value", 0)
        self.servoSlider2.setSliderPosition(0)
        self.servoSlider2.setOrientation(QtCore.Qt.Horizontal)
        self.servoSlider2.setTickPosition(QtWidgets.QSlider.TicksAbove)
        self.servoSlider2.setObjectName("servoSlider2")
        self.verticalLayout_2.addWidget(self.servoSlider2)
        self.servoSlider3 = QtWidgets.QSlider(self.layoutWidget2)
        self.servoSlider3.setMinimum(-60)
        self.servoSlider3.setMaximum(120)
        self.servoSlider3.setProperty("value", 0)
        self.servoSlider3.setSliderPosition(0)
        self.servoSlider3.setOrientation(QtCore.Qt.Horizontal)
        self.servoSlider3.setTickPosition(QtWidgets.QSlider.TicksAbove)
        self.servoSlider3.setObjectName("servoSlider3")
        self.verticalLayout_2.addWidget(self.servoSlider3)
        self.servoSlider4 = QtWidgets.QSlider(self.layoutWidget2)
        self.servoSlider4.setMinimum(-90)
        self.servoSlider4.setMaximum(90)
        self.servoSlider4.setProperty("value", 0)
        self.servoSlider4.setSliderPosition(0)
        self.servoSlider4.setOrientation(QtCore.Qt.Horizontal)
        self.servoSlider4.setTickPosition(QtWidgets.QSlider.TicksAbove)
        self.servoSlider4.setObjectName("servoSlider4")
        self.verticalLayout_2.addWidget(self.servoSlider4)
        self.servoSlider5 = QtWidgets.QSlider(self.layoutWidget2)
        self.servoSlider5.setMinimum(-90)
        self.servoSlider5.setMaximum(90)
        self.servoSlider5.setProperty("value", 0)
        self.servoSlider5.setSliderPosition(0)
        self.servoSlider5.setOrientation(QtCore.Qt.Horizontal)
        self.servoSlider5.setTickPosition(QtWidgets.QSlider.TicksAbove)
        self.servoSlider5.setObjectName("servoSlider5")
        self.verticalLayout_2.addWidget(self.servoSlider5)
        self.servoSlider6 = QtWidgets.QSlider(self.layoutWidget2)
        self.servoSlider6.setMinimum(-90)
        self.servoSlider6.setMaximum(90)
        self.servoSlider6.setSingleStep(1)
        self.servoSlider6.setPageStep(10)
        self.servoSlider6.setSliderPosition(0)
        self.servoSlider6.setOrientation(QtCore.Qt.Horizontal)
        self.servoSlider6.setTickPosition(QtWidgets.QSlider.TicksAbove)
        self.servoSlider6.setObjectName("servoSlider6")
        self.verticalLayout_2.addWidget(self.servoSlider6)
        self.servoSlider7 = QtWidgets.QSlider(self.layoutWidget2)
        self.servoSlider7.setMinimum(0)
        self.servoSlider7.setMaximum(100)
        self.servoSlider7.setSingleStep(5)
        self.servoSlider7.setPageStep(40)
        self.servoSlider7.setProperty("value", 0)
        self.servoSlider7.setSliderPosition(0)
        self.servoSlider7.setOrientation(QtCore.Qt.Horizontal)
        self.servoSlider7.setTickPosition(QtWidgets.QSlider.TicksAbove)
        self.servoSlider7.setObjectName("servoSlider7")
        self.verticalLayout_2.addWidget(self.servoSlider7)
        self.servoSlider8 = QtWidgets.QSlider(self.layoutWidget2)
        self.servoSlider8.setMinimum(-360)
        self.servoSlider8.setMaximum(360)
        self.servoSlider8.setPageStep(40)
        self.servoSlider8.setProperty("value", 0)
        self.servoSlider8.setSliderPosition(0)
        self.servoSlider8.setOrientation(QtCore.Qt.Horizontal)
        self.servoSlider8.setTickPosition(QtWidgets.QSlider.TicksAbove)
        self.servoSlider8.setObjectName("servoSlider8")
        self.verticalLayout_2.addWidget(self.servoSlider8)
        self.verticalLayoutWidget = QtWidgets.QWidget(self.tab)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 19, 58, 291))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_7 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_7.setAlignment(QtCore.Qt.AlignCenter)
        self.label_7.setObjectName("label_7")
        self.verticalLayout.addWidget(self.label_7)
        self.label_6 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName("label_6")
        self.verticalLayout.addWidget(self.label_6)
        self.label_8 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_8.setAlignment(QtCore.Qt.AlignCenter)
        self.label_8.setObjectName("label_8")
        self.verticalLayout.addWidget(self.label_8)
        self.label_9 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_9.setAlignment(QtCore.Qt.AlignCenter)
        self.label_9.setObjectName("label_9")
        self.verticalLayout.addWidget(self.label_9)
        self.label_5 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName("label_5")
        self.verticalLayout.addWidget(self.label_5)
        self.label_10 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_10.setAlignment(QtCore.Qt.AlignCenter)
        self.label_10.setObjectName("label_10")
        self.verticalLayout.addWidget(self.label_10)
        self.label_11 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_11.setAlignment(QtCore.Qt.AlignCenter)
        self.label_11.setObjectName("label_11")
        self.verticalLayout.addWidget(self.label_11)
        self.label_13 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_13.setAlignment(QtCore.Qt.AlignCenter)
        self.label_13.setObjectName("label_13")
        self.verticalLayout.addWidget(self.label_13)
        self.tabWidget.addTab(self.tab, "")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.layoutWidget3 = QtWidgets.QWidget(self.tab_3)
        self.layoutWidget3.setGeometry(QtCore.QRect(30, 40, 221, 261))
        self.layoutWidget3.setObjectName("layoutWidget3")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.layoutWidget3)
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.label_12 = QtWidgets.QLabel(self.layoutWidget3)
        self.label_12.setMaximumSize(QtCore.QSize(16777215, 20))
        self.label_12.setAlignment(QtCore.Qt.AlignCenter)
        self.label_12.setObjectName("label_12")
        self.verticalLayout_6.addWidget(self.label_12)
        self.radioButton_1 = QtWidgets.QRadioButton(self.layoutWidget3)
        self.radioButton_1.setEnabled(True)
        self.radioButton_1.setChecked(False)
        self.radioButton_1.setObjectName("radioButton_1")
        self.verticalLayout_6.addWidget(self.radioButton_1)
        self.radioButton_2 = QtWidgets.QRadioButton(self.layoutWidget3)
        self.radioButton_2.setEnabled(True)
        self.radioButton_2.setChecked(False)
        self.radioButton_2.setObjectName("radioButton_2")
        self.verticalLayout_6.addWidget(self.radioButton_2)
        self.radioButton_3 = QtWidgets.QRadioButton(self.layoutWidget3)
        self.radioButton_3.setEnabled(True)
        self.radioButton_3.setCheckable(True)
        self.radioButton_3.setChecked(False)
        self.radioButton_3.setObjectName("radioButton_3")
        self.verticalLayout_6.addWidget(self.radioButton_3)
        self.radioButton_4 = QtWidgets.QRadioButton(self.layoutWidget3)
        self.radioButton_4.setEnabled(True)
        self.radioButton_4.setChecked(False)
        self.radioButton_4.setObjectName("radioButton_4")
        self.verticalLayout_6.addWidget(self.radioButton_4)
        self.radioButton_5 = QtWidgets.QRadioButton(self.layoutWidget3)
        self.radioButton_5.setEnabled(True)
        self.radioButton_5.setChecked(False)
        self.radioButton_5.setObjectName("radioButton_5")
        self.verticalLayout_6.addWidget(self.radioButton_5)
        self.radioButton_mute = QtWidgets.QRadioButton(self.layoutWidget3)
        self.radioButton_mute.setEnabled(True)
        self.radioButton_mute.setChecked(False)
        self.radioButton_mute.setObjectName("radioButton_mute")
        self.verticalLayout_6.addWidget(self.radioButton_mute)
        self.verticalLayoutWidget_3 = QtWidgets.QWidget(self.tab_3)
        self.verticalLayoutWidget_3.setGeometry(QtCore.QRect(340, 40, 241, 261))
        self.verticalLayoutWidget_3.setObjectName("verticalLayoutWidget_3")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_3)
        self.verticalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.slider_r = QtWidgets.QSlider(self.verticalLayoutWidget_3)
        self.slider_r.setMaximumSize(QtCore.QSize(16777215, 183))
        self.slider_r.setMaximum(255)
        self.slider_r.setOrientation(QtCore.Qt.Vertical)
        self.slider_r.setTickPosition(QtWidgets.QSlider.TicksAbove)
        self.slider_r.setObjectName("slider_r")
        self.horizontalLayout.addWidget(self.slider_r)
        self.slider_g = QtWidgets.QSlider(self.verticalLayoutWidget_3)
        self.slider_g.setMaximumSize(QtCore.QSize(16777215, 183))
        self.slider_g.setMaximum(255)
        self.slider_g.setOrientation(QtCore.Qt.Vertical)
        self.slider_g.setTickPosition(QtWidgets.QSlider.TicksAbove)
        self.slider_g.setObjectName("slider_g")
        self.horizontalLayout.addWidget(self.slider_g)
        self.slider_b = QtWidgets.QSlider(self.verticalLayoutWidget_3)
        self.slider_b.setMaximumSize(QtCore.QSize(16777215, 183))
        self.slider_b.setMaximum(255)
        self.slider_b.setOrientation(QtCore.Qt.Vertical)
        self.slider_b.setTickPosition(QtWidgets.QSlider.TicksAbove)
        self.slider_b.setObjectName("slider_b")
        self.horizontalLayout.addWidget(self.slider_b)
        self.verticalLayout_8.addLayout(self.horizontalLayout)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label = QtWidgets.QLabel(self.verticalLayoutWidget_3)
        self.label.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.horizontalLayout_3.addWidget(self.label)
        self.label_3 = QtWidgets.QLabel(self.verticalLayoutWidget_3)
        self.label_3.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_3.addWidget(self.label_3)
        self.label_2 = QtWidgets.QLabel(self.verticalLayoutWidget_3)
        self.label_2.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_3.addWidget(self.label_2)
        self.verticalLayout_8.addLayout(self.horizontalLayout_3)
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.light_slider = QtWidgets.QSlider(self.verticalLayoutWidget_3)
        self.light_slider.setMaximum(100)
        self.light_slider.setProperty("value", 50)
        self.light_slider.setOrientation(QtCore.Qt.Horizontal)
        self.light_slider.setTickPosition(QtWidgets.QSlider.TicksAbove)
        self.light_slider.setObjectName("light_slider")
        self.verticalLayout_5.addWidget(self.light_slider)
        self.label_4 = QtWidgets.QLabel(self.verticalLayoutWidget_3)
        self.label_4.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_5.addWidget(self.label_4)
        self.verticalLayout_8.addLayout(self.verticalLayout_5)
        self.checkBox_LED_13 = QtWidgets.QCheckBox(self.tab_3)
        self.checkBox_LED_13.setGeometry(QtCore.QRect(260, 50, 71, 18))
        self.checkBox_LED_13.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.checkBox_LED_13.setObjectName("checkBox_LED_13")
        self.tabWidget.addTab(self.tab_3, "")
        self.tab_4 = QtWidgets.QWidget()
        self.tab_4.setObjectName("tab_4")
        self.tabWidget.addTab(self.tab_4, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.layoutWidget4 = QtWidgets.QWidget(self.tab_2)
        self.layoutWidget4.setGeometry(QtCore.QRect(20, 20, 401, 301))
        self.layoutWidget4.setObjectName("layoutWidget4")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.layoutWidget4)
        self.verticalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.startScenarioButton = QtWidgets.QPushButton(self.layoutWidget4)
        self.startScenarioButton.setObjectName("startScenarioButton")
        self.horizontalLayout_2.addWidget(self.startScenarioButton)
        self.stopScenarioButton = QtWidgets.QPushButton(self.layoutWidget4)
        self.stopScenarioButton.setObjectName("stopScenarioButton")
        self.horizontalLayout_2.addWidget(self.stopScenarioButton)
        self.addPointButton = QtWidgets.QPushButton(self.layoutWidget4)
        self.addPointButton.setObjectName("addPointButton")
        self.horizontalLayout_2.addWidget(self.addPointButton)
        self.verticalLayout_7.addLayout(self.horizontalLayout_2)
        self.textEditScenario = QtWidgets.QTextEdit(self.layoutWidget4)
        self.textEditScenario.setObjectName("textEditScenario")
        self.verticalLayout_7.addWidget(self.textEditScenario)
        self.tabWidget.addTab(self.tab_2, "")
        self.layoutWidget5 = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget5.setGeometry(QtCore.QRect(10, 0, 461, 51))
        self.layoutWidget5.setObjectName("layoutWidget5")
        self.gridLayout = QtWidgets.QGridLayout(self.layoutWidget5)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.ejectButton = QtWidgets.QPushButton(self.layoutWidget5)
        self.ejectButton.setObjectName("ejectButton")
        self.gridLayout.addWidget(self.ejectButton, 0, 5, 1, 1)
        self.comboBox = QtWidgets.QComboBox(self.layoutWidget5)
        self.comboBox.setEnabled(True)
        self.comboBox.setObjectName("comboBox")
        self.gridLayout.addWidget(self.comboBox, 0, 0, 1, 1)
        self.connectButton = QtWidgets.QPushButton(self.layoutWidget5)
        self.connectButton.setObjectName("connectButton")
        self.gridLayout.addWidget(self.connectButton, 0, 4, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 1, 1, 1)
        self.refreshCOMbutton = QtWidgets.QPushButton(self.layoutWidget5)
        self.refreshCOMbutton.setToolTip("")
        self.refreshCOMbutton.setObjectName("refreshCOMbutton")
        self.gridLayout.addWidget(self.refreshCOMbutton, 0, 3, 1, 1)
        self.connectLabel = QtWidgets.QLabel(self.layoutWidget5)
        self.connectLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.connectLabel.setWordWrap(True)
        self.connectLabel.setObjectName("connectLabel")
        self.gridLayout.addWidget(self.connectLabel, 0, 2, 1, 1)
        self.home_button = QtWidgets.QPushButton(self.centralwidget)
        self.home_button.setGeometry(QtCore.QRect(580, 12, 31, 31))
        self.home_button.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("home.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.home_button.setIcon(icon)
        self.home_button.setObjectName("home_button")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 620, 18))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.action = QtWidgets.QAction(MainWindow)
        self.action.setEnabled(False)
        self.action.setVisible(True)
        self.action.setObjectName("action")
        self.action_2 = QtWidgets.QAction(MainWindow)
        self.action_2.setEnabled(False)
        self.action_2.setObjectName("action_2")
        self.action_3 = QtWidgets.QAction(MainWindow)
        self.action_3.setEnabled(False)
        self.action_3.setObjectName("action_3")
        self.exit_btn = QtWidgets.QAction(MainWindow)
        self.exit_btn.setObjectName("exit_btn")
        self.menu.addAction(self.action)
        self.menu.addAction(self.action_2)
        self.menu.addAction(self.action_3)
        self.menu.addSeparator()
        self.menu.addAction(self.exit_btn)
        self.menubar.addAction(self.menu.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Подключение к СОМ порту"))
        self.pushButton_1.setText(_translate("MainWindow", "Установить"))
        self.pushButton_2.setText(_translate("MainWindow", "Установить"))
        self.pushButton_3.setText(_translate("MainWindow", "Установить"))
        self.pushButton_4.setText(_translate("MainWindow", "Установить"))
        self.pushButton_5.setText(_translate("MainWindow", "Установить"))
        self.pushButton_6.setText(_translate("MainWindow", "Установить"))
        self.pushButton_7.setText(_translate("MainWindow", "Установить"))
        self.pushButton_8.setText(_translate("MainWindow", "Установить"))
        self.label_7.setText(_translate("MainWindow", "Ось 1"))
        self.label_6.setText(_translate("MainWindow", "Ось 2"))
        self.label_8.setText(_translate("MainWindow", "Ось 3"))
        self.label_9.setText(_translate("MainWindow", "Ось 4"))
        self.label_5.setText(_translate("MainWindow", "Ось 5"))
        self.label_10.setText(_translate("MainWindow", "Ось 6"))
        self.label_11.setText(_translate("MainWindow", "Схват"))
        self.label_13.setText(_translate("MainWindow", "Карусель"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Управление осями"))
        self.label_12.setText(_translate("MainWindow", "Звуковые дорожки"))
        self.radioButton_1.setText(_translate("MainWindow", "Композиция 1"))
        self.radioButton_2.setText(_translate("MainWindow", "Композиция 2"))
        self.radioButton_3.setText(_translate("MainWindow", "Композиция 3"))
        self.radioButton_4.setText(_translate("MainWindow", "Композиция 4"))
        self.radioButton_5.setText(_translate("MainWindow", "Композиция 5"))
        self.radioButton_mute.setText(_translate("MainWindow", "Без звука"))
        self.label.setText(_translate("MainWindow", "Красный"))
        self.label_3.setText(_translate("MainWindow", "Зеленный"))
        self.label_2.setText(_translate("MainWindow", "Голубой"))
        self.label_4.setText(_translate("MainWindow", "Яркость"))
        self.checkBox_LED_13.setText(_translate("MainWindow", "LASER"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("MainWindow", "Управление компонентами"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), _translate("MainWindow", "KRL"))
        self.startScenarioButton.setText(_translate("MainWindow", "Запуск"))
        self.stopScenarioButton.setText(_translate("MainWindow", "Стоп"))
        self.addPointButton.setText(_translate("MainWindow", "Добавить"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "Сценарии"))
        self.ejectButton.setText(_translate("MainWindow", "Отключить"))
        self.connectButton.setText(_translate("MainWindow", "Подключить"))
        self.refreshCOMbutton.setText(_translate("MainWindow", "Обновить"))
        self.connectLabel.setText(_translate("MainWindow", "Нет подключения"))
        self.menu.setTitle(_translate("MainWindow", "Файл"))
        self.action.setText(_translate("MainWindow", "Открыть"))
        self.action_2.setText(_translate("MainWindow", "Сохранить"))
        self.action_3.setText(_translate("MainWindow", "Информация"))
        self.exit_btn.setText(_translate("MainWindow", "Выход"))

