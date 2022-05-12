import enum
import os
import numpy as np
import pandas as pd
from PIL import Image, ImageFont, ImageDraw
from difflib import SequenceMatcher

def matching(a, b, la, lb):
    if a == 0 and b == 0:
        return True
    elif a == 0 and b == lb:
        return True
    elif a == la and b == 0:
        return True
    elif a == la and b == lb:
        return True
    else:
        return False

def make_group(ids):
    groups = {}
    group_result = np.zeros(len(ids))
    group_index = 1
    #strong match
    group_bool = group_result==0
    for idx, idboolx in enumerate(group_bool):
        if idboolx:
            for idy, idbooly in enumerate(group_bool):
                if idbooly:
                    if idx < idy:
                        match = SequenceMatcher(None, ids[idx], ids[idy]).find_longest_match()
                        if match.size > 1 and matching(match.a,match.b,len(ids[idx])-match.size,len(ids[idy])-match.size):
                            tag = ids[idx][match.a:match.a+match.size].split(' ')[0]
                            if tag in groups.keys():
                                groups[tag] += [idy]
                                group_result[idy] = group_index
                            else:
                                groups[tag] = [idx,idy]
                                group_result[idx] = group_index
                                group_result[idy] = group_index
                            group_index+=1
                            group_bool = group_result==0

    #weak match
    group_bool = group_result==0
    if np.sum(group_bool*1)>0:
        for idx, idboolx in enumerate(group_bool):
            if idboolx:
                for idy, idbooly in enumerate(group_bool):
                    if idbooly:
                        if idx < idy:
                            match = SequenceMatcher(None, ids[idx], ids[idy]).find_longest_match()
                            if match.size > 0 and matching(match.a,match.b,len(ids[idx])-match.size,len(ids[idy])-match.size):
                                tag = ids[idx][match.a:match.a+match.size].split(' ')[0]
                                if tag in groups.keys():
                                    groups[tag] += [idy]
                                    group_result[idy] = group_index
                                else:
                                    groups[tag] = [idx,idy]
                                    group_result[idx] = group_index
                                    group_result[idy] = group_index
                                group_index+=1
                                group_bool = group_result==0

    #no match
    if np.sum(group_bool*1)==len(ids):
        return None

    #zero match
    elif np.sum(group_bool*1)>0:
        groups[''] = []
        group_bool = group_result==0
        for idx, idboolx in enumerate(group_bool):
            if idboolx:
                groups[''] += [idx]

    groups_out = {}
    temp = groups.copy()
    for tag in groups.keys():
        try:
            temp.pop(tag)
            to_remove = []
            for k in temp.keys():
                if SequenceMatcher(None, tag, k).ratio() >= 0.75:
                    to_remove.append(k)
            for k in to_remove:
                groups[tag] += temp.pop(k)
            groups_out[tag] = list(set(groups[tag]))
        except KeyError:
            pass

    return groups_out

