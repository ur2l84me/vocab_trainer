from contextlib import AbstractAsyncContextManager
import yaml
import check_vocab as CheckVocab
import MakeLevelVocab as mlv
from unittest.mock import patch
import VocabTrainer as VocTrain


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
    CheckVocab .check_vocab(path=path).run_validity_check()
    mlv.MakeLevelVocab(path=path).make_vocab_level_list()

vocTrai = VocTrain.VocabTrainer()

txt_int = '(Enter the integer)'
choose_lang = "Which language wouldyou like to practice?"
options = vocTrai._generate_option_dict(list(config.keys()))
input_text = choose_lang + txt_int + '\n'
vocTrai.input_handler(options=options, input_text=input_text)

