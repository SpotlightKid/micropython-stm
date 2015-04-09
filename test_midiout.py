# -*- coding: utf-8 -*-
"""Unit tests for MicroPython MIDI library."""

import midi


class MockUART:
    def __init__(self, *args, **kw):
        self.buf = bytearray()

    def write(self, buf):
        self.buf.extend(buf)
        return len(buf)

def test_note_on():
    serial = MockUART()
    midiout = midi.MidiOut(serial)
    midiout.note_on(60)
    assert serial.buf == b'\x90<\x7f'

def test_note_off():
    serial = MockUART()
    midiout = midi.MidiOut(serial)
    midiout.note_off(60)
    assert serial.buf == b'\x80<\0'


if __name__ == '__main__':
    for name, obj in locals().items():
        if name.startswith('test_') and callable(obj):
            obj()
