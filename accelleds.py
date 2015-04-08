import pyb
from staccel import STAccel


def led_angle():
    # make LED objects
    l1 = pyb.Led(1)
    l2 = pyb.Led(2)
    accel = STAccel()

    while True:
        # get x-axis
        accel = accel.x() * 50

        # turn on LEDs depending on angle
        if accel < -10:
            l1.on()
            l2.off()
        elif accel > 10:
            l1.off()
            l2.on()
        else:
            l1.off()
            l2.off()

        # delay so that loop runs at at 1/50ms = 20Hz
        pyb.delay(50)


if __name__ == '__main__':
    led_angle()
