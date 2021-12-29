
import unittest
import copy
import os.path
import MakeLevelVocab as Test_Vocab
import pandas as pd
from pandas.testing import assert_frame_equal


class Test_MakeLevelVocab(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(Test_MakeLevelVocab, self).__init__(*args, **kwargs)
        self.test_path = './test/test_csv_check_vocab.csv'
        self.d = {'id': [1,2],
            'german': ['h', 'a'],
            'other' : ['1','2']}
        self.test_pd_base = pd.DataFrame(data=self.d)


    def test_init_args_pd_base(self):
        # This should work fine
        vocTest = Test_Vocab.MakeLevelVocab(pd_base=self.test_pd_base)
        assert_frame_equal(vocTest.base_data, self.test_pd_base)

        # This should thow an Exception
        test_pd_d = copy.deepcopy(self.d)
        test_pd_d['col4'] = ['hh','hh']
        test_pd = pd.DataFrame(data=test_pd_d)
        with self.assertRaises(IndexError):
            Test_Vocab.MakeLevelVocab(pd_base=test_pd)

        test_pd_d = copy.deepcopy(self.d)
        test_pd_d['id4'] = test_pd_d.pop('id')
        test_pd = pd.DataFrame(data=test_pd_d)
        with self.assertRaises(TypeError):
            Test_Vocab.MakeLevelVocab(pd_base=test_pd)

    def test_init_args(self):
        with self.assertRaises(KeyError):
            Test_Vocab.MakeLevelVocab()

        # Check that it works correctly for given path
        vocTest = Test_Vocab.MakeLevelVocab(path=self.test_path)
        assert vocTest.path == self.test_path
        assert len(vocTest.base_data.columns) == 3


if __name__ == '__main__':
    unittest.main()
