import os
import json
import discord
import requests
import numpy as np
from bs4 import BeautifulSoup

from random_word import RandomWords
from duckduckgo_search import ddg, ddg_images
from random import choice, random

import infoHelp
from chat import kamek

def qa(message, guild_path, collect_message, image_results = 10, text_results = 10):
    raw_input = message.content
    message_length = len(raw_input.split())

    if collect_message:
        chatbot = kamek(guild_path)
        chatbot.load()

    if message_length == 1:
        if collect_message:
            return chatbot.speak(np.random.poisson(8))
        else:
            r = RandomWords()
            return choice([input,r.get_random_word()])

    else:
        with open(os.path.join(guild_path,'CustomAnswers.txt'),"r") as f:
            infoDict = json.loads(f.read())
        input = str.lower(raw_input.split(' ',1)[1].lstrip(' '))
        if input == "help":
            return infoHelp.helpmessage
        elif input == "hi":
            return choice([f'Hi {message.author}!','Hi!',f'Hi <@{message.author.id}>!'])
        elif input in infoDict.keys():
            return infoDict[input]
        elif input.lower().startswith('say '):
            out = ''
            for word in raw_input.split(' ')[2:]:
                if word.lower() in ['i','me']:
                    word = choice([word,'you',f'{message.author}',f'{message.author.id}'])
                elif word.lower() in ['you']:
                    word = choice([word,'I',f'{message.author}',f'{message.author.id}'])
                out += str(word) + ' '
            return out
        elif input.lower().startswith('show me '):
            reply = '404 Not Found.'
            img_input = input.replace('show me ','')
            try:
                results = ddg_images(img_input, region='wt-wt', safesearch='Off', time=None, max_results=image_results)
                reply = choice(results)['image']
            except json.decoder.JSONDecodeError:
                pass
            return reply
        elif input.lower().startswith('language code '):
            url = 'https://www.loc.gov/standards/iso639-2/php/code_list.php'
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            lan = input.replace('language code ','')
            dic = np.char.lower(np.array((soup.get_text().split('\n'))))
            try:
                out = dic[np.where(dic==lan)[0][0]-1]
            except TypeError:
                out = 'Language not found.'
            except IndexError:
                out = 'Service not available.'
            return out
        elif input.lower().startswith('who am i'):
            return f'You are {message.author}.'
        elif input.lower().startswith('who are you'):
            return 'I am shyguy bot.'
        else:
            if random()<0.5 and collect_message:
                words = input.split()
                return chatbot.speak(np.random.poisson(len(words)),choice(words))
            else:
                reply = '404 Not Found.'
                try:
                    results = ddg(input, region='wt-wt', safesearch='Off', time=None, max_results=text_results)
                    reply = choice(results)['body']
                    chatbot.process(reply)
                    chatbot.record()
                    chatbot.save()
                    return reply
                except json.decoder.JSONDecodeError:
                    pass
                return reply