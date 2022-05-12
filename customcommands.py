import os
import json

from random import choice

def CustomCommand(cc_input, guild_path):
    fn = os.path.join(guild_path,'CustomCommands.txt')
    command = cc_input[1]
    clength = len(cc_input)
    with open(fn,"r") as f:
        ccDict = json.loads(f.read())

    #add
    if command == 'add':
        if clength == 4:
            addSTAT = True
            for k in ccDict.keys():
                if k == cc_input[2]:
                    addSTAT = False
                    return 'Command already exist!'

            if addSTAT:
                ccDict[cc_input[2]]=cc_input[3]
                with open(fn,"w") as f:
                    json.dump(ccDict,f)
                return 'Command '+cc_input[2]+' added for '+cc_input[3]
        else:
            return 'Incorrect number of arguments, try _cc add commandname commandcontent'

    #remove
    elif command == 'remove':
        if clength == 3:
            out = ccDict.pop(cc_input[2], None)
            if not out:
                return 'Custom command not found.'
            else:
                with open(fn,"w") as f:
                    json.dump(ccDict,f)
                return 'Command '+cc_input[2]+' removed.'

        else:
            return 'Incorrect number of arguments, try _cc remove commandname'

    #update
    elif command ==  'update':
        if clength == 4:
            ccDict[cc_input[2]]=cc_input[3]
            with open(fn,"w") as f:
                json.dump(ccDict,f)
            return 'Command '+cc_input[2]+' updated for '+cc_input[3]
        
        else:
            return 'Incorrect number of arguments, try _cc update commandname commandcontent'

    elif clength == 2:
        #list all custom commands
        if command == 'list':
            respond=''
            if ccDict:
                for k in ccDict.keys():
                    respond += (k+',\t')
                return respond
                
            else:
                return '0 custom commands exist.'
                
        #call existing commands
        else:
            for k in ccDict.keys():
                if cc_input[1] == k:
                    return ccDict[k]

            return 'Custom command '+cc_input[1]+' does not exist.'

    else:
        return 'I do not understand.'

def fastCustomCommand(cc_input, guild_path):
    fn = os.path.join(guild_path,'CustomCommands.txt')
    command = cc_input[1]
    with open(fn,"r") as f:
        ccDict = json.loads(f.read())

    out = 'Custom command does not exist'

    if command == 'random':
        return choice(list(ccDict.values()))
    for k in ccDict.keys():
        if command == k:
            out = ccDict[k]
    
    return out

if __name__ == '__main__':
    guild_path = './shyguy/'
    f = os.path.isdir(guild_path)
    if not f:
        os.mkdir(guild_path)
    inputs = [['_cc','list'],['_cc','add','1','a'],['_cc','1']]
    for input in inputs:
        print(CustomCommand(input,guild_path))
    finput = ['_','1']
    print(fastCustomCommand(finput,guild_path))