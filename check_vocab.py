import pandas as pd

class check_vocab:

    def __init__(self, lang='test', path=None):
        if path is None:
            if lang == 'test':
                self.voc_path = './test/test_csv_check_vocab.csv'
            elif lang == 'spanisch':
                self.voc_path = 'input_spanisch.csv'
            else:
                raise ValueError('No Specified csv')
        else:
            self.voc_path  = path
        self.raw_data = self._load_raw_data()


    def _load_raw_data(self):
        df = pd.read_csv(self.voc_path, sep=',')
        return df

    def get_raw_data(self):
        return self.raw_data

    def _drop_duplicates(self):
        self.raw_data = self.raw_data.drop_duplicates(['german', 'other'])

    def _save_new_file(self, filename = None):
        if filename is None:
            filename = 'modified_' + self.voc_path
        self.raw_data.to_csv(filename, sep = ',')

    def _set_id(self):
        self.raw_data['id'] = self.raw_data.index

    def run_validity_check(self):
        self._drop_duplicates()
        self._set_id()
        self._save_new_file()


#check_vocab()._no_duplicated_vocab()