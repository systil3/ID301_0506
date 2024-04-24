import sys
from PyQt5 import QtWidgets, uic
from functools import partial
import waveplayerloop
class Window(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.buttons = [
            self.button0,
            self.button1,
            self.button2,
            self.button3,
            self.button4,
            self.button5,
            self.button6,
            self.button7
        ]

        self.sliders = [
            self.slider0,
            self.slider1,
            self.slider2,
            self.slider3,
            self.slider4,
            self.slider5,
            self.slider6,
            self.slider7
        ]

        self.effectLCDs = [
            self.effectLCD0,
            self.effectLCD1,
            self.effectLCD2,
            self.effectLCD3,
            self.effectLCD4,
            self.effectLCD5,
            self.effectLCD6,
            self.effectLCD7
        ]

        self.lcdButtons = [
            self.lcdButton0,
            self.lcdButton1,
            self.lcdButton2,
            self.lcdButton3,
            self.lcdButton4,
            self.lcdButton5,
            self.lcdButton6,
            self.lcdButton7
        ]

        self.loop = waveplayerloop.WavePlayerLoop("test.wav")

        run = partial(self.loop.start_playback)
        self.playButton.clicked.connect(run)

        for i, b in enumerate(self.buttons):
            te = partial(self.loop.toggleEnable, i)
            b.clicked.connect(te)

        def changePattern(i, s):
            value = s.value()
            self.loop.changePattern(i, value)

        for i, s in enumerate(self.sliders):
            cp = partial(changePattern, i, s)
            s.valueChanged.connect(cp)

        def changeEffect(i, el):
            try:
                value = (el.value() + 1) % 5
                el.display(value)
                self.loop.changeEffect(i)
            except Exception as e:
                print(e)

        for i, lb in enumerate(self.lcdButtons):
            el = self.effectLCDs[i]
            ce = partial(changeEffect, i, el)
            lb.clicked.connect(ce)

        def tapeEffect():
            speed = self.tapeDial.value() / 100
            pass
        self.tapeDial.valueChanged.connect(tapeEffect)

        def changeVolume():
            value = self.volumeSlider.value() / 25
            self.loop.changeVolume(value)
        self.volumeSlider.valueChanged.connect(changeVolume)
    def initUI(self):
        # Load the UI file
        uic.loadUi('0420.ui', self)

        # Show the window
        self.show()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec_())