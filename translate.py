import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()
DEEPL = os.getenv('DEEPL_TOKEN')

def translate(target_lang, text):

    data = {
        'auth_key': DEEPL,
        'text': text,
        'target_lang': target_lang
        }

    try:
        response = requests.post('https://api-free.deepl.com/v2/translate', data=data)
    except requests.exceptions.JSONDecodeError:
        return 'Authentication Error.'

    try:
        out = list(response.json().values())[0][0]['text']
    except json.decoder.JSONDecodeError:
        return 'Authentication Error.'
    except TypeError:
        return 'Wrong language code.'
    
    return out

if __name__ == '__main__':
    print(translate(['$say','de','hello']))