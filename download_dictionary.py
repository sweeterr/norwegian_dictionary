# -*- coding: utf-8 -*-
__author__ = 'sweeterr'


# install requests for python http://docs.python-requests.org/en/master/
import requests
import re
import xml.etree.ElementTree as ET
import time
import os
import random


reg_file_name = re.compile('[ \.,"?!()/]')
reg_word = re.compile('<h1>(.+?) это:</h1>')
reg_article = re.compile('<dl>(.+?)</dl>', flags=re.DOTALL)


UAS = ("Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1",
       "Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0",
       "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10; rv:33.0) Gecko/20100101 Firefox/33.0",
       "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36",
       "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 Safari/537.36",
       "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36",
       )


def get_article(text):
    word = None
    article = None
    m = reg_word.search(text)
    #m = re.search('<h1>(.+?) это:</h1>', text)
    if m:
        word = m.group(1)
        n = reg_article.search(text)
        if n:
            article = n.group(1)
    return word, article


def write_article(count, word, article, path):
    folder = str(count // 1000)
    folder_path = os.path.join(path, folder)
    if not os.path.exists(folder_path):
        os.mkdir(folder_path)
    file_name = '{}_{}.txt'.format(count, reg_file_name.sub('_', word))
    article_path = os.path.join(folder_path, file_name)
    with open(article_path, 'w', encoding='utf-8') as f:
        f.write(article)


def download_articles(main_url, articles_path):
    count = 1
    next_page = True
    while next_page:
        page_url = '{}{}'.format(main_url, count)
        ua = UAS[random.randrange(len(UAS))]
        headers = {'user-agent': ua}
        page = requests.get(page_url, headers=headers)
        word, article = get_article(page.text)
        if word is not None:
            write_article(count, word, article, articles_path)
            count += 1
        else:
            next_page = False


if __name__ == u'__main__':
    start_time = time.time()
    main_url = u'http://norwegian_russian.academic.ru/'
    articles_path = 'articles'
    if not os.path.exists(articles_path):
        os.mkdir(articles_path)
    download_articles(main_url, articles_path)
    print('{} seconds'.format(time.time() - start_time))



