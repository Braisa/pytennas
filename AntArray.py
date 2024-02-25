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
                Number of elements. Redundant when feed coefficients are input. Necessary when no feed
                coefficients are specificed, in which case uniform illumination is assumed.
            deltas : array, None
                Difference between each element's position with respect to its position in an equally
                spaced array. By default an equally spaced array is assumed.
        
        """
        
        self.lam = lam
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
