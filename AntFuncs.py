# -*- coding: utf-8 -*-
"""
Created on Fri Mar  1 11:31:13 2024

@author: Brais
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

class AntFuncs:
    
    @staticmethod
    def get_relative_power(power, clamp_min = -np.inf, clamp_max = +np.inf, maximum = None):
        
        """
        
        Parameters
        ----------
            power : array
                Power in absolute value.
            clampdBi : float
                Minimum to which lower values of relative power are clamped. Allows selection of a region of interest.
        
            maximum : float, optional
                Allows to get power relative to a value not included in the input
        
        Returns
        -------
            dB : array
                Relative power in decibels. Expressed as a function of the same argument as AF.
        
        """
        
        if maximum is None:
            maximum = np.max(power)
        
        dB = 20*np.log10(power/maximum)
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
    
    def plot_patterns(gains, angle = np.linspace(0, np.pi/2, 1000), cos = False, projection = None, xlabel = r"$\theta$", ylabel = "dB"):
        
        """
        
        Parameters
        ----------
            gains : array
                Patterns to plot, assumed to be relative power expressed in dB.
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
        colors = [mpl.cm.viridis(i) for i in np.linspace(.1, 1, np.shape(gains)[0])]
        
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        
        for g, gain in enumerate(gains):        
            ax.plot(angle, gain, color = colors[g], label = f"{g}")
        
        ax.legend(loc = "best")
    
    def find_side_peaks(AF, step = 1, number = None):
        
        """
        
        Parameters
        ----------
            AF : array
                Array factor from which side lobes will be located.
            step : int
                Array factor value spacing, in degrees. Defaulted to 1 degree.
            number: int, optional
                Number of side lobes to be located. By default the entire factor will be iterated.
        
        Returns
        -------
            peaks : array
                Estimated locations of the side peaks, obtained through quadratic approximation of the side lobes.
        
        """

        step *= np.pi/180
        peak_locs = np.array(())
        peak_bounds = np.array(((0, 0), (0, 0)))
        peak_fits = np.array(((0,0,0)))
        peak_levels = np.array(())
        
        func = lambda theta, a, b, c : a + b*theta + c*theta**2
        from scipy.optimize import curve_fit
        
        # Setup cursor
        a, b = 0, step
        fa, fb = AF[:2]
        lobe_num = 1
        
        for c, fc in enumerate(AF[2::]):
            c *= step
            # Concave down located
            if fa < fb and fb > fc:
                peak = b + step*(fc-fa)/2/(2*fb-fa-fc)
                peak_locs = np.append(peak_locs, peak)
                peak_fits = np.vstack((peak_fits, curve_fit(func, (a, b, c), (fa, fb, fc))[0]))
                peak_levels = np.append(peak_levels, fb)
                if not number is None and np.size(peak_locs) >= number:
                    break
            # Concave up located
            if fa > fb and fb < fc:
                # Right bound of current lobe
                peak_bounds[-1][1] = b
                # Left bound of next lobe
                peak_bounds = np.vstack((peak_bounds, (b, 0)))
                # Update cursor
                lobe_num += 1
            
            # Move cursor
            a, b = b, c
            fa, fb = fb, fc
        
        # Right bound of first lobe, which for some reason I cant get to work in the loop # It works if you change b to any given number
        peak_bounds[1][1] = peak_bounds[2][0]
        # Right bound of last lobe
        peak_bounds[-1][1] = a
        
        # Eliminate dummy tuples that servd to make arrays non-1D
        peak_bounds = peak_bounds[1::]
        peak_fits = peak_fits[1::]
        return peak_locs, peak_bounds, peak_fits, peak_levels
        