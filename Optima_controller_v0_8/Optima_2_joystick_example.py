from PyQt5 import QtWidgets, uic
from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo
from PyQt5.QtCore import QIODevice, QThread
from time import sleep
import threading
import joystickapi
import msvcrt
import time
import sys

# from PyQt5 import QRadioButton


scenario_work = False

axis_list = [0, 0, 0, 0, 0, 0, 0]

app = QtWidgets.QApplication([])
app.setStyle('Fusion')
ui = uic.loadUi('Optima_2_controller_v0.6.ui')
ui.setWindowTitle("Optima-2 Controller")

serial = QSerialPort()
serial.setBaudRate(115200)
portList = []
portListDescription = ['Выберите устройство']
ports = QSerialPortInfo().availablePorts()
for port in ports:
    portList.append(port.portName())
    portListDescription.append(port.description())
print(portList)
print(portListDescription)
# ui.comboBox.addItems(portListDescription)
ui.comboBox.addItems(portList)


def onRead():
    rx = serial.readLine()
    rxs = str(rx, 'utf-8').strip()
    data = rxs.split(' ')
    print(data)


def onOpen2():
    serial.setPortName(ui.comboBox.currentText())
    answer = serial.open(QIODevice.ReadWrite)
    print('connected to', ui.comboBox.currentText())
    print('answer =', answer)
    if answer:
        ui.connectLabel.setText('Подключено')

    while 1:
        sleep(0.01)
    # sleep(2)
    # serialSend([1, 50, 0, 0, 0, 0, 0, 0, 0])

def onOpen1():
    my_thread = threading.Thread(target=onOpen2)
    my_thread.start()
    # ui.connectLabel.setText('Подключено')



def onClose():
    serial.close()
    ui.connectLabel.setText('Нет подключения')


def refreshCOM():
    ports = QSerialPortInfo().availablePorts()
    ports.clear()
    for port in ports:
        portList.append(port.portName())
        portListDescription.append(port.description())
    print(portList)
    print(portListDescription)
    # ui.comboBox.addItems(portListDescription)
    ui.comboBox.clear()
    ui.comboBox.addItems(portList)


def serialSend(data):

    txs = ''
    for val in data:
        txs += str(val)
        txs += ','
    txs = txs[:-1]
    txs += ';'
    serial.write(txs.encode())
    serial.waitForBytesWritten(1)
    print("serial send", txs)


def ledControll(val):
    if val == 2:
        val = 1
    print('ledControl', val)
    # serialSend(['0', str(val)])
    s = [0, val, 0]
    txs = ''
    for val in s:
        txs += str(val)
        txs += ','
    txs = txs[:-1]
    txs += ';'

    serial.write(txs.encode())


def DFPlayer():
    button = ui.sender
    try:
        print(button.text)
    except:
        pass


def RGB_control():
    # r = int(ui.slider_r.value()*ui.light_slider.value()/100)
    # print('r =', ui.light_slider.value())
    serialSend([2, int(ui.slider_r.value() * ui.light_slider.value() / 100),
                int(ui.slider_g.value() * ui.light_slider.value() / 100),
                int(ui.slider_b.value() * ui.light_slider.value() / 100), 5])


def axis_control():
    ui.lineEdit.selectAll()
    ui.lineEdit.insert(str(ui.servoSlider1.value()))
    ui.lineEdit_2.selectAll()
    ui.lineEdit_2.insert(str(ui.servoSlider2.value()))
    ui.lineEdit_3.selectAll()
    ui.lineEdit_3.insert(str(ui.servoSlider3.value()))
    ui.lineEdit_4.selectAll()
    ui.lineEdit_4.insert(str(ui.servoSlider4.value()))
    ui.lineEdit_5.selectAll()
    ui.lineEdit_5.insert(str(ui.servoSlider5.value()))
    ui.lineEdit_6.selectAll()
    ui.lineEdit_6.insert(str(ui.servoSlider6.value()))
    ui.lineEdit_7.selectAll()
    ui.lineEdit_7.insert(str(ui.servoSlider7.value()))

    setAxisListTo()

    serialSend([1, ui.servoSlider1.value(),
                ui.servoSlider2.value(),
                ui.servoSlider3.value(),
                ui.servoSlider4.value(),
                ui.servoSlider5.value(),
                ui.servoSlider6.value(),
                ui.servoSlider7.value(), 0])


