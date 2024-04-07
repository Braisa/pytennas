# -*- coding: utf-8 -*-
"""
Created on Mon Feb 26 17:23:31 2024

@author: Brais
"""

import numpy as np
import matplotlib.pyplot as plt
import AntArray as ant
from AntFuncs import AntFuncs as antf
"""
arr = ant.AntArray(lam = 1, N = 10)
ang = np.linspace(0, 2*np.pi, 1000)
g = arr.get_relative_power(arr.get_AF(ang, alpha = np.pi/2), clampdBi = -30)

dels = arr.estimate_deltas(theta = ang, diff = .5*arr.num*arr.d*np.cos(ang))
arr2 = ant.AntArray(lam = 1, deltas = dels)
g2 = arr.get_relative_power(arr2.get_AF(ang, alpha = np.pi/2), clampdBi = -30)

fig, ax = plt.subplots(subplot_kw = {"projection" : "polar"})
ax.plot(ang, g)
fig, ax = plt.subplots(subplot_kw = {"projection" : "polar"})
ax.plot(ang, g2)
plt.show()
"""

feed = 1e-4 * np.array((10000, 9189, 8654,10002,11141,12405,13397,14251,14807,15108,
                        15108,14807,14251,13397,12405,11141,10002, 8654, 9189,10000))
phases = 1e-4 * np.array((2,2,1,1,1,1,1,1,1,1,
                          1,1,0,0,0,0,0,0,0,0))

angle_number = 900
angle_step = 90/angle_number

arr = ant.AntArray(lam = 1, w = feed*np.exp(1j*phases))
ang = np.linspace(0, np.pi/2, angle_number)
g = antf.get_relative_power(arr.get_AF(ang), clamp_min = -60)

#antf.plot_pattern(g, angle = ang, cos = False)

pks, bds = antf.find_side_peaks(arr.get_AF(ang), step = angle_step)
fig, ax = plt.subplots()
ax.plot(ang, g, ".")
vertical = np.linspace(-60, 0, 100)
for p in pks:
    ax.plot(p*np.ones_like(vertical), vertical, ls = "dashed", color = "tab:orange")
    ps = np.array((p-angle_step, p, p+angle_step))
    gps = np.array(np.round(ps/angle_step), dtype = int)
    f = antf.approximate_peak((ps, g[gps]))
    ax.plot(ang, f[0]+ang*f[1]+ang**2*f[2], ".", color = "tab:red")
for b in bds:
    ax.plot(b[0]*np.ones_like(vertical), vertical, ls = "dotted", color = "tab:green")
    ax.plot(b[1]*np.ones_like(vertical), vertical, ls = "dotted", color = "tab:green")

"""
diff = np.abs(np.cos(ang)) * .5
dels = arr.estimate_deltas(theta = ang, diff = diff)

arr2 = ant.AntArray(lam = 1, w = feed*np.exp(1j*phases), deltas = dels)
g2 = antf.get_relative_power(arr2.get_AF(ang), clamp_min = -60)

antf.plot_patterns((g, g2), cos = True)
"""
