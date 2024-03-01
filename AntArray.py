# -*- coding: utf-8 -*-
"""
Created on Sun Feb 25 16:57:54 2024

@author: brais
"""

import numpy as np
import matplotlib.pyplot as plt

class AntArray:
    
    def __init__(self, lam : float, d = None, w = None, N = None, deltas = None):
        
        """
        
        Parameters
        ----------
            lam : float
                Wavelength.
            d : float, None
                Element spacing for equally spaced arrays. If no value is specified, then a standard half-wavelength element spacing will be assumed.
            w : array, None
                Feed coefficients. If no array is input, then uniform illumination will be assumed.
            N : int, None
                Number of elements. Redundant when feed coefficients are input. Necessary when no feed coefficients are specificed, in which case uniform illumination is assumed.
            deltas : array, None
                Difference between each element's position with respect to its position in an equally spaced array. By default an equally spaced array is assumed.
        
        """
        
        self.lam = lam
        self.num = 2*np.pi / lam
        
        # Element spacing
        if d is None:
            self.d = lam / 2
        else:
            self.d = d
        
        # Illumination
        if w is None and deltas is None:
            self.w = np.ones(N)
            self.N = N
        elif deltas is None:
            self.w = w
            self.N = np.size(w)
        else:
            self.w = np.ones(np.size(deltas))
            self.N = np.size(deltas)
        
        # Create element position array
        if deltas is None:
            self.deltas = np.zeros_like(self.w)
            self.pos = self.d * np.arange(self.N)
        else:
            self.deltas = deltas
            self.pos = self.d * np.arange(self.N) + deltas
        
    def get_AF(self, theta = np.linspace(0, 2*np.pi, 1000)):
        
        """
        
        Parameters
        ----------
            theta : array
                Visible angular range, in radians. Array factor will be computed for the specified angles.
        
        Returns
        -------
            AF : array
                Array factor, expressed as a function of polar angle theta.
        
        """
        
        eta = self.num * np.cos(theta)
        AF = np.sum(self.w[n] * np.exp(1j*self.pos[n]*eta) for n in np.arange(self.N))
        return np.abs(AF)
    
    def estimate_deltas(self, theta = np.linspace(0, 2*np.pi, 1000), diff = None):
        
        """
        
        Parameters
        ----------
            theta : array
                Visible angular range, in radians.
            diff : array
                Difference between the array factor of an unevenly spaced array and an evenly spaced array with the same parameters. Expressed as a function of psi.
        
        Returns
        -------
            deltas : array
                Difference between each element's position relative to its position in an evenly spaced array.
        
        """
        
        psi = self.num * self.d * np.cos(theta)
        deltas = np.zeros(self.N)
        for n in np.arange(self.N):
            deltas[n] = self.w[n]**-1 * -1j/(2*self.num) * np.trapz(diff / psi * np.exp(-1j*n*psi), psi)
        return deltas
