import sys
from RPi import GPIO
from device import *
from waveplayerloop import *
import LCD1602

PLAY_BUTTON_PIN = 21
BASS_BUTTON_PIN = 5
SWITCH_BUTTON_PIN = 6

GPIO.setmode(GPIO.BCM)
# 40Pin SP1_SCLK
GPIO.setup(PLAY_BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(BASS_BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(SWITCH_BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

is_looping = False
is_pressing_play = False

if __name__ == "__main__":

    print("loading wave file...")
    wavePlayerLoop = WavePlayerLoop('test.wav')
    is_looping = False
    print("load complete.")

    print('\nInitializing device system...')
    spi1 = SpiReader(1)
    spi2 = SpiReader(0)
    spi1.max_speed_hz = 1000000
    spi2.max_speed_hz = 1000000
    slider_input = [1, 3, 5, 7]
    positions = [-1, -1, -1, -1, -1, -1, -1, -1]

    bassButton = Button(BASS_BUTTON_PIN, callback=wavePlayerLoop.start_playback_bass)
    switchButton = Button(SWITCH_BUTTON_PIN, callback=wavePlayerLoop.switch_drum_break)

    # todo. need to change default address when re-connecting lcd with raspi
    # to check out : i2cdetect -y 1 on terminal
    LCD1602.init(0x27, 1)
    LCD1602.write(0, 0, 'I D 3 0 1')
    LCD1602.write(0, 1, 'Y u n g K i m')
    time.sleep(2)
    print("Initializing complete.")

    def switch_callback():
        global is_looping
        is_looping = False
        wavePlayerLoop.switch_drum_break()
        LCD1602.clear()
        LCD1602.write(0, 0, f"> {wavePlayerLoop.breaks[wavePlayerLoop.break_num]}")
        LCD1602.write(0, 1, f"  {wavePlayerLoop.breaks[(wavePlayerLoop.break_num+1)%len(wavePlayerLoop.breaks)]}")
    switchButton.callback = switch_callback

    prev_state = True

    try:
        while True:
            if is_looping:
                spi1.read_channels()
                spi2.read_channels()
                #spi2.print_channels([0, 2, 4, 6])

                for i, j in enumerate(slider_input):
                    value = spi1.values[j]
                    chunk_num = value // 128
                    if i % 2 == 1:
                        chunk_num = 7 - chunk_num
                    LCD1602.write(i*2, 0, str(chunk_num))

                    positions[i] = chunk_num
                    wavePlayerLoop.changePattern(i, chunk_num)

                for i, j in enumerate(slider_input):
                    value = spi2.values[j]
                    chunk_num = value // 128
                    if i % 2 == 1:
                        chunk_num = 7 - chunk_num
                    LCD1602.write((i+4)*2, 0, str(chunk_num))

                    positions[i+4] = chunk_num
                    wavePlayerLoop.changePattern(i+4, chunk_num)

                play_pos = wavePlayerLoop.play_position
                position_indicator = ['  '] * 8
                position_indicator[play_pos] = '^ '
                LCD1602.write(0, 1, ''.join(position_indicator))
                time.sleep(0.025)

            else:
                pass

            curr_state = GPIO.input(PLAY_BUTTON_PIN)
            # button pressed state, only once
            if curr_state == True and prev_state == False:

                is_looping = not is_looping
                if is_looping == True:
                    print("playing sound")
                    LCD1602.clear()
                    wavePlayerLoop.start_playback()
                else:
                    print("stopped")
                    LCD1602.clear()
                    wavePlayerLoop.stop_playback()
                    play_pos = -1
            prev_state = curr_state


            bassButton.check_pressed()
            switchButton.check_pressed()

    except KeyboardInterrupt:
        spi1.close()
        spi2.close()