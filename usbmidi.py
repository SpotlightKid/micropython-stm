# -*- coding: utf-8 -*-
"""Micro Python MIDI library"""

import midi

def main():
    import pyb

    serial = pyb.USB_VCP()
    midiout = midi.MidiOut(serial, channel=1)
    switch = pyb.Switch()

    if hasattr(pyb, 'Accel'):
        accel = pyb.Accel()
        SCALE = 1.27
    else:
        from staccel import STAccel
        accel = STAccel()
        SCALE = 127

    while True:
        while not switch():
            pyb.delay(10)

        note = abs(int(accel.x() * SCALE))
        velocity = abs(int(accel.y() * SCALE))
        midiout.note_on(note, velocity)

        while switch():
            pyb.delay(50)

        midiout.note_off(note)


if __name__ == '__main__':
    main()
