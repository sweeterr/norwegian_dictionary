# -*- coding: utf-8 -*-
__author__ = 'sweeterr'


import re
import time
import os


RE_WHITE = re.compile('^\s+')
SUPER = '<superEntry>\n<metalemma>{}</metalemma>\n{}</superEntry>'
RE_DD1 = re.compile('<dd itemprop="definition" class="descript" lang="ru">')
#RE_DD2 = re.compile('/dd')
RE_DD2 = re.compile('<>')
RE_STRONG = re.compile('<div><strong>([IVX]+)</strong>')
RE_FIRST = re.compile('<div><strong>I</strong>')
ENTRY_START = '<entry>\n<index></index>\n<form>\n<orth type="lemma">{}</orth>\n'
RE_LEMMA = re.compile('<metalemma>(.+?)</metalemma>')
RE_EXAMPLE1 = re.compile('<div style="margin-left:5px"><strong><p><span class="dic_example">(.+?) — (.+?)</span></p></strong></div>')
#RE_EM = re.compile(<em><span class="dic_color"><span class="dic_comment">-'en, -'er</span></span></em></div>)
RE_EM = re.compile('<em><span class="dic_color"><span class="dic_comment">(.+?)</span></span></em></div>')



def read_from_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        text = f.read()
    return text


def write_to_file(text, path):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(text)


def clean_text(path):
    for root, dirs, files in os.walk(path):
        for file_name in files:
            if file_name.endswith('.txt'):
                new_text = ''
                file_path = os.path.join(root, file_name)
                with open(file_path, 'r', encoding='utf-8') as f:
                    for line in f:
                        line = RE_WHITE.sub('', line)
                        new_text += line
                write_to_file(new_text, file_path)


