import pandas as ps
import numpy as np 
import os
import re
from nltk import sent_tokenize
from bs4 import BeautifulSoup as bs
import requests
import random
import tqdm
from spacy.training import Example
import spacy
import pickle
colors = [
    "rouge",
    "rose",
    "bleu",
    "pourpre",
    "violet",
    "jaune",
    "orange",
    "crème",
    "blanc",
    "blanche",
    "vert",
    "brun"
]
organes = [
    "racine",
    "tige",
    "bourgeon",
    "rhizome",
    "tubercule",
    "bulbe",
    "collet",
    "limbe",
    "lobe",
    "pétiole",
    "sessile",
    "foliole",
    "calice",
    "sépale",
    "calicule",
    "corolle",
    "anthère"
    "tépale",
    "stipule",
    "foliole",
    "carpelle",
    "grappe ",
    "vrille",
    "feuille"
]

from nltk import pos_tag, word_tokenize
from nltk.stem.snowball import SnowballStemmer
stemmer = SnowballStemmer(language='french')


def f_remove_accents(old):
    """
    Removes common accent characters, lower form.
    Uses: regex.
    """
    new = old.lower()
    new = re.sub(r'[àáâãäå]', 'a', new)
    new = re.sub(r'[èéêë]', 'e', new)
    new = re.sub(r'[ìíîï]', 'i', new)
    new = re.sub(r'[òóôõö]', 'o', new)
    new = re.sub(r'[ùúûü]', 'u', new)
    return new
def especes_pages(path):
    pages = []
    for i in range(len(os.listdir(path))):
        with open(path+'/'+ str(i+1) +'.txt', 'r') as fp:
            lines = fp.readlines()
            #print("=================")
            for j in range(len(lines)):
                l = lines[j].strip()
                l = l.replace('  ',' ')
                l = f_remove_accents(l)
                x = re.search("cle.?\sdes\sespece", l)
                if(x):
                    pages.append(i+1)
                    pages.append(i+2)
                    pages.append(i+3)
    return pages
def get_especes(pages,path):
    especes = []
    for p in pages:
        with open(path+'/'+ str(p) +'.txt', 'r') as fp:
            lines = fp.readlines()
            for j in range(len(lines)):
                l = lines[j].strip()
                l = l.replace('  ',' ')
                l = f_remove_accents(l)
                x = re.findall("\s\w\.\s\w+$", l)
                x = re.findall("[A-Za-z0-9]\.\s\w\.\s\w+\.?$", l)
                if(x):
                    especes.append(x)
    especes = np.array(especes).reshape(-1)
    esp = [esp.strip().split(' ')[2][:-1] for esp in especes]
    initials = [esp.strip().split(' ')[1][:-1].upper() for esp in especes]
    return esp, initials

def preprocess(line):
    l = line.strip()
    l = l.replace('  ',' ')
    #l = f_remove_accents(l)
    return l
def get_especes_names(especes, initials, path):
    esp_names = []
    for i in range(len(os.listdir(path))):
        with open(path+'/'+ str(i+1) +'.txt', 'r') as fp:
            lines = fp.readlines()
            for j in range(len(lines)):
                l = preprocess(lines[j])
                for i, esp in enumerate(especes):
                    contains = l.find(esp.capitalize()) != -1 or l.find(esp) != -1 
                    if contains:
                        exp = "^[1-9]\.\s{}[a-z]+.*".format(initials[i])
                        x = re.findall(exp, l)
                        if(x):
                            full_name = x[0].strip()[3:]
                            full_name = full_name.split(' ')[0]+' '+full_name.split(' ')[1]
                            esp_names.append(full_name)
    return esp_names


def espece_(especes, initials, path,l):
    esp_names = []
    pos=[]
    l = preprocess(l)
    for i, esp in enumerate(especes):
        contains = l.find(esp.capitalize()) != -1 or l.find(esp) != -1 
        if contains:
            exp = "^[1-9]\.\s{}[a-z]+.*".format(initials[i])
            x = re.findall(exp, l)
            if(x):
                full_name = x[0].strip()[3:]
                full_name = full_name.split(' ')[0]+' '+full_name.split(' ')[1]
                start = [m.start() for m in re.finditer(full_name, l)]
                for st in start:
                    pos.append([st,st+len(full_name),'ESPECE'])
    return pos

def is_digit(c):
    try:
        d = int(c)
        return True
    except :
        return False



def get_glossaire():
    url="https://fr.wikipedia.org/wiki/Glossaire_de_botanique"
    response = requests.get(url)

    html = response.content

    soup = bs(html, 'lxml')

    glossaire = []
    div = soup.find("div", {"class" : "mw-parser-output"})
    uls = div.find_all("ul")
    for i, ul in enumerate(uls):
        lis = ul.find_all("li")
        for li in lis:
            if li.find("b") != None:
                noun = li.get_text().split(':')[0][:-1].strip()
                if re.search("adjectif",li.get_text()) or re.search("se dit\s",li.get_text()) or re.search("é$",noun) or re.search("qualifie\s",li.get_text()):
                    glossaire.append((noun.split(' ')[0].lower(), "adj"))
                    #print(noun.strip().split(' ')[0].lower() + ': adj')
                else:
                    glossaire.append((noun.split(' ')[0].lower(), "noun"))
                    #print(noun.strip().split(' ')[0].lower() + ': adj')
    return glossaire
