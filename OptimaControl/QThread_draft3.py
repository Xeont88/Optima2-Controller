from PyQt5.QtCore import QThread
from time import sleep


class Thread(QThread):

    def __init__(self):
        super().__init__()

    def run(self):
        i=0
        while 1:
            i+=1
            print(i)
            sleep(1)
        pass


# Создать новую тему
thread = Thread()
thread.start()



while 1:
    print('hellohellohellohellohellohellohellohellohellohellohellohello')
    sleep(1.5)