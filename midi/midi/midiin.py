# -*- coding: utf-8 -*-
"""MicroPython MIDI input library."""

import sys

from .constants import *


class MidiIn:
    """MIDI input class."""

    def __init__(self, device, callback=None, debug=False):
        if not hasattr(device, 'any'):
            raise TypeError("device instance must have a 'any' method.")

        if not hasattr(device, 'read'):
            raise TypeError("device instance must have a 'read' method.")

        self.device = device
        self.callback = callback
        self.debug = debug
        self._msgbuf = None
        self._status = None

    def __repr__(self):
        return '<MidiIn: device={} callback={}>'.format(
            self.device, 'yes' if callable(self.callback) else 'no')

    def poll(self):
        """Poll the input device for newly received MIDI messages.

        Calls the callback function for any received complete message.

        """
        msgs = self._read()

        if msgs and self.callback:
            for msg in msgs:
                self.callback(msg)

    def _error(self, msg, *args):
        if self.debug:
            print(msg % args, file=sys.stderr)

    def _read(self):
        """Read data from input device and buffer incomplete messages.

        Returns list of complete messages received. Messages are bytearray
        instances.

        """
        msgs = []
        while self.device.any():
            data = self.device.read(1)[0]

            if data & 0x80:
                # A status byte
                if TIMING_CLOCK <= data <= SYSTEM_RESET:
                    # System real-time message
                    if data != 0xFD:
                        msgs.append(bytearray([data]))
                    else:
                        self._error("Read undefined system real-time status "
                                    "byte 0x%0X.", data)
                elif data == SYSTEM_EXCLUSIVE:
                    # Start of sysex message
                    self._status = None
                    self._msgbuf = bytearray([data])
                elif data == END_OF_EXCLUSIVE:
                    # End of sysex message
                    if self._msgbuf:
                        self._msgbuf.append(data)
                        msgs.append(self._msgbuf)

                    self._msgbuf = None
                    self._status = None
                elif MIDI_TIME_CODE <= data <= TUNING_REQUEST:
                    # System common message
                    self._status = None
                    self._msgbuf = None

                    if data == TUNING_REQUEST:
                        msgs.append(bytearray([data]))
                    elif data <= SONG_SELECT:
                        self._msgbuf = bytearray([data])
                    else:
                        self._error("Read undefined system common status byte "
                                    "0x%0X.", data)
                else:
                    # Channel mode/voice message
                    self._status = data
                    self._msgbuf = bytearray([data])
            else:
                # A data byte
                if self._status and not self._msgbuf:
                    # Running status assumed
                    self._msgbuf = bytearray([self._status])

                if not self._msgbuf:
                    self._error("Read unexpected data byte 0x%0X." % data)
                    continue

                self._msgbuf.append(data)

                if (self._msgbuf[0] != SYSTEM_EXCLUSIVE and
                        (len(self._msgbuf) == 3 or self._msgbuf[0] & 0xF0 in
                        (PROGRAM_CHANGE, CHANNEL_PRESSURE, MTC, SPP))):
                    msgs.append(self._msgbuf)
                    self._msgbuf = None

        return msgs
