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
import pinyin
import pykakasi

from random import random, choice
from dotenv import load_dotenv
from duckduckgo_search import ddg_translate

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

client = discord.Client(intents=discord.Intents.default()) # new stuff intent

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

    author = message.author
    if not author.bot:
        channel = message.channel
        input = message.content.split(' ',1)

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
            await channel.send(msg)
            #reloadconfigs
            with open(args.config) as f:
                config = yaml.load(f,Loader=yaml.Loader)
            for k, v in config.items():
                setattr(args, k, v)

        guild_subscription = args.subscription

        chatbot = kamek(guild_path)
        if not chatbot.check():
            chatbot.save()
        if args.collect_message:
            if input[0].isalpha():
                lan = ddg_translate(message.content)[0]['detected_language']
                data_in = message.content
                if lan.startswith('zh'):
                    data_in = pinyin.get(message.content, format="strip", delimiter=" ")
                    
                elif lan.startswith('ja'):
                    kks = pykakasi.kakasi()
                    result = kks.convert(message.content)
                    words = ''
                    for w in result:
                        words += w['orig'] + ' '
                    data_in = words

                chatbot.load()
                chatbot.process(data_in)
                chatbot.record()
                chatbot.save()

        #commands
        command = input[0]
        is_admin = author.guild_permissions.administrator

        #manage
        if command == '$manage' and is_admin:
            tmp_var = vars(args)
            del tmp_var['config']

            session = config_io(tmp_var, guild_path)
            await channel.send(session.show())

            def check(m):
                return m.author == author and m.channel == channel
                    
            await channel.send('Please enter the number of the setting you want to modify in '+str(args.manage_timeout)+' seconds.')
            try:
                option_message = await client.wait_for('message', timeout=args.learn_timeout, check=check)
                await channel.send(session.update(option_message.content))
            except asyncio.TimeoutError:
                await channel.send('Timeout.')

        #help message
        elif command == '$help':
            await channel.send(helpmessage)

        #greeting
        elif command == '$hello':
            await channel.send('Hello!')

        elif command == '$hira' or command == '$kana':
            if len(input)>1:
                lan = ddg_translate(message.content)[0]['detected_language']
                if lan == 'ja':
                    kks = pykakasi.kakasi()
                    result = kks.convert(input[1])
                    words = ''
                    for w in result:
                        words += w[command[1:]]
                    await channel.send(words)
                else:
                    await channel.send('Not Japanese.')
            else:
                await channel.send('Missing input.')

        #random choice
        elif command == '$choose':
            if len(input)>1:
                inputs = input[1].split(' ')
                await channel.send(choice(inputs))
            else:
                await channel.send('Nothing to choose from.')

        #translate
        elif command == '$say':
            reply = 'Nothing to say.'
            if input[1:]:
                inputs = input[1].split(' ',1)
                if inputs[1:]:
                    reply = translate(inputs[0],inputs[1])
            await channel.send(reply)

        #sympy
        elif command == '$calc':
            reply = 'Nothing to compute.'
            if input[1:]:
                reply = sympy.sympify(input[1])
            await channel.send(reply)

        #learn
        elif command == '$learn':
            def check(m):
                return m.author == author and m.channel == channel
            
            if input[1:]:
                question = str.lower(input[1].lstrip(' '))
            else:
                await channel.send('Please provide the question in '+str(args.learn_timeout)+' seconds.')
                question_message = await client.wait_for('message', timeout=args.learn_timeout, check=check)
                question = str.lower(question_message.content.lstrip(' '))
            await channel.send('Please provide the respond to '+question+' in '+str(args.learn_timeout)+' seconds.')

            try:
                answer_message = await client.wait_for('message', timeout=args.learn_timeout, check=check)
                answer = answer_message.content
                learn(question, answer, guild_path)
                await channel.send('Learned answer to question '+question+' is '+answer+'.')
            except asyncio.TimeoutError:
                await channel.send('Timeout.')

        #forget
        elif command == '$forget':
            def check(m):
                return m.author == author and m.channel == channel
            
            if input[1:]:
                question = str.lower(input[1].lstrip(' '))
            else:
                await channel.send('Please provide the question in '+str(args.learn_timeout)+' seconds.')
                question_message = await client.wait_for('message', timeout=args.learn_timeout, check=check)
                question = str.lower(question_message.content.lstrip(' '))

            reply = forget(question, guild_path)
            if reply:
                await channel.send(reply)
            else:
                await channel.send('Forgot the answer to '+question+'.')

        #addReaction

        #maketable
        elif command == '$maketable':
            if message.attachments:
                attachment = message.attachments[0]
                tmp = os.path.join(guild_path,'tmp')
                temp_dir = os.path.join(tmp,str(uuid.uuid4()))
                os.mkdir(temp_dir)
                temp_fn = str(uuid.uuid4())+'.png'
                await attachment.save(os.path.join(temp_dir,temp_fn))
                img = cv2.imread(os.path.join(temp_dir,temp_fn))
                table_args = message.content.split(' ')
                pars = [-1,0]
                pars, msg = param_read(pars,table_args)
                if msg:
                    await channel.send(msg)
                await channel.send('Reading information from input image.')
                ids, scores = read_image(img,type=pars[0],pos=pars[1],gpu=False)
                await channel.send('Below are the player ids and scores read from input. Please check the results in {0} seconds, click on \u2705 if no changes need to be made, or click on \u274e if you need to make changes. If the result is mostly empty, please specify the type of match result image provided: 0 for final result screen, 1 for 12th race screen.'.format(args.readimage_timeout))
                resp = await channel.send(write_text(ids,scores,separate=True))
                await resp.add_reaction("\u2705")
                await resp.add_reaction("\u274e")
        
                def check(reaction, user):
                    return user == author and str(reaction.emoji) in ["\u2705","\u274e"]
                try:
                    reaction, _ = await client.wait_for('reaction_add', timeout=args.readimage_timeout, check=check)
                    if str(reaction.emoji) == "\u2705":
                        write_image(ids, scores, outdir=os.path.join(temp_dir,'out.png'), bkgd = None)
                        await channel.send(file = discord.File(os.path.join(temp_dir,'out.png')))
                    elif str(reaction.emoji) == "\u274e":
                        await channel.send('Please make changes in {0} seconds, and send the modified text back.'.format(args.maketable_timeout))
                        def check(m):
                            return m.author == author and m.channel == channel
                        try:
                            msg = await client.wait_for('message', timeout=args.maketable_timeout, check=check)
                            ids, scores = read_text(msg.content)
                            write_image(ids, scores, outdir=os.path.join(temp_dir,'out.png'), bkgd = None)
                            await channel.send(file = discord.File(os.path.join(temp_dir,'out.png')))
                        except asyncio.TimeoutError:
                            await channel.send('Timeout.')
                    
                except asyncio.TimeoutError:
                    await channel.send('Timeout.')
                
                os.system('rm -rf '+temp_dir)

            elif input[1:]:
                if input[1] == "sample":
                    await channel.send('Here is a sample of how to make a table.')
                    await channel.send('''First call $maketable with two optional arguments,
                    1st is the type of result image, 0 for final result screen, 1 for 12th race screen.
                    2nd is the position of the player who made the screenshot, indicating which row is yellow.
                    Example:
                    $maketable 1 1
                    ''')
                    await channel.send(file = discord.File('./resource/sample.png'))
                    img = cv2.imread('./resource/sample.png')
                    ids, scores = read_image(img,type=1,pos=1,gpu=False)
                    await channel.send(write_text(ids,scores,separate=True))
                    write_image(ids, scores, outdir='./resource/out.png', bkgd = None)
                    await channel.send(file = discord.File('./resource/out.png'))

            else:
                await channel.send('Please provide an image of your match result.')

        #nita look up
        elif command == '$nita':
            input2 = message.content.split(' ',2)[1:]
            course, place, warning  = param_read_nita(input2)
            if warning:
                await channel.send(warning)
            if course:
                if course in mk8_course:
                    reply = place_conversion(place)+' of '+mk8_course_full[mk8_course.index(course)]+' is '+nita(course,place)
                elif course in mk8_course_full:
                    reply = place_conversion(place)+' of '+course+' is '+nita(name_conversion(course),place)
                else:
                    course_ids = partial_match(course)
                    await channel.send('Incorrect track name, checking partial match.')
                    if course_ids:
                        reply = ''
                        for id in course_ids:
                            reply += place_conversion(place)+' of '+mk8_course_full[id]+' is '+nita(mk8_course[id],place)+'\n'
                    else:
                        reply = 'Track name not found.'
                await channel.send(reply)

        #wiggler nita look up
        elif command == '$wiggler':
            input2 = message.content.split(' ',2)[1:]
            course, place, warning  = param_read_nita(input2)
            if warning:
                await channel.send(warning)
            if course:
                if course in mk8_course:
                    reply = place_conversion(place)+' of '+mk8_course_full[mk8_course.index(course)]+' is '+wiggler(course,place)
                elif course in mk8_course_full:
                    reply = place_conversion(place)+' of '+course+' is '+wiggler(name_conversion(course),place)
                else:
                    course_ids = partial_match(course)
                    await channel.send('Incorrect track name, checking partial match.')
                    if course_ids:
                        reply = ''
                        for id in course_ids:
                            reply += place_conversion(place)+' of '+mk8_course_full[id]+'(partial match) is '+wiggler(mk8_course[id],place)+'\n'
                    else:
                        reply = 'Track name not found.'
                await channel.send(reply)

        #wr look up
        elif command == '$wr':
            if input[1:]:
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
                
            else:
                reply = 'Missing input for track abbreviation or name.'

            await channel.send(reply)

        #customcommand
        elif command == '_cc':
            input3 = message.content.split(' ',3)
            if input3[1:]:
                reply = CustomCommand(input3, guild_path)
                await channel.send(reply)
            else:
                await message.channel.send('No input given.')

        elif message.content.startswith('_'):
            cinput = message.content.split('_',1)
            if cinput[1:]:
                reply = fastCustomCommand(cinput, guild_path)
                await channel.send(reply)
            else:
                await channel.send('No input given.')

        #interactive
        elif client.user.mentioned_in(message):
            msg = message.content.split()
            reply_stat = True
            if '@everyone' in msg or '@here' in msg:
                reply_stat = args.react_to_mention_all

            if reply_stat:
                reply = qa(message, guild_path, args.collect_message, args.ddg_imageresults, args.ddg_textresults)
                await channel.send(reply)

        #random repeat
        else:
            r = random()
            if r < args.repeat:
                await channel.send(choice([message.content,'I have no idea.','I believe you are correct.']))

client.run(TOKEN)
