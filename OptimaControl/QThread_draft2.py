import sys
import traceback

from PyQt5.QtCore import (QCoreApplication, QObject, QRunnable, QThread,
                          QThreadPool, pyqtSignal, pyqtSlot)
from PyQt5 import Qt



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


def progress_fn(n):
    progressBar.setValue(n)
    msgWorker.label.setText(str(n))
    # Восстанавливаем визуализацию потокового окна, если его закрыли. Поток работает.
    if not msgWorker.isVisible():
        msgWorker.show()


def execute_this_fn(progress_callback):
    for n in range(0, 11):
        Qt.QThread.msleep(600)
        progress_callback.emit(n * 100 / 10)
    return "Готово."


def print_output(s):
    print("\ndef print_output(self, s):", s)


def thread_complete():
    print("\nTHREAD ЗАВЕРШЕН!, self->", )


threadpool = QThreadPool()
print("Max потоков, кот. будут использоваться=`%d`" % threadpool.maxThreadCount())
msgWorker = MsgBoxWorker()

threadtest = QThread()
idealthreadcount = threadtest.idealThreadCount()
print("Ваша машина может обрабатывать `{}` потокa оптимально.".format(idealthreadcount))

# Передайте функцию для выполнения
# Любые другие аргументы, kwargs передаются функции run
worker = Worker(execute_this_fn)
worker.signals.result.connect(print_output)
worker.signals.finish.connect(thread_complete)
worker.signals.progress.connect(progress_fn)
threadpool.start(worker)

app = Qt.QApplication([])

app.exec()