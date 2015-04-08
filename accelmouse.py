import pyb
from staccel import STAccel


MAG = 10.0

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
        #print((x, y))
        hid.send((0, int(x * MAG), int(-y * MAG), 0))
        pyb.delay(20)
