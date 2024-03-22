import sys
import os
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QCheckBox
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent

number_of_chops = 2
class AudioPlayer(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Audio Player")
        self.resize(300, 200)
        self.setAcceptDrops(True)

        btn = QPushButton("Play", self)
        btn.clicked.connect(self.playAudio)
        btn.move(100, 40)  # Move button to a desired position within the widget

        self.muteCheckBox = QCheckBox("Mute", self)
        self.muteCheckBox.move(100, 80)
        self.muteCheckBox.stateChanged.connect(self.toggleMute)

        self.mediaPlayer = QMediaPlayer()
        self.playCount = 0
        self.mediaPlayer.mediaStatusChanged.connect(self.checkMediaStatus)

        self.duration = 0
        self.setAudio()
    def setAudio(self):
        path = os.path.join(os.path.dirname(__file__), "test2.wav")
        if not os.path.exists(path):
            print("File not found:", path)
            return
        url = QUrl.fromLocalFile(path)
        content = QMediaContent(url)
        self.mediaPlayer.setMedia(content)
    def playAudio(self, position_num):
        self.duration = self.mediaPlayer.duration()
        self.playCount = 0  # Reset play count
        position = (self.duration * position_num) // number_of_chops
        self.mediaPlayer.setPosition(position)
        self.mediaPlayer.play()

    def readSignal(self, signal):
        splitted = signal.split(":")
        command = splitted[0]
        if command == "play":
            position = int(splitted[1])
            self.playAudio(position)

    def checkMediaStatus(self, status):
        if status == QMediaPlayer.EndOfMedia:
            self.playCount += 1
            if self.playCount < 3:
                self.mediaPlayer.play()

    def toggleMute(self, state):
        self.mediaPlayer.setMuted(state)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    player = AudioPlayer()
    player.show()
    sys.exit(app.exec_())