import pandas as pd
from datetime import datetime
from datetime import timedelta


class VocabTrainer():

    def __init__(self,
                 number_voc=5,
                 levelarray=["level" + str(i) for i in list(range(0, 6))]):
        self.dict_days = {
            0: 0,
            1: 2,
            2: 4,
            3: 10,
            4: 20
        }
        self.days_l1 = 2
        self.days_l2 = 4
        self.days_l3 = 6
        self.days_l4 = 10
        self.days_l5 = 20
        self.n = number_voc
        self.levels = levelarray

    def set_path(self, path):
        self.path = path

    def load_vocab_inital(self, path=None):
        self.data = self._load_vocab_inital(path=path)
        self.dataRAW = self._load_vocab_inital(path=path)

        self.__extract_info_from_vocab()

    def _get_timediff_for_level(self, level, last_date):
        # Get
        # FEhlerhandling fehlt
        # Test fehlt
        if level > 5:
            return False
        else:
            print(self.dict_days)
            print(level)
            days = self.dict_days[level]
            return last_date + timedelta(days) <= datetime.now()

    def _load_vocab_inital(self, path=None):
        path = self.path if path is None else path
        df = pd.read_csv(path, sep=',')
        # this should be done earlier
        df[self.levels] = df[self.levels].apply(pd.to_datetime)
        return df

    def _get_cnt_per_level(self):
        return (self.data[self.data['todo']][['todo', 'last_index']]
                .groupby('last_index').count())

    def __extract_info_from_vocab(self):
        self.data['last_date'] = self.data[self.levels] \
                                 .stack().dropna() \
                                 .groupby(level=[0]).max()
        self.data['last_index'] = (self.data[self.levels]
                                   .idxmax(1)).str[-1:].astype(int)
        self.data['todo'] = self.data.apply(lambda x:
                                            self._get_timediff_for_level(
                                                    x['last_index'],
                                                    x['last_date']),
                                            axis=1)

    def __get_input_text_options(self,
                                 options,
                                 pre_key='',
                                 pre_value='',
                                 input_text=''):
        for key, value in options.items():
            input_text = "{0}{1}{2}. {3}{4}\n".format(input_text,
                                                      pre_key,
                                                      key,
                                                      pre_value,
                                                      value)
        return input_text

    def get_vocab(self, level=-1):
        if level == -1:
            return self.data[self.data['todo']]
        else:
            return self.data[self.data['todo'] & self.data["last_index"] == level]

    def __set_date(self, id):
        curr_level = self.data[self.data['id'] == id].iloc[0]['last_index']
        if curr_level > 5:
            raise ValueError('You cant have a level > 5. Something is wrong')
        else:
            curr_level = curr_level + 1
            curr_level_str = 'level' + str(curr_level)
            self.dataRAW.at[id, curr_level_str] = datetime.now()
            self.dataRAW.to_csv(self.path, sep=',', index=False)

    def __check_input(self, id, answer):
        return (self.data[self.data['id'] == id]['other'] == answer) \
               .head(1).astype('category').values[0]

    def list_vocab_to_do(self, train_col='german', level=-1):
        # vocab_to_train = list(self.get_vocab().iloc[:, 1:2])
        vocab = (self.get_vocab(level=level)[train_col]).tolist()
        id = (self.get_vocab(level=level)['id']).tolist()
        vocab_to_train = list(zip(id, vocab))
        return vocab_to_train

    def __enter__(self):
        pass

    def __del__(self):
        print('del proceddure')
        self.dataRAW.to_csv(self.path, sep=',', index=False)

    def __exit__(self):
        print('exit proceddure')
        self.dataRAW.to_csv(self.path, sep=',', index=False)

    def train_vocab(self, train_col='german', level=-1):
        self.__vocab_list = self.list_vocab_to_do(train_col=train_col, level=level)

        while len(self.__vocab_list) > 0:
            vocab = self.__vocab_list.pop(0)
            id = vocab[0]
            voc = vocab[1]
            text = 'what is the translation of the following vocabulary? \n'  \
                   + str(voc) + '\n'
            res = input(text)
            if self.__check_input(id, res):
                text = 'This is correct \n \n'
                self.__set_date(id)
            else:
                text = 'This is incorrect. We will try this one Later again. \n \n'
                self.__vocab_list.append(vocab)
            print(text)
        print('We are done. ')

    def input_handler(self,
                      options,
                      input_text='',
                      typ=int,
                      pre_key='',
                      pre_value=''):

        input_text = self.__get_input_text_options(options=options,
                                                   input_text=input_text,
                                                   pre_key=pre_key,
                                                   pre_value=pre_value)
        valid_input = False
        while not valid_input:
            try:
                res = input(input_text)
                valid_input = self._check_input_valid(input=res,
                                                      definition=options.keys(),
                                                      typ=typ)
            except Exception as e:
                print(e)
        return(typ(res))

    def _check_input_valid(self, input=None, definition=None, typ=None):
        try:
            assert input is not None, 'Must fill the parameters input'
            assert definition is not None, 'Must fill the parameters definition'
            assert typ is not None, 'Must fill the parameters type'
            try:
                assert typ(input), 'Inputtype is not ' + str(typ)
            except ValueError as e:
                raise AssertionError('Inputtype is not ' + str(typ))
            assert typ(input) in definition, 'Input is not a valid option'
            return(True)
        except AssertionError as e:
            print(e)
            return(False)

    def _generate_option_dict(self, li):
        dic = {}
        i = 1
        for k in li:
            dic[i] = k
            i = i + 1
        return dic
