import os
import json
import discord
import requests
import numpy as np
from bs4 import BeautifulSoup

from random_word import RandomWords
from duckduckgo_search import ddg, ddg_images
from random import choice

import infoHelp
from chat import kamek

def qa(message, guild_path, collect_message, image_results = 10, text_results = 10):
    raw_input = message.content
    message_length = len(raw_input.split(' '))

    if collect_message:
        chatbot = kamek(guild_path)
        chatbot.load()

    if message_length == 1 and collect_message:
        return chatbot.speak(np.random.randint(1,15))

    elif message_length == 2:
        with open(os.path.join(guild_path,'CustomAnswers.txt'),"r") as f:
            infoDict = json.loads(f.read())
        input = str.lower(raw_input.split(' ')[1].lstrip(' '))
        if input == "help":
            return infoHelp.helpmessage
        elif input == "hi":
            return choice([f'Hi {message.author}!','Hi!',f'Hi <@{message.author.id}>!'])
        elif input in infoDict.keys():
                return infoDict[input]
        else:
            r = RandomWords()
            return choice([input,r.get_random_word()])

    else:
        input = raw_input.split(' ')[1:]
        if input[0].lower() == "say":
            out = ''
            for word in raw_input.split(' ')[2:]:
                if word.lower() in ['i','me']:
                    word = choice([word,'you',f'{message.author}',f'{message.author.id}'])
                elif word.lower() in ['you']:
                    word = choice([word,'I',f'{message.author}',f'{message.author.id}'])
                out += str(word) + ' '
            return out

        elif input[0].lower() == "language" and input[1].lower() == "code":
            url = 'https://www.loc.gov/standards/iso639-2/php/code_list.php'
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            lan = str.lower(input[2])
            dic = np.char.lower(np.array((soup.get_text().split('\n'))))
            try:
                out = dic[np.where(dic==lan)[0][0]-1]
            except TypeError:
                out = 'Language not found.'
            except IndexError:
                out = 'Service not available.'
            return out

        else:
            #custom answer
            with open(os.path.join(guild_path,'CustomAnswers.txt'),"r") as f:
                infoDict = json.loads(f.read())
            input = str.lower(raw_input.split(' ',1)[1].lstrip(' '))
            if input in infoDict.keys():
                return infoDict[input]
            elif input == 'who am i' or input == 'who am i?':
                return f'You are {message.author}.'
            elif input == 'who are you' or input == 'who are you?':
                return 'I am shyguy bot.'
            elif input.startswith('show me'):
                img_input = input.replace('show me','')
                results = ddg_images(img_input, region='wt-wt', safesearch='Off', time=None, max_results=image_results)
                return choice(results)['image']
            else:
                results = ddg(input, region='wt-wt', safesearch='Off', time=None, max_results=text_results)
                return choice(results)['body']
