# main.py
"""Blink all four LEDS one after another

Use USER switch to toggle blinking on off.

"""

leds = [pyb.LED(i+1) for i in range(4)]
sw_state = False

def main():
    while True:
        if sw_state:
            for i in range(4):
                leds[i].on()
                pyb.delay(100)
                leds[i].off()
        else:
            for i in range(4):
                leds[i].off()
            pyb.delay(200)

def set_sw_state():
    global sw_state
    sw_state = not sw_state

if __name__ == '__main__':
    sw1 = pyb.Switch()
    sw1.callback(set_sw_state)
    main()