'''
# no using
def servoCheckBoxControl(val):
    # if val == 2: val = 1;
    print('checkBoxControl', str(ui.checkBox_servo1.isChecked()))
    serialSend(['3', int(ui.checkBox_servo1.isChecked()),
                int(ui.checkBox_servo2.isChecked()),
                int(ui.checkBox_servo3.isChecked()),
                int(ui.checkBox_servo4.isChecked()),
                int(ui.checkBox_servo5.isChecked())])
'''


# def axis_set_func(servo):
def axis_set_func():
    try:
        if int(ui.lineEdit.text()) > 120:
            ui.lineEdit.selectAll()
            ui.lineEdit.insert('120')
        if int(ui.lineEdit.text()) < -120:
            ui.lineEdit.selectAll()
            ui.lineEdit.insert('-120')
        ui.servoSlider1.setSliderPosition(int(ui.lineEdit.text()))

        if int(ui.lineEdit_2.text()) > 120:
            ui.lineEdit_2.selectAll()
            ui.lineEdit_2.insert('120')
        if int(ui.lineEdit_2.text()) < -60:
            ui.lineEdit_2.selectAll()
            ui.lineEdit_2.insert('-60')
        ui.servoSlider2.setSliderPosition(int(ui.lineEdit_2.text()))

        if int(ui.lineEdit_3.text()) > 120:
            ui.lineEdit_3.selectAll()
            ui.lineEdit_3.insert('120')
        if int(ui.lineEdit_3.text()) < -60:
            ui.lineEdit_3.selectAll()
            ui.lineEdit_3.insert('-60')
        ui.servoSlider3.setSliderPosition(int(ui.lineEdit_3.text()))

        if int(ui.lineEdit_4.text()) > 90:
            ui.lineEdit_4.selectAll()
            ui.lineEdit_4.insert('90')
        if int(ui.lineEdit_4.text()) < -90:
            ui.lineEdit_4.selectAll()
            ui.lineEdit_4.insert('-90')
        ui.servoSlider4.setSliderPosition(int(ui.lineEdit_4.text()))

        if int(ui.lineEdit_5.text()) > 90:
            ui.lineEdit_5.selectAll()
            ui.lineEdit_5.insert('90')
        if int(ui.lineEdit_5.text()) < -90:
            ui.lineEdit_5.selectAll()
            ui.lineEdit_5.insert('-90')
        ui.servoSlider5.setSliderPosition(int(ui.lineEdit_5.text()))

        if int(ui.lineEdit_6.text()) > 90:
            ui.lineEdit_6.selectAll()
            ui.lineEdit_6.insert('90')
        if int(ui.lineEdit_6.text()) < -90:
            ui.lineEdit_6.selectAll()
            ui.lineEdit_6.insert('-90')
        ui.servoSlider6.setSliderPosition(int(ui.lineEdit_6.text()))

        if int(ui.lineEdit_7.text()) > 360:
            ui.lineEdit_7.selectAll()
            ui.lineEdit_7.insert('360')
        if int(ui.lineEdit_7.text()) < -360:
            ui.lineEdit_7.selectAll()
            ui.lineEdit_7.insert('-360')
        ui.servoSlider7.setSliderPosition(int(ui.lineEdit_7.text()))

        setAxisListTo()
    except:
        print("don't do that!")


