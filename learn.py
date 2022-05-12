import os
import json

def learn(input1, input2, guild_path):
    with open(os.path.join(guild_path,'CustomAnswers.txt'),'r') as f:
        infoDict = json.loads(f.read())

    infoDict[input1] = input2

    with open(os.path.join(guild_path,'CustomAnswers.txt'),'w') as f:
        json.dump(infoDict,f)

def forget(input1, guild_path):
    with open(os.path.join(guild_path,'CustomAnswers.txt'),'r') as f:
        infoDict = json.loads(f.read())

    out = infoDict.pop(input1, None)
    if not out:
        return 'Question not found.'
    else:
        with open(os.path.join(guild_path,'CustomAnswers.txt'),'w') as f:
            json.dump(infoDict,f)