###===============================
# utils functions 
###===============================

def prepare(sentence):
    sent = sentence.replace("\n", "").lower()
    sent = preprocess(sent)
    sent = " ".join(word_tokenize(sent))
    return sent

def did_overlap(pos, begin, end):
    for i, p in enumerate(pos):
        if p[0] == begin or p[1] == end:
            return True
    return False

def fix_overlap(temp):
    for i in range(len(temp)-1):
        for j in temp[i+1:]:
            if temp[i][0] == j[0] or temp[i][1] == j[1]:
                len_i = temp[i][1] - temp[i][0]
                len_j = j[1] - j[0]
                if(len_i > len_j):
                    temp.remove(j)
                else:
                    temp.remove(temp[i])
    return temp

def get_measure_begining(sent, last_index):
    last = last_index
    while True:
        virg_ind = sent[:last].rfind(",")
        if sent[virg_ind - 1].isdigit():
            last = virg_ind
        else:
            break
    if virg_ind == -1:
        try:
            begin = re.search("\d+",sent[:last]).span()[0]
        except:
            begin = sent[:last].rfind(" ") + 1
    else:
        begin = virg_ind + re.search("\d+",sent[virg_ind:]).span()[0]
    return begin

#Extract organs
def organe_(sent):
    pos = []
    tokens = word_tokenize(sent)
    for org in organes:
        stem = org
        start = [m.start() for m in re.finditer(stem, sent)]
        if len(start) != 0:
            for st in start:
                begin = st
                end = st + sent[begin:].find(' ')
                if did_overlap(pos, begin, end):
                    continue
                else:
                    pos.append([begin, end, 'ORGAN' ])
    return pos
#Extract descriptor
def descripteur(sent):
    pos = []
    tokens = word_tokenize(sent)
    for adj in adjs:
        stem = adj
        start = [m.start() for m in re.finditer(stem, sent)]
        if len(start) != 0:
            for st in start:
                begin = st
                end = st + sent[begin:].find(' ')
                if did_overlap(pos, begin, end):
                    continue
                else:
                    pos.append([begin, end, 'FORM' ])
    # try to find descriptors using POS (adjectivs ends with é,ée,és,ées)
    start = [m.start() for m in re.finditer("\w+é\s|\w+ée\s|\w+és\s|\w+ées\s", sent)]
    if len(start) != 0:
        for st in start:
            begin = st
            end = st + sent[begin:].find(' ')
            if did_overlap(pos, begin, end):
                continue
            else:
                pos.append([begin, end, 'FORM' ])
    #pos = list(set(pos))
    return pos

#Extract measure
import warnings
def measure(sent):
    pos = []
    tokens = word_tokenize(sent)
    if(re.search(" m | cm | mm ", sent)):
        measures = re.findall(" m | cm | mm ", sent)
        start = [m.start() for m in re.finditer(" m | cm | mm ", sent)]
        for i, st in enumerate(start):
            try:
                begin = get_measure_begining(sent, st)
                end = st + len(measures[i]) -1  
            except:
                msg = f"Skipping measures in the following text because the character span '{sent}' does not align with token boundaries\n"
                warnings.warn(msg)  
                continue
            if did_overlap(pos, begin, end):
                continue
            else:
                pos.append([begin, end, 'MEASURE'] )
    return pos
    
def color_1(sent):
    pos = []
    tokens = word_tokenize(sent)
    for c in colors:
        start = [m.start() for m in re.finditer(c , sent)]
        if len(start) != 0:
            for st in start:
                begin = st
                # solve the problem of finding DESC & COLOR in the same Entity
                if sent[begin:].find('-') == -1:
                    end = begin + sent[begin:].find(' ')
                else:
                    
                    end = begin + min(sent[begin:].find(' '),sent[begin:].find('-'))
                # for example verticalisé is classified as a color so we check its length 
                if did_overlap(pos, begin, end) or ((end - begin) > len(c)+2) :
                    continue
                else:
                    pos.append([begin, end, 'COLOR' ])
    return pos
# word ends with âtre
def color_2(sent):
    pos = []
    tokens = word_tokenize(sent)
    for c in colors:
        stem = c
        start = [m.start() for m in re.finditer("\s\w+âtre|\s\w+âtres" , sent)]
        if len(start) != 0:
            for st in start:
                begin = st+1
                end = begin + sent[begin:].find(' ')
                if did_overlap(pos, begin, end):
                    continue
                else:
                    pos.append([begin, end, 'COLOR'] )
    return pos
# combine both functions
def color(sent):
    pos = color_1(sent) + color_2(sent)
    pos = fix_overlap(pos)
    return pos
glossaire = get_glossaire()
adjs = [gls[0].lower() for gls in glossaire if gls[1] == "adj"]
nouns = [gls[0].lower() for gls in glossaire if gls[1] == "noun"]