#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import pandas as pd
import unicodedata
from selenium import webdriver
import re
import sys
import time
from xml.sax.saxutils import *
import chardet
import MeCab
m = MeCab.Tagger(' -d /usr/local/lib/mecab/dic/mecab-ipadic-neologd')

def mecab_parse(sentence):
    sets = m.parse(sentence.replace("\n","")).split("\n")
    sets.pop()#EOSとよくわからんやつの除去
    sets.pop()
    words = []
    for set in sets:
        words.append(set.split()[0])
    return words

#入力された文字列が日本語かどうか返す
def is_japanese(string):
    for ch in string:
        name = unicodedata.name(ch,'null')
        if "CJK UNIFIED" in name \
        or "HIRAGANA" in name \
        or "KATAKANA" in name:
            return True
    return False

#入力された文字列が存在するかbool型で返す
def is_exist(str):
     return str != None and isinstance(str,type('NoneType')) != True

#文字列が重複してないかどうか
def is_double(stri,ls):
    p = re.compile(r"<[^>]*?>")
    stri = p.sub("",stri)
    res = is_japanese(stri)
    for l in ls:
        if str == l:
            res = False
    return res

def crawl(url,driver):
    lines = []
    lists = []
    url = url.replace('"','')
    driver.get(url)
    soup=BeautifulSoup(driver.page_source, 'html.parser')
    comp = re.compile(r"<[^>]*?>")
    ######

    line = soup.prettify()
    #line = re.sub(r"<[^>]*?>",'',line)
    line = re.sub(r'[a-zA-Z0-9¥"¥.¥,¥@]+','',line)
    line = re.sub(r'[!"“#$%&()\*\+\-\.,\/:;<=>?@\[\\\]^_`{|}~]', '', line)
    line = re.sub(r'[\n|\r|\t| |]', '', line)
    line = re.sub(r'[!-~]', '', line)
    line= re.sub(r'[︰-＠]', '', line)
    time.sleep(1)
    #形態素解析に邪魔なものを除く
    #for l in lines:
    if isinstance(line,type('str')):
        for w in mecab_parse(line):
            if is_japanese(w):
                lists.append(w)
    return lists

def put_word(i):
    frac = open('list.txt', 'rb')
    words = frac.readlines()
    w = words[i].decode('utf-8').split(",")[0]
    frac.close()
    return w

def make_dict(lists):
    dic={}
    for l in lists:
        if is_japanese(l):
            if dic.get(l) == None:
                dic[l] = 1
            else:
                dic[l] += 1
    return dic

def ng_block(link):
    ng_list=["google","twitter.com","anipo.jp/anime/","tvanimedouga.blog93.fc2.com/","www.st-trigger.co.jp/","攻略wiki.","www.youtube.com"]
    for ng in ng_list:
        if link.find(ng)!=-1:
            return False
    return True

def get_urls(w,driver):
    driver.get("https://www.google.co.jp/search?q="+w)
    soup = BeautifulSoup(unescape(driver.page_source), 'html.parser')
    all_links=soup.find_all('a')
    links = []
    for l in all_links:
        if l.prettify().find("href=") != -1 and l.prettify().find("onmousedown") != -1:
            link = l.prettify().split("href=")[1].split(" ")[0]
            if ng_block(link):
                links.append(link)
    return links

if __name__ == '__main__' :
    driver = webdriver.Chrome()
    for i in range(int(sys.argv[1]),int(sys.argv[2])):
        big_list = []
        for l in get_urls(put_word(i),driver):
            big_list.extend(crawl(l,driver))
        dic = make_dict(big_list)
        out = pd.Series(dic)
        out.to_csv("sums/sum"+str(i)+".csv")
    driver.quit()