def setAxisListTo():
    global axis_list
    axis_list[0] = int(ui.lineEdit.text())
    axis_list[1] = int(ui.lineEdit_2.text())
    axis_list[2] = int(ui.lineEdit_3.text())
    axis_list[3] = int(ui.lineEdit_4.text())
    axis_list[4] = int(ui.lineEdit_5.text())
    axis_list[5] = int(ui.lineEdit_6.text())
    axis_list[6] = int(ui.lineEdit_7.text())


# Serial connections
serial.readyRead.connect(onRead)
ui.refreshCOMbutton.clicked.connect(refreshCOM)
ui.connectButton.clicked.connect(onOpen1)
ui.ejectButton.clicked.connect(onClose)

# LED 13 control
ui.checkBox_LED_13.stateChanged.connect(ledControll)
# ui.checkBox_LED_14.stateChanged.connect(ledControll)

# Servos control
ui.servoSlider1.valueChanged.connect(axis_control)
ui.servoSlider2.valueChanged.connect(axis_control)
ui.servoSlider3.valueChanged.connect(axis_control)
ui.servoSlider4.valueChanged.connect(axis_control)
ui.servoSlider5.valueChanged.connect(axis_control)
ui.servoSlider6.valueChanged.connect(axis_control)
ui.servoSlider7.valueChanged.connect(axis_control)

# ui.checkBox_servo1.stateChanged.connect(servoCheckBoxControl)
# ui.checkBox_servo2.stateChanged.connect(servoCheckBoxControl)
# ui.checkBox_servo3.stateChanged.connect(servoCheckBoxControl)
# ui.checkBox_servo4.stateChanged.connect(servoCheckBoxControl)
# ui.checkBox_servo5.stateChanged.connect(servoCheckBoxControl)

ui.pushButton_1.clicked.connect(axis_set_func)
ui.lineEdit.returnPressed.connect(axis_set_func)
ui.pushButton_2.clicked.connect(axis_set_func)
ui.lineEdit_2.returnPressed.connect(axis_set_func)
ui.pushButton_3.clicked.connect(axis_set_func)
ui.lineEdit_3.returnPressed.connect(axis_set_func)
ui.pushButton_4.clicked.connect(axis_set_func)
ui.lineEdit_4.returnPressed.connect(axis_set_func)
ui.pushButton_5.clicked.connect(axis_set_func)
ui.lineEdit_5.returnPressed.connect(axis_set_func)
ui.pushButton_6.clicked.connect(axis_set_func)
ui.lineEdit_6.returnPressed.connect(axis_set_func)
ui.pushButton_7.clicked.connect(axis_set_func)
ui.lineEdit_7.returnPressed.connect(axis_set_func)

# RGB control
ui.slider_r.valueChanged.connect(RGB_control)
ui.slider_g.valueChanged.connect(RGB_control)
ui.slider_b.valueChanged.connect(RGB_control)
ui.light_slider.valueChanged.connect(RGB_control)

# DFPlayer binding
ui.radioButton_1.toggled.connect(DFPlayer)
ui.radioButton_2.toggled.connect(DFPlayer)
ui.radioButton_3.toggled.connect(DFPlayer)
ui.radioButton_4.toggled.connect(DFPlayer)
ui.radioButton_5.toggled.connect(DFPlayer)
ui.radioButton_mute.toggled.connect(DFPlayer)

axis_control()

prject_name = 'newOptimaProject'


def add_point_in_scenario():
    ax1 = (ui.lineEdit.text())
    ax2 = (ui.lineEdit_2.text())
    ax3 = (ui.lineEdit_3.text())
    ax4 = (ui.lineEdit_4.text())
    ax5 = (ui.lineEdit_5.text())
    ax6 = (ui.lineEdit_6.text())
    carousel = (ui.lineEdit_7.text())

    text = ax1 + ',' + ax2 + ',' + ax3 + ',' + ax4 + ',' + ax5 + ',' + ax6 + ',' + carousel + '\n'
    print('add scenario point', text)
    ui.textEditScenario.insertPlainText(text)


# ui.textEdit.insertPlainText('text')

