#-*- coding: utf-8 -*-
""" Unit Tests for PSignal Module

@author j.wojak
"""

import unittest
import PSignal
import numpy as np
import warnings

class PSignalTest(unittest.TestCase):

    #set of tests for samp_freq 
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

    def test_samp_freq_auto_estimation_evenly_spaced_time_axis(self):
        """ test samp freq auto estimation (case evenly spaced time axis) """
        P = PSignal.PSignal(np.array([1,2,3,4,5]), i_time=np.array([2,4,6,8,10]))
        self.assertEqual(P.samp_freq, 2)

    def test_samp_freq_auto_estimation_unevenly_spaced_time_axis(self):
        """ test samp freq auto estimation (case unevenly spaced time axis """
        P = PSignal.PSignal(np.array([1,2,3,4,5]), i_time=np.array([1,2,4,6,7]))
        self.assertEqual(P.samp_freq, 1.5)

        
    #test time axis assignement
    def test_time_axis_auto_init(self):
        """ test auto init of time axis """
        P = PSignal.PSignal(np.array([1,2,3,4,5]))
        self.assertSequenceEqual(list(P.time_axis),[0,1,2,3,4])

    def test_time_axis_explicit_init(self):
        """ test time axis explicit init """
        P = PSignal.PSignal(np.array([1,2,3]),i_time=np.array([7,8,9]))
        self.assertSequenceEqual(list(P.time_axis),[7,8,9])

    #test PSignal assignement
    def test_signal_init(self):
        P = PSignal.PSignal(np.array([1,2,1,2]))
        self.assertSequenceEqual(list(P.time_axis),[1,2,1,2])
        
    #test whole assignement    
    def test_inconsistant_time_sig_vec(self):
        """ test exception for inconsistant time and signal axis"""
        self.assertRaises(ValueError, PSignal.PSignal,np.arange(3),np.arange(4),i_samp_freq = -1)

        
