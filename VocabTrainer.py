

class VocabTrainer():

    def __init__(self):
        pass

    def input_handler(self, options, input_text='', typ=int):
        for key, value in options.items():
            input_text = "{0}{1}. {2}\n".format(input_text, key, value)
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