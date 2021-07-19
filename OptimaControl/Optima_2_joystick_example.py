from PyQt5 import QtWidgets, uic, QtGui
from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo
from PyQt5.QtCore import QIODevice
from time import sleep
import sys
from PyQt5.QtWidgets import QMessageBox

# from PyQt5 import QRadioButton



axis_list = [0, 0, 0, 0, 0, 0, 0]

port_busi = 0

app = QtWidgets.QApplication(sys.argv)
app.setStyle('Fusion')
ui = uic.loadUi('src/ui_desig_v0.6.ui')
ui.setWindowTitle("Optima-2 Controller")
ui.setWindowIcon(QtGui.QIcon('src/zarnitza64g.ico'))

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

reply = QMessageBox.question(ui, 'Внимание!',
                             'Для использования геймпада подключите его к компьютеру, и нажмите на нем кнопку "Mode"',
                             QMessageBox.Ok | QMessageBox.Cancel, QMessageBox.Ok)


def onRead():
    rx = serial.readLine()
    rxs = str(rx, 'utf-8').strip()
    data = rxs.split(' ')
    print(data)


def onOpen():
    serial.setPortName(ui.comboBox.currentText())
    answer = serial.open(QIODevice.ReadWrite)
    print('connected to', ui.comboBox.currentText())
    print('answer =', answer)
    if answer:
        ui.connectLabel.setText('Подключено')


def onClose():
    serial.close()
    ui.connectLabel.setText('Нет подключения')


def refreshCOM():
    ports = QSerialPortInfo().availablePorts()
    # ports.clear()
    for port in ports:
        portList.append(port.portName())
        portListDescription.append(port.description())
    print(portList)
    print(portListDescription)
    ui.comboBox.addItems(portListDescription)
    ui.comboBox.clear()
    ui.comboBox.addItems(portList)


def serialSend(data):
    # answer = serial.isBreakEnabled()
    # print('answer =', answer)
    # if answer:
    #     ui.connectLabel.setText('Подключено')
    # else:
    #     ui.connectLabel.setText('Нет подключения')

    txs = ''
    for val in data:
        txs += str(val)
        txs += ','
    txs = txs[:-1]
    txs += ';'


    # global port_busi
    # while port_busi:
    #     sleep(0.01)

    # port_busi = 1
    serial.write(txs.encode())
    # sleep(0.1)
    # port_busi = 0

    # print(txs)


def ledControll(val):

    if val == 2:
        val = 1
    # print('ledControl', val)
    # serialSend(['0', str(val)])
    s = [0, val, 0]
    txs = ''
    for val in s:
        txs += str(val)
        txs += ','
    txs = txs[:-1]
    txs += ';'

    # global port_busi
    # while port_busi:
    #     sleep(0.01)

    # port_busi = 1
    serial.write(txs.encode())
    # sleep(0.1)
    # port_busi = 0


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


def servoControl():
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


# def servoSetFunc(servo):
def servoSetFunc():
    # TODO: поправить конечные положения шаговиков. -90, 90 и тд.
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

        if int(ui.lineEdit_6.text()) > 100:
            ui.lineEdit_6.selectAll()
            ui.lineEdit_6.insert('100')
        if int(ui.lineEdit_6.text()) < 0:
            ui.lineEdit_6.selectAll()
            ui.lineEdit_6.insert('0')
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
ui.connectButton.clicked.connect(onOpen)
ui.ejectButton.clicked.connect(onClose)

# LED 13 control
ui.checkBox_LED_13.stateChanged.connect(ledControll)
# ui.checkBox_LED_14.stateChanged.connect(ledControll)

# Servos control
ui.servoSlider1.valueChanged.connect(servoControl)
ui.servoSlider2.valueChanged.connect(servoControl)
ui.servoSlider3.valueChanged.connect(servoControl)
ui.servoSlider4.valueChanged.connect(servoControl)
ui.servoSlider5.valueChanged.connect(servoControl)
ui.servoSlider6.valueChanged.connect(servoControl)
ui.servoSlider7.valueChanged.connect(servoControl)

# ui.checkBox_servo1.stateChanged.connect(servoCheckBoxControl)
# ui.checkBox_servo2.stateChanged.connect(servoCheckBoxControl)
# ui.checkBox_servo3.stateChanged.connect(servoCheckBoxControl)
# ui.checkBox_servo4.stateChanged.connect(servoCheckBoxControl)
# ui.checkBox_servo5.stateChanged.connect(servoCheckBoxControl)

