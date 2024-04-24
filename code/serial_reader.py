import serial
import audioplayer
import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QThread, pyqtSignal

class SerialThread(QThread):
    signal = pyqtSignal(str)

    def __init__(self, port, baudrate):
        super().__init__()
        self.ser = serial.Serial()
        self.ser.port = port
        self.ser.baudrate = baudrate
        self.ser.timeout = 0.1

    def run(self):
        self.ser.open()
        data_cnt = 0
        while True:
            data = self.ser.readline().decode()
            if data != '':
                if not (data.split("/")[0] != "analogRead" or data.split("/")[0] != "digitalRead"):
                    continue
                self.signal.emit(data)

            data_cnt += 1
            print("read : " + data)
            if data_cnt > 10000:
                break
        self.ser.close()

if __name__ == "__main__":
    try:
        app = QApplication(sys.argv)
        audioPlayer = audioplayer.AudioPlayer()
        audioPlayer.show()

        serial_thread = SerialThread('COM4', 9600)
        serial_thread.signal.connect(audioPlayer.readSignal)
        serial_thread.start()

        sys.exit(app.exec_())

    except Exception as e:
        print(e)
        exit(-1)