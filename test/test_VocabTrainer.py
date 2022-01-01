import unittest
import VocabTrainer as VocTrain


class Test_VocabTrainer(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(Test_VocabTrainer, self).__init__(*args, **kwargs)
        self.vocTrain = VocTrain.VocabTrainer()

    def test_generate_option_dic(self):
        li = ['h', 'n']
        exp = {1: 'h', 2: 'n'}
        res = self.vocTrain._generate_option_dict(li)
        assert exp == res

    def test_check_input_valid(self):
        self.assertFalse(self.vocTrain._check_input_valid(None, None, None))
        self.assertFalse(self.vocTrain._check_input_valid('1', None, None))
        self.assertFalse(self.vocTrain._check_input_valid(None, [1, 2], None))
        self.assertFalse(self.vocTrain._check_input_valid(None, None, int))
        self.assertTrue(self.vocTrain._check_input_valid('1', [1, 2], int))
        self.assertFalse(self.vocTrain._check_input_valid('6', [1, 2], int))
        self.assertFalse(self.vocTrain._check_input_valid('h', [1, 2], int))

    def test_set_path(self):
        p = 'test_path'
        self.vocTrain.set_path(path=p)
        assert p == self.vocTrain.path

    def test_get_all_vocab(self):
        # will not be tested
        pass

    def test_get_timediff_for_level(self):
        # will not be teste
        pass
