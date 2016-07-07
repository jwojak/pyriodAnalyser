#-*- coding: utf-8 -*-
""" Module dedicated to the IO management of pyriodFinder:
       - .csv or .dat import
       - .csv or .dat export

@author j. wojak   
"""


from abc import ABCMeta, abstractmethod
import os
import csv
import numpy as np
import PSignal

class _FileReader_(metaclass=ABCMeta):
    def __init__(self, i_fname):
        self.filename = i_fname
       
    @property
    def filename(self):
        return self.__filename
    
    @filename.setter
    def filename(self, f):
        self.__filename = f
        
    @abstractmethod
    def getPSig(self):
        pass
        

class _FileReaderCSV_(_FileReader_):
    def getPSig(self):
        with open(self.filename,'r') as csvfile:
            local_reader = csv.reader(csvfile)
            cpt_row = 1
            read_sig = np.array([])
            read_time = np.array([])
            for row in local_reader:
                if( len(row) < 1 ):
                    raise IOException('.csv is misformed, no column found, please check your file %s' %self.filename)
                elif(len(row) > 2):
                    raise IOException('.csv is misformed, more than two column found, please check your file %s' %self.filename)
                else:
                    try:
                        cur_row = np.array([float(x) for x in row])
                        if(cur_row.size == 2):
                            read_time = np.append(read_time,cur_row[0])
                            print(cur_row[0])
                            read_sig = np.append(read_sig,cur_row[1])
                        elif(cur_row.size == 1):
                            read_sig = np.append(read_sig,cur_row[0])
                        else:
                            raise 
                    except ValueError:
                        if(cpt_row == 1):
                            print('read csv header')
                        else:
                            raise IOException('.csv is misformed, a row, wich is not the first one, contains non-numeric caraters in %s' %self.filename)
                    cpt_row = cpt_row + 1
                    
        P = PSignal.PSignal(read_sig, i_time=read_time, i_samp_freq = 0.0) 
        return P
                                         
                                    
                
            

class _FileReaderDAT_(_FileReader_):
    def getPSig(self):
        return 0    

class _FileReaderTXT_(_FileReader_):
    def getPSig(self):
        return 0



class DataReader(object):
    """ implements a set of functions for data import """
    def __init__(self, i_fname):
        self.filename = i_fname

    @property
    def psig(self):
        return self.__reader.getPSig()
    
    @property
    def filename(self):
        return self.__filename
    
    @filename.setter
    def filename(self, f):
        self.__filename = f
        if( not(os.path.exists(self.filename)) ):
            raise IOException('File does not exist: %s'  % self.filename)
        else:
            extension = os.path.splitext(self.filename)[-1]
            if( extension == '.csv'):
                self.__reader = _FileReaderCSV_(self.filename)
            elif( extension == '.txt'):
                self.__reader = _FileReaderTXT_(self.filename)
            elif( extension == '.dat'):
                self.__reader = _FileReaderDAT_(self.filename)
            else:
                raise IOException('File extension is not correct, only .txt, .csv or .dat are accepted %s' %self.filename)

        
              