ui.pushButton_1.clicked.connect(servoSetFunc)
ui.lineEdit.returnPressed.connect(servoSetFunc)
ui.pushButton_2.clicked.connect(servoSetFunc)
ui.lineEdit_2.returnPressed.connect(servoSetFunc)
ui.pushButton_3.clicked.connect(servoSetFunc)
ui.lineEdit_3.returnPressed.connect(servoSetFunc)
ui.pushButton_4.clicked.connect(servoSetFunc)
ui.lineEdit_4.returnPressed.connect(servoSetFunc)
ui.pushButton_5.clicked.connect(servoSetFunc)
ui.lineEdit_5.returnPressed.connect(servoSetFunc)
ui.pushButton_6.clicked.connect(servoSetFunc)
ui.lineEdit_6.returnPressed.connect(servoSetFunc)
ui.pushButton_7.clicked.connect(servoSetFunc)
ui.lineEdit_7.returnPressed.connect(servoSetFunc)

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

servoControl()


# Работа геймпада. Потоки, функции и мэйнлуп для работы геймпада
import threading
# import joystickapi
import msvcrt
import time
import ctypes

try:
    winmmdll = ctypes.WinDLL('winmm.dll')

    # [joyGetNumDevs](https://docs.microsoft.com/en-us/windows/win32/api/joystickapi/nf-joystickapi-joygetnumdevs)
    """
    UINT joyGetNumDevs();
    """
    joyGetNumDevs_proto = ctypes.WINFUNCTYPE(ctypes.c_uint)
    joyGetNumDevs_func = joyGetNumDevs_proto(("joyGetNumDevs", winmmdll))

    # [joyGetDevCaps](https://docs.microsoft.com/en-us/windows/win32/api/joystickapi/nf-joystickapi-joygetdevcaps)
    """
    MMRESULT joyGetDevCaps(UINT uJoyID, LPJOYCAPS pjc, UINT cbjc);

    32 bit: joyGetDevCapsA
    64 bit: joyGetDevCapsW

    sizeof(JOYCAPS): 728
    """
    joyGetDevCaps_proto = ctypes.WINFUNCTYPE(ctypes.c_uint, ctypes.c_uint, ctypes.c_void_p, ctypes.c_uint)
    joyGetDevCaps_param = (1, "uJoyID", 0), (1, "pjc", None), (1, "cbjc", 0)
    joyGetDevCaps_func = joyGetDevCaps_proto(("joyGetDevCapsW", winmmdll), joyGetDevCaps_param)

    # [joyGetPosEx](https://docs.microsoft.com/en-us/windows/win32/api/joystickapi/nf-joystickapi-joygetposex)
    """
    MMRESULT joyGetPosEx(UINT uJoyID, LPJOYINFOEX pji);
    sizeof(JOYINFOEX): 52
    """
    joyGetPosEx_proto = ctypes.WINFUNCTYPE(ctypes.c_uint, ctypes.c_uint, ctypes.c_void_p)
    joyGetPosEx_param = (1, "uJoyID", 0), (1, "pji", None)
    joyGetPosEx_func = joyGetPosEx_proto(("joyGetPosEx", winmmdll), joyGetPosEx_param)
except:
    winmmdll = None


# joystickapi - joyGetNumDevs
def joyGetNumDevs():
    try:
        num = joyGetNumDevs_func()
    except:
        num = 0
    return num


# joystickapi - joyGetDevCaps
def joyGetDevCaps(uJoyID):
    try:
        buffer = (ctypes.c_ubyte * JOYCAPS.SIZE_W)()
        p1 = ctypes.c_uint(uJoyID)
        p2 = ctypes.cast(buffer, ctypes.c_void_p)
        p3 = ctypes.c_uint(JOYCAPS.SIZE_W)
        ret_val = joyGetDevCaps_func(p1, p2, p3)
        ret = (False, None) if ret_val != JOYERR_NOERROR else (True, JOYCAPS(buffer))
    except:
        ret = False, None
    return ret


