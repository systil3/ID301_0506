import time

import Adafruit_MCP3008
import spidev

class SpiReader():
    def __init__(self, device):
        self.spi = spidev.SpiDev()
        self.spi.open(0, device)
        self.spi.max_speed_hz = 1000000
        self.channels = [i for i in range(8)]
        self.values = [0] * 8

    def read_channel(self, channel):
        adc = self.spi.xfer2([1, (0x08 + channel) << 4, 0])
        data = ((adc[1] & 3) << 8) + adc[2]
        return data

    def read_channels(self):
        for i, channel in enumerate(self.channels):
            value = self.read_channel(channel)
            self.values[i] = value

    def print_channels(self, channels):
        for i, channel in enumerate(channels):
            print("Channel {}: {}".format(channel, self.values[i]))

    def close(self):
        self.spi.close()

