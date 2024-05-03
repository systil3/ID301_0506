from gpiozero import Button, LED
from time import sleep
switch = Button(20)
pulldown = LED(16)

while True:
    #pulldown.off()
    if not switch.is_active:
        print("on")

    sleep(0.1)