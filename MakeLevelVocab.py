from typing import Type
import pandas as pd
import numpy as np
import os.path
from pandas.core.indexes.period import period_range

'''
    This class has the following responsibilities:
    - if there is no csv yet with the needed columnsfor the Vocab level,
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
            self.outpath = path[:len(path) - 3] +'_level.csv'
        elif pd_base is not None:
            self._validate_pd_base(pd_base)
            self.base_data = pd_base
            self.outpath = 'output_level.csv'

        self.first_run = self._check_if_output_file_exists()

        if self.first_run:
            self.data = self._read_existing_data()
        else:
            self.data = 3

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

    def _check_if_output_file_exists(self):
        return os.path.exists(self.outpath)

    def _read_existing_data(self):
        return pd.read_csv(self.outpath, sep=',')

    def _generate_level_df(self):
        cnt_vocab = len(self.base_data.index)
        c = [None for i in range(0, cnt_vocab)]
        for i in self.cols:
            self.base_data[i] = c

