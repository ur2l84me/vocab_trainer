from contextlib import AbstractAsyncContextManager
import yaml
import check_vocab as CheckVocab
import MakeLevelVocab as mlv
from unittest.mock import patch
import VocabTrainer as VocTrain
import os


with open("config.yaml", "r") as stream:
    try:
        config = (yaml.safe_load(stream))
    except yaml.YAMLError as exc:
        print(exc)

print(config)


# validate Data for all languages in yaml
# generate Data for all languages in yaml
for key in config.keys():
    path = config[key]['path']
    CheckVocab.check_vocab(path=path).run_validity_check()
    mlv.MakeLevelVocab(path=path).make_vocab_level_list()

vocTrai = VocTrain.VocabTrainer()

txt_int = '(Enter the integer)'
choose_lang = "Which language wouldyou like to practice?"
options = vocTrai._generate_option_dict(list(config.keys()))
input_text = choose_lang + txt_int + '\n'
lang = vocTrai.input_handler(options=options, input_text=input_text)
print('h')

print('You choose {}. Lets begin.'.format(options[lang]))

options_ger_other = {1: 'german - {}'.format(options[lang]),
                     2:  '{} - german'.format(options[lang])}

input_text = 'Which kind would you like to train? ' + txt_int + '\n'
kind = vocTrai.input_handler(options=options_ger_other, input_text=input_text)

if kind == 1:
    path = config[options[lang]]['path'][:len(path) - 4] + '_level.csv'
elif kind == 2:
    path = 1
    config[options[lang]]['path'][:len(path) - 4] + '_level_switch.csv'

vocTrai.set_path(path)
vocTrai.load_vocab_inital()
voc = vocTrai._get_cnt_per_level()
# was wenn empty? TODO AK
options_level_ex = voc.to_dict()['todo']
options_level_ex[-1] = voc['todo'].sum()


level = vocTrai.input_handler(options=options_level_ex,
                              input_text=input_text,
                              pre_key='Level ',
                              pre_value='Vocabulary to train:')

vocTrai.train_vocab(level=level,
                    train_col=options_ger_other[kind].split('-')[0].strip())

print('h')
