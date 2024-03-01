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

arr = ant.AntArray(lam = 1, w = feed*np.exp(1j*phases))
ang = np.linspace(0, np.pi/2, 1000)
g = antf.get_relative_power(arr.get_AF(ang), clamp_min = -60)

antf.plot_pattern(g)
