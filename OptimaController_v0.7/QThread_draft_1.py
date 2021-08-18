from PyQt5.QtCore import pyqtSignal, QThread, QIODevice
from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo


class SerialThreadClass(QThread):
    rx_signal = pyqtSignal(bytes)

    def __init__(self, port, parent=None):
        super(SerialThreadClass, self).__init__(parent)
        # open the serial port
        self.serport = QSerialPort()
        self.serport.setBaudRate(14400)
        self.serport.setPortName(port)
        self.serport.open(QIODevice.ReadWrite)
    def run(self):
        # Устанавливаем таймаут на приём в 2 секунды
        if self.serport.waitForReadyRead(1000):
            # Принимаем данные
            rx_data = self.serport.readLine()
            # Если данные приняты, передаём их с сигналом
            if len(rx_data) > 0:
                self.rx_signal.emit(bytes(rx_data))
        # При наступлении таймаута передаём сигнал об ошибке
        else:
            rx_data = [0xAA, 0x00, 0x00, 0x00, 0x00, 0x00, 0xE1]
            self.rx_signal.emit(bytes(rx_data))

    # Передача данных через порт
    def senddata(self, data):
        tx_data = bytes(data)
        self.serport.write(tx_data)


# Определяем доступные в системе порты
class SerialInfoClass(QSerialPortInfo):

    def __init__(self, parent=None):
        super(SerialInfoClass, self).__init__(parent)

    def avaliable_ports(self):
        avaliable_comport_list = ['']
        self.my_ports = QSerialPortInfo()
        ports = self.my_ports.availablePorts()
        for port in ports:
            port_name = port.portName()
            avaliable_comport_list.append(port_name)
        return avaliable_comport_list



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
