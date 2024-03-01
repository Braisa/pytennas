# -*- coding: utf-8 -*-
"""
Created on Fri Mar  1 11:31:13 2024

@author: Brais
"""

import numpy as np

class AntFuncs:
    
    @staticmethod
    def get_relative_power(power, clamp_min = -np.inf, clamp_max = +np.inf):
        
        """
        
        Parameters
        ----------
            power : array
                Power in absolute value.
            clampdBi : float
                Minimum to which lower values of relative power are clamped. Allows selection of a region of interest.
        
        Returns
        -------
            dB : array
                Relative power in decibels. Expressed as a function of the same argument as AF.
        
        """
        
        dB = 20*np.log10(power/np.max(power))
        return np.clip(dB, clamp_min, clamp_max)
        