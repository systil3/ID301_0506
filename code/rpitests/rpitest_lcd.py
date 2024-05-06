#!/usr/bin/env python3
import LCD1602
import time

def setup():
    # todo. need to change default address when re-connecting lcd with raspi
    # to check out : i2cdetect -y 1 on terminal
    LCD1602.init(0x27, 1)
    LCD1602.write(0, 0, 'Hello World!!')
    LCD1602.write(5, 1, '- RPi 400 -')
    time.sleep(2)

def destroy():
    pass

if __name__ == "__main__":
    try:
        setup()
        while True:
            pass
    except KeyboardInterrupt:
        destroy()