import design_v0_9
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QFileDialog, QMessageBox
import os
from PyQt5.QtGui import QIcon
from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo
from PyQt5.QtCore import QIODevice, QObject, pyqtSignal, pyqtSlot, QThread
from time import sleep
from gamepad_class import *

# Работа геймпада. Потоки, функции и мэйнлуп для работы геймпада
import threading
# import joystickapi
import msvcrt
import time
import ctypes



# class ScenarioThread(QObject):
#     running = False
#     newPositionPoint = pyqtSignal(list)
#
#     def run(self):
#         while self.running:
#             self.newPositionPoint.emit(['some info'])
#             print('running in "scenario thread"')
#             QThread.msleep(2000)


# class OptimaSerial(QSerialPortInfo, design_v0_8.Ui_MainWindow):
#
#     portList = []
#     portListDescription = ['Выберите устройство']
#
#     def __init__(self, parent=None):
#         super(OptimaSerial, self).__init__(parent)
#         self.serial = QSerialPort(self)
#         self.serial.setBaudRate(115200)
#
#         ports = QSerialPortInfo().availablePorts()
#         for port in ports:
#             self.portList.append(port.portName())
#             self.portListDescription.append(port.description())
#         self.comboBox.addItems(self.portList)
#
#
#     def available_ports(self):
#         available_comport_list = ['']
#         self.my_ports = QSerialPorts()
#         ports = self.my_ports.availablePorts()
#         for port in ports:
#             available_comport_list.append(port_name)
#         return available_comport_list


