# -*- coding: utf-8 -*-
"""
Created on Mon Feb 26 17:23:31 2024

@author: Brais
"""

import numpy as np
import matplotlib.pyplot as plt
import AntArray as ant

arr = ant.AntArray(lam = 1, d = .5, N = 10)
ang = np.linspace(0, 2*np.pi, 1000)
g = arr.get_relative_power(arr.get_AF(ang, alpha = np.pi/2), clampdBi = -30)

fig, ax = plt.subplots(subplot_kw = {"projection" : "polar"})
ax.plot(ang, g)
plt.show()
