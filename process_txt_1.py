# -*- coding: utf-8 -*-
__author__ = 'sweeterr'


import re
import xml.etree.ElementTree as ET
import time
import os
import pickle


RE_CLEAN1 = re.compile('<div itemscope itemtype="http://webmaster.yandex.ru/vocabularies/term-def.xml">')
RE_CLEAN2 = re.compile('<br />\s*<p id="TerminSourceInfo" class="src">\s*<em><span itemprop="source">Норвежско-русский словарь</span>.\s*<span itemprop="source-date">2013</span>.</em>\s*</p>\s*</div>')
RE_NAME = re.compile('<dt itemprop="term" class="term" lang="no">(.+?)</dt>')
RE_NAME1 = re.compile('(.+?)\n')
RE_WHITE = re.compile('^\s+')
RE_LIST = re.compile('[0-9]+\)')
RE_SUPER = re.compile('<strong>I')
RE_PARADIGM = re.compile('<em>(.+?)</em>')
RE_TAG = re.compile('<.+?>')
RE_STYLE = re.compile('<u>([а-яА-ЯёЁ\.]+)</u>')
RE_POS = re.compile('<u>([a-zA-Z. ]+?)</u>')
#RE_STYLE1 = re.compile('<u>([а-яА-ЯёЁ\.]+)</u>.....+<u>([а-яА-ЯёЁ\.]+)</u>')


'''
<span class="dic_comment">(.+?)</span>'
    pret — от
    |bi∫utə'ri:|
    см.</u> <a href="http://norwegian_russian.academic.ru/8735/bev%C3%A6pne">bevæpne</a>
    besang, besunget
    p.p. от

<em>...</em>
    |kvi'taŋsə|
    kvatte (kvetjet), kvatt (kvetjet)
    от
    (
    физиол.
    pres — от

'''


class EasyEntry:
    def __init__(self, path, name, text):
        self.path = path
        self.name = name
        self.letter = name[0].lower()
        self.text = text
        self.paradigm = None
        self.style = None
        self.pos = None


def clean_text(path):
    for root, dirs, files in os.walk(source):
        for file_name in files:
            if file_name.endswith('.txt'):
                file_path = os.path.join(root, file_name)
                text = read_from_file(file_path)
                name = get_name(text)
                text = RE_CLEAN1.sub('', text)
                text = RE_CLEAN2.sub('', text)
                text = RE_NAME.sub('{}\n'.format(name), text)
                text = RE_WHITE.sub('', text)
                write_to_file(text, file_path)


def get_name(text):
    name = None
    m = RE_NAME.search(text)
    if m:
        name = m.group(1)
    return name


def read_from_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        text = f.read()
    return text


def write_to_file(text, path):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(text)


def get_entry(path, name, text):
    entry = EasyEntry(path, name, text)
    #p = RE_PARADIGM.search(text)
    #if p:
    #    paradigm = RE_TAG.sub('', p.group(1))
    #    print(paradigm)
    #    entry.paradigm = paradigm
    entry.style = get_style(text)
    entry.pos = get_pos(text)
    return entry


def get_style(text):
    style = None
    s = RE_STYLE.findall(text)
    if len(s) > 0:
        style = s
    #s1 = RE_STYLE1.findall(text)
    #if s1:
    #    print(s1)
    return style


def get_pos(text):
    pos = None
    s = RE_POS.findall(text)
    if len(s) > 0:
        pos = s
    #s1 = RE_STYLE1.findall(text)
    if len(s) > 1:
        print(s)
    return pos


def create_vocables(source):
    entries = {}
    for root, dirs, files in os.walk(source):
        for file_name in files:
            if file_name.endswith('.txt'):
                file_path = os.path.join(root, file_name)
                text = read_from_file(file_path)
                name = RE_NAME1.search(text).group(1)
                list = RE_LIST.search(text)
                if not list:
                    super = RE_SUPER.search(text)
                    if not super:
                        entry = get_entry(file_path, name, text)
                        if name not in entries:
                            entries[name] = entry
                        else:
                            if text != entries[name].text:
                                new_name = '{}_1'.format(name)
                                entries[new_name] = entry
    return entries


def write_class(entries, path):
    with open(path, 'wb') as output:
        for entry in entries:
            pickle.dump(entry, output, -1)


#def print_paradigm(path_from, path_to):
#    with open(path_from, 'rb') as input:
#        company1 = pickle.load(input)
#    print(company1.name)


if __name__ == u'__main__':
    start_time = time.time()
    source = 'articles'
    #clean_text(source)
    easy_entries = create_vocables(source)



    poses = set()
    with open('pos.txt', 'w', encoding='utf-8') as f:
        for word in easy_entries:
            entry = easy_entries[word]
            if entry.pos is not None:
                for pos in entry.pos:
                    if pos not in poses:
                        print(pos)
                        poses.add(pos)
                    f.write('{}\t{}\n'.format(pos, entry.path))
    #write_class(easy_entries, 'easy_entries.pkl')
    #print_paradigm('easy_entries.pkl', 'easy_entries_paradigm.txt')
    print('{} seconds'.format(time.time() - start_time))


    '''
    styles = set()
    with open('style_combined.txt', 'w', encoding='utf-8') as f:
        for word in easy_entries:
            entry = easy_entries[word]
            if entry.style is not None:
                for style in entry.style:
                    if style not in styles:
                        print(style)
                        styles.add(style)
                    #f.write('{}\t{}\n{}\n'.format(style, entry.path, entry.text))
'''