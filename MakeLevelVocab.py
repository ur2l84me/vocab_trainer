from typing import Type
import pandas as pd
import numpy as np
import os.path
from pandas.core.indexes.period import period_range

'''
    This class has the following responsibilities:
    - if there is no csv yet with the needed columns for the Vocab level,
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
            self.base_data = self._read_base_data()
            self.outpath = path[:len(path) - 4] + '_level.csv'
            self.outpath_switch = path[:len(path) - 4] + '_level_switch.csv'
        elif pd_base is not None:
            self._validate_pd_base(pd_base)
            self.base_data = pd_base
            self.outpath = 'output_level.csv'

        self.data = self.base_data.copy()
        self.first_run = not self._check_if_output_file_exists()

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

    def _read_existing_data(self, path=None):
        if path is None:
            path = self.outpath
        return pd.read_csv(path, sep=',')

    def _generate_level_df(self):
        cnt_vocab = len(self.data.index)
        c = [None for i in range(0, cnt_vocab)]
        for i in self.cols:
            self.data[i] = c

    def _save_data(self, df, path=None):
        if path is None:
            path = self.outpath
        print('Data saved to: ' + path)
        df[self.cols] = df[self.cols].apply(pd.to_datetime)
        df['id'] = df.index
        df.to_csv(path, sep=',', index=False)

    def make_vocab_level_list(self):
        if self.first_run:
            self._generate_level_df()
            self._save_data(df=self.data, path=self.outpath)
            self._save_data(df=self.data, path=self.outpath_switch)
        else:
            self.data = self._read_existing_data()
            self.data_switch = self._read_existing_data(path=self.outpath_switch)
            res = self._get_new_data()
            self.data = pd.concat([self.data, res])
            self.data_switch = pd.concat([self.data_switch, res])
            self._save_data(df=self.data, path=self.outpath)
            self._save_data(df=self.data_switch, path=self.outpath_switch)

    def _get_new_data(self):
        '''
        Checks if we have new Vocabulary that is not yet in our
        Trainings Set
        '''
        TableA = self.data[['german', 'other']]
        TableB = self.base_data[['german', 'other']]
        outer_join = TableA.merge(TableB, how='outer', indicator=True)
        anti_join = outer_join[~(outer_join._merge == 'both')].drop('_merge', axis=1)
        return anti_join
