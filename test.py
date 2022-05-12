import os
from initialize_guild import guildInitializer

root = './'
guild_id = 'shyguy'
guild_path = os.path.join(root,guild_id)


f = os.path.isdir(guild_path)
if not f:
    os.mkdir(guild_path)

#guildInitializer(guild_path)

def param_read(p, input):
    pars = p
    error_message = ''

    for i in range(len(pars)):
        try:
            pars[i] = int(input[i+1])
        except IndexError:
            error_message += f'Missing input at position {i}, using default value.'+'\n'
        except ValueError:
            error_message += f'Invalid input at position {i}. using default value.'+'\n'

    return pars, error_message

t = '''
data = 'a 1 2'
input = data.split(' ')
p,t = param_read([-1,0],input)
if t:
    print(t)
'''

x = '''
a b
c d
d f
'''

def read_text(text_in):
    list = [[],[]]
    lines = text_in.splitlines()
    for line in lines[1:]:
        elements = line.strip(' ').split(' ',1)
        for idy,element in enumerate(elements):
            list[idy].append(element.strip(' '))

    return list

import pandas as pd

import infoCourselist

mk8_course = infoCourselist.mk8_abbrv
mk8_course_full = infoCourselist.mk8_full

def write_text(list1,list2,columns):
    data = list(zip(list1,list2))
    df = pd.DataFrame(data, columns=columns)
    return df.to_string(index=False)

#read_text(x)
x = write_text(mk8_course,mk8_course_full,['abbrv','full'])
list = read_text(x)
print(list[0],list[1])

data = 'a 1 2'
input = data.split(' ')
p,t = param_read([-1,0],input)
if t:
    print(t)
else:
    print('ok')

a = []
for aa in a:
    print(aa)

if a:
    print('aaa')

b = ['a']
print(b[1:])
print(b.index('a'))