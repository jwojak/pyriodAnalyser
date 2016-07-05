#-*- coding: utf-8 -*-
""" Unit Tests for PSignal Module

@author j.wojak
"""

import unittest
import PSignal
import numpy as np
import warnings

class PSignalTest(unittest.TestCase):
 
    def test_samp_freq_assigment_posVal01(self):
        """ test samp_freq assignement by construction """
        P = PSignal.PSignal(np.array([]),i_samp_freq = 1)
        self.assertEqual(P.samp_freq, 1)

    def test_samp_freq_assigment_posVal02(self):    
        """ test samp_freq assignement by setter """
        P = PSignal.PSignal(np.array([]),i_samp_freq = 1)
        P.samp_freq = 2
        self.assertEqual(P.samp_freq, 2)
        
    def test_samp_freq_assigment_negVal01(self):
        """ test exeception in case of neg samp_freq by construction """
        self.assertRaises(ValueError, PSignal.PSignal,np.array([]),i_samp_freq = -1)


    def test_samp_freq_assigment_negVal02(self):
        """ test execption in case of neg samp_freq by setter """
        P = PSignal.PSignal(np.array([]),i_samp_freq = 0)
        self.assertRaises(ValueError, setattr, P,"samp_freq", -1)

    #test execption for inconsistant time_axis and signal vector    
    def test_inconsistant_time_sig_vec(self):
        self.assertRaises(ValueError, PSignal.PSignal,np.arange(3),np.arange(4),i_samp_freq = -1)

        