def write_image(ids, scores, outdir, bkgd=None, theme='default', fontfile='./fonts/DotGothic16/DotGothic16-Regular.ttf'):
    if bkgd:
        out = Image.open(bkgd)
        out = out.resize((1280,720))
    else:
        out = Image.new('RGBA',(1280,720),color=(0,0,0))
    f_size = 25
    f_space = 0.75

    img = ImageDraw.Draw(out)
    white = (255,255,255)
    au = (255,215,0)
    ag = (192,192,192)
    cu = (184,115,51)
    gray = (128,128,128)

    font = ImageFont.truetype(fontfile, f_size*3)
    img.text((425,30), 'Match Result', white, font=font)
    font = ImageFont.truetype(fontfile, f_size)
    img.text((1100,10), 'shyguy bot', gray, font=font)

    scores_copy = []
    for s in scores:
        try:
            scores_copy.append(int(s))
        except ValueError:
            scores_copy.append(0)

    groups = make_group(ids)

    if not groups:
        font = ImageFont.truetype(fontfile, f_size)
        ranks = np.argsort(-1.0*np.array(scores_copy))
        for idx,rank in enumerate(ranks):
            if idx == 0:
                color = au
            elif idx == 1:
                color = ag
            elif idx == 2:
                color = cu
            else:
                color = white
            img.text((550,160+idx*f_size*(f_space+1)), ids[rank], color, font=font)
            img.text((750,160+idx*f_size*(f_space+1)), scores[rank], color, font=font)
        out.save(outdir)
        return 0

    else:
        group_height = 100
        group_scores = []
        for group in groups.keys():
            group_score = 0
            for i in groups[group]:
                group_score += scores_copy[i]
            group_scores.append(group_score)
        ranks = np.argsort(-1*np.array(group_scores))

        idz = 0
        for idx,group in enumerate(groups.keys()):

            group_players = len(groups[group])
            this_group_height = 560*group_players/len(ids)

            if idx == ranks[0]:
                color = au
            elif idx == ranks[1]:
                color = ag
            elif idx == ranks[2]:
                color = cu
            else:
                color = white

            font = ImageFont.truetype(fontfile, f_size*2)
            coord = (200,group_height+this_group_height*0.5)
            img.text(coord, group, color, font=font)
            coord = (450,group_height+this_group_height*0.5)
            img.text(coord, str(group_scores[idx]), color, font=font)
            group_height += this_group_height
            for id in groups[group]:
                font = ImageFont.truetype(fontfile, f_size)
                pid = ids[id].replace(group,'')
                coord = (800,160+idz*f_size*(f_space+1))
                img.text(coord, pid, color, font=font)
                coord = (1000,160+idz*f_size*(f_space+1))
                img.text(coord, str(scores[id]), color, font=font)
                idz+=1
    
        out.save(outdir)
        return 0

if __name__ == '__main__':
    bkgd = './tests/ifJPbUm9XMsQdt7AQAets.jpeg'
    ids = ['VJASLOVE', 'てきせいブロンズ', 'てきせい"irロn"', 'Z* Trickpa', 'CT Nathan', 'Z Carton', 'CT※Yaans', 'CT Srps', 'アーニャLOVE', 'Z Antonup', 'てきせいグラマス', ':LOVE']
    scores = ['105', '92', '91', '90', '81', '78', '77', '74', '71', '65', '60', '14']
    write_image(ids, scores, outdir='./test1.png', bkgd = bkgd)

    ids = ['PHG Rein', 'SKR" dOhOh', 'PHG Start', 'くえんちゃんっ !', 'くえん', 'SKRsanchan', 'SKR*おたんちん', 'くえん', 'SKR*はるにゃん', 'PHG Andrs', 'PHGxAndyEM', 'くえん']
    scores = ['114', '112', '94', '92', '92', '80', '74', '72', '66', '63', '61', '56']
    write_image(ids, scores, outdir='./test2.png', bkgd = bkgd)

    ids = ['HD cynda', 'ARCsBran', 'HD James', 'ARC*Monfi', 'HD chibi', 'ARC Arti', 'ARC> Teeps', 'HD Markus', 'HD Soldier', 'HD DUGO', 'ARC Mori', 'ARC Blue']
    scores = ['98', '97', '91', '86', '85', '83', '81', '79', '77', '75', '73', '59']
    write_image(ids, scores, outdir='./test3.png', bkgd = bkgd)

    ids = ['LL', 'Chiyodabb', 'Az', 'Flare', '15 Den', 'LLxpatreze', '15*toraaa', 'Flower', 'Chocoyama', 'DD', 'DDDDDh', 'A']
    scores = ['101', '89', '71', '104', '68', '70', '91', '58', '64', '62', '94', '87']
    write_image(ids, scores, outdir='./test4.png', bkgd = bkgd)

    ids = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'か', 'ま', 'は', 'ば', 'さ']
    scores = ['101', '89', '71', '104', '68', '70', '91', '58', '64', '62', '94', '87']
    write_image(ids, scores, outdir='./test5.png', bkgd = bkgd)

    ids = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'か', 'ま', 'は', 'ば', 'さ']
    scores = ['', '89', '71', '104', '68', '70', '91', '58', '64', '62', '94', '87']
    write_image(ids, scores, outdir='./test5.png', bkgd = None)