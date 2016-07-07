#-*- coding: utf-8 -*-
"""Script to show how to use pyriodAnalyser

@author j.wojak
"""

import matplotlib.pyplot as plt
import matplotlib.cm as cm
import data_io
import PeriodogramEngine
import sys
import numpy as np
sys.path.insert(0,'thirdparty')
from waveletFunctions import wavelet, wave_signif

def main():
    print('Hello World !! This is pyriodAnalyser demo !')
    
    #---------------------------------------------------
    #FIRST STEP:: READ A SIGNAL IN A CSV FILE
    #---------------------------------------------------
    demo_dataset_reader = data_io.DataReader('dataElec.csv')
    
    #---------------------------------------------------
    #SECOND STEP:: SET UP SIGNAL PROPERTIES
    #---------------------------------------------------
    #get time_axis en signal in PSignal object
    demo_signal = demo_dataset_reader.psig
    #set up sample frequency
    demo_signal.samp_freq = 1./12

    #---------------------------------------------------
    #THIRD STEP:: PERFORM FOURIER ANALYSIS
    #---------------------------------------------------
    demo_spectrum = PeriodogramEngine.FourierAnalyser(demo_signal)
    
    #---------------------------------------------------
    #THIRD STEP BIS:: PERFORM WAVELET ANALYSIS
    #---------------------------------------------------
    variance = np.std(demo_signal.signal, ddof=1) ** 2
    sst = (demo_signal.signal - np.mean(demo_signal.signal))/np.std(demo_signal.signal, ddof=1)
    n = len(sst)
    pad = 1  # pad the time series with zeroes (recommended)
    dt = 1.0/12
    dj = 0.025  # this will do 4 sub-octaves per octave
    s0 = 2 * dt  # this says start at a scale of 6 months
    j1 = 5 / dj  # this says do 7 powers-of-two with dj sub-octaves each
    lag1 = 0.9  # lag-1 autocorrelation for red noise background
    mother = 'MORLET'
    
    wave, period, scale, coi = wavelet(sst, 1./12, pad, dj, s0, j1, mother)
    power = (np.abs(wave)) ** 2  # compute wavelet power spectrum
    # Significance levels: (variance=1 for the normalized SST)
    signif = wave_signif(([1.0]), dt=dt, sigtest=0, scale=scale, lag1=lag1, mother=mother)
    sig95 = signif[:, np.newaxis].dot(np.ones(n)[np.newaxis, :])  # expand signif --> (J+1)x(N) array
   

    #---------------------------------------------------
    #FOURTH STEP:: PLOT RESULTS
    #---------------------------------------------------
    plt.figure()
    plt.plot(demo_signal.time_axis,demo_signal.signal )
    
    plt.figure()
    plt.plot(demo_spectrum.periodogram_freq(),demo_spectrum.periodogram_amplitude())


    sig95 = power / sig95  # where ratio > 1, power is significan
    plt.figure()
    rcmap=cm.get_cmap('rainbow')
    levels = [0.000001,0.0039625,0.0625, 0.125, 0.25, 0.5, 1, 2, 4, 8, 16,24]
    CS = plt.contourf(1981+demo_signal.time_axis/12.0, period, np.log2(power), 256)  #*** or use 'contour'
    im = plt.contourf(CS,cmap=rcmap)# levels=np.log2(levels))
   
    plt.xlabel('Time (years)')
    plt.ylabel('Period (years)')
    plt.hold(True)
    plt.contour(1981+demo_signal.time_axis/12.0, period, sig95, [-99, 1], colors='k')
    #plt.plot(demo_signal.time_axis, coi, 'k')
    plt.hold(False)
    #plt.colorbar(im,  orientation='horizontal')

    plt.show()
if __name__ == '__main__':
    main()
    
