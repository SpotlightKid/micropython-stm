import math
import pyb


# Sweep generator
def sine_sweep(dac, start, end, mult, delay=1000):
    """Emit sine wave on given DAC."""
    nsamples = 100
    buf = bytearray(nsamples)
    for i in range(nsamples):
        buf[i] = 128 + int(110 * math.sin(2 * math.pi * i / nsamples))

    freq = start
    while True:
        dac.write_timed(buf, int(freq) * nsamples, mode=pyb.DAC.CIRCULAR)
        print(freq, "Hz")
        pyb.delay(delay)
        freq *= mult
        if freq > end:
            freq = start


if __name__ == '__main__':
    dac1 = pyb.DAC(1)
    sine_sweep(dac1, 10, 400, 1.33)
