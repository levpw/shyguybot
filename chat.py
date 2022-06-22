import numpy as np
import random
import json
import os

class kamek():
    def __init__(self, path = './'):
        self.dict = {}
        self.data = None
        self.path = path
        self.fn = 'chat_dict.txt'

    def save(self):
        with open(os.path.join(self.path,self.fn),'w+') as f:
            json.dump(self.dict,f)

    def check(self):
        return os.path.exists(os.path.join(self.path,self.fn))

    def load(self):
        with open(os.path.join(self.path,self.fn),'r') as f:
            self.dict = json.loads(f.read())

    def process(self, message):
        self.data = message.lower().split(' ')
        self.data = [x for x in self.data if x]

    def record(self):
        for idx,w in enumerate(self.data[:-1]):
            w_next = self.data[idx+1]
            if w in self.dict.keys():
                if w_next in self.dict[w].keys():
                    self.dict[w][w_next] += 1
                else:
                    self.dict[w][w_next] = 1
            else:
                self.dict[w] = {w_next:1}

    def speak(self, length):
        pick_from = random.choice(list(self.dict.keys()))
        next = self.dict[pick_from]
        out = pick_from
        for _ in range(length-1):
            keys_list = list(next.keys())
            prob_list = np.array(list(next.values()))
            prob_list = prob_list/np.sum(prob_list)
            pick_from = np.random.choice(keys_list,p=prob_list)
            try:
                next = self.dict[pick_from]
            except KeyError:
                break
            out += ' '+pick_from

        return out