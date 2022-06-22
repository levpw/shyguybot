import os
import re
import discord
import json
import yaml
import argparse
import asyncio
import sympy
import uuid
import cv2

from random import random, choice
from dotenv import load_dotenv

from utils import place_conversion, param_read, write_text, read_text, param_read_nita
from initialize_guild import guildInitializer
from customcommands import CustomCommand, fastCustomCommand
from ta import wr, nita, wiggler, partial_match, name_conversion
from result_gen import read_image
from img_gen import write_image
from interactive import qa
from translate import translate
from learn import learn, forget
from upgrader import guildconfigUpgrade
from chat import kamek
from configio import config_io

import infoHelp
import infoCourselist

client = discord.Client()

load_dotenv()
#TOKEN = os.getenv('DISCORD_TOKEN')
TOKEN = os.getenv('SHYGUY_E')

#protected command list

helpmessage = infoHelp.helpmessage
mk8_course = infoCourselist.mk8_abbrv
mk8_course_full = infoCourselist.mk8_full

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):

    if message.author.bot:
        return 0

    root = './'
    guild_root = './guilds/'

    #read guild id
    guild_id = str(message.guild.id)
    guild_path = os.path.join(guild_root,guild_id)

    #initialize
    guildExist = os.path.isdir(guild_path)
    if not guildExist:
        os.mkdir(os.path.join(guild_path))
        guildInitializer(guild_path)

    #loadconfigs
    configpath = os.path.join(guild_path,'GuildConfigs.yaml')
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', default=configpath)
    args = parser.parse_args()

    with open(args.config) as f:
        config = yaml.load(f,Loader=yaml.Loader)
    for k, v in config.items():
        setattr(args, k, v)

    #update
    msg = guildconfigUpgrade(guild_path, args)
    if msg:
        await message.channel.send(msg)
        #reloadconfigs
        with open(args.config) as f:
            config = yaml.load(f,Loader=yaml.Loader)
        for k, v in config.items():
            setattr(args, k, v)

    chatbot = kamek(guild_path)
    if not chatbot.check():
        chatbot.save()
    if args.collect_message:
        msg_in = message.content.split(' ')
        if msg_in[0].isalpha():
            chatbot.load()
            chatbot.process(message.content)
            chatbot.record()
            chatbot.save()

    #manage
    if message.content.startswith('$manage') and message.author.guild_permissions.administrator:
        author = message.author
        channel = message.channel
        tmp_var = vars(args)
        del tmp_var['config']

        session = config_io(tmp_var, guild_path)
        await message.channel.send(session.show())

        def check(m):
            return m.author == author and m.channel == channel
                
        await channel.send('Please enter the number of the setting you want to modify in '+str(args.manage_timeout)+' seconds.')
        try:
            option_message = await client.wait_for('message', timeout=args.learn_timeout, check=check)
            await channel.send(session.update(option_message.content))
        except asyncio.TimeoutError:
            await channel.send('Timeout.')

    #help message
    elif message.content.startswith('$help'):
        await message.channel.send(helpmessage)

    #greeting
    elif message.content.startswith('$hello'):
        await message.channel.send('Hello!')
        
    #random choice
    elif message.content.startswith('$choose'):
        input = message.content.split(' ')
        if input[1:]:
            await message.channel.send(choice(input[1:]))
        else:
            await message.channel.send('Nothing to choose from.')

    #translate
    elif message.content.startswith('$say'):
        input = message.content.split(' ',2)
        if input[1:]:
            if input[2:]:
                reply = translate(input)
            else:
                reply = 'Nothing to say.'
        else:
            reply = 'Nothing to say.'
        await message.channel.send(reply)

    #sympy
    elif message.content.startswith('$calc'):
        input = message.content.split(' ',1)[1]
        await message.channel.send(sympy.sympify(input))

    #learn
    elif message.content.startswith('$learn'):
        author = message.author
        channel = message.channel
        input = message.content.split(' ',1)

        def check(m):
            return m.author == author and m.channel == channel
        
        if len(input) < 2:
            await channel.send('Please provide the question in '+str(args.learn_timeout)+' seconds.')
            question_message = await client.wait_for('message', timeout=args.learn_timeout, check=check)
            question = str.lower(question_message.content.lstrip(' '))
        else:
            question = str.lower(input[1].lstrip(' '))
        await channel.send('Please provide the respond to '+question+' in '+str(args.learn_timeout)+' seconds.')

        try:
            answer_message = await client.wait_for('message', timeout=args.learn_timeout, check=check)
            answer = answer_message.content
            learn(question, answer, guild_path)
            await channel.send('Learned answer to question '+question+' is '+answer+'.')
        except asyncio.TimeoutError:
            await channel.send('Timeout.')

    #forget
    elif message.content.startswith('$forget'):
        author = message.author
        channel = message.channel
        input = message.content.split(' ',1)

        def check(m):
            return m.author == author and m.channel == channel
        
        if len(input) < 2:
            await channel.send('Please provide the question in '+str(args.learn_timeout)+' seconds.')
            question_message = await client.wait_for('message', timeout=args.learn_timeout, check=check)
            question = str.lower(question_message.content.lstrip(' '))
        else:
            question = str.lower(input[1].lstrip(' '))

        reply = forget(question, guild_path)
        if reply:
            await channel.send(reply)
        else:
            await channel.send('Forgot the answer to '+question+'.')

    #addReaction

    #maketable
    elif message.content.startswith('$maketable'):
        if message.attachments:
            author = message.author
            channel = message.channel
            attachment = message.attachments[0]
            tmp = os.path.join(guild_path,'tmp')
            temp_dir = os.path.join(tmp,str(uuid.uuid4()))
            os.mkdir(temp_dir)
            temp_fn = str(uuid.uuid4())+'.png'
            await attachment.save(os.path.join(temp_dir,temp_fn))
            img = cv2.imread(os.path.join(temp_dir,temp_fn))
            input = message.content.split(' ')
            pars = [-1,0]
            pars, msg = param_read(pars,input)
            if msg:
                await message.channel.send(msg)
            await message.channel.send('Reading information from input image.')
            ids, scores = read_image(img,type=pars[0],pos=pars[1],gpu=False)
            await message.channel.send('Below are the player ids and scores read from input. Please check the results in {0} seconds, click on \u2705 if no changes need to be made, or click on \u274e if you need to make changes. If the result is mostly empty, please specify the type of match result image provided: 0 for final result screen, 1 for 12th race screen.'.format(args.readimage_timeout))
            resp = await message.channel.send(write_text(ids,scores,separate=True))
            await resp.add_reaction("\u2705")
            await resp.add_reaction("\u274e")
    
            def check(reaction, user):
                return user == message.author and str(reaction.emoji) in ["\u2705","\u274e"]
            try:
                reaction, _ = await client.wait_for('reaction_add', timeout=args.readimage_timeout, check=check)
                if str(reaction.emoji) == "\u2705":
                    write_image(ids, scores, outdir=os.path.join(temp_dir,'out.png'), bkgd = None)
                    await message.channel.send(file = discord.File(os.path.join(temp_dir,'out.png')))
                elif str(reaction.emoji) == "\u274e":
                    await message.channel.send('Please make changes in {0} seconds, and send the modified text back.'.format(args.maketable_timeout))
                    def check(m):
                        return m.author == author and m.channel == channel
                    try:
                        msg = await client.wait_for('message', timeout=args.maketable_timeout, check=check)
                        ids, scores = read_text(msg.content)
                        write_image(ids, scores, outdir=os.path.join(temp_dir,'out.png'), bkgd = None)
                        await message.channel.send(file = discord.File(os.path.join(temp_dir,'out.png')))
                    except asyncio.TimeoutError:
                        await channel.send('Timeout.')
                
            except asyncio.TimeoutError:
                await channel.send('Timeout.')
            
            os.system('rm -rf '+temp_dir)

        elif message.content.split(' ',1)[1:]:
            if message.content.split(' ',1)[1] == "sample":
                await message.channel.send('Here is a sample of how to make a table.')
                await message.channel.send('''First call $maketable with two optional arguments,
                1st is the type of result image, 0 for final result screen, 1 for 12th race screen.
                2nd is the position of the player who made the screenshot, indicating which row is yellow.
                Example:
                $maketable 1 1
                ''')
                await message.channel.send(file = discord.File('./resource/sample.png'))
                img = cv2.imread('./resource/sample.png')
                ids, scores = read_image(img,type=1,pos=1,gpu=False)
                await message.channel.send(write_text(ids,scores,separate=True))
                write_image(ids, scores, outdir='./resource/out.png', bkgd = None)
                await message.channel.send(file = discord.File('./resource/out.png'))

        else:
            await message.channel.send('Please provide an image of your match result.')

    #nita look up
    elif message.content.startswith('$nita'):
        input = message.content.split(' ',2)[1:]
        course, place, warning  = param_read_nita(input)
        if warning:
            await message.channel.send(warning)
        if course:
            if course in mk8_course:
                reply = place_conversion(place)+' of '+mk8_course_full[mk8_course.index(course)]+' is '+nita(course,place)
            elif course in mk8_course_full:
                reply = place_conversion(place)+' of '+course+' is '+nita(name_conversion(course),place)
            else:
                course_ids = partial_match(course)
                await message.channel.send('Incorrect track name, checking partial match.')
                if course_ids:
                    reply = ''
                    for id in course_ids:
                        reply += place_conversion(place)+' of '+mk8_course_full[id]+' is '+nita(mk8_course[id],place)+'\n'
                else:
                    reply = 'Track name not found.'
            await message.channel.send(reply)

    #wiggler nita look up
    elif message.content.startswith('$wiggler'):
        input = message.content.split(' ',2)[1:]
        course, place, warning  = param_read_nita(input)
        if warning:
            await message.channel.send(warning)
        if course:
            if course in mk8_course:
                reply = place_conversion(place)+' of '+mk8_course_full[mk8_course.index(course)]+' is '+wiggler(course,place)
            elif course in mk8_course_full:
                reply = place_conversion(place)+' of '+course+' is '+wiggler(name_conversion(course),place)
            else:
                course_ids = partial_match(course)
                await message.channel.send('Incorrect track name, checking partial match.')
                if course_ids:
                    reply = ''
                    for id in course_ids:
                        reply += place_conversion(place)+' of '+mk8_course_full[id]+'(partial match) is '+wiggler(mk8_course[id],place)+'\n'
                else:
                    reply = 'Track name not found.'
            await message.channel.send(reply)

    #wr look up
    elif message.content.startswith('$wr'):
        input = message.content.split(' ',1)
        course = input[1].lower()
        if course in mk8_course:
            reply = wr(course)
        elif course in mk8_course_full:
            reply = wr(name_conversion(course))
        else:
            course_ids = partial_match(course)
            reply = ''
            if course_ids:
                for id in course_ids:
                    reply += mk8_course[id]+' WR '+wr(mk8_course[id])+'\n'
            else:
                reply = 'Track name not found.'
        await message.channel.send(reply)

    #customcommand
    elif message.content.startswith('_cc'):
        input = message.content.split(' ',3)
        if input[1:]:
            reply = CustomCommand(input, guild_path)
            await message.channel.send(reply)
        else:
            await message.channel.send('No input given.')
    elif message.content.startswith('_'):
        input = message.content.split('_',1)
        if input[1:]:
            reply = fastCustomCommand(input, guild_path)
            await message.channel.send(reply)
        else:
            await message.channel.send('No input given.')

    #interactive
    elif client.user.mentioned_in(message):
        reply_stat = True
        if '@everyone' in message.content.split(' ') or '@here' in message.content.split(' '):
            reply_stat = args.react_to_mention_all

        if reply_stat:
            reply = qa(message, guild_path, args.collect_message, args.ddg_imageresults, args.ddg_textresults)
            await message.channel.send(reply)

    #random repeat
    else:
        r = random()
        if r < args.repeat:
            await message.channel.send(choice([message.content,'I have no idea.','I believe you are correct.']))

client.run(TOKEN)
