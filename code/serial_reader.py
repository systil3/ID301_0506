import serial
import audioplayer
import sys
import os
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QCheckBox
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent

ser = serial.Serial()  # 시리얼을 연결한다.
ser.port = 'COM3'  # 아두이노가 연결된 포트
ser.baudrate = 9600  # baudrate를 지정해줄 수 있다.
ser.timeout = 0.1  # 시리얼에 데이터를 불러올 때 지정하는 딜레이
ser.open()

data3 = []
try:
    app = QApplication(sys.argv)
    audioPlayer = audioplayer.AudioPlayer()
    audioPlayer.show()
except Exception as e:
    print(e)
    exit(-1)

while True:
    data = ser.readline().decode()
    if data != '':
        data = data.split("/")[0]
        audioPlayer.readSignal(data)

    data3.append(data)
    print("read : " + data)
    if len(data3) > 10000:
        break

ser.close()