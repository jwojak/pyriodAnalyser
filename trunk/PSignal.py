#-*- coding: utf-8 -*-
""" Module to store a signal 1D
    and it also  provides basic info such
    as mean, stdev, sampling_rate..

@author j. wojak
"""

import numpy as np
import warnings

class PSignal(object):
    def __init__( self,  i_signal, i_time=np.array([]), i_samp_freq = 0.0 ):
        self.__time_axis = i_time
        self.__signal = i_signal
        self.samp_freq = i_samp_freq # use the setter in the constructor (<0 sampfreq are avoided by construction)
        self.__misc_info = ""
        self.__is_evenly_sampled = False


        # Sanity check after the construction    
        if( self.time_axis.size == 0 ):
            warnings.warn("Unknown time axis, linear time axis from 0 to signal length will be used",UserWarning)
            self.__time_axis = np.arange(self.signal.size)

        if( self.time_axis.size != self.signal.size ):
            raise ValueError("Time and signal array must have the same size: time size :" \
                                 ,self.time_axis.size, "signal size:", self._signal.size)

        if( self.samp_freq == 0):
            warnings.warn("Unknown sampling rate, trying to estimate it", UserWarning)
            self.estimateSampleFreq()   
        else:
            self.__is_evenly_sampled = True

    #implements getter for private attributes    
    # signal and time_axis have no setter
    #  they are build and checked by constructor and should never be changed after        
    @property
    def time_axis(self):
        return self.__signal     

    @property
    def signal(self):
        return self.__signal

    @property
    def is_evenly_sampled(self):
        return self.__is_evenly_sampled

    @property
    def misc_info(self):
        return self.__misc_info
        
    #implements getters and setters for privates attributes
    @property
    def samp_freq(self):
        return self.__samp_freq

    @samp_freq.setter
    def samp_freq(self, val):
        if(val < 0):
            raise ValueError('Sampling rate must be >= 0 (not', val,')', \
                                 'info: 0 means unknown sampling rate (estimated from i_time)')        
        self.__samp_freq = val
         

    def estimateSampleFreq(self):        
        tab_diff = self.time_axis[1:] - self.time_axis[:-1:]
        diff_time_step = np.unique(tab_diff)
        if( diff_time_step.size == 1 ):
            self.__is_evenly_sampled = True
            self.samp_freq = diff_time_step[0]
            print('Info: time axis is evenly spaced, estimated samp_freq', self.samp_freq)
        else:
            self.__is_evenly_sampled = False
            self.samp_freq = np.mean(tab_diff)
            warnings.warn("time axis is unevenly spaced !!! ",UserWarning)
            print('Info: time axis in unevenly spaced !! estimated (but probably false) samp_fred', self.samp_freq)


