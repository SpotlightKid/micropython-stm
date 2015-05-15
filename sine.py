# -*- coding: utf-8 -*-
"""Emit a sine wave frequency sweep on DAC 1."""

import math
import pyb


# Sweep generator
def sine_sweep(dac, start, end, mult, nsamples=100, delay=1000):
    """Emit sine wave frequency sweep on given DAC."""
    buf = bytearray(nsamples)

    for i in range(nsamples):
        buf[i] = 128 + int(110 * math.sin(2 * math.pi * i / nsamples))

    freq = start
    while True:
        dac.write_timed(buf, int(freq) * nsamples, mode=pyb.DAC.CIRCULAR)
        #print(freq, "Hz")
        pyb.delay(delay)
        freq *= mult

        if freq > end:
            freq = start

def main():
    dac1 = pyb.DAC(1)
    sine_sweep(dac1, 10, 400, 1.33)


if __name__ == '__main__':
    main()
