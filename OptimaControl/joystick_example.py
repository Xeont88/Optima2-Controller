import joystickapi
import msvcrt
import time

print("start")

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


axes_list = [0, 0, 0, 0, 0, 0]


def binding_sticks(x, y, z):

    global axes_list

    if x[0] != 0:
        axes_list[0] += round(x[0] / 32768)
    if x[1] != 0:
        axes_list[1] -= round(x[1] / 32768)
    if y[0] != 0:
        axes_list[2] += round(y[0] / 32768)
    if y[1] != 0:
        axes_list[3] -= round(y[1] / 32768)
    if z[0] != True:
        axes_list[4] -= 1
    if z[2] != True:
        axes_list[4] += 1
    if z[1] != True:
        axes_list[5] -= 1
    if z[3] != True:
        axes_list[5] += 1

    print(axes_list)

run = ret
while run:
    time.sleep(0.1)
    if msvcrt.kbhit() and msvcrt.getch() == chr(27).encode(): # detect ESC
        run = False

    ret, info = joystickapi.joyGetPosEx(id)
    if ret:
        btns = [(1 << i) & info.dwButtons != 0 for i in range(caps.wNumButtons)]
        axisXYZ = [info.dwXpos-startinfo.dwXpos, info.dwYpos-startinfo.dwYpos, info.dwZpos-startinfo.dwZpos]
        axisRUV = [info.dwRpos-startinfo.dwRpos, info.dwUpos-startinfo.dwUpos, info.dwVpos-startinfo.dwVpos]
        if info.dwButtons:
            print("buttons: ", btns)
            binding_sticks([0,0], [0,0], [btns[0], btns[1], btns[2], btns[3]])

            if btns[5]:
                print('LASER ON')
            if btns[4]:
                print('LASER OFF')


        if any([abs(v) > 10 for v in axisXYZ]):
            # print("axis:", axisXYZ)
            binding_sticks([axisXYZ[0], axisXYZ[1]], [axisXYZ[2], 0], [0,0,0,0])
        if any([abs(v) > 10 for v in axisRUV]):
            # print("roation axis:", axisRUV)
            binding_sticks([0,0], [0, axisRUV[0]], [0,0,0,0])

print("end")
