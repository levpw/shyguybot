import os
version = 1.02

def guildconfigUpgrade(guild_path, args):
    try:
        need_update = (args.version < version)
    except AttributeError:
        need_update = True
    if need_update:
        os.system('cp ./default.yaml '+guild_path+'/GuildConfigs.yaml')
        msg = 'Shyguy bot has been upgraded to version {:.2f}. Check github for mor info.'.format(version)
        return msg