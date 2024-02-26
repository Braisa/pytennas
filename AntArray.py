# -*- coding: utf-8 -*-
"""
Created on Sun Feb 25 16:57:54 2024

@author: brais
"""

import numpy as np
import matplotlib.pyplot as plt

class AntArray:
    
    def __init__(self, lam, d, w = None, N = None, deltas = None):
        
        """
        
        Parameters
        ----------
            lam : float
                Wavelength.
            d : float
                Element spacing for equally spaced arrays.
            w : array, None
                Feed coefficients. If no array is input, then uniform illumination will be assumed.
            N : int, None
                Number of elements. Redundant when feed coefficients are input. Necessary when no feed coefficients are specificed, in which case uniform illumination is assumed.
            deltas : array, None
                Difference between each element's position with respect to its position in an equally spaced array. By default an equally spaced array is assumed.
        
        """
        
        self.lam = lam
        self.num = 2*np.pi / lam
        self.d = d
        
        # Illumination
        if not w:
            self.w = np.ones(N)
            self.N = N
        else:
            self.w = w
            self.N = np.size(w)
        
        # Create element position array
        if not deltas:
            self.deltas = np.zeros_like(w)
            self.pos = d * np.arange(self.N)
        else:
            self.deltas = deltas
            self.pos = d * np.arange(self.N) + deltas
        
    def get_AF(self, theta = np.linspace(0, 2*np.pi, 1000), alpha = 0.):
        
        """
        
        Parameters
        ----------
            theta : array
                Visible angular range. Array factor will be computed for the specified angles.
            alpha : float
                Main lobe angular position. By default it is zero.
        
        Returns
        -------
            AF : array
                Array factor, expressed as a function of polar angle theta.
        
        """
        
        eta = self.num * (np.cos(theta) - np.cos(alpha))
        AF = np.sum(self.w[n] * np.exp(1j*self.pos[n]*eta) for n in np.arange(self.N))
        return AF
    
    def get_relative_power(self, AF, clampdBi = -20.):
        
        """
        
        Parameters
        ----------
            AF : array
                Array factor.
            clampdBi : float
                Minimum to which lower values of relative power are clamped. Allows selection of a region of interest.
        
        Returns
        -------
            dBi : array
                Relative power in decibels over an isotropic radiator. Expressed as a function of the same argument as AF.
        
        """
        
        dBi = 10 * np.log10(AF / np.max(AF))
        return np.clip(dBi, clampdBi, None)
        
