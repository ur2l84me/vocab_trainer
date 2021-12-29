import unittest
import os.path
import check_vocab as Test_Vocab


class Test_check_vocab(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(Test_check_vocab, self).__init__(*args, **kwargs)
        self.test_path = './test/test_csv_check_vocab.csv'

    def test_init_args(self):
        vocTest = Test_Vocab.check_vocab()
        assert vocTest.voc_path == self.test_path

        assert Test_Vocab.check_vocab(path=self.test_path).voc_path = self.test_path

        with self.assertRaises(ValueError):
            Test_Vocab.check_vocab(lang='notinTest')

    def test_get_data(self):
        df = Test_Vocab.check_vocab().get_raw_data()
        assert len(df.index) > 4

    def test_drop_duplicates(self):
        vocab = Test_Vocab.check_vocab(path=self.test_path)
        leng_raw_data = len(vocab.get_raw_data().index)
        vocab._drop_duplicates()
        leng_after_drop = len(vocab.get_raw_data().index)
        assert leng_raw_data == leng_after_drop + 1

    def test_save_file(self):
        filename = './test/outputfile1.csv'
        vocab = Test_Vocab.check_vocab(path=self.test_path)
        vocab._save_new_file(filename=filename)

        assert os.path.isfile(filename)
        if os.path.isfile(filename):
            os.remove(filename)


if __name__ == '__main__':
    unittest.main()