# joystickapi - joyGetPosEx
def joyGetPosEx(uJoyID):
    try:
        buffer = (ctypes.c_uint32 * (JOYINFOEX.SIZE // 4))()
        buffer[0] = JOYINFOEX.SIZE
        buffer[1] = JOY_RETURNALL
        p1 = ctypes.c_uint(uJoyID)
        p2 = ctypes.cast(buffer, ctypes.c_void_p)
        ret_val = joyGetPosEx_func(p1, p2)
        ret = (False, None) if ret_val != JOYERR_NOERROR else (True, JOYINFOEX(buffer))
    except:
        ret = False, None
    return ret


JOYERR_NOERROR = 0
JOY_RETURNX = 0x00000001
JOY_RETURNY = 0x00000002
JOY_RETURNZ = 0x00000004
JOY_RETURNR = 0x00000008
JOY_RETURNU = 0x00000010
JOY_RETURNV = 0x00000020
JOY_RETURNPOV = 0x00000040
JOY_RETURNBUTTONS = 0x00000080
JOY_RETURNRAWDATA = 0x00000100
JOY_RETURNPOVCTS = 0x00000200
JOY_RETURNCENTERED = 0x00000400
JOY_USEDEADZONE = 0x00000800
JOY_RETURNALL = (JOY_RETURNX | JOY_RETURNY | JOY_RETURNZ | \
                 JOY_RETURNR | JOY_RETURNU | JOY_RETURNV | \
                 JOY_RETURNPOV | JOY_RETURNBUTTONS)


# joystickapi - JOYCAPS
class JOYCAPS:
    SIZE_W = 728
    OFFSET_V = 4 + 32 * 2

    def __init__(self, buffer):
        ushort_array = (ctypes.c_uint16 * 2).from_buffer(buffer)
        self.wMid, self.wPid = ushort_array

        wchar_array = (ctypes.c_wchar * 32).from_buffer(buffer, 4)
        self.szPname = ctypes.cast(wchar_array, ctypes.c_wchar_p).value

        uint_array = (ctypes.c_uint32 * 19).from_buffer(buffer, JOYCAPS.OFFSET_V)
        self.wXmin, self.wXmax, self.wYmin, self.wYmax, self.wZmin, self.wZmax, \
        self.wNumButtons, self.wPeriodMin, self.wPeriodMax, \
        self.wRmin, self.wRmax, self.wUmin, self.wUmax, self.wVmin, self.wVmax, \
        self.wCaps, self.wMaxAxes, self.wNumAxes, self.wMaxButtons = uint_array


# joystickapi - JOYINFOEX
class JOYINFOEX:
    SIZE = 52

    def __init__(self, buffer):
        uint_array = (ctypes.c_uint32 * (JOYINFOEX.SIZE // 4)).from_buffer(buffer)
        self.dwSize, self.dwFlags, \
        self.dwXpos, self.dwYpos, self.dwZpos, self.dwRpos, self.dwUpos, self.dwVpos, \
        self.dwButtons, self.dwButtonNumber, self.dwPOV, self.dwReserved1, self.dwReserved2 = uint_array


# def servoSetFunc(servo):
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
            ui.lineEdit_2.insert('-60')
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
        # print("don't do that!")
        pass


def binding_sticks(x, y, z, table, laser):

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
    if table[0]:
        axis_list[6] -= 5
    if table[1]:
        axis_list[6] += 5
    if laser[0]:
        ledControll(1)
        # ui.checkBox_LED_13.setChecked(True)
    if laser[1]:
        ledControll(0)
        # ui.checkBox_LED_13.setChecked(False)

    # print(axis_list)
    axisSetFunc()


def laser_on():
    ledControll(1)
    ui.checkBox_LED_13.setChecked(True)


def laser_off():
    ledControll(0)
    ui.checkBox_LED_13.setChecked(False)


def gamepad_thread():
    print("start of gamepad script")

    # num = joystickapi.joyGetNumDevs()
    num = joyGetNumDevs()
    ret, caps, startinfo = False, None, None
    for id in range(num):
        ret, caps = joyGetDevCaps(id)
        if ret:
            print("gamepad detected: " + caps.szPname)
            ret, startinfo = joyGetPosEx(id)
            break
    else:
        print("no gamepad detected")

    run = ret
    while run:
        time.sleep(0.1)
        if msvcrt.kbhit() and msvcrt.getch() == chr(27).encode():  # detect ESC
            run = False

        ret, info = joyGetPosEx(id)
        if ret:
            btns = [(1 << i) & info.dwButtons != 0 for i in range(caps.wNumButtons)]
            axisXYZ = [info.dwXpos - startinfo.dwXpos, info.dwYpos - startinfo.dwYpos, info.dwZpos - startinfo.dwZpos]
            axisRUV = [info.dwRpos - startinfo.dwRpos, info.dwUpos - startinfo.dwUpos, info.dwVpos - startinfo.dwVpos]
            if info.dwButtons:
                # print("buttons: ", btns)
                binding_sticks([0, 0], [0, 0], [btns[0], btns[1], btns[2], btns[3]],
                               table=[btns[6], btns[7]], laser=[btns[5],btns[4]])
                # if btns[5]:
                #     # print('LASER ON')
                #     laser_on()
                # if btns[4]:
                #     # print('LASER OFF')
                #     laser_off()
                #
                # if btns[6]:
                #     # print('rotate С left')
                #     pass
                # if btns[7]:
                #     # print('rotate С right')
                #     pass

            if any([abs(v) > 10 for v in axisXYZ]):
                # print("axis:", axisXYZ)
                binding_sticks([axisXYZ[0], axisXYZ[1]], [axisXYZ[2], 0], [0, 0, 0, 0], table=[0, 0], laser=[0,0])
            if any([abs(v) > 10 for v in axisRUV]):
                # print("roation axis:", axisRUV)
                binding_sticks([0, 0], [0, axisRUV[0]], [0, 0, 0, 0], table=[0, 0], laser=[0,0])


my_thread = threading.Thread(target=gamepad_thread )
my_thread.start()


ui.show()
sys.exit(app.exec_())

# serial.close()

# app.exit()