def move_in_point(point, serial):
    print('point=',point)
    # TODO: цикл выполняется пока все оси не дойдут до своих позиций
    # while 1:
    serialSend([1, point[0],
                point[1],
                point[2],
                point[3],
                point[4],
                point[5],
                0, 0])
    # serial.update()
    # print([1, point[0], point[1], point[2], point[3], point[4], point[5]])


def scenario_thread():
    sc_thread = threading.Thread(target=start_scenario)
    sc_thread.start()
    print('scenario started')

send_data = 0
def start_scenario():
    global send_data
    send_data = 1
    # print('thread')
    text = ui.textEditScenario.toPlainText()
    print(text)
    t = text.split('\n')
    # print(t)
    # serial.close()
    # onClose()
    QThread.sleep(1)
    onOpen1()
    # serial.open(QIODevice.ReadWrite)
    for line in t[:-1]:
        # try:
        line = line.split(',')
        print('line', line)
        QThread.sleep(3)
        # serial.close()

        # serial1 = QSerialPort()
        # serial1.setPortName(ui.comboBox.currentText())
        # serial1.open(QIODevice.ReadWrite)
        # serial.setPortName(ui.comboBox.currentText())
        move_in_point(line, serial)
        # serial.update()

        # timer = threading.Timer(3, lambda: move_in_point(line))
        # timer.start()
        # except:
        #     print('incorrect command in text edit')
        #     pass
    print('scenario over')
    send_data = 0
    # serial.open()
# ---------------------------------------------------------------------------



#
# class Thread(QThread):
#
#     def __init__(self):
#         super().__init__()
#
#     def run(self):
#         # print('thread')
#         text = ui.textEditScenario.toPlainText()
#         print(text)
#         t = text.split('\n')
#         # print(t)
#         for line in t[-1]:
#             # try:
#             line = line.split(',')
#             print('line', line)
#             sleep(3)
#             # move_in_point(line)
#             timer = threading.Timer(3, lambda: move_in_point(line))
#             timer.start()
#             # except:
#             #     print('incorrect command in text edit')
#             #     pass
#
#
#
# def scenario_thread():
#     # Создать новую тему
#     thread = Thread()
#     thread.start()


ui.addPointButton.clicked.connect(add_point_in_scenario)
ui.startScenarioButton.clicked.connect(scenario_thread)


# Работа геймпада. Потоки, функции и мэйнлуп для работы геймпада

# def axis_set_func(servo):
def axisSetFunc():
    global axis_list
    try:
        if int(axis_list[0]) > 120:
            axis_list[0] = 120
            ui.lineEdit.selectAll()
            ui.lineEdit.insert('120')
        if int(axis_list[0]) < -120:
            axis_list[0] = -120
            ui.lineEdit.selectAll()
            ui.lineEdit.insert('-120')
        ui.servoSlider1.setSliderPosition(int(axis_list[0]))

        if int(axis_list[1]) > 120:
            axis_list[1] = 120
            ui.lineEdit_2.selectAll()
            ui.lineEdit_2.insert('120')
        if int(axis_list[1]) < -60:
            axis_list[1] = -60
            ui.lineEdit_2.selectAll()
            ui.lineEdit_2.insert('0')
        ui.servoSlider2.setSliderPosition(int(axis_list[1]))

        if int(axis_list[2]) > 120:
            axis_list[2] = 120
            ui.lineEdit_3.selectAll()
            ui.lineEdit_3.insert('120')
        if int(axis_list[2]) < -60:
            axis_list[2] = -60
            ui.lineEdit_3.selectAll()
            ui.lineEdit_3.insert('-60')
        ui.servoSlider3.setSliderPosition(int(axis_list[2]))

        if int(axis_list[3]) > 90:
            axis_list[3] = 90
            ui.lineEdit_4.selectAll()
            ui.lineEdit_4.insert('90')
        if int(axis_list[3]) < -90:
            axis_list[3] = -90
            ui.lineEdit_4.selectAll()
            ui.lineEdit_4.insert('-90')
        ui.servoSlider4.setSliderPosition(int(axis_list[3]))

        if int(axis_list[4]) > 90:
            axis_list[4] = 90
            ui.lineEdit_5.selectAll()
            ui.lineEdit_5.insert('90')
        if int(axis_list[4]) < -90:
            axis_list[4] = -90
            ui.lineEdit_5.selectAll()
            ui.lineEdit_5.insert('-90')
        ui.servoSlider5.setSliderPosition(int(axis_list[4]))

        if int(axis_list[5]) > 100:
            axis_list[5] = 100
            ui.lineEdit_6.selectAll()
            ui.lineEdit_6.insert('100')
        if int(axis_list[5]) < 0:
            axis_list[5] = 0
            ui.lineEdit_6.selectAll()
            ui.lineEdit_6.insert('0')
        ui.servoSlider6.setSliderPosition(int(axis_list[5]))

        if int(axis_list[6]) > 360:
            axis_list[6] = 360
            ui.lineEdit_7.selectAll()
            ui.lineEdit_7.insert('360')
        if int(axis_list[6]) < -360:
            axis_list[6] = -360
            ui.lineEdit_7.selectAll()
            ui.lineEdit_7.insert('-360')
        ui.servoSlider7.setSliderPosition(int(axis_list[6]))

    except:
        print("don't do that!")


