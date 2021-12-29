
import unittest
import copy
import os.path
import os

from numpy import asscalar, e
import MakeLevelVocab as Test_Vocab
import pandas as pd
from pandas.testing import assert_frame_equal


class Test_MakeLevelVocab(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(Test_MakeLevelVocab, self).__init__(*args, **kwargs)
        self.test_path = './test/test_csv_check_vocab.csv'
        self.d = {'id': [1, 2],
                  'german': ['h', 'a'],
                  'other': ['1', '2']}
        self.test_pd_base = pd.DataFrame(data=self.d)

    def test_init_args_pd_base(self):
        # This should work fine
        vocTest = Test_Vocab.MakeLevelVocab(pd_base=self.test_pd_base)
        assert_frame_equal(vocTest.base_data, self.test_pd_base)

        # This should thow an Exception
        test_pd_d = copy.deepcopy(self.d)
        test_pd_d['col4'] = ['hh', 'hh']
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

    def test_genertate_level_df(self):
        d = {'id': [1, 2],
             'german': ['h', 'a'],
             'other': ['1', '2']}
        test_pd_base = pd.DataFrame(data=d)
        c = [None, None]

        d['level1'] = c
        d['level2'] = c
        d['level3'] = c
        d['level4'] = c
        d['level5'] = c

        exp_pd_base = pd. DataFrame(data=d)
        vocTest = Test_Vocab.MakeLevelVocab(pd_base=self.test_pd_base)
        vocTest._generate_level_df()
        assert_frame_equal(exp_pd_base, vocTest.data)

    def test_get_new_data(self):

        # Instanziate Class
        vocTest = Test_Vocab.MakeLevelVocab(pd_base=self.test_pd_base)
        e = {'id': [1, 2, 3],
             'german': ['h', 'a', 'ää'],
             'other': ['1', '2', '55-ä']}
        vocTest.base_data = pd.DataFrame(data=e)
        vocTest._generate_level_df()

        exp_df = pd.DataFrame({'german': ['ää'],
                               'other': ['55-ä']})

        res = vocTest._get_new_data()
        assert_frame_equal(res.reset_index(drop=True), exp_df.reset_index(drop=True))

    def test_make_vocab_list(self):
        # 1. Test nur Base data
        path = './test/test_only_base_data.csv'
        out_path = './test/test_only_base_data_level.csv'
        exp_path = './test/test_only_base_data_result.csv'

        vocTest = Test_Vocab.MakeLevelVocab(path=path)
        vocTest.make_vocab_level_list()
        res = pd.read_csv(out_path, sep=',')
        exp = pd.read_csv(exp_path, sep=',')

        assert_frame_equal(res, exp, check_dtype=False)
        os.remove(out_path)

        # 2. Test Base Data and existing Data
        path = './test/test_exist_data.csv'
        out_path = './test/test_exist_data_level.csv'
        exp_path = './test/test_exist_data_result.csv'
        vocTest2 = Test_Vocab.MakeLevelVocab(path=path)
        vocTest2.make_vocab_level_list()
        res = pd.read_csv(out_path, sep=',')
        exp = pd.read_csv(exp_path, sep=',')

        assert_frame_equal(res, exp,  check_dtype=False)


if __name__ == '__main__':
    unittest.main()
