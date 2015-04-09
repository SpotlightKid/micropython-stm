# -*- coding: utf-8 -*-
"""Micro Python MIDI library"""

from midiconstants import *


###################################################
## Helper functions

def is_status(byte):
    return (byte & 0x80) == 0x80  # 1000 0000


###################################################
## API classes

class MidiOut:
    """MIDI Output class."""

    def __init__(self, device, channel=1):
        if not hasattr(device, 'write'):
            raise TypeError("device instance must have a 'write' method.")

        if channel < 1 or channel > 16:
            raise ValueError('channel must be an integer between 1..16.')

        self.device = device
        self.channel = channel

    def __repr__(self):
        return '<MidiOut: device={} channel={}>'.format(
            self.device, self.channel)

    def channel_message(self, command, *data, ch=None):
        """Send a MIDI message to the serial device."""
        command |= (ch if ch else self.channel) - 1 & 0xf
        msg = bytearray([command] + [value & 0x7f for value in data])
        self.device.write(msg)

    def note_off(self, note, velocity=0, ch=None):
        """Send a 'Note Off' message."""
        self.channel_message(NOTE_OFF, note, velocity)

    def note_on(self, note, velocity=127, ch=None):
        """Send a 'Note On' message."""
        self.channel_message(NOTE_ON, note, velocity)

    def pressure(self, value, note=None, ch=None):
        """Send an 'Aftertouch' or 'Channel Pressure' message.

        If a note value is provided then send an Aftertouch (Polyphonic
        pressure) message, otherwise send a Channel (mono) pressure message.

        """
        if note:
            self.channel_message(POLYPHONIC_PRESSURE, note, value, ch=ch)
        else:
            self.channel_message(CHANNEL_PRESSURE, value, ch=ch)

    def control_change(self, control, value, ch=None):
        """Send a 'Control Change' message."""
        self.channel_message(CONTROLLER_CHANGE, control, value, ch=ch)

    def program_change(self, value, bank=None, ch=None):
        """Send 'Program Change' message, preceded by 'Bank Select'."""
        if bank:
            self.control_change(BANK_SELECT_LSB, bank, ch=ch)
            self.control_change(BANK_SELECT, bank >> 7, ch=ch)

        self.channel_message(PROGRAM_CHANGE, value, ch=ch)

    def pitch_bend(self, value=0x2000, ch=None):
        """Send a 'Pitch Bend' message.

        Pitch bend is a 14-bit value, centered at 0x2000.

        """
        self.channel_message(PITCH_BEND, value, value >> 7, ch=ch)

    def modulation(self, value, fine=False, ch=None):
        """Send modulation control change."""
        if fine:
            self.control_change(MODULATION_WHEEL_LSB, value, ch=ch)
            self.control_change(MODULATION_WHEEL, value >> 7, ch=ch)
        else:
            self.control_change(MODULATION_WHEEL, value, ch=ch)

    def volume(self, value, fine=False, ch=None):
        """Send volume control change."""
        if fine:
            self.control_change(CHANNEL_VOLUME_LSB, value, ch=ch)
            self.control_change(CHANNEL_VOLUME, value >> 7, ch=ch)
        else:
            self.control_change(CHANNEL_VOLUME, value, ch=ch)

    def all_sound_off(self, ch=None):
        """Send 'All Sound Off' controller change message."""
        self.control_change(ALL_SOUND_OFF, 0, ch=ch)

    def reset_all_controllers(self, ch=None):
        """Send 'Reset All Controllers' controller change message."""
        self.control_change(RESET_ALL_CONTROLLERS, 0, ch=ch)

    def local_control(self, enable=True, ch=None):
        """Enable or disable local control."""
        self.control_change(LOCAL_CONTROL_ONOFF, 127 if enable else 0, ch=ch)

    def all_notes_off(self, ch=None):
        """Send 'All Notes Off' message."""
        self.control_change(ALL_NOTES_OFF, 0, ch=ch)

    def panic(self, channels=range(1,17)):
        """Reset everything and stop making noise."""
        if isinstance(channels, int):
            channels = [channels]

        for ch in channels:
            self.all_notes_off(ch=ch)
            self.all_sound_off(ch=ch)
            self.reset_all_controllers(ch=ch)


def main():
    import pyb

    serial = pyb.UART(2, 31250)
    midiout = MidiOut(serial, channel=1)
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
