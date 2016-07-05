#-*- coding: utf-8 -*-
""" Unit Tests for PeriodogramEngine Module

@author j.wojak
"""

import unittest
import PeriodogramEngine
import PSignal
import numpy as np

class PeriodogramEngineTest(unittest.TestCase):
    """ class implementing unit tests for PeriodogramEngine Module """

    def test_FourierAnalyser_freq_even_case(self):
        """ test freq val of Fourier Analyser 
            in case of the use of an input signal
            with a even length """
        P = PSignal.PSignal(np.array([-2, 8, 6, 4, 1, 0, 3, 5], dtype=float), i_samp_freq = 0.1 )
        spectrum = PeriodogramEngine.FourierAnalyser(P)
        self.assertSequenceEqual( list(spectrum.periodogram_freq()), list(np.array([1.25,2.5,3.75])) )

        
    def test_FourierAnalyser_freq_odd_case(self):
        """ test freq val of Fourier Analyser
            in case of the use of an input signal
            with a odd length """  
        P = PSignal.PSignal(np.array([-2, 8, 6, 4, 1, 0, 3, 5,8], dtype=float), i_samp_freq = 0.1 )
        spectrum = PeriodogramEngine.FourierAnalyser(P)
        self.assertTrue( np.allclose(spectrum.periodogram_freq(), np.array([ 1.11111111,  2.22222222,  3.33333333,  4.44444444])) )
        

    def test_lag1Cor_Estimation(self):
        """ test that computation of lag1Cor is the same as the value 
            provided by wave_matlab (Torrence Compo)"""
        P = PSignal.PSignal(np.arange(10))
        spectrum = PeriodogramEngine.FourierAnalyser(P)
        self.assertAlmostEqual(spectrum.__estimateLag1Cor__(), 0.777777778)
    
