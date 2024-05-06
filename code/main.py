import sys
from device import *
from waveplayerloop import *

if __name__ == "__main__":

    print("loading wave file...")
    wavePlayerLoop = WavePlayerLoop('test.wav')
    print("load complete.")

    print('\nInitializing device system...')
    spi1 = SpiReader(1)
    spi2 = SpiReader(0)
    spi1.max_speed_hz = 1000000
    spi2.max_speed_hz = 1000000
    print("Initializing complete.")

    try:
        while True:
            channels = [1, 3, 5, 7]
            spi1.read_channels()
            spi2.read_channels()
            print("")
            time.sleep(0.5)

    except KeyboardInterrupt:
        spi1.close()
        spi2.close()