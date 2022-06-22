import os
version = 1.01

def guildconfigUpgrade(guild_path, args):
    try:
        need_update = (args.version < version)
    except AttributeError:
        need_update = True
    if need_update:
        os.system('cp ./default.yaml '+guild_path+'/GuildConfigs.yaml')
        msg = 'Shyguy bot has been upgraded to version {:.2f}. The new version includes a new chat function which requires collecting data from your server, and will not be used across other servers. If you do not like this, you can turn it off using $manage command and turn off collect_message. The default setting is on.'.format(version)
        return msg