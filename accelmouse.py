# -*- coding: utf-8 -*-
"""Move mouse pointer via USB-HID according to accelerometer measurements."""

import pyb
from staccel import STAccel


FREQ = const(50)
MAG = const(30)

def set_sw_state():
    global sw_state
    sw_state = not sw_state
    led.toggle()

sw_state = False
led = pyb.LED(1)
switch = pyb.Switch()
switch.callback(set_sw_state)
accel = STAccel()
hid = pyb.USB_HID()

while True:
    if sw_state:
        x, y, z = accel.xyz()
        hid.send((0, int(x * MAG), int(-y * MAG), 0))

    pyb.delay(int(1000 / FREQ))
