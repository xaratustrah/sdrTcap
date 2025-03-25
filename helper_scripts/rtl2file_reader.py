#!/usr/bin/env python
"""
Process the binary files from the rtl2file

needs the iqtools library

https://github.com/xaratustrah/iqtools

xaratustrah 2025

"""

import sys
from iqtools import *
import numpy as np
import matplotlib.pyplot as plt

lframes = 2048
samp_rate = 2.048e6 # SPS
center_freq = 245e6 # Hz

plt.rcParams["font.size"] = 6
plt.rcParams["font.weight"] = "bold"


def largest_power_of_2(n):
    power = 1
    while power * 2 < n:
        power *= 2
    return power


def do_it(filename):
    iq = BINData(filename=filename, includes_header=False)
    nframes = largest_power_of_2(iq.nsamples_total / lframes)
    iq.read(lframes=lframes, nframes=nframes)
    iq.fs = samp_rate
    iq.center = center_freq

    plt.clf()
    xx, yy, zz = iq.get_power_spectrogram(
        lframes=lframes, nframes=nframes, sparse=False
    )
    xx, yy, zz = get_averaged_spectrogram(xx, yy, zz, every=4)
    plot_spectrogram(
        xx,
        yy,
        zz / np.max(zz),
        cen=iq.center,
        title=iq.file_basename,
        dbm=True,
        filename=f"{iq.filename}_gram",
    )
    np.savez(file=f"{iq.filename}.npz", ff=xx[0], pp=zz[0], fs=iq.fs, cen=iq.center)


def main():
    for filename in sys.argv[1:]:
        print("Processing file: " + filename)
        do_it(filename)


# ------------------------

if __name__ == "__main__":
    main()
