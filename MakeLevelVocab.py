from typing import Type
import pandas as pd 
import numpy as np
from pandas.core.indexes.period import period_range

'''
    This class has the following responsibilities: 
    - if there is no csv yet with the needed columsn for the Vocab level,
      it generates it
    - it checks if new vocal in the base csv was added and needs to be 
      transfered into our training csv 
    - if generates/ updates the corresponding "language switches" file 
'''
class MakeLevelVocab():
    def __init__(self, path=None, pd_base=None, levelarray=None):
        if levelarray is None: 
            b = list(range(1, 6))
            self.cols = ["level" + str(i) for i in b]
        else: 
            self.cols = levelarray
        if path is None and pd_base is None: 
            raise KeyError('Please specifiy the path to the csv or enter a pd df')
        elif path is not None:
            self.path = path 
            self.base_data=self._read_base_data() 
        elif pd_base is not None:
            self._validate_pd_base(pd_base)
            self.base_data = pd_base

    def _read_base_data(self):
        ''' 
            Reads data (csv) from given os path
        '''
        df = pd.read_csv(self.path, sep=',')
        return df 

    def _validate_pd_base(self, pd_base):
        ''' 
            Validates that the input pd_base has the correct
            number of columns with the correct names
        '''
        mand_cols = ['id', 'german', 'other']
        pd_cols = pd_base.columns

        if len(pd_cols) != len(mand_cols):
            raise IndexError()
        for i in mand_cols:
            if i not in pd_cols:
                raise TypeError('cols must be named correctly')