def binding_sticks(x, y, z):
    global axis_list

    if x[0] != 0:
        axis_list[0] += round(x[0] / 32768)
    if x[1] != 0:
        axis_list[1] -= round(x[1] / 32768)
    if y[0] != 0:
        axis_list[3] += round(y[0] / 32768)
    if y[1] != 0:
        axis_list[2] -= round(y[1] / 32768)
    if z[0] != True:
        axis_list[4] -= 1
    if z[2] != True:
        axis_list[4] += 1
    if z[1] != True:
        axis_list[5] -= 5
    if z[3] != True:
        axis_list[5] += 5

    print(axis_list)
    axisSetFunc()
    pass


def gamepad_thread():
    print("start of gamepad script")

    num = joystickapi.joyGetNumDevs()
    ret, caps, startinfo = False, None, None
    for id in range(num):
        ret, caps = joystickapi.joyGetDevCaps(id)
        if ret:
            print("gamepad detected: " + caps.szPname)
            ret, startinfo = joystickapi.joyGetPosEx(id)
            break
    else:
        print("no gamepad detected")

    run = ret
    while run:
        if send_data == 0:
            time.sleep(0.1)
            if msvcrt.kbhit() and msvcrt.getch() == chr(27).encode():  # detect ESC
                run = False

            ret, info = joystickapi.joyGetPosEx(id)
            if ret:
                btns = [(1 << i) & info.dwButtons != 0 for i in range(caps.wNumButtons)]
                axisXYZ = [info.dwXpos - startinfo.dwXpos, info.dwYpos - startinfo.dwYpos, info.dwZpos - startinfo.dwZpos]
                axisRUV = [info.dwRpos - startinfo.dwRpos, info.dwUpos - startinfo.dwUpos, info.dwVpos - startinfo.dwVpos]
                if info.dwButtons:
                    # print("buttons: ", btns)
                    binding_sticks([0, 0], [0, 0], [btns[0], btns[1], btns[2], btns[3]])
                if any([abs(v) > 10 for v in axisXYZ]):
                    # print("axis:", axisXYZ)
                    binding_sticks([axisXYZ[0], axisXYZ[1]], [axisXYZ[2], 0], [0, 0, 0, 0])
                if any([abs(v) > 10 for v in axisRUV]):
                    # print("roation axis:", axisRUV)
                    binding_sticks([0, 0], [0, axisRUV[0]], [0, 0, 0, 0])


my_thread = threading.Thread(target=gamepad_thread)
my_thread.start()

ui.show()
sys.exit(app.exec())

# serial.close()
