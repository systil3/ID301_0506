import time
from waveplayerloop import *
import LCD1602

def setup():
    loop = WavePlayerLoop('test.wav')

    # todo. need to change default address when re-connecting lcd with raspi
    # to check out : i2cdetect -y 1 on terminal
    #LCD1602.init(0x27, 1)
    #LCD1602.write(0, 0, 'Estimated BPM')
    #LCD1602.write(5, 1, f'{round(loop.original_bpm)}')

    loop.run()
    time.sleep(2)



if __name__ == "__main__":
    try:
        setup()
        while True:
            pass
    except:
        pass