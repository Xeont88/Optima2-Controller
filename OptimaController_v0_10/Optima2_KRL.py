import design_v0_11
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QFileDialog, QMessageBox
import os, signal, subprocess
from PyQt5.QtGui import QIcon
from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo
from PyQt5.QtCore import QIODevice, QObject, pyqtSignal, pyqtSlot, QThread
from time import sleep
from gamepad_class import *
from CardDetection import CardDetection as CD
import cv2


# KRL
import re
import math
import numpy as np


# Работа геймпада. Потоки, функции и мэйнлуп для работы геймпада
import threading
# import joystickapi
import msvcrt
import time
import ctypes

# разделитель между значениями осей, в сценариях
delimit = ' '
point_delay = 0.08


class Optima2Controller(QMainWindow, design_v0_11.Ui_MainWindow, Gamepad, CD):
    '''
    Главный класс приложения.
    Работа GUI.
    Работа с потоками Serial, Сценария, и Gamepad.

    '''
    axis_list = [0, 0, 0, 0, 0, 0, 0, 0]
    portList = []
    portListDescription = ['Выберите устройство']
    send_data = 0
    MV_script_flag = False

    def __init__(self, ):
        super().__init__()
        self.gamepad_init()
        self.setupUi(self)
        self.home_button.setToolTip("Установить оси в исходное положение")
        self.comboBox.setToolTip("Список СОМ-портов")
        self.play_button.setToolTip("Запустить программу")
        self.plus_button.setToolTip("Добавить позицию в сценарий")
        self.refreshCOMbutton.setToolTip("Обновить список СОМ-портов")
        self.connectButton.setToolTip("Подключиться к роботу")
        self.ejectButton.setToolTip("Отключить соединение")
        self.compileBtn.setToolTip("Скомпилировать KRL код")

        self.photo_cam_button.setToolTip("Создать фото объекта")
        self.create_picture_button.setToolTip("Сделать снимок")
        self.MV_mode_combobox.setToolTip("Режимы работы Тех Зрения")
        self.play_button_vision.setToolTip("Запустить работу Тех Зрения")
        self.stop_button_vision.setToolTip("Остановить работу Тех Зрения")

        self.action_open_scen.triggered.connect(self.open_scenario_file)
        self.action_open_KRL.triggered.connect(self.open_KRL_file)
        self.action_save_KRL.triggered.connect(self.save_KRL_file)
        self.action_save_scen.triggered.connect(self.save_scenario_file)
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

        #
        self.pushButton_1.clicked.connect(self.servo_set_func)
        self.lineEdit.returnPressed.connect(self.servo_set_func)
        self.pushButton_2.clicked.connect(self.servo_set_func)
        self.lineEdit_2.returnPressed.connect(self.servo_set_func)
        self.pushButton_3.clicked.connect(self.servo_set_func)
        self.lineEdit_3.returnPressed.connect(self.servo_set_func)
        self.pushButton_4.clicked.connect(self.servo_set_func)
        self.lineEdit_4.returnPressed.connect(self.servo_set_func)
        self.pushButton_5.clicked.connect(self.servo_set_func)
        self.lineEdit_5.returnPressed.connect(self.servo_set_func)
        self.pushButton_6.clicked.connect(self.servo_set_func)
        self.lineEdit_6.returnPressed.connect(self.servo_set_func)
        self.pushButton_7.clicked.connect(self.servo_set_func)
        self.lineEdit_7.returnPressed.connect(self.servo_set_func)


        self.my_thread = threading.Thread(target=self.gamepad_thread)
        self.my_thread.daemon = True
        self.my_thread.start()

        self.addPointButton.clicked.connect(self.add_point_in_scenario)
        self.plus_button.clicked.connect(self.add_point_in_scenario)
        self.startScenarioButton.clicked.connect(self.scenario_thread)
        self.play_button.clicked.connect(self.scenario_thread)
        self.home_button.clicked.connect(self.go_home)
        self.play_button_vision.clicked.connect(self.start_MV_script)
        self.stop_button_vision.clicked.connect(self.stop_MV_script)

        # KRL
        # self.adressLine.setText('myProgram.krl')  # Указывание название файла
        self.codeEditor.setPlainText('''DEF my_program()

DECL POS HOME
INI
HOME = {A1 0, A2 0, A3 0, A4 0, A5 0}

PTP HOME

PTP HOME

END''')  # Назначаем стартовый текст
        self.compileBtn.clicked.connect(self.parser)  # Если нажали "compile", то начинаем парсить
        # self.saveBtn.clicked.connect(
        #     self.KRL_file_saver)  # Если нажали "save", то сохраняем код в файл с указанным в адресной строке именем

        print(self.tableWidget.columnWidth(2))
        self.tableWidget.setColumnWidth(0, 220)
        self.tableWidget.setColumnWidth(1, 220)
        self.tableWidget.setColumnWidth(2, 107)


    def stop_MV_script(self):
        while self.flag:
            sleep(0.001)
        try:
            # ch = cv2.waitKey(5)
            # if ch == 27:
            # self.cap.release()
            cv2.destroyAllWindows()
            self.MV_script_flag = False
        except:
            raise

    def start_MV_script(self):
        self.MV_script_flag = True
        MV_thread = threading.Thread(target=self.MV_script)
        MV_thread.daemon = True
        MV_thread.start()
        # ui.connectLabel.setText('Подключено')

    def scenario_file_thread(self, scen):
        self.sc_file_thread = threading.Thread(target=lambda : self.start_scenario_from_file(scen))
        self.sc_file_thread.daemon = True
        self.sc_file_thread.start()
        print('scenario started')

    def check_MV_event_list(self, key):
        '''
        Проверяется таблица на наличие искомого объекта(-ов),
        в случае успеха - запускается соответствующий сценарий
        :param key: имя файла фото.
        '''
        # print('in da ya4eyka ', self.tableWidget.item(0, 1).text())
        for row in range(self.tableWidget.rowCount()):
            if self.tableWidget.item(row, 1):
                item = self.tableWidget.item(row, 1).text()
                if item == key and not self.send_data:
                    scen = self.tableWidget.item(row, 0).text()
                    if scen[-4:] != '.scn':
                        scen += '.scn'
                    print(scen)
                    self.scenario_file_thread(scen)


    def start_scenario_from_file(self, file_name):
        self.send_data = 1
        print('start_scenario_from_file')
        data = ''
        try:
            # Тут есть ошибка с библиотекой log4cplus, как то связано с тем, что на компе установлен Autodesk 360
            print('open')
            f = open(file_name, 'r')
            # with f:
            data = f.read()
            print(data)
            f.close()
        except:
            print('ошибка чтения файла сценария.')


        t = data.split('\n')
        last_axes = self.axis_list
        i = 0
        for line in t[:-1]:
            line = line.split(delimit)
            print('line', line)
            delay = self.finding_longest_way(last_axes, line)
            last_axes = line
            self.move_in_point(line)
            while self.robot_moving:            # ждем пока робот не достигнет новой позиции всеми осями
                sleep(0.01)
            i += 1
            print('end of line', i)
        self.send_data = 0
        print('scenario over')

    def MV_script(self):
        self.cap = cv2.VideoCapture(0)

        # TODO: открытие окна видео, при повторном запуске.
        while self.MV_script_flag:
            try:
                self.flag = True
                flag, img = self.cap.read()
                gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                cnts = self.find_countours_of_cards(gray_img)
                card_location = self.find_coordinates_of_cards(cnts, gray_img)
                key = self.draw_rectangle_aroudn_cards(card_location, img)
                print(key)
                if key:
                    self.check_MV_event_list(key)
                self.flag = False
            except:
                self.cap.release()
                raise
            ch = cv2.waitKey(50)
            if ch == 27:
                self.cap.release()
                cv2.destroyAllWindows()
                self.MV_script_flag = False
                break

    def open_scenario_file(self):
        # fname = QFileDialog.getOpenFileName(self, 'Open file', '/home')
        fname = QFileDialog.getOpenFileName(self, "Choose a path and filename", os.getcwd().replace("\\", "/") +
                                            "/data/", filter="Text Files (*.scn);; All Files (*.*)")

        print(fname)
        try:
            # Тут есть ошибка с библиотекой log4cplus, как то связано с тем, что на компе установлен Autodesk 360
            print('open')
            f = open(fname[0], 'r')
            # with f:
            data = f.read()
            print(data)
            self.textEditScenario.selectAll()
            self.textEditScenario.setText(data)
            f.close()
        except:
            pass

    def save_scenario_file(self):
        # fname = QFileDialog.getOpenFileName(self, 'Open file', '/home')
        fname = QFileDialog.getSaveFileName(self, "Choose a path and filename", os.getcwd().replace("\\", "/") +
                                            "/data/", filter="Text Files (*.scn);; All Files (*.*)")

        print(fname)
        try:
            # Тут есть ошибка с библиотекой log4cplus, как то связано с тем, что на компе установлен Autodesk 360
            print('open')
            f = open(fname[0], 'w')
            # with f:
            # self.textEditScenario.selectAll()
            data = self.textEditScenario.getText()
            f.write(data)
            # print(data)
            f.close()
        except:
            print('.scn file not saved')
            pass

    def save_KRL_file(self):
        # fname = QFileDialog.getOpenFileName(self, 'Open file', '/home')
        fname = QFileDialog.getSaveFileName(self, "Choose a path and filename", os.getcwd().replace("\\", "/") +
                                            "/data/myProgram", filter="Text Files (*.krl);; All Files (*.*)")

        print(fname)
        try:
            # Тут есть ошибка с библиотекой log4cplus, как то связано с тем, что на компе установлен Autodesk 360
            print('open to save')
            f = open(fname[0], 'w')
            # with f:
            # self.textEditScenario.selectAll()
            data = self.codeEditor.toPlainText()
            print(data)
            f.write(data)
            f.close()
        except:
            print('.krl file not saved')
            pass

    def open_KRL_file(self):
        # fname = QFileDialog.getOpenFileName(self, 'Open file', '/home')
        fname = QFileDialog.getOpenFileName(self, "Choose a path and filename", os.getcwd().replace("\\", "/") +
                                            "/data/", filter="Text Files (*.krl);; All Files (*.*)")

        # Тут есть ошибка с библиотекой log4cplus, как то связано с тем, что на компе установлен Autodesk 360
        print('open')
        try:
            f = open(fname[0], 'r')
            # with f:
            data = f.read()
            print(fname)
            print(data)
            self.codeEditor.setPlainText(data)
            f.close()
        except:
            print('KRL not opened')
            pass

    def go_home(self):
        self.servoSlider1.setSliderPosition(0)
        self.servoSlider2.setSliderPosition(0)
        self.servoSlider3.setSliderPosition(0)
        self.servoSlider4.setSliderPosition(0)
        self.servoSlider5.setSliderPosition(0)
        self.servoSlider6.setSliderPosition(0)
        self.servoSlider7.setSliderPosition(0)
        self.servoSlider8.setSliderPosition(0)
        self.move_in_point(['0', '0', '0', '0', '0', '0'])

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
        print('Robot answer >', data[0])
        if data[0] == 'Ok':
            self.robot_moving = False

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
        my_thread.daemon = True
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

        text = ax1 + delimit + ax2 + delimit + ax3 + delimit + ax4 + delimit + ax5 + delimit \
               + ax6 + delimit + gripper + delimit + carousel + '\n'
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

    # TODO: не закончено
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
    def axis_set_func(self):

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
        self.axis_set_func()

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

    def move_in_point(self, point):
        print('point=', point)
        # TODO: цикл выполняется пока все оси не дойдут до своих позиций
        # while 1:
        # self.serialSend(serial, [1, point[0],
        sending_data = [1]
        i = 0
        for a in point:
            sending_data.append(point[i])
            i += 1
        print('sending data', sending_data[-1])
        if sending_data[-1] == ' ':
            sending_data = sending_data[:-1]

        self.robot_moving = True
        self.serial_send(sending_data)

    def scenario_thread(self):
        self.sc_thread = threading.Thread(target=self.start_scenario)
        self.sc_thread.daemon = True
        self.sc_thread.start()
        print('scenario started')

    def finding_longest_way(self, last_axes, new_axes):
        '''
        Поиск самого долгово пути, который пройдет каждый из сервоприводов.
        last_axes: последняя координата(осей)
        new_axes: новая координата (осей)
        '''
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
        last_axes = self.axis_list
        i = 0
        for line in t[:-1]:
            # try:
            line = line.split(delimit)
            print('line', line)
            delay = self.finding_longest_way(last_axes, line)
            last_axes = line
            # serial.close()

            # serial1 = QSerialPort()
            # serial1.setPortName(ui.comboBox.currentText())
            # serial1.open(QIODevice.ReadWrite)
            # serial.setPortName(ui.comboBox.currentText())
            self.move_in_point(line)
            # serial.update()

            # sleep(delay*point_delay)
            while self.robot_moving:
                sleep(0.01)

            i += 1
            print('end of line', i)
            # timer = threading.Timer(3, lambda: move_in_point(line))
            # timer.start()
            # except:
            #     print('incorrect command in text edit')
            #     pass
        send_data = 0
        print('scenario over')

    # KRL part of code

    # Функция-слот сохранения кода
    def KRL_file_saver(self):
        fileName = self.adressLine.text()  # считываем имя файла с адресной строки
        text = self.codeEditor.toPlainText()  # считываем код с текстового входа
        # print('Имя файла: ', fileName)
        # print('Текст файла:, ', text)
        adressTemplate = re.compile(r'^\w+\.krl')  # шаблон адресной строки
        adressStroke = re.match(adressTemplate, fileName)  # совпадение шаблону адресной строки
        if adressStroke:  # если совпало
            code = open(fileName, 'w')  # сохраняем файл
            code.write(text)
            code.close()
            logStroke = 'File ' + fileName + ' is saved'
            self.logShower.setText(logStroke)  # выводим сообщения о сохранении файла
            self.repaint()
        else:  # если не совпало
            logStroke = 'File type error: check file type'
            self.logShower.setText(logStroke)  # выводим сообщение о не совпадении имени или типа фйла
            self.logShower.repaint()

    def scenario_file_saver(self):
        fileName = self.adressLine.text()  # считываем имя файла с адресной строки
        text = self.codeEditor.toPlainText()  # считываем код с текстового входа
        # print('Имя файла: ', fileName)
        # print('Текст файла:, ', text)
        adressTemplate = re.compile(r'^\w+\.krl')  # шаблон адресной строки
        adressStroke = re.match(adressTemplate, fileName)  # совпадение шаблону адресной строки
        if adressStroke:  # если совпало
            code = open(fileName, 'w')  # сохраняем файл
            code.write(text)
            code.close()
            logStroke = 'File ' + fileName + ' is saved'
            self.logShower.setText(logStroke)  # выводим сообщения о сохранении файла
            self.repaint()
        else:  # если не совпало
            logStroke = 'File type error: check file type'
            self.logShower.setText(logStroke)  # выводим сообщение о не совпадении имени или типа фйла
            self.logShower.repaint()

    def parser(self):
        try:
            isObjectCreated = False  # флаг создания объекта
            isVarIniStarted = False  # флаг начала инициализации переменных
            varDictionary = dict()
            varNameDictionary = dict()
            text = self.codeEditor.toPlainText()
            self.textEditScenario.selectAll()
            strokes = text.split('\n')  # Получаем текст в виде списка строк
            defTemplate = re.compile(
                r'^(\s+)?DEF(\s+){1}(?P<objectName>\w{1,24})(\s+)?\((\s+)?(?P<objectParams>(.+)?)\)(\s+)?$')  # Шаблон для объявления объекта
            declTemplate = re.compile(
                r'^(\s+)?DECL(\s+){1}(?P<varType>(INT|REAL|BOOL|CHAR|POS))(\s+){1}(?P<varName>\w{1,24})(\s+)?$')  # Шаблон для объявления переменных
            iniTemplate = re.compile(r'(\s+)?INI(\s+)?')  # Шаблон для начала инициализации переменных
            varTemplate = re.compile(r'^(\s+)?(?P<varIni>\w{1,24})(\s+)?\=(\s+)?(?P<varValue>.+)(\s+)?$')
            ptpCommonTemplate = re.compile(r'^(\s+)?PTP(\s+){1}(?P<pointName>\w{1,24})(\s+)?$')
            linCommonTemplate = re.compile(r'^(\s+)?LIN(\s+){1}(?P<pointName>\w{1,24})(\s+)?$')
            circCommonTemplate = re.compile(r'^(\s+)?CIRC(\s+){1}(?P<auxPoint>\w{1,24}),(\s+){1}(?P<pointName>\w{1,24})$(\s+)?')
            ifTemplate=re.compile(r'^(\s+)?IF(\s+){1}(?P<exeCondition>.+)(\s+){1}THEN(\s+)?$')
            endIfTemplate=re.compile(r'^(\s+)?ENDIF(\s+)?$')

            file = open('coordinates.txt', 'w')
            file.close()
            for i in strokes:
                defStroke = re.match(defTemplate, i)
                declStroke = re.match(declTemplate, i)
                varInit = re.match(varTemplate, i)
                ptpCommonStroke = re.match(ptpCommonTemplate, i)
                linCommonStroke = re.match(linCommonTemplate, i)
                circCommonStroke = re.match(circCommonTemplate, i)
                ifStroke=re.match(ifTemplate, i)
                endIfStroke=re.match(endIfTemplate, i)
                # print(defStroke)
                # print(declStroke)
                # print(varIni)

                if defStroke:
                    objectName = defStroke.group('objectName')
                    objectParams = defStroke.group('objectParams')
                    isObjectCreated = True
                # else:
                # print('Объект не создан')

                if isObjectCreated:
                    # print('Объект создан')
                    if declStroke:
                        # print('Вижу декларирование переменных')
                        varType = declStroke.group('varType')
                        varName = declStroke.group('varName')
                        varDictionary[varName] = varType
                    # else:
                    # print('Переменные не были задекларированы')

                    if iniTemplate:
                        # print('Вижу начало инициализации переменных')
                        isVarIniStarted = True
                    # else:
                    # print('Переменные не были инициализированны')
                    if isVarIniStarted:
                        isIfStarted=False
                        if varInit:
                            #print(i)
                            varId = varInit.group('varIni')
                            varValue = varInit.group('varValue')
                            #print(varId)
                            #print(varValue)
                            name = self.varCorrelator(varId, varValue, varDictionary)[0]
                            value = self.varCorrelator(varId, varValue, varDictionary)[1]
                            varNameDictionary[name] = value
                    if ptpCommonStroke:
                        self.ptpStroke(ptpCommonStroke,varNameDictionary)

                    if linCommonStroke:
                        self.linStroke(linCommonStroke,varNameDictionary)
                    if ifStroke:
                        isIfStarted=True
                        exeCondition=ifStroke.group('exeCondition')
                        self.ifConditionDeterminer(exeCondition)
                    if endIfStroke:
                        isIfStarted=False

            print('Словарь вне функции:', varNameDictionary)
            self.logShower.setText('Compiled!')
        except:
            self.logShower.setText('Compilation error!')

    def ifConditionDeterminer(self, exeCondition):
        #print ('Условие: ', exeCondition)
        conditionTemplate=re.compile(r'^(\s+)?(?P<firstVal>.+)(\s)+(==|<=|>=|<|>)(\s+)?.+(\s+)$')
        conditionMatch=re.match(conditionTemplate, exeCondition)

    def directKinematicsTransformer(self,a1, a2, a3, a4, a5):
        # Параметры Денавита-Хартенберга
        # Если считаем относительно стрелы
        alpha=(-math.pi/2, 0, -math.pi/2, math.pi/2, math.pi/2)
        a=(0, -221.12, 0, 0, 185.52)
        d=(230.6, 0, 0, -224, 0)
        theta=(float(a1)*math.pi/180, float(a2)*math.pi/180+math.pi/2, float(a3)*math.pi/180-math.pi/2, float(a4)*math.pi/180, float(a5)*math.pi/180-math.pi/2)
        # Если считаем относительно сгиба на 90 в третьем джоинте
        '''
        a=(0, -221.12, 0, 0, 185.52)
        alpha=(-math.pi/2, 0, math.pi/2, -math.pi/2, math.pi/2)
        d=(230.6, 0, 0, 224, 0)
        theta=(float(a1)*math.pi/180, float(a2)*math.pi/180+math.pi/2, float(a3)*math.pi/180, float(a4)*math.pi/180, float(a5)*math.pi/180-math.pi/2) 
        '''
        rxList=[]
        ryList=[]
        rzList=[]
        diList = []
        axList = []
        ayList = []
        for i in range (0,5):
            rx=np.array([[1, 0, 0, 0], [0, math.cos(alpha[i]), -math.sin(alpha[i]), 0], [0, math.sin(alpha[i]), math.cos(alpha[i]), 0], [0, 0, 0, 1]])
            rxList.append(rx)
        for i in range (0,5):
            ry=np.array([[math.cos(alpha[i]), 0, math.sin(alpha[i]), 0], [0, 1, 0, 0], [-math.sin(alpha[i]), 0, math.cos(alpha[i]), 0], [0, 0, 0, 1]])
            ryList.append(ry)
        for i in range (0,5):
            rz=np.array([[math.cos(theta[i]), -(math.sin(theta[i])), 0, 0], [math.sin(theta[i]), math.cos(theta[i]), 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
            rzList.append(rz)
        for i in range (0,5):
            di=np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, d[i]], [0, 0, 0, 1]])
            diList.append(di)
        for i in range (0,5):
            ax=np.array([[1, 0, 0, a[i]], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
            axList.append(ax)
        for i in range (0,5):
            ay=np.array([[1, 0, 0, 0], [0, 1, 0, a[i]], [0, 0, 1, 0], [0, 0, 0, 1]])
            ayList.append(ay)
        #print('Список матриц rxaplha: ',rxalphaList)
        #print('Список матриц rzthetta: ', rzthettaList)
        #print('Список матриц di: ', diList)
        #print('Список матриц ai: ', aiList)
        hList=[]

        for i in range (0,5):
            #if i!=2 and i != 3:
            rzdi=np.matmul(rzList[i], diList[i])
            #print('Первая матрица:', rzdi)
            rzdiai=np.matmul(rzdi, axList[i])
            #print('Вторая матрица:',rzdiai)
            h=np.matmul(rzdiai, rxList[i])
            #print('Итоговая матрица:',h)
            hList.append(h)
        #else:
        #if i == 2:
        #    rzdi = np.matmul(rzList[i], diList[i])
        #    rzdiai = np.matmul(rzdi, axList[i])
        #    h = np.matmul(rzdiai, ryList[i])
        #    hList.append(h)
        # if i == 3:
        #  rzdi=np.matmul(rzList[i], diList[i])
        #   rzdiai=np.matmul(rzdi, ayList[i])
        #  h = np.matmul(rzdiai, rxList[i])
        #hList.append(h)
        print('Список итоговых матриц: ', hList)
        unitMatrix=np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
        hTotal=np.matmul(unitMatrix, hList[0])
        #print(h)
        for i in range (1,5):
            hTotal=np.matmul(hTotal, hList[i])

        print('Итоговая матрица преобразований:', hTotal)
        p = []
        for i in range (0,3):
            p.append(round(hTotal[i,3], 2))
        print ('Координаты положения актуатора:', p)
        #x=round(hTotal[0,3], 2)
        #y=round(hTotal[1])
        r=hTotal[0:3, 0:3]
        #print(r)
        r11 = round(r[0,0], 2)
        r12 = round(r[0,1], 2)
        r13 = round(r[0,2], 2)
        r21 = round(r[1,0], 2)
        r22 = round(r[1,1], 2)
        r23 = round(r[1,2], 2)
        r31 = round(r[2,0], 2)
        r32 = round(r[2,1], 2)
        r33 = round(r[2,2], 2)
        #print(r11, r12, r13, r21, r22, r23, r31, r32, r33)
        if r31!=1 and r31!=-1:
            bettaAngle=round(math.degrees(-math.atan2(r31, math.sqrt(1-math.pow(r31,2)))), 2)
            gammaAngle=round(math.degrees(math.atan2(r21, r11)), 2)
            alphaAngle=round(math.degrees(math.atan2(r32, r33)), 2)
            print('Углы Эйлера (r31!=+-1):', gammaAngle, bettaAngle, alphaAngle)
        elif r31==1:
            sumGammaAlpha=round(math.degrees(math.atan2(r13, r23)), 2)
            print('Сумма альфы и гаммы (r31=1): ', sumGammaAlpha)
        elif r31==-1:
            difGammaAlpha=round(math.degrees(-math.atan2(r13, r23)), 2)
            print('Разность гаммы и альфы (r31=-1): ', difGammaAlpha)
        #else:
        #if r31!=0:
        #bettaAngle=round(math.degrees(math.cos(r33)), 2)
        #alphaAngle=round(math.degrees(math.sin(0)), 2)
        #gammaAngle=round(math.degrees(math.atan2(r21, r11)), 2)
        #print('Углы Эйлера (r31!=0):', alphaAngle, bettaAngle, gammaAngle)
        #else:
        #bettaAngle=round(math.degrees(math.cos(r33)), 2)
        #alphaAngle=round(math.degrees(math.sin(0)), 2)
        #gammaAngle=round(math.degrees(math.atan2(-r12, -r11)), 2)
        #print('Углы Эйлера (r33=-1):', alphaAngle, bettaAngle, gammaAngle)

    def ptpStroke(self, ptpCommonStroke, varNameDictionary):
        pointName = ptpCommonStroke.group('pointName')
        motionType = 'PTP'
        #print('Тип движения:', motionType, ', имя точки:', pointName)
        coordinate = self.coordinateParser(pointName, motionType, varNameDictionary)[0]
        motionType = self.coordinateParser(pointName, motionType, varNameDictionary)[1]
        #print('Тип движения:', motionType, ',', 'координаты точки:', coordinate)
        self.angleParser(coordinate, motionType, pointName)
        return (pointName, motionType, coordinate)

    def linStroke(self, linCommonStroke, varNameDictionary):
        pointName = linCommonStroke.group('pointName')
        motionType = 'LIN'
        #print('Тип движения:', motionType, ', имя точки:', pointName)
        coordinate = self.coordinateParser(pointName, motionType, varNameDictionary)[0]
        motionType = self.coordinateParser(pointName, motionType, varNameDictionary)[1]
        #print('Тип движения:', motionType, ',', 'координаты точки:', coordinate)
        self.angleParser(coordinate, motionType, pointName)

    def varCorrelator(self, varId, varValue, varDictionary):
        iniDict = dict()
        boolTemplate = re.compile(r'(TRUE|FALSE)')
        intTemplate = re.compile(r'(\-)?\d+')
        realTemplate = re.compile(r'(\-)?\d+\.\d+')
        charTemplate = re.compile(r'[a-z,A-Z]+')
        posTemplate = re.compile(
            r'\{(\s+)?((X|A1)(\s+){1}\-?\d+\.?(\d+)?)?(\s+)?,?(\s+)?((Y|A2)(\s+){1}\-?\d+\.?(\d+)?)?(\s+)?,?(\s+)?((Z|A3)(\s+){1}\-?\d+\.?(\d+)?)?(\s+)?,?(\s+)?((A|A4)(\s+){1}\-?\d+\.?(\d+)?)?(\s+)?,?(\s+)?((B|A5)(\s+){1}\-?\d+\.?(\d+)?)?(\s+)?,?(\s+)?((C|A6)(\s+){1}\-?\d+\.?(\d+)?)?(\s+)?\}')

        boolVar = re.match(boolTemplate, varValue)
        intVar = re.match(intTemplate, varValue)
        realVal = re.match(realTemplate, varValue)
        charVal = re.match(charTemplate, varValue)
        posVal = re.match(posTemplate, varValue)
        for i in varDictionary.keys():
            if i == varId:
                if boolVar or intVar or realVal or charVal or posVal:
                    iniDict[varId] = varValue
                    name = varId
                    value = varValue
        return (name, value)

    def coordinateParser(self, pointName, motionType, varNameDictionary):
        for i in varNameDictionary.keys():
            if i == pointName:
                coordinate = varNameDictionary[i]
        return (coordinate, motionType)

    def angleParser(self, coordinate, motionType, pointName):
        xyzTemplate = re.compile(
            r'^\{(\s+)?(X(\s+){1}(?P<x>\-?\d{1,3}\.?(\d{1,2})?)(\s+)?,?(\s+)?)?(Y(\s+){1}(?P<y>\-?\d{1,3}\.?(\d{1,2})?)(\s+)?,?(\s+)?)?(Z(\s+){1}(?P<z>\-?\d{1,3}\.?(\d{1,2})?)(\s+)?,?(\s+)?)?(A(\s+){1}(?P<a>\-?\d{1,3}\.?(\d{1,2})?)(\s+)?,?(\s+)?)?(B(\s+){1}(?P<b>\-?\d{1,3}\.?(\d{1,2})?)(\s+)?,?(\s+)?)?(C(\s+){1}(?P<c>\-?\d{1,3}\.?(\d{1,2})?)(\s+)?,?(\s+)?)?(\s+)?\}$')
        angleTemplate = re.compile(
            r'^\{(\s+)?(A1(\s+){1}(?P<a1>\-?\d{1,3}\.?(\d{1,2})?)(\s+)?,?(\s+)?)?(A2(\s+){1}(?P<a2>\-?\d{1,3}\.?(\d{1,2})?)(\s+)?,?(\s+)?)?(A3(\s+){1}(?P<a3>\-?\d{1,3}\.?(\d{1,2})?)(\s+)?,?(\s+)?)?(A4(\s+){1}(?P<a4>\-?\d{1,3}\.?(\d{1,2})?)(\s+)?,?(\s+)?)?(A5(\s+){1}(?P<a5>\-?\d{1,3}\.?(\d{1,2})?)(\s+)?,?(\s+)?)?(A6(\s+){1}(?P<a6>\-?\d{1,3}\.?(\d{1,2})?)(\s+)?,?(\s+)?)?(\s+)?\}$')
        xyzDescription = re.match(xyzTemplate, coordinate)
        angleDescription = re.match(angleTemplate, coordinate)
        file = open('coordinates.txt', 'a')
        #file.write(str(motionType) + ' ')
        #file.write(str(pointName) + ' ')
        if xyzDescription:
            #print('Точка в декартовых координатах')
            file.write('DESC ')
            x = xyzDescription.group('x')
            y = xyzDescription.group('y')
            z = xyzDescription.group('z')
            a = xyzDescription.group('a')
            b = xyzDescription.group('b')
            c = xyzDescription.group('c')
            #print('x', x, ',''y', y, ',''z', z, ',''a', a, ',''b', b, ',''c', c)
            # print(type(x))
            coordinatesList = [x, y, z, a, b, c]
            #print(coordinatesList)
            #print(len(coordinatesList))
            counter = 0
            for i in coordinatesList:

                if counter == len(coordinatesList) - 1:
                    if i is None:
                        #print('Нет последнего значения')
                        file.write('0 ')
                        self.textEditScenario.insertPlainText('0 ')
                    else:
                        #print('Есть последнее значение')
                        file.write(str(i) + ' ')
                        self.textEditScenario.insertPlainText(str(i) + ' ')
                    file.write('\n')
                    self.textEditScenario.insertPlainText('\n')
                    file.close()
                    break
                else:
                    if i is None:
                        #print('Нет значения')
                        file.write('0 ')
                        self.textEditScenario.insertPlainText('0 ')
                    else:
                        #print('Есть значение')
                        file.write(str(i) + ' ')
                        self.textEditScenario.insertPlainText(str(i) + ' ')
                counter += 1
        elif angleDescription:
            #print('Точка в обобщенных координатах')
            #file.write('ANGL ')
            a1 = angleDescription.group('a1')
            a2 = angleDescription.group('a2')
            a3 = angleDescription.group('a3')
            a4 = angleDescription.group('a4')
            a5 = angleDescription.group('a5')
            a6 = angleDescription.group('a6')
            #print('a1', a1, ',''a2', a2, ',''a3', a3, ',''a4', a4, ',''a5', a5, ',''a6', a6)
            coordinatesList = [a1, a2, a3, a4, a5, a6]
            #print(coordinatesList)
            #print(len(coordinatesList))
            counter = 0
            self.directKinematicsTransformer(a1,a2,a3,a4,a5)
            for i in coordinatesList:
                if counter == len(coordinatesList) - 1:
                    if i is None:
                        #print('Нет последнего значения')
                        file.write('0 ')
                        self.textEditScenario.insertPlainText('0 ')
                    else:
                        #print('Есть последнее значение')
                        file.write(str(i) + ' ')
                        self.textEditScenario.insertPlainText(str(i) + ' ')
                    file.write('\n')
                    self.textEditScenario.insertPlainText('\n')
                    file.close()
                    break
                else:
                    if i is None:
                        #print('Нет значения')
                        file.write('0 ')
                        self.textEditScenario.insertPlainText('0 ')
                    else:
                        #print('Есть значение')
                        file.write(str(i) + ' ')
                        self.textEditScenario.insertPlainText(str(i) + ' ')
                counter += 1

def main():
    app = QApplication(sys.argv)  # Новый экземпляр QApplication
    app.setStyle('Fusion')
    window = Optima2Controller()  # Создаём объект класса ExampleApp
    window.setWindowTitle("Optima-2 Controller")
    window.setWindowIcon(QIcon('src/zarnitza64g.ico'))
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение


if __name__ == '__main__':
    main()
