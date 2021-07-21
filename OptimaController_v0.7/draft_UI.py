import design_v0_7a
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QFileDialog, QMessageBox
import os
from PyQt5.QtGui import QIcon
from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo
from PyQt5.QtCore import QIODevice
from time import sleep

# Работа геймпада. Потоки, функции и мэйнлуп для работы геймпада
import threading
# import joystickapi
import msvcrt
import time
import ctypes



class Example(QMainWindow, design_v0_7a.Ui_MainWindow):
    axis_list = [0, 0, 0, 0, 0, 0, 0, 0]
    portList = []
    portListDescription = ['Выберите устройство']


    def __init__(self, ):
        super().__init__()
        self.setupUi(self)
        reply = QMessageBox.question(self, 'Внимание!',
                                     'Для использования геймпада подключите его к компьютеру, \nи нажмите кнопку "OK"',
                                     QMessageBox.Ok | QMessageBox.Cancel, QMessageBox.Ok)
        self.serialInit()
        # Serial connections
        self.serial.readyRead.connect(self.onRead)
        self.refreshCOMbutton.clicked.connect(self.refreshCOM)
        self.connectButton.clicked.connect(self.onOpen)
        self.ejectButton.clicked.connect(self.onClose)

        # RGB control
        self.slider_r.valueChanged.connect(self.RGB_control)
        self.slider_g.valueChanged.connect(self.RGB_control)
        self.slider_b.valueChanged.connect(self.RGB_control)
        self.light_slider.valueChanged.connect(self.RGB_control)

        # Servos control
        self.servoSlider1.valueChanged.connect(self.servoControl)
        self.servoSlider2.valueChanged.connect(self.servoControl)
        self.servoSlider3.valueChanged.connect(self.servoControl)
        self.servoSlider4.valueChanged.connect(self.servoControl)
        self.servoSlider5.valueChanged.connect(self.servoControl)
        self.servoSlider6.valueChanged.connect(self.servoControl)
        self.servoSlider7.valueChanged.connect(self.servoControl)
        self.servoSlider8.valueChanged.connect(self.servoControl)
        self.servoControl()


    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Quit?',
                                     'Вы действительно хотите выйти?',
                                     QMessageBox.Yes|QMessageBox.No|QMessageBox.Cancel, QMessageBox.Yes)
        if reply == QMessageBox.Yes:
            event.accept()
            print('Quit')
        else:
            print('stay')
            event.ignore()

    def serialInit(self):
        # open the serial port
        self.serial = QSerialPort(self)
        self.serial.setBaudRate(115200)

        ports = QSerialPortInfo().availablePorts()
        for port in ports:
            self.portList.append(port.portName())
            self.portListDescription.append(port.description())
        print(self.portList)
        print(self.portListDescription)
        self.comboBox.addItems(self.portList)

    def onRead(self):
        rx = self.serial.readLine()
        rxs = str(rx, 'utf-8').strip()
        data = rxs.split(' ')
        print(data)

    def onOpen(self):
        self.serial.setPortName(self.comboBox.currentText())
        answer = self.serial.open(QIODevice.ReadWrite)
        print('connected to', self.comboBox.currentText())
        print('answer =', answer)
        if answer:
            self.connectLabel.setText('Подключено')

    def onClose(self):
        self.serial.close()
        self.connectLabel.setText('Нет подключения')

    def refreshCOM(self):
        ports = QSerialPortInfo().availablePorts()
        # ports.clear()
        for port in ports:
            self.portList.append(port.portName())
            self.portListDescription.append(port.description())
        print(self.portList)
        print(self.portListDescription)
        self.comboBox.addItems(self.portListDescription)
        self.comboBox.clear()
        self.comboBox.addItems(self.portList)

    def serialSend(self, data):
        txs = ''
        for val in data:
            txs += str(val)
            txs += ','
        txs = txs[:-1]
        txs += ';'
        self.serial.write(txs.encode())

    def servoControl(self):
        self.lineEdit.selectAll()
        self.lineEdit.insert(str(self.servoSlider1.value()))
        self.lineEdit_2.selectAll()
        self.lineEdit_2.insert(str(self.servoSlider2.value()))
        self.lineEdit_3.selectAll()
        self.lineEdit_3.insert(str(self.servoSlider3.value()))
        self.lineEdit_4.selectAll()
        self.lineEdit_4.insert(str(self.servoSlider4.value()))
        self.lineEdit_5.selectAll()
        self.lineEdit_5.insert(str(self.servoSlider5.value()))
        self.lineEdit_6.selectAll()
        self.lineEdit_6.insert(str(self.servoSlider6.value()))
        self.lineEdit_7.selectAll()
        self.lineEdit_7.insert(str(self.servoSlider7.value()))
        self.lineEdit_8.selectAll()
        self.lineEdit_8.insert(str(self.servoSlider8.value()))

        self.setAxisListTo()

        self.serialSend([1, self.servoSlider1.value(),
                         self.servoSlider2.value(),
                         self.servoSlider3.value(),
                         self.servoSlider4.value(),
                         self.servoSlider5.value(),
                         self.servoSlider6.value(),
                         self.servoSlider7.value(),
                         self.servoSlider8.value(),
                         0])

    def ledControll(self, val):
        if val == 2:
            val = 1
        s = [0, val, 0]
        txs = ''
        for val in s:
            txs += str(val)
            txs += ','
        txs = txs[:-1]
        txs += ';'
        self.serial.write(txs.encode())

    def DFPlayer(self):
        button = self.sender
        try:
            print(button.text)
        except:
            pass

    def RGB_control(self):
        # r = int(ui.slider_r.value()*ui.light_slider.value()/100)
        # print('r =', ui.light_slider.value())
        self.serialSend([2, int(self.slider_r.value() * self.light_slider.value() / 100),
                    int(self.slider_g.value() * self.light_slider.value() / 100),
                    int(self.slider_b.value() * self.light_slider.value() / 100), 5])

    def servoSetFunc(self):
        # TODO: поправить конечные положения шаговиков. -90, 90 и тд.
        try:
            if int(self.lineEdit.text()) > 120:
                self.lineEdit.selectAll()
                self.lineEdit.insert('120')
            if int(self.lineEdit.text()) < -120:
                self.lineEdit.selectAll()
                self.lineEdit.insert('-120')
            self.servoSlider1.setSliderPosition(int(self.lineEdit.text()))

            if int(self.lineEdit_2.text()) > 120:
                self.lineEdit_2.selectAll()
                self.lineEdit_2.insert('120')
            if int(self.lineEdit_2.text()) < -60:
                self.lineEdit_2.selectAll()
                self.lineEdit_2.insert('-60')
            self.servoSlider2.setSliderPosition(int(self.lineEdit_2.text()))

            if int(self.lineEdit_3.text()) > 120:
                self.lineEdit_3.selectAll()
                self.lineEdit_3.insert('120')
            if int(self.lineEdit_3.text()) < -60:
                self.lineEdit_3.selectAll()
                self.lineEdit_3.insert('-60')
            self.servoSlider3.setSliderPosition(int(self.lineEdit_3.text()))

            if int(self.lineEdit_4.text()) > 90:
                self.lineEdit_4.selectAll()
                self.lineEdit_4.insert('90')
            if int(self.lineEdit_4.text()) < -90:
                self.lineEdit_4.selectAll()
                self.lineEdit_4.insert('-90')
            self.servoSlider4.setSliderPosition(int(self.lineEdit_4.text()))

            if int(self.lineEdit_5.text()) > 90:
                self.lineEdit_5.selectAll()
                self.lineEdit_5.insert('90')
            if int(self.lineEdit_5.text()) < -90:
                self.lineEdit_5.selectAll()
                self.lineEdit_5.insert('-90')
            self.servoSlider5.setSliderPosition(int(self.lineEdit_5.text()))

            if int(self.lineEdit_6.text()) > 90:
                self.lineEdit_6.selectAll()
                self.lineEdit_6.insert('90')
            if int(self.lineEdit_6.text()) < -90:
                self.lineEdit_6.selectAll()
                self.lineEdit_6.insert('-90')
            self.servoSlider6.setSliderPosition(int(self.lineEdit_6.text()))

            if int(self.lineEdit_7.text()) > 100:
                self.lineEdit_7.selectAll()
                self.lineEdit_7.insert('100')
            if int(self.lineEdit_7.text()) < 0:
                self.lineEdit_7.selectAll()
                self.lineEdit_7.insert('0')
            self.servoSlider7.setSliderPosition(int(self.lineEdit_7.text()))

            if int(self.lineEdit_8.text()) > 360:
                self.lineEdit_8.selectAll()
                self.lineEdit_8.insert('360')
            if int(self.lineEdit_8.text()) < -360:
                self.lineEdit_8.selectAll()
                self.lineEdit_8.insert('-360')
            self.servoSlider8.setSliderPosition(int(self.lineEdit_8.text()))

            self.setAxisListTo()
        except:
            print("don't do that!")

    def setAxisListTo(self):
        self.axis_list[0] = int(self.lineEdit.text())
        self.axis_list[1] = int(self.lineEdit_2.text())
        self.axis_list[2] = int(self.lineEdit_3.text())
        self.axis_list[3] = int(self.lineEdit_4.text())
        self.axis_list[4] = int(self.lineEdit_5.text())
        self.axis_list[5] = int(self.lineEdit_6.text())
        self.axis_list[6] = int(self.lineEdit_7.text())
        self.axis_list[7] = int(self.lineEdit_8.text())

    def browse_folder(self):
        self.listWidget.clear()  # На случай, если в списке уже есть элементы
        directory = QFileDialog.getExistingDirectory(self, "Выберите папку")
        # открыть диалог выбора директории и установить значение переменной
        # равной пути к выбранной директории

        if directory:  # не продолжать выполнение, если пользователь не выбрал директорию
            for file_name in os.listdir(directory):  # для каждого файла в директории
                self.listWidget.addItem(file_name)  # добавить файл в listWidget




def main():
    app = QApplication(sys.argv)  # Новый экземпляр QApplication
    app.setStyle('Fusion')
    window = Example()  # Создаём объект класса ExampleApp
    window.setWindowTitle("Optima-2 Controller")
    window.setWindowIcon(QIcon('src/zarnitza64g.ico'))
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение


if __name__ == '__main__':
    main()
