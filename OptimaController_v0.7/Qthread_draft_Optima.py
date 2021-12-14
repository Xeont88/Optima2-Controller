import sys
import time

from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QColor
from PyQt5.QtCore import pyqtSignal, QThread, QIODevice


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(453, 408)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.textBrowser = QtWidgets.QTextBrowser(Form)
        self.textBrowser.setObjectName("textBrowser")
        self.verticalLayout_2.addWidget(self.textBrowser)
        self.verticalLayout.addLayout(self.verticalLayout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Example"))
        self.pushButton.setText(_translate("Form", "Input"))


# Объект, который будет перенесён в другой поток для выполнения кода
class BrowserHandler(QtCore.QObject):
    running = False
    newTextAndColor = QtCore.pyqtSignal(str, object)

    # метод, который будет выполнять алгоритм в другом потоке
    def run(self):
        print('brhar run')
        while True:
            # посылаем сигнал из второго потока в GUI поток
            self.newTextAndColor.emit(
                '{} - thread 2 variant 1.\n'.format(str(time.strftime("%Y-%m-%d-%H.%M.%S", time.localtime()))),
                QColor(0, 0, 255)
            )
            QtCore.QThread.msleep(10000)

            # посылаем сигнал из второго потока в GUI поток
            self.newTextAndColor.emit(
                '{} - thread 2 variant 2.\n'.format(str(time.strftime("%Y-%m-%d-%H.%M.%S", time.localtime()))),
                QColor(255, 0, 0)
            )
            QtCore.QThread.msleep(10000)


class MyWindow(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        # используем кнопку для добавления текста с цветом в главном потоке
        self.ui.pushButton.clicked.connect(self.addAnotherTextAndColor)

        # создадим поток
        self.thread = QtCore.QThread()
        # создадим объект для выполнения кода в другом потоке
        self.browserHandler = BrowserHandler()
        # перенесём объект в другой поток
        self.browserHandler.moveToThread(self.thread)
        # после чего подключим все сигналы и слоты
        self.browserHandler.newTextAndColor.connect(self.addNewTextAndColor)
        # подключим сигнал старта потока к методу run у объекта, который должен выполнять код в другом потоке
        self.thread.started.connect(self.browserHandler.run)
        # запустим поток
        self.thread.start()

        port = ''
        # portList = SerialInfoClass().avaliable_ports()
        # for port in portList:
        #     if port:
        #         app = SerialThreadClass(port)
        #         print('connect to', port)
        #         break

        self.serial_thread = QtCore.QThread()

        # self.serial = SerialThreadClass(port)
        self.serial = SerialThreadClass("COM23")
        self.serial.moveToThread(self.serial_thread)
        self.serial.rx_signal.connect(self.addSerialText)
        self.serial_thread.started.connect(self.serial.run)
        self.serial_thread.start()


    @QtCore.pyqtSlot(str, object)
    def addNewTextAndColor(self, string, color):
        self.ui.textBrowser.setTextColor(color)
        self.ui.textBrowser.append(string)

    @QtCore.pyqtSlot(str)
    def addSerialText(self, text):
        self.ui.textBrowser.append(text)

    def addAnotherTextAndColor(self):
        self.ui.textBrowser.setTextColor(QColor(0, 255, 0))
        self.ui.textBrowser.append(
            '{} - thread 2 variant 3.\n'.format(str(time.strftime("%Y-%m-%d-%H.%M.%S", time.localtime()))))


class SerialThreadClass(QThread):
    rx_signal = pyqtSignal(str)
    running = True
    def __init__(self, port, parent=None):
        super(SerialThreadClass, self).__init__(parent)
        # open the serial port
        self.serport = QSerialPort()
        self.serport.setBaudRate(9600)
        self.serport.setPortName(port)
        self.serport.open(QIODevice.ReadWrite)
        print('connected to ', port)

    def run(self):
        print('start "run"')
        while self.running:
            # Устанавливаем таймаут на приём в 1 секунды
            if self.serport.waitForReadyRead(100):
                # Принимаем данные
                rx_data = self.serport.readLine()
                print(rx_data)
                # Если данные приняты, передаём их с сигналом
                if len(rx_data) > 0:
                    self.rx_signal.emit(str(rx_data))
            # При наступлении таймаута передаём сигнал об ошибке
            else:
                pass
                # rx_data = [0xAA, 0x00, 0x00, 0x00, 0x00, 0x00, 0xE1]
                # print(rx_data)
                # self.rx_signal.emit(str(rx_data))

    # Передача данных через порт
    def senddata(self, data):
        tx_data = bytes(data)
        self.serport.write(tx_data)


# Определяем доступные в системе порты
class SerialInfoClass(QSerialPortInfo):

    def __init__(self, parent=None):
        super(SerialInfoClass, self).__init__(parent)

    def avaliable_ports(self):
        avaliable_comport_list = ['']
        self.my_ports = QSerialPortInfo()
        ports = self.my_ports.availablePorts()
        for port in ports:
            port_name = port.portName()
            avaliable_comport_list.append(port_name)
        return avaliable_comport_list


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow()
    window.show()


    sys.exit(app.exec())
