# main.py
"""Blink all four LEDS one after another

Use USER switch to toggle blinking on off.

"""

sw_state = False


def main():
    leds = [pyb.LED(i+1) for i in range(4)]
    sw1 = pyb.Switch()
    sw1.callback(set_sw_state)

    while True:
        if sw_state:
            for led in leds:
                led.on()
                pyb.delay(100)
                led.off()
        else:
            for led in leds:
                leds.off()

            pyb.delay(200)


def set_sw_state():
    global sw_state
    sw_state = not sw_state


if __name__ == '__main__':
    main()
