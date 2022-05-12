import os
import json

def guildInitializer(guild_path):
    attrs = ['CustomCommands.txt','CustomAnswers.txt','AddReactions.txt']
    for attr in attrs:
        with open(os.path.join(guild_path,attr), 'w') as newfile:
            json.dump({},newfile)

    os.mkdir(os.path.join(guild_path,'tmp'))
    os.system('cp ./default.yaml '+guild_path+'/GuildConfigs.yaml')

if __name__ == '__main__':
    try:
        os.mkdir('./123')
    except OSError:
        pass
    guildInitializer('./123')