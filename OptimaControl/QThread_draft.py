import sys
import traceback

from PyQt5.QtCore import (QCoreApplication, QObject, QRunnable, QThread,
                          QThreadPool, pyqtSignal, pyqtSlot)
from PyQt5 import Qt


# Если при ошибке в слотах приложение просто падает без стека,
# есть хороший способ ловить такие ошибки:
def log_uncaught_exceptions(ex_cls, ex, tb):
    text = '{}: {}:\n'.format(ex_cls.__name__, ex)
    #import traceback
    text += ''.join(traceback.format_tb(tb))

    print(text)
    Qt.QMessageBox.critical(None, 'Error', text)
    quit()
sys.excepthook = log_uncaught_exceptions


class WorkerSignals(QObject):
    ''' Определяет сигналы, доступные из рабочего рабочего потока Worker(QRunnable).'''

    finish   = pyqtSignal()
    error    = pyqtSignal(tuple)
    result   = pyqtSignal(object)
    progress = pyqtSignal(int)


class Worker(QRunnable):
    ''' Наследует от QRunnable, настройки рабочего потока обработчика, сигналов и wrap-up. '''

    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()

        # Хранить аргументы конструктора (повторно используемые для обработки)
        self.fn      = fn
        self.args    = args
        self.kwargs  = kwargs
        self.signals = WorkerSignals()
        print("\nfn=`{}`, \nargs=`{}`, kwargs=`{}`, \nself.signals=`{}`"\
              .format(fn, args, kwargs, self.signals))

        #== Добавьте обратный вызов в наши kwargs ====================================###
        kwargs['progress_callback'] = self.signals.progress
        print("kwargs['progress_callback']->`{}`\n".format(kwargs['progress_callback']))

    @pyqtSlot()
    def run(self):
        # Получите args/kwargs здесь; и обработка с их использованием
        try:                       # выполняем метод `execute_this_fn` переданный из Main
            result = self.fn(*self.args, **self.kwargs)
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:  # если ошибок не была, испускаем сигнал .result и передаем результат `result`
            self.signals.result.emit(result)      # Вернуть результат обработки
        finally:
            self.signals.finish.emit()            # Done / Готово


# Подклассификация QThread
# http://qt-project.org/doc/latest/qthread.html
class AThread(QThread):
    threadSignalAThread = pyqtSignal(int)
    def __init__(self):
        super().__init__()

    def run(self):
        count = 0
        while count < 1000:
            #time.sleep(1)
            Qt.QThread.msleep(200)
            count += 1
            self.threadSignalAThread.emit(count)


# Подкласс QObject и использование moveToThread
class SomeObject(QObject):

    finishedSomeObject     = pyqtSignal()
    threadSignalSomeObject = pyqtSignal(int)

    def long_running(self):
        print('SomeObject(QObject) id', int(QThread.currentThreadId()))
        count = 0
        while count < 150:
            Qt.QThread.msleep(100)
            count += 1
            self.threadSignalSomeObject.emit(count)

        self.finishedSomeObject.emit()


class MsgBoxAThread(Qt.QDialog):
    """ Класс инициализации окна для визуализации дополнительного потока
        и кнопка для закрытия потокового окна, если поток остановлен! """

    def __init__(self):
        super().__init__()

        layout     = Qt.QVBoxLayout(self)
        self.label = Qt.QLabel("")
        layout.addWidget(self.label)

        close_btn  = Qt.QPushButton("Close Окно")
        layout.addWidget(close_btn)

        # ------- Сигнал   это только закроет окно, поток как работал, так и работает
        close_btn.clicked.connect(self.close)

        self.setGeometry(900, 65, 400, 80)
        self.setWindowTitle('MsgBox AThread(QThread)')


class MsgBoxSomeObject(Qt.QDialog):
    def __init__(self):
        super().__init__()

        layout     = Qt.QVBoxLayout(self)
        self.label = Qt.QLabel("")
        layout.addWidget(self.label)

        close_btn  = Qt.QPushButton("Close Окно")
        layout.addWidget(close_btn)

        # ------- Сигнал   это только закроет окно, поток как работал, так и работает
        close_btn.clicked.connect(self.close)

        self.setGeometry(900, 185, 400, 80)
        self.setWindowTitle('MsgBox SomeObject(QObject)')


class MsgBoxWorker(Qt.QDialog):
    def __init__(self):
        super().__init__()

        layout     = Qt.QVBoxLayout(self)
        self.label = Qt.QLabel("")
        layout.addWidget(self.label)

        close_btn  = Qt.QPushButton("Close Окно")
        layout.addWidget(close_btn)

        # ------- Сигнал   это только закроет окно, поток как работал, так и работает
        close_btn.clicked.connect(self.close)

        self.setGeometry(900, 300, 400, 80)
        self.setWindowTitle('MsgBox Worker(QRunnable)')


