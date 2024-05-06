import time

import Adafruit_MCP3008
import spidev

class SpiReader():
    def __init__(self, device):
        self.spi = spidev.SpiDev()
        self.spi.open(0, device)
        self.spi.max_speed_hz = 1000000
        self.channels = [1, 3, 5, 7]

    def read_channel(self, channel):
        adc = self.spi.xfer2([1, (0x08 + channel) << 4, 0])
        data = ((adc[1] & 3) << 8) + adc[2]
        return data

    def print_channels(self):
        for i, channel in enumerate(self.channels):
            value = self.read_channel(channel)
            section = value // 128
            if i % 2 == 1:
                section = 7 - section
            print("Channel {}: {}".format(channel // 2, section))

    def close(self):
        self.spi.close()

spi1 = SpiReader(1)
spi2 = SpiReader(0)
spi1.max_speed_hz = 1000000
spi2.max_speed_hz = 1000000

try:
    while True:
        channels = [1, 3, 5, 7]
        spi1.print_channels()
        spi2.print_channels()
        print("")
        time.sleep(0.5)

except KeyboardInterrupt:
    spi1.close()
    spi2.close()