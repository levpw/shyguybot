import re
import numpy as np
import pandas as pd
import requests

from bs4 import BeautifulSoup

import infoCourselist

mk8_course = infoCourselist.mk8_abbrv
mk8_course_full = infoCourselist.mk8_full
mk8_course_lower = [x.lower() for x in infoCourselist.mk8_full]

def partial_match(input, full=mk8_course_lower):
    match = []
    idx = 0
    for track in full:
        if track.lower().find(input) != -1:
            match.append(idx)
        idx += 1
    return match

def name_conversion(input, abbrv=mk8_course, full=mk8_course_lower):
    found = None
    idx = 0
    for track in full:
        if track.lower() == input:
            found = abbrv[idx]
        idx += 1

    return found

def nita(input, place=None, abbrv=mk8_course):
    url = 'https://docs.google.com/spreadsheets/u/1/d/e/2PACX-1vRDdedRm18RtIu2hB9l5WrbaClaIPnZAVh_Xf7IeGzmsOVHcNdjoD3VWo8EdMxJ7JKdtcbFnebLjCcV/pubhtml'
    _ = requests.get(url)
    data = np.array(re.findall(r'(\d+):(\d+).(\d+)', requests.get(url).text))
    all_time = data[0:560].reshape(14,10,4,3)
    course = abbrv.index(str.lower(input))

    if place:
        nita = np.transpose(all_time,(0,2,1,3)).reshape(56,10,3)[course][place-1]
        return nita[0]+':'+nita[1]+'.'+nita[2]
    
    else:
        nita = np.transpose(all_time,(0,2,1,3)).reshape(56,10,3)[course][0]
        return nita[0]+':'+nita[1]+'.'+nita[2]

def wiggler(input, place=None, abbrv=mk8_course):
    url = 'https://docs.google.com/spreadsheets/u/1/d/e/2PACX-1vTOT3PJwMcMrOE--rBPV3Vz1SUegmpmpCtP8NzMQoxHljks2JDaYQ8H1pj4Pi0i5xOmnnS3eDAxc4zY/pubhtml'
    _ = requests.get(url)
    data = np.array(re.findall(r'(\d+):(\d+).(\d+)', requests.get(url).text))
    all_time = data[0:560].reshape(14,10,4,3)
    course = abbrv.index(str.lower(input))

    if place:
        nita = np.transpose(all_time,(0,2,1,3)).reshape(56,10,3)[course][place-1]
        return nita[0]+':'+nita[1]+'.'+nita[2]
    
    else:
        nita = np.transpose(all_time,(0,2,1,3)).reshape(56,10,3)[course][0]
        return nita[0]+':'+nita[1]+'.'+nita[2]

def wr(input, abbrv=mk8_course, full=mk8_course_lower):
    url = 'https://mkwrs.com/mk8dx/wrs.php'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    course = full[abbrv.index(input.lower())]
    course_link = 'track='+mk8_course_full[abbrv.index(input.lower())].replace(' ','+')
    links = []
    for link in soup.find_all('a'):
        links.append(link.get('href'))

    wr_link = 'not available'
    for idx,link in enumerate(links):
        if link.endswith(course_link):
            temp = links[idx+1]
            if temp.startswith('https://www.youtube.com/'):
                wr_link = temp

    data = np.char.lower(np.array((soup.get_text().split('\n'))))
    
    match = np.where(data==course)[0][0]
    time = data[match+1].split('\'')[0]+':'+data[match+1].split('\'')[1].split('"')[0]+'.'+data[match+1].split('\'')[1].split('"')[1]
    time = data[match+1].split('\'')[0]+':'+data[match+1].split('\'')[1].split('"')[0]+'.'+data[match+1].split('\'')[1].split('"')[1]
    player = data[match+2]
    return time+'\tby '+player+'\tvideo: '+wr_link

if __name__ == '__main__':
    print(wr('rr'))