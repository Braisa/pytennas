# -*- coding: utf-8 -*-
"""
Created on Fri Mar  1 11:31:13 2024

@author: Brais
"""

import numpy as np
import matplotlib.pyplot as plt

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
    
    def plot_pattern(gain, angle = np.linspace(0, np.pi/2, 1000), cos = False, projection = None, xlabel = r"$\theta$", ylabel = "dB"):
        
        """
        
        Parameters
        ----------
            gain : array
                Pattern to plot, assumed to be relative power expressed in dB.
            angle : array
                Angles over which gain will be plotted.
            cos : bool
                If true, gain will be plotted over the cosine of angle. False by default.
            projection : str, None
                Type of plot. Will be passed on to subplot_kw.
        
        """
        
        if cos:
            angle = np.cos(angle)
            xlabel = r"$\cos\theta$"
        
        fig, ax = plt.subplots(subplot_kw = {"projection" : projection})
        
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        
        ax.plot(angle, gain)
        