class Example(QMainWindow, design_v0_9.Ui_MainWindow, Gamepad):
    axis_list = [0, 0, 0, 0, 0, 0, 0, 0]
    portList = []
    portListDescription = ['Выберите устройство']
    send_data = 0

    def __init__(self, ):
        super().__init__()
        self.gamepad_init()
        self.setupUi(self)
        reply = QMessageBox.question(self, 'Внимание!',
                                     'Для использования геймпада подключите его к компьютеру, \nи нажмите кнопку "OK"',
                                     QMessageBox.Ok | QMessageBox.Cancel, QMessageBox.Ok)
        # Serial connections
        self.serial_init()
        self.serial.readyRead.connect(self.on_read)
        self.refreshCOMbutton.clicked.connect(self.refresh_COM)
        self.connectButton.clicked.connect(self.on_open)
        self.ejectButton.clicked.connect(self.on_close)

        # RGB control
        self.slider_r.valueChanged.connect(self.RGB_control)
        self.slider_g.valueChanged.connect(self.RGB_control)
        self.slider_b.valueChanged.connect(self.RGB_control)
        self.light_slider.valueChanged.connect(self.RGB_control)

        # Servos control
        self.servoSlider1.valueChanged.connect(self.servo_control)
        self.servoSlider2.valueChanged.connect(self.servo_control)
        self.servoSlider3.valueChanged.connect(self.servo_control)
        self.servoSlider4.valueChanged.connect(self.servo_control)
        self.servoSlider5.valueChanged.connect(self.servo_control)
        self.servoSlider6.valueChanged.connect(self.servo_control)
        self.servoSlider7.valueChanged.connect(self.servo_control)
        self.servoSlider8.valueChanged.connect(self.servo_control)
        self.servo_control()

        self.my_thread = threading.Thread(target=self.gamepad_thread)
        self.my_thread.start()

        self.addPointButton.clicked.connect(self.add_point_in_scenario)
        self.startScenarioButton.clicked.connect(self.scenario_thread)
        self.home_button.clicked.connect(self.go_home)

        # self.scenario2_thread = QThread()
        # self.scenarioThread = ScenarioThread()
        # self.scenarioThread.running = True
        # self.scenarioThread.moveToThread(self.scenario2_thread)
        # self.scenarioThread.newPositionPoint.connect(self.addNewPosPoint)
        # self.scenario2_thread.started.connect(self.scenarioThread.run)
        # self.scenario2_thread.start()

    # @pyqtSlot(list)
    # def addNewPosPoint(self, string):
    #     self.textEditScenario.insertPlainText(string[0])

    def go_home(self):
        self.servoSlider1.setSliderPosition(0)
        self.servoSlider2.setSliderPosition(0)
        self.servoSlider3.setSliderPosition(0)
        self.servoSlider4.setSliderPosition(0)
        self.servoSlider5.setSliderPosition(0)
        self.servoSlider6.setSliderPosition(0)
        self.servoSlider7.setSliderPosition(0)
        self.servoSlider8.setSliderPosition(0)

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Quit?',
                                     'Вы действительно хотите выйти?',
                                     QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel, QMessageBox.Yes)
        if reply == QMessageBox.Yes:
            self.run = False
            event.accept()
            print('Quit')
        else:
            print('stay')
            event.ignore()

    def serial_init(self):
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

    def on_read(self):
        rx = self.serial.readLine()
        rxs = str(rx, 'utf-8').strip()
        data = rxs.split(' ')
        print(data)

    def on_open2(self):
        self.serial.setPortName(self.comboBox.currentText())
        answer = self.serial.open(QIODevice.ReadWrite)
        print('connected to', self.comboBox.currentText())
        print('answer =', answer)
        if answer:
            self.connectLabel.setText('Подключено')

        # while 1:
        #     sleep(0.01)
        # sleep(2)
        # serialSend([1, 50, 0, 0, 0, 0, 0, 0, 0])

    def on_open1(self):
        my_thread = threading.Thread(target=self.on_open2)
        my_thread.start()
        # ui.connectLabel.setText('Подключено')

    def on_open(self):
        self.serial.setPortName(self.comboBox.currentText())
        answer = self.serial.open(QIODevice.ReadWrite)
        print('connected to', self.comboBox.currentText())
        print('answer =', answer)
        if answer:
            self.connectLabel.setText('Подключено')

    def on_close(self):
        self.serial.close()
        self.connectLabel.setText('Нет подключения')

    def refresh_COM(self):
        ports = QSerialPortInfo().availablePorts()
        # ports.clear()
        self.portList.clear()
        self.portListDescription.clear()
        for port in ports:
            self.portList.append(port.portName())
            self.portListDescription.append(port.description())
        print(self.portList)
        print(self.portListDescription)
        self.comboBox.addItems(self.portListDescription)
        self.comboBox.clear()
        self.comboBox.addItems(self.portList)

    def serial_send(self, data):
        txs = ''
        for val in data:
            txs += str(val)
            txs += ','
        txs = txs[:-1]
        txs += ';'
        self.serial.write(txs.encode())
        self.serial.waitForBytesWritten(10)
        print("serial send", txs)

    def add_point_in_scenario(self):
        ax1 = (self.lineEdit.text())
        ax2 = (self.lineEdit_2.text())
        ax3 = (self.lineEdit_3.text())
        ax4 = (self.lineEdit_4.text())
        ax5 = (self.lineEdit_5.text())
        ax6 = (self.lineEdit_6.text())
        gripper = (self.lineEdit_7.text())
        carousel = (self.lineEdit_8.text())

        text = ax1 + ',' + ax2 + ',' + ax3 + ',' + ax4 + ',' + ax5 + ',' + ax6 + ',' + gripper + ',' + carousel + '\n'
        print('add scenario point', text)
        self.textEditScenario.insertPlainText(text)

    def servo_control(self):
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

        self.set_axis_list_to()

        self.serial_send([1, self.servoSlider1.value(),
                          self.servoSlider2.value(),
                          self.servoSlider3.value(),
                          self.servoSlider4.value(),
                          self.servoSlider5.value(),
                          self.servoSlider6.value(),
                          self.servoSlider7.value(),
                          self.servoSlider8.value(),
                          0])

    def led_control(self, val):
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
        self.serial_send([2, int(self.slider_r.value() * self.light_slider.value() / 100),
                          int(self.slider_g.value() * self.light_slider.value() / 100),
                          int(self.slider_b.value() * self.light_slider.value() / 100), 5])

    def servo_set_func(self):
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

            self.set_axis_list_to()
        except:
            print("don't do that!")

    def set_axis_list_to(self):
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

    def laser_on(self):
        self.led_control(1)
        self.checkBox_LED_13.setChecked(True)

    def laser_off(self):
        self.led_control(0)
        self.checkBox_LED_13.setChecked(False)

    # def servoSetFunc(servo):
    def axisSetFunc(self):

        try:
            if int(self.axis_list[0]) > 120:
                self.axis_list[0] = 120
                self.lineEdit.selectAll()
                self.lineEdit.insert('120')
            if int(self.axis_list[0]) < -120:
                self.axis_list[0] = -120
                self.lineEdit.selectAll()
                self.lineEdit.insert('-120')
            self.servoSlider1.setSliderPosition(int(self.axis_list[0]))

            if int(self.axis_list[1]) > 120:
                self.axis_list[1] = 120
                self.lineEdit_2.selectAll()
                self.lineEdit_2.insert('120')
            if int(self.axis_list[1]) < -60:
                self.axis_list[1] = -60
                self.lineEdit_2.selectAll()
                self.lineEdit_2.insert('-60')
            self.servoSlider2.setSliderPosition(int(self.axis_list[1]))

            if int(self.axis_list[2]) > 120:
                self.axis_list[2] = 120
                self.lineEdit_3.selectAll()
                self.lineEdit_3.insert('120')
            if int(self.axis_list[2]) < -60:
                self.axis_list[2] = -60
                self.lineEdit_3.selectAll()
                self.lineEdit_3.insert('-60')
            self.servoSlider3.setSliderPosition(int(self.axis_list[2]))

            if int(self.axis_list[3]) > 90:
                self.axis_list[3] = 90
                self.lineEdit_4.selectAll()
                self.lineEdit_4.insert('90')
            if int(self.axis_list[3]) < -90:
                self.axis_list[3] = -90
                self.lineEdit_4.selectAll()
                self.lineEdit_4.insert('-90')
            self.servoSlider4.setSliderPosition(int(self.axis_list[3]))

            if int(self.axis_list[4]) > 90:
                self.axis_list[4] = 90
                self.lineEdit_5.selectAll()
                self.lineEdit_5.insert('90')
            if int(self.axis_list[4]) < -90:
                self.axis_list[4] = -90
                self.lineEdit_5.selectAll()
                self.lineEdit_5.insert('-90')
            self.servoSlider5.setSliderPosition(int(self.axis_list[4]))

            if int(self.axis_list[5]) > 90:
                self.axis_list[5] = 90
                self.lineEdit_6.selectAll()
                self.lineEdit_6.insert('90')
            if int(self.axis_list[5]) < -90:
                self.axis_list[5] = -90
                self.lineEdit_6.selectAll()
                self.lineEdit_6.insert('-90')
            self.servoSlider6.setSliderPosition(int(self.axis_list[5]))

            if int(self.axis_list[6]) > 100:
                self.axis_list[6] = 100
                self.lineEdit_7.selectAll()
                self.lineEdit_7.insert('100')
            if int(self.axis_list[6]) < 0:
                self.axis_list[6] = 0
                self.lineEdit_7.selectAll()
                self.lineEdit_7.insert('0')
            self.servoSlider7.setSliderPosition(int(self.axis_list[6]))

            if int(self.axis_list[7]) > 360:
                self.axis_list[7] = 360
                self.lineEdit_8.selectAll()
                self.lineEdit_8.insert('360')
            if int(self.axis_list[7]) < -360:
                self.axis_list[7] = -360
                self.lineEdit_8.selectAll()
                self.lineEdit_8.insert('-360')
            self.servoSlider8.setSliderPosition(int(self.axis_list[7]))

        except:
            print("don't do that!")
            pass

    def binding_sticks(self, x, y, z, table, axis_6):

        if x[0] != 0:
            self.axis_list[0] += round(x[0] / 32768)
        if x[1] != 0:
            self.axis_list[1] -= round(x[1] / 32768)
        if y[0] != 0:
            self.axis_list[3] += round(y[0] / 32768)
        if y[1] != 0:
            self.axis_list[2] -= round(y[1] / 32768)
        if z[0] != True:
            self.axis_list[4] += 1
        if z[2] != True:
            self.axis_list[4] -= 1
        if z[1] != True:
            self.axis_list[5] += 1
        if z[3] != True:
            self.axis_list[5] -= 1
        if table[0]:
            self.axis_list[7] -= round(table[0] / 32768) * 5
        if axis_6[0]:
            self.axis_list[6] += 5
            # ui.checkBox_LED_13.setChecked(True)
        if axis_6[1]:
            self.axis_list[6] -= 5
            # ui.checkBox_LED_13.setChecked(False)

        # print(axis_list)
        self.axisSetFunc()

    def gamepad_thread(self):
        print("start of gamepad script")

        # num = joystickapi.joyGetNumDevs()
        num = self.joyGetNumDevs()
        ret, caps, startinfo = False, None, None
        for id in range(num):
            ret, caps = self.joyGetDevCaps(id)
            if ret:
                print("gamepad detected: " + caps.szPname)
                ret, startinfo = self.joyGetPosEx(id)
                break
        else:
            print("no gamepad detected")

        self.run = ret
        while self.run:
            # QThread.sleep(100)
            time.sleep(0.1)
            if msvcrt.kbhit() and msvcrt.getch() == chr(27).encode():  # detect ESC
                run = False

            ret, info = self.joyGetPosEx(id)
            if ret:
                btns = [(1 << i) & info.dwButtons != 0 for i in range(caps.wNumButtons)]
                axisXYZ = [info.dwXpos - startinfo.dwXpos, info.dwYpos - startinfo.dwYpos, info.dwZpos - startinfo.dwZpos]
                axisRUV = [info.dwRpos - startinfo.dwRpos, info.dwUpos - startinfo.dwUpos, info.dwVpos - startinfo.dwVpos]
                if info.dwButtons:
                    # print("buttons: ", btns)
                    self.binding_sticks(x=[0, 0], y=[0, 0], z=[btns[0], btns[2], btns[1], btns[3]],
                                   table=[btns[6], btns[7]], axis_6=[btns[5],btns[4]])

                if any([abs(v) > 10 for v in axisXYZ]):
                    # print("axis:", axisXYZ)
                    self.binding_sticks(x=[axisXYZ[0], axisXYZ[1]], y=[0, 0], z=[0, 0, 0, 0], table=[axisXYZ[2], 0], axis_6=[0,0])
                if any([abs(v) > 10 for v in axisRUV]):
                    # print("roation axis:", axisRUV)
                    self.binding_sticks(x=[0, 0], y=[axisRUV[1], axisRUV[0]], z=[0, 0, 0, 0], table=[0, 0], axis_6=[0,0])

    def move_in_point(self, point, serial):
        print('point=', point)
        # TODO: цикл выполняется пока все оси не дойдут до своих позиций
        # while 1:
        # self.serialSend(serial, [1, point[0],
        self.serial_send([1, point[0],
                          point[1],
                          point[2],
                          point[3],
                          point[4],
                          point[5],
                          0, 0])

    def scenario_thread(self):
        self.sc_thread = threading.Thread(target=self.start_scenario)
        self.sc_thread.start()
        print('scenario started')

    def finding_longest_way(self, last_axes, new_axes):
        longest_way = 0
        i = 0
        for axis in new_axes[:-1]:
            print('last & new', last_axes[i], axis)
            if longest_way < abs(int(axis)-int(last_axes[i])):
                longest_way = abs(int(axis)-int(last_axes[i]))
            i += 1

        print('longest_way =', longest_way)
        return longest_way

    def start_scenario(self):
        self.send_data = 1
        # print('thread')
        text = self.textEditScenario.toPlainText()
        print(text)
        t = text.split('\n')
        # print(t)
        # serial.close()
        last_axes = self.axis_list
        i = 0
        for line in t[:-1]:
            # try:
            line = line.split(',')
            print('line', line)
            delay = self.finding_longest_way(last_axes, line)
            last_axes = line
            # serial.close()

            # serial1 = QSerialPort()
            # serial1.setPortName(ui.comboBox.currentText())
            # serial1.open(QIODevice.ReadWrite)
            # serial.setPortName(ui.comboBox.currentText())
            self.move_in_point(line, self.serial)
            # serial.update()
            sleep(delay*0.07)
            i += 1
            print('end of line', i)
            # timer = threading.Timer(3, lambda: move_in_point(line))
            # timer.start()
            # except:
            #     print('incorrect command in text edit')
            #     pass
        send_data = 0
        print('scenario over')

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
