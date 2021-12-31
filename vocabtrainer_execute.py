import yaml
import check_vocab as CheckVocab
import MakeLevelVocab as mlv


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



