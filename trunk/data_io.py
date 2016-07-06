#-*- coding: utf-8 -*-
""" Module dedicated to the IO management of pyriodFinder:
       - .csv or .dat import
       - .csv or .dat export

@author j. wojak   
"""


from abc import ABCMeta, abstractmethod
import os


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
        return 0

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
                raise IOException('File extension is not correct, only .txt, .csv or .dat are accepted %s' %self.filename);

        
              