def top_markup(path):
    for root, dirs, files in os.walk(path):
        for file_name in files:
            if file_name.endswith('.txt'):
                file_path = os.path.join(root, file_name)
                with open(file_path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    lemma = lines[0].replace('\n', '')
                    text = ''.join(lines[1:])
                    new_text = SUPER.format(lemma, text)
                write_to_file(new_text, file_path)


def del_dd(path):
    for root, dirs, files in os.walk(path):
        for file_name in files:
            if file_name.endswith('.txt'):
                file_path = os.path.join(root, file_name)
                with open(file_path, 'r', encoding='utf-8') as f:
                    text = f.read()
                    #text = RE_DD1.sub('', text)
                    text = RE_DD2.sub('', text)
                write_to_file(text, file_path)


def separate_entries(path):
    for root, dirs, files in os.walk(path):
        for file_name in files:
            if file_name.endswith('.txt'):
                file_path = os.path.join(root, file_name)
                with open(file_path, 'r', encoding='utf-8') as f:
                    text = f.read()
                    lemma = RE_LEMMA.search(text).group(1)
                    new_entry = ENTRY_START.format(lemma)
                    text = re.sub('</metalemma>', '</metalemma>\n' + new_entry, text)
                    text = re.sub('</superEntry>', '</entry>\n</superEntry>', text)
                    text = RE_FIRST.sub('', text)
                    text = RE_STRONG.sub('</entry>\n' + new_entry, text)
                write_to_file(text, file_path)


def find_examples(path):
    exs = []
    for root, dirs, files in os.walk(path):
        for file_name in files:
            if file_name.endswith('.txt'):

                file_path = os.path.join(root, file_name)
                with open(file_path, 'r', encoding='utf-8') as f:
                    text = f.read()
                    e = RE_EXAMPLE1.findall(text)
                    for ex in e:
                        nor = ex[0].strip(' –:')
                        rus = ex[1].strip(' –:')
                        exs.append((file_path, nor, rus))
    with open('examples1.txt', 'w', encoding='utf-8') as f:
        for ex in exs:
            f.write('{}; {}; {}\n'.format(ex[0], ex[1], ex[2]))


def find_gram(path):
    ems = []
    for root, dirs, files in os.walk(path):
        for file_name in files:
            if file_name.endswith('.txt'):
                file_path = os.path.join(root, file_name)
                with open(file_path, 'r', encoding='utf-8') as f:
                    text = f.read()
                    em = RE_EM.findall(text)
                    for e in em:
                        ems.append((file_path, em))
    with open('ems1.txt', 'w', encoding='utf-8') as f:
        for em in ems:
            f.write('{}; {}\n'.format(em[0], em[1]))


def separate_senses(path):
    ems = []
    for root, dirs, files in os.walk(path):
        for file_name in files:
            if file_name.endswith('.txt'):
                file_path = os.path.join(root, file_name)
                with open(file_path, 'r', encoding='utf-8') as f:
                    text = f.read()
                    text = re.sub('<div>1\)', '</form>\n<sense>', text)
                    text = re.sub('<div style="margin-left:5px"><strong><p><span class="dic_example">1\)',
                                  '</form>\n<sense>\n<div style="margin-left:5px"><strong><p><span class="dic_example">',
                                  text)
                    text = re.sub('<div style="margin-left:5px"><strong><p><span class="dic_example">[1-9][0-9]?\)',
                                  '</sense>\n<sense>\n<div style="margin-left:5px"><strong><p><span class="dic_example">',
                                  text)
                    text = re.sub('</entry>', '</sense>\n</entry>', text)
                    text = re.sub('<div>[1-9][0-9]?\)', '</sense>\n<sense>', text)
                write_to_file(text, file_path)


def translation1(path):
    for root, dirs, files in os.walk(source):
        for file_name in files:
            if file_name.endswith('.txt'):
                file_path = os.path.join(root, file_name)
                with open(file_path, 'r', encoding='utf-8') as f:
                    text = f.read()
                    text = re.sub('<div style="margin-left:5px"><strong><p><span class="dic_example">'
                                  '(\( — .+?)</span></p></strong></div>',
                                  '<cit type="translation">\n<language>\n<idno type="iso639-3">rus</idno>\n'
                                  '</language>\n<quote>\\1</quote>\n</cit>\n', text)
                write_to_file(text, file_path)


def find_string(path1, path2):
    lines = []
    for root, dirs, files in os.walk(path1):
        for file_name in files:
            if file_name.endswith('.txt'):
                file_path = os.path.join(root, file_name)
                with open(file_path, 'r', encoding='utf-8') as f:
                    for line in f:
                        m = re.search('^[^<]', line)
                        #m = re.search('.+?<div>', line)
                        if m:
                            #lines.append((file_path, m.group(1) + '; ' + m.group(2)))
                            lines.append((file_path, line))
    with open(path2, 'w', encoding='utf-8') as f:
        for line in lines:
            f.write('{}; {}'.format(line[0], line[1]))


def find_multiline(path1, path2):
    lines = []
    for root, dirs, files in os.walk(path1):
        for file_name in files:
            if file_name.endswith('.txt'):
                file_path = os.path.join(root, file_name)
                with open(file_path, 'r', encoding='utf-8') as f:
                    text = f.read()
                    m = re.findall('</sense>', text)
                    for case in m:
                        #lines.append((file_path, m.group(1) + '; ' + m.group(2)))
                        lines.append((file_path, case))
    with open(path2, 'w', encoding='utf-8') as f:
        for line in lines:
            f.write('{}{}\n\n'.format(line[0], line[1]))


def sub_multiline(path1):
    lines = []
    for root, dirs, files in os.walk(path1):
        for file_name in files:
            if file_name.endswith('.txt'):
                file_path = os.path.join(root, file_name)
                with open(file_path, 'r', encoding='utf-8') as f:
                    text = f.read()
                    #text = re.sub('(<div style="margin-left:5px"><strong><p><span class="dic_example">([ a-zA-ZæøåÆØÅé(),—:]+)\n)'
                    #              'а\)(.+?)\n',
                    #              '\g<1><сit type = "example"><text>\g<2></text><cit type ="ex_translation"><language><idno type="iso639-3">rus</idno></language><text>\g<3></text></cit></cit>\n', text)
                    text = re.sub('(<div style="margin-left:5px"><strong><p><span class="dic_example">([ a-zA-ZæøåÆØÅé(),—:]+)\n)'
                                  '((.+[^:]\n)*?)'
                                  'г\)(.+?)\n',
                                  '\g<1>\g<3><сit type = "example"><text>\g<2></text><cit type ="ex_translation"><language><idno type="iso639-3">rus</idno></language><text>\g<5></text></cit></cit>\n', text)

                write_to_file(text, file_path)




def examples(path):
    for root, dirs, files in os.walk(source):
        for file_name in files:
            if file_name.endswith('.txt'):
                file_path = os.path.join(root, file_name)
                with open(file_path, 'r', encoding='utf-8') as f:
                    text = f.read()
                    #lemma = RE_LEMMA.search(text)
                    #new_entry = ENTRY_START.format(lemma.group(1))
                    text = re.sub('<div style="margin-left:5px"><strong><p><span class="dic_example">(.+?) — (.+?)?<',
                                  '<сit type="example"><text>\g<1></text><cit type ="ex_translation"><language><idno type="iso639-3">rus</idno></language><text>\g<2></text></cit></cit>', text)
                write_to_file(text, file_path)

def orth(path):
    for root, dirs, files in os.walk(source):
        for file_name in files:
            if file_name.endswith('.txt'):
                file_path = os.path.join(root, file_name)
                with open(file_path, 'r', encoding='utf-8') as f:
                    text = f.read()
                    #lemma = RE_LEMMA.search(text)
                    #new_entry = ENTRY_START.format(lemma.group(1))
                    text = re.sub('<em><span class="dic_color"><span class="dic_comment">(.+?)</span></span></em>',
                                  '<gramGrp></gramGrp><inflection><orth>\g<1></orth></inflection>', text)
                write_to_file(text, file_path)


def num(path):
    for root, dirs, files in os.walk(source):
        for file_name in files:
            if file_name.endswith('.txt'):
                file_path = os.path.join(root, file_name)
                with open(file_path, 'r', encoding='utf-8') as f:
                    text = f.read()
                    #lemma = RE_LEMMA.search(text)
                    #new_entry = ENTRY_START.format(lemma.group(1))
                    text = re.sub('(<div>)?<u>pl</u>(</div>)?',
                                  '<gramGrp><num>pl</num></gramGrp>', text)
                write_to_file(text, file_path)


def pos(path):
    for root, dirs, files in os.walk(source):
        for file_name in files:
            if file_name.endswith('.txt'):
                file_path = os.path.join(root, file_name)
                with open(file_path, 'r', encoding='utf-8') as f:
                    text = f.read()
                    #lemma = RE_LEMMA.search(text)
                    #new_entry = ENTRY_START.format(lemma.group(1))
                    text = re.sub('(<div>)?<u>(.+?)</u>(</div>)?',
                                  '<gramGrp><pos>\g<2></pos></gramGrp>', text)
                write_to_file(text, file_path)


def usg(path):
    for root, dirs, files in os.walk(source):
        for file_name in files:
            if file_name.endswith('.txt'):
                file_path = os.path.join(root, file_name)
                with open(file_path, 'r', encoding='utf-8') as f:
                    text = f.read()
                    #lemma = RE_LEMMA.search(text)
                    #new_entry = ENTRY_START.format(lemma.group(1))
                    text = re.sub('<gramGrp><pos>([а-яА-ЯёЁ\.]+?)</pos></gramGrp>',
                                  '<usg>\g<1></usg>', text)
                write_to_file(text, file_path)


def del_text(path):
    for root, dirs, files in os.walk(path):
        for file_name in files:
            if file_name.endswith('.txt'):
                file_path = os.path.join(root, file_name)
                with open(file_path, 'r', encoding='utf-8') as f:
                    text = f.read()
                    #lemma = RE_LEMMA.search(text)
                    #new_entry = ENTRY_START.format(lemma.group(1))

#                    text = re.sub('(<div style="margin-left:5px"><strong><p><span class="dic_example">[ a-zA-ZæøåÆØÅ,]+)\n',

                    text = re.sub('</usg>\n<usg>',
                                  ', ', text)
                write_to_file(text, file_path)


def sense1(source):
    for root, dirs, files in os.walk(source):
        for file_name in files:
            if file_name.endswith('.txt'):
                file_path = os.path.join(root, file_name)
                with open(file_path, 'r', encoding='utf-8') as f:
                    text = f.read()
                    entries = re.findall('<entry>.+?</entry>', text, flags=re.DOTALL)
                    for entry in entries:
                        sense_o = re.findall('<sense>', entry)
                        sense_c = re.findall('</sense>', entry)
                        if len(sense_o) != len(sense_c):
                            i_inf = entry.find('</inflection>')
                            i_gram = entry.find('</gramGrp>')
                            i_usg = entry.find('</usg>')
                            i_orth = entry.find('</orth>')
                            i_phon = entry.find('</phon>')
                            i = max(i_gram, i_inf, i_orth, i_usg, i_phon)
                            if i == i_usg:
                                entry1 = re.sub('</usg>', '</usg>\n</form>\n<sense>', entry)
                            elif i == i_inf:
                                entry1 = re.sub('</inflection>', '</inflection>\n</form>\n<sense>', entry)
                            elif i == i_gram:
                                entry1 = re.sub('</gramGrp>', '</gramGrp>\n</form>\n<sense>', entry)
                            elif i == i_phon:
                                entry1 = re.sub('</phon>', '</phon>\n</form>\n<sense>', entry)
                            elif i == i_orth:
                                entry1 = re.sub('(\n<orth.+?)</orth>', '\g<1></orth>\n</form>\n<sense>', entry)
                            if i == -1:
                                print(file_path)
                            text = re.sub(re.escape(entry), entry1, text)
                write_to_file(text, file_path)



def translation(source):
    for root, dirs, files in os.walk(source):
        for file_name in files:
            if file_name.endswith('.txt'):
                file_path = os.path.join(root, file_name)
                with open(file_path, 'r', encoding='utf-8') as f:
                    text = f.read()
                    #lemma = RE_LEMMA.search(text)
                    #new_entry = ENTRY_START.format(lemma.group(1))
                    text = re.sub('^[а-яА-ЯёЁ].+',
                                  '<cit type="translation"><language><idno type="iso639-3">rus</idno></language><text>\g<0></text></cit>', text)
                write_to_file(text, file_path)



if __name__ == u'__main__':
    start_time = time.time()
    source = 'articles'
    #clean_text(source)
    #top_markup(source)
    #del_dd(source)
    #separate_entries(source)
    #find_gram(source)
    #separate_senses(source)
    #find_examples(source)
    #translation1(source)
    #find_string(source, 'example_list.txt')
    #find_multiline(source, 'example_list.txt')
    #sub_multiline(source)
    #del_text('pilot')
    #del_text(source)
    #examples('pilot')
    #orth('pilot')
    #num(source)
    #pos(source)
    #usg(source)
    sense1(source)
    #translation(source)
    print('{} seconds'.format(time.time() - start_time))



# <gramGrp><pos><span class="dic_color"><span class="dic_comment">см.</pos></gramGrp>
# порядок Gram vs inflection
# тк. sg
# rel
# <sense> <u>мат.</u><span class="dic_color"><span class="dic_comment">, <u>астр.</u> высота ЗНАЧЕНИЕ НЕ НА ОТД СТРОКЕ
#

'''
text = re.sub('(\n[а-яА-ЯёЁ ][а-яА-ЯёЁ ]+.+?):\n'
                                   'а\)(.+?\n'
                                   '(.+\n)*?)'
                                   'б\)(.+?\n'
                                   '(.+\n)*?)'
                                   'в\)(.+?\n'
                                   '(.+\n)*?)'
                                   'г\)(.+?\n'
                                   '(.+\n)*?)'
                                   'д\)(.+?\n'
                                   '(.+\n)*?)'
                                   'е\)(.+?\n'
                                   '(.+\n)*?)'
                                   '</sense>',
                               '\g<1>\g<2></sense>\n<sense>'
                               '\g<1>\g<4></sense>\n<sense>'
                               '\g<1>\g<6></sense>\n<sense>'
                               '\g<1>\g<8></sense>\n<sense>'
                               '\g<1>\g<10></sense>\n<sense>'
                               '\g<1>\g<12></sense>', text)




m = re.findall('(\n[а-яА-ЯёЁ ][а-яА-ЯёЁ ]+.+?:\n'
                                   'а\).+?\n'
                                   '(.+\n)*?'
                                   'б\).+?\n'
                                   '(.+\n)*?'
                                   '(в\).+?\n)?'
                                   '(.+\n)*?'
                                   '(г\).+?\n)?'
                                   '(.+\n)*?'
                                   '(д\).+?\n)?'
                                   '(.+\n)*?'
                                   '(е\).+?\n)?'
                                   '(.+\n)*?'
                                   '(ё\).+?\n)?'
                                   '(.+\n)*?'
                                   '(ж\).+?\n)?'
                                   '(.+\n)*?'
                                   '(з\).+?\n)?'
                                   '(.+\n)*?'
                                   '</sense>)', text)


'''