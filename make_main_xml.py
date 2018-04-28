# -*- coding: utf-8 -*-
__author__ = 'sweeterr'


import re
import time
import os
from lxml import etree


RE_LEMMA = re.compile('<metalemma>(.+?)</metalemma>')


def main_xml(text):
    xml = etree.Element('xml')

    # file description
    fileDesc = etree.Element('fileDesc')
    respStmt = etree.Element('respStmt')
    name = etree.Element('name')
    name.text = 'Svetlana Pavlova'
    respStmt.append(name)
    fileDesc.append(respStmt)
    extent = etree.Element('extent')
    extent.text = str(79129)
    fileDesc.append(extent)
    sourceDesc = etree.Element('sourceDesc')
    ref = etree.Element('ref', target="http://norwegian_russian.academic.ru/")
    ref.text = 'Норвежско-русский словарь'
    sourceDesc.append(ref)
    p = etree.Element('p')
    p.text = 'This database was converted from the Norwegian-Russian dictionary ' \
             'downloaded from dic.academic.ru by Svetlana Pavlova.'
    sourceDesc.append(p)
    fileDesc.append(sourceDesc)
    xml.append(fileDesc)

    # dictionary description
    front = etree.Element('front')
    head = etree.Element('head')

    title = etree.Element('title', dict_id="")
    title.text = '"Норвежско-русский словарь"'
    volume = etree.Element('volume', n="1", of="1")
    author = etree.Element('author')
    publisher = etree.Element('publisher')
    editor = etree.Element('editor')
    edition = etree.Element('edition')
    translator = etree.Element('translator')
    pubdate = etree.Element('pubdate')
    pubdate.text = str(2013)
    isbn = etree.Element('isbn')
    iso = etree.Element('iso')
    for element in [title, volume, author, publisher, editor, edition, translator, pubdate, isbn, iso]:
        head.append(element)

    languages = [('source', 'nor'), ('target', 'rus'), ('content', 'rus')]
    for pair in languages:
        language = etree.Element('language', type=pair[0])
        idno = etree.Element('idno', type="iso639-3")
        idno.text = pair[1]
        language.append(idno)
        head.append(language)

    front.append(head)
    xml.append(front)

    # the entries
    body = etree.fromstring(text)
    xml.append(body)
    return xml


def alphanum_key(s):
    return int(re.split('([0-9]+)', s)[1])

def sort_nicely(l):
    return l.sort(key=lambda f: alphanum_key(f))


def combine(source):
    text = ''
    for root, dirs, files in os.walk(source):
        files = [file_name for file_name in files if file_name.endswith('.txt')]
        files = sorted(files, key=alphanum_key)
        for file_name in files:
            file_path = os.path.join(root, file_name)
            with open(file_path, 'r', encoding='utf-8') as f:
                text += f.read()
    return text


if __name__ == u'__main__':
    start_time = time.time()

    #for i in range(0,80):
    #    text = combine('articles/' + str(i))
    #    with open('big_xmls/{}.txt'.format(i), 'w', encoding='utf-8') as f:
    #        f.write(text)
    godzilla = '<body>\n{}\n</body>'.format(combine('big_xmls'))
    with open('godzilla.txt', 'w', encoding='utf-8') as f:
        f.write(godzilla)
    xml = main_xml(godzilla)
    xml_string = etree.tostring(xml, encoding='utf-8', pretty_print=True)
    with open('xml/main_xml.xml', 'w', encoding='utf-8') as f:
        f.write(xml_string.decode(encoding='utf-8'))
    print('{} seconds'.format(time.time() - start_time))
