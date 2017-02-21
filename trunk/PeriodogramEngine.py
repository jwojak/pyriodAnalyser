#-*- coding: utf-8 -*-
""" Module to compute periodogram of a signal
    by Fourier Analysis, Max Entropy, and Lomb Scargle Methods 

@author j. wojak
""" 

from abc import ABCMeta, abstractmethod
import PSignal as ps
import numpy as np

class PeriodAnalyser(metaclass=ABCMeta):
    def __init__(self, i_psig, i_conf_level_thresh=0.95):
        self.psig = i_psig #use setter in constructor
        self.conf_level_thresh = i_conf_level_thresh
        
    @property
    def psig(self):
        return self.__psig
    @psig.setter
    def psig(self, s):
        self.__psig = s

    @property    
    def conf_level_thresh(self):
        return self.__conf_level_thresh  
    @conf_level_thresh.setter
    def conf_level_thresh(self,cl):
        if(cl < 0 ) :
            raise ValueError("Confidence level threshold must be positiv (in [0 1]")
        elif(cl > 1):
            raise ValueError("Confidence level threshold must be in [0 1], (0.95 meaning 95%)")
        else:
            self.__conf_level_thresh = cl
            
    @abstractmethod
    def periodogram_amplitude(self):
        pass

    @abstractmethod
    def periodogram_freq(self):
        pass



class FourierAnalyser(PeriodAnalyser):
    """ class implementing periodogram computation 
        by classical fourier transform
    """
    def __init__(self, i_psig, i_conf_level_thresh=0.95):
        """constructor, inherited from the asbstract class PeriodAnalyser """
        PeriodAnalyser.__init__(self,i_psig, i_conf_level_thresh=0.95)
       
    def periodogram_amplitude(self):
        """compute periodogram amplitude by fourier transform"""
        spectrum = np.fft.fft(self.psig.signal)
        n = self.psig.signal.size
        print(n)
        print(((n-1)/2+1))
        print('------------------')
        if( n%2 == 0): #even case
            return np.abs(spectrum[1:n/2])
        else: #odd case
            return np.abs(spectrum[1:np.int(((n-1)/2+1))])
    
    def periodogram_freq(self):
        """compute periodogram frequencies
            frequencies are [1,...,n/2 - 1]/(d*n) if n is even 
                            [1,...,(n-1)/2)/(d*n) if n is odd 
            n is the number of elements in the signal
            d is the inverse of the the sampling rate
        """
        n = self.psig.signal.size
        if (n%2 == 0): #even case
            freq = (np.arange(n/2 - 1) + 1)*(1./self.psig.samp_freq)/n
        else: #odd case
            freq = (np.arange((n-1)/2) + 1)*(1./self.psig.samp_freq)/n
        return freq 

    def red_noise_limit(self):
        """compute red noise limit"""
        #step 1 get theoritical red noise
        freq = self.periodogram_freq()
        Msp = freq.size;
        h = np.arange(Msp);
        alpha2 = self.__estimateLag1Cor__()*self.__estimateLag1Cor__();
        theo_red_noise = (1.0 - alpha2)/(1.0 - 2.0*self.__estimateLag1Cor__()*np.cos(h*np.pi*2/self.psig.signal.size)+alpha2);
        #step 2 scale red noise according to confidence level
        scaled_red_noise  = theo_red_noise*20000
        return scaled_red_noise
    
    def white_noise_limit(self):
        """compute white noise limit"""

    def __estimateLag1Cor__(self):
        """ compute lag1 coeff for red noise estimation
            (private function, should not be called
             outside the scope of this class)  """
        x = self.psig.signal
        m = np.mean(x)
        x = x - m
        c0 = np.dot(x.transpose(), x)/(float(x.size))
        x_first = x[:-1:]
        x_last = x[1:]
        c1 = np.dot(x_first.transpose(),x_last)/(x.size-1.0)
        return c1/c0
    
class MaxEntropyAnalyser(PeriodAnalyser):
    def __init__(self, i_psig, i_conf_level_thresh=0.95):
        PeriodAnalyser.__init__(self,i_psig, i_conf_level_thresh=0.95)

class LombScargleAnalyser(PeriodAnalyser):
    def __init__(self, i_psig, i_conf_level_thresh=0.95):
        PeriodAnalyser.__init__(self,i_psig, i_conf_level_thresh=0.95)