class ExampleThread(Qt.QWidget):
    def __init__(self, parent=None):
        super(ExampleThread, self).__init__(parent)

        layout     = Qt.QVBoxLayout(self)
        self.lbl = Qt.QLabel("Start")
        layout.addWidget(self.lbl)
        self.btnA = Qt.QPushButton("Запустить AThread(QThread)")
        layout.addWidget(self.btnA)
        self.btnB = Qt.QPushButton("Запустить SomeObject(QObject)")
        layout.addWidget(self.btnB)
        self.btnC = Qt.QPushButton("Запустить Worker(QRunnable)")
        layout.addWidget(self.btnC)
        self.progressBar = Qt.QProgressBar()
        self.progressBar.setProperty("value", 0)
        layout.addWidget(self.progressBar)

        self.setGeometry(550, 65, 300, 300)
        self.setWindowTitle('3 разных и простых способа работы с потоками.')


        self.btnA.clicked.connect(self.using_q_thread)
        self.btnB.clicked.connect(self.using_move_to_thread)
        self.btnC.clicked.connect(self.using_q_runnable)

        self.msg       = MsgBoxAThread()
        self.thread    = None

        self.msgSomeObject = MsgBoxSomeObject()
        self.objThread     = None

        self.counter = 0
        self.timer = Qt.QTimer()
        self.timer.setInterval(1000)
        # -------- timeout -------> def recurring_timer(self):
        self.timer.timeout.connect(self.recurring_timer)
        self.timer.start()

        self.threadpool = QThreadPool()
        print("Max потоков, кот. будут использоваться=`%d`" % self.threadpool.maxThreadCount())
        self.msgWorker = MsgBoxWorker()

        self.threadtest = QThread(self)
        self.idealthreadcount = self.threadtest.idealThreadCount()
        print("Ваша машина может обрабатывать `{}` потокa оптимально.".format(self.idealthreadcount))


    def recurring_timer(self):
        self.counter += 1
        self.lbl.setText(f"СЧЁТЧИК цикл GUI: {self.counter}")


    # ---- AThread(QThread) -----------#
    def using_q_thread(self):
        if self.thread is None:
            self.thread = AThread()
            self.thread.threadSignalAThread.connect(self.on_threadSignalAThread)
            self.thread.finished.connect(self.finishedAThread)
            self.thread.start()
            self.btnA.setText("Stop AThread(QThread)")
        else:
            self.thread.terminate()
            self.thread = None
            self.btnA.setText("Start AThread(QThread)")

    def finishedAThread(self):
        self.thread = None
        self.btnA.setText("Start AThread(QThread)")

    def on_threadSignalAThread(self, value):
        self.msg.label.setText(str(value))
        # Восстанавливаем визуализацию потокового окна, если его закрыли. Поток работает.
        # .setVisible(true) или .show() устанавливает виджет в видимое состояние,
        # если видны все его родительские виджеты до окна.
        if not self.msg.isVisible():
            self.msg.show()

    # --END-- AThread(QThread) -------------------#


    # ---- SomeObject(QObject) -------------------#
    def using_move_to_thread(self):
        if self.objThread is None:
            self.objThread = QThread()
            self.obj       = SomeObject()
            self.obj.moveToThread(self.objThread)  # Переместить в поток для выполнения

            self.obj.threadSignalSomeObject.connect(self.on_threadSignalSomeObject)
            self.obj.finishedSomeObject.connect(self.finishedSomeObject)
            self.objThread.started.connect(self.obj.long_running)
            self.objThread.start()

            self.btnB.setText("Wait SomeObject(QObject)")
            self.btnB.setEnabled(False)
        else:
            pass

    def finishedSomeObject(self):
        self.objThread.terminate()
        self.objThread.wait(1)

        self.objThread = None
        self.btnB.setEnabled(True)
        self.btnB.setText("Start SomeObject(QObject)")

    def on_threadSignalSomeObject(self, value):
        self.msgSomeObject.label.setText(str(value))
        # Восстанавливаем визуализацию потокового окна, если его закрыли. Поток работает.
        if not self.msgSomeObject.isVisible():
            self.msgSomeObject.show()

    # --END-- SomeObject(QObject) -------------------#


    # ---- Worker(QRunnable) ------------------------#
    def using_q_runnable(self):
        # Передайте функцию для выполнения
        # Любые другие аргументы, kwargs передаются функции run
        worker = Worker(self.execute_this_fn)
        worker.signals.result.connect(self.print_output)
        worker.signals.finish.connect(self.thread_complete)
        worker.signals.progress.connect(self.progress_fn)
        self.threadpool.start(worker)

    def progress_fn(self, n):
        self.progressBar.setValue(n)
        self.msgWorker.label.setText(str(n))
        # Восстанавливаем визуализацию потокового окна, если его закрыли. Поток работает.
        if not self.msgWorker.isVisible():
            self.msgWorker.show()

    def execute_this_fn(self, progress_callback):
        for n in range(0, 11):
            Qt.QThread.msleep(600)
            progress_callback.emit(n*100/10)
        return "Готово."

    def print_output(self, s):
        print("\ndef print_output(self, s):", s)

    def thread_complete(self):
        print("\nTHREAD ЗАВЕРШЕН!, self->", self)

    # --END-- Worker QRunnable) -------------------#


    #==============================================###
    # потоки или процессы должны быть завершены    ###
    def closeEvent(self, event):
        reply = Qt.QMessageBox.question\
        (self, 'Информация',
            "Вы уверены, что хотите закрыть приложение?",
             Qt.QMessageBox.Yes,
             Qt.QMessageBox.No)
        if reply == Qt.QMessageBox.Yes:
            if self.thread:
                self.thread.quit()
            del self.thread
            self.msg.close()

            if self.objThread:
                self.objThread.setTerminationEnabled(True)
                self.objThread.terminate()
                self.objThread.wait(1)
            self.msgSomeObject.close()

            # закрыть поток Worker(QRunnable)
            self.msgWorker.close()

            super(ExampleThread, self).closeEvent(event)
        else:
            event.ignore()


if __name__ == '__main__':
    app = Qt.QApplication([])
    mw  = ExampleThread()
    mw.show()
    app.exec()