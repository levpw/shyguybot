import yaml
import argparse
import pandas as pd
import os

class config_io():
    def __init__(self, args_dict, path = None):
        self.args_dict = args_dict
        self.path = path
        self.fn = 'GuildConfigs.yaml'
        self.protected = ['version']
        self.allowed = ['repeat','collect_message','react_to_mention_all']
        self.arg_list = list(self.args_dict.keys())
        self.allowed_index = [str(self.arg_list.index(x)) for x in self.arg_list if x in self.allowed]
        self.m = 'Currently only modifications to\n'
        for idx,cmd in enumerate(self.allowed):
            self.m += '{:s}\t{:s}\n'.format(self.allowed_index[idx],cmd)

        self.m += 'are allowed.'

    def save(self):
        with open(os.path.join(self.path,self.fn),'w+') as f:
            yaml.dump(self.args_dict,f,default_flow_style=False)

    def show(self):
        df = pd.DataFrame(data=[list(self.args_dict.keys()),[str(x) for x in list(self.args_dict.values())]],index=['Name','Value']).transpose()
        return df.to_string(header=False, formatters={'Name':'{:25s}'.format,'Value':'{:10s}'.format})+'\n\n'+self.m

    def update(self, choice):
        if str(choice) not in self.allowed_index:
            out = 'Your option {:s} is invalid.\n\n'.format(str(choice))+self.m
        elif self.arg_list[int(choice)] == 'repeat':
            var_name = 'repeat'
            var_value = self.args_dict[var_name]
            if str(var_value) == '0.0':
                next_value = 0.001
            else:
                next_value = 0.0
            out = 'The {:s} setting of your server has been changed from {:s} to {:s}.'.format(var_name,str(var_value),str(next_value))
            self.args_dict[var_name] = next_value
            self.save()
        else:
            var_name = self.arg_list[int(choice)]
            var_value = self.args_dict[var_name]
            next_value = not var_value
            out = 'The {:s} setting of your server has been changed from {:s} to {:s}.'.format(var_name,str(var_value),str(next_value))
            self.args_dict[var_name] = next_value
            self.save()
        return out