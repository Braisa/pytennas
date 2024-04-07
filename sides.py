# -*- coding: utf-8 -*-
"""
Created on Sun Apr  7 22:37:36 2024

@author: Brais
"""

import numpy as np
import matplotlib.pyplot as plt
import AntArray as ant
from AntFuncs import AntFuncs as antf

feed = 1e-4 * np.array((10000, 9189, 8654,10002,11141,12405,13397,14251,14807,15108,
                        15108,14807,14251,13397,12405,11141,10002, 8654, 9189,10000))
phases = 1e-4 * np.array((2,2,1,1,1,1,1,1,1,1,
                          1,1,0,0,0,0,0,0,0,0))

angle_number = 900
angle_step = 90/angle_number

arr = ant.AntArray(lam = 1, w = feed*np.exp(1j*phases))
ang = np.linspace(0, np.pi/2, angle_number)
g = antf.get_relative_power(arr.get_AF(ang), clamp_min = -60)

pks, bds, fts, lvs = antf.find_side_peaks(arr.get_AF(ang), step = angle_step)
lvs = antf.get_relative_power(lvs, clamp_min = -60, maximum = np.max(arr.get_AF(ang)))

fig, ax = plt.subplots()
ax.plot(ang, g, ".")

vertical = np.linspace(-60, 0, 100)

for p, peak in enumerate(pks):
    ax.plot(peak*np.ones_like(vertical), vertical, ls = "dashed", color = "tab:orange")
    bd = np.linspace(np.min(bds[p]), np.max(bds[p]), 100)
    approx_lobe = fts[p][0] + fts[p][1] * bd + fts[p][2] * bd**2
    ax.plot(bd, lvs[p] + antf.get_relative_power(approx_lobe, clamp_min = -60), ".", color = "tab:red")

for b in bds:
    ax.plot(b[0]*np.ones_like(vertical), vertical, ls = "dotted", color = "tab:green")
    ax.plot(b[1]*np.ones_like(vertical), vertical, ls = "dotted", color = "tab:green")