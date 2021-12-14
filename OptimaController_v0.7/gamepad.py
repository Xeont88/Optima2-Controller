
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

        if int(axis_list[5]) > 90:
            axis_list[5] = 90
            ui.lineEdit_6.selectAll()
            ui.lineEdit_6.insert('90')
        if int(axis_list[5]) < -90:
            axis_list[5] = -90
            ui.lineEdit_6.selectAll()
            ui.lineEdit_6.insert('-90')
        ui.servoSlider6.setSliderPosition(int(axis_list[5]))

        if int(axis_list[6]) > 100:
            axis_list[6] = 100
            ui.lineEdit_7.selectAll()
            ui.lineEdit_7.insert('100')
        if int(axis_list[6]) < 0:
            axis_list[6] = 0
            ui.lineEdit_7.selectAll()
            ui.lineEdit_7.insert('0')
        ui.servoSlider7.setSliderPosition(int(axis_list[6]))

        if int(axis_list[7]) > 360:
            axis_list[7] = 360
            ui.lineEdit_8.selectAll()
            ui.lineEdit_8.insert('360')
        if int(axis_list[7]) < -360:
            axis_list[7] = -360
            ui.lineEdit_8.selectAll()
            ui.lineEdit_8.insert('-360')
        ui.servoSlider8.setSliderPosition(int(axis_list[7]))

    except:
        # print("don't do that!")
        pass


def binding_sticks(x, y, z, table, axis_6):

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
        axis_list[4] += 1
    if z[2] != True:
        axis_list[4] -= 1
    if z[1] != True:
        axis_list[5] += 1
    if z[3] != True:
        axis_list[5] -= 1
    if table[0]:
        axis_list[7] -= round(table[0] / 32768) * 5
    if axis_6[0]:
        axis_list[6] += 5
        # ui.checkBox_LED_13.setChecked(True)
    if axis_6[1]:
        axis_list[6] -= 5
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
                binding_sticks(x=[0, 0], y=[0, 0], z=[btns[0], btns[2], btns[1], btns[3]],
                               table=[btns[6], btns[7]], axis_6=[btns[5],btns[4]])

            if any([abs(v) > 10 for v in axisXYZ]):
                # print("axis:", axisXYZ)
                binding_sticks(x=[axisXYZ[0], axisXYZ[1]], y=[0, 0], z=[0, 0, 0, 0], table=[axisXYZ[2], 0], axis_6=[0,0])
            if any([abs(v) > 10 for v in axisRUV]):
                # print("roation axis:", axisRUV)
                binding_sticks(x=[0, 0], y=[axisRUV[1], axisRUV[0]], z=[0, 0, 0, 0], table=[0, 0], axis_6=[0,0])


my_thread = threading.Thread(target=gamepad_thread )
my_thread.start()
