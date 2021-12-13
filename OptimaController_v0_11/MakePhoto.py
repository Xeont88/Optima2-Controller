import os
import numpy as np
import cv2 as cv
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox
# class MakePhoto:

def make_photo():
    cap = cv.VideoCapture(0)
    cap.open(cv.CAP_DSHOW)
    # take first frame of the video
    i = 0

    while True:
        ret,frame = cap.read()
        if ret:
            cv.imshow('Press Space for Photo, Press Esc for Exit', frame)

            k = cv.waitKey(1)
            print(k)
            if k == 27:
                break
            if k == 32:
                i += 1
                filename = QtWidgets.QFileDialog.getSaveFileName()
                # filename = str(filename)
                if filename[0]:
                    filename = filename[0]
                    # filename = filename.replace('/', '\\')
                    name = filename[filename.rfind('/')+1:]
                    name = name + '.jpg'
                    path = filename[:filename.rfind('/')]

                    print (path, name)
                    os.chdir(path)
                    cv.imwrite(name, frame)
                    # break

    cv.destroyAllWindows()
    cap.release()
