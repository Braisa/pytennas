# -*- coding: utf-8 -*-
"""
Created on Sun Feb 25 02:18:13 2024

@author: brais
"""

import numpy as np
import matplotlib.pyplot as plt

# https://scipython.com/book2/chapter-7-matplotlib/examples/modelling-an-antenna-array/

def gain(d, w):
    """

    Parameters
    ----------
    d : float
        Spacing between array elements. Assumes equally spaced arrays.
    w : float
        Feed coefficients of the arrays.

    Returns
    -------
    phi : array
        Azimuthal angle.
    
    g : array
        Power radiated/received. Expressed as a function of phi.

    """
    
    phi = np.linspace(0, 2*np.pi, 1000)
    psi = 2 * np.pi * d / lam * np.cos(phi)
    A = w[0] + w[1] * np.exp(1j*psi)
    g = np.abs(A)**2
    return phi, g

def relative_gain(g, minDdBi = -20):
    
    """
    
    Parameters
    ----------
    
    g : array
        Power radiated/received. Expressed as a function of phi.
    
    minDdBi : float
        Minimum relative power to where lower values are clamped. Allows for selection of a region of interest.
    
    """
    
    DdBi = 10 * np.log10(g / np.max(g))
    return np.clip(DdBi, minDdBi, None)

# Wavelength, element spacing and element feed coefficients.
lam = 1
d = .5
w = np.array((1, -1j))

# Calculate gain and relative power.
phi, g = gain(d, w)
DdBi = relative_gain(g)

# Plot relative power on a polar chart.
fig, ax = plt.subplots(subplot_kw = {"projection" : "polar"})
ax.plot(phi, DdBi)
plt.show()