# This Raspberry Pi code was developed by newbiely.com
# This Raspberry Pi code is made available for public use without any restriction
# For comprehensive instructions and wiring diagrams, please visit:
# https://newbiely.com/tutorials/raspberry-pi/raspberry-pi-led-matrix


from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.virtual import viewport, sevensegment
from luma.core.legacy import show_message
from time import sleep

CS_PIN = 16  # Replace with your actual CS pin
BLOCK_NUM = 4  # Replace with your block number

HEIGHT = 8
WIDTH = 8 * BLOCK_NUM

# Define SPI interface
serial = spi(port=0, device=0, gpio=noop(), cs=CS_PIN)

# Define LED matrix device
device = max7219(serial, cascaded=BLOCK_NUM, block_orientation=-90)

# Define virtual device
virtual = viewport(device, width=WIDTH, height=HEIGHT)

# Create instance of sevensegment for text display
ledMatrix = sevensegment(virtual)

def clear_display():
    ledMatrix.text = "        "
    sleep(1)

while True:
    ledMatrix.text = "Hello"
    show_message(device, ledMatrix.text, fill=None, font=None, scroll_delay=0.1)

try:
    pass  # Do other things if needed
except KeyboardInterrupt:
    pass
finally:
    device.cleanup()