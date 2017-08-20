#!/usr/bin/env python
# coding=utf-8
from bs4 import BeautifulSoup
import urllib.request
import urllib.parse
import re
import getopt
import sys
from multiprocessing import Process


#导入包,又是一个恶心的东西
try:
    from audio import *
except:
    from .audio import *

try:
    from version import script_name, __version__
except:
    from .version import script_name, __version__
    
def useage():
    print("""Useage:
                    by your_word     (basic use)
                    by your_word  -e (prounce in UK English accent, for english word only)
                    by your_word  -u (prounce in US. English accent, for english word only)
                    by -h            (for help)
                    by -a            (for my spygg's github)
                  """)

def play(filename):
    play_mp3(filename)
    
def play_mp3_by_process(filename):
    p = Process(target=play, args=(filename,))
    p.start()
    p.join()
    
def by_dict(argv):
    argc = len(argv)
    if argc <= 1:
        print("必应词典,by spygg 尝试输入一点东西吧!!")
        useage()
        return

    #是否发音
    audio = ''

    #要查询的单词
    word = ''
    
    args = argv[1:]
   
    for arg in args:
        if arg in ('-h',):
            print(argv[0] + " " + "word")
            return
        elif arg in ('--help',):
            useage()
            return
        elif arg in ('-v', '--version'):
            print(script_name + " version " +  __version__)
            return
        elif arg in ('-a', '--about'):
            print('biying dict by spygg, for more infomation goto')
            print('www.github.com/spygg/bydict')
            return
        elif arg in ('-e',):
            audio = 'en'
        elif arg in ('-u',):
            audio = 'us'
        else:
            if arg.find('-') >= 0:
                useage()
                return
            word = "%s %s" % (word, arg)

        
          
    url = 'http://cn.bing.com/dict/search?q='

    #使用网址转码
    key = urllib.parse.quote(word)
    url = url + key
    
    response = urllib.request.urlopen(url)
    html = response.read().decode('utf-8')
  
    #print(html)
    soup = BeautifulSoup(html, "lxml")

    #print(soup.find_all(class_='hd_p1_1'))
    
    #拼音
    pronunciation_list = []
    mp3_list = []
    for prs in soup.find_all(class_=re.compile("hd_p1_1")):

        #英文读音
        for pr in prs.find_all(class_=re.compile("hd_pr")):
            pronunciation_list.append(pr.text)

        #中文拼音
        if len(pronunciation_list) <= 0 and prs.text:
            pronunciation_list.append(prs.text)
            
        for sound in prs.find_all(class_='bigaud'):
            if str(sound):
                #print(str(sound))
                pattern = re.compile(r"(?P<url>http.+?mp3)");
                result = re.search(pattern, str(sound))
                if result:
                    mp3_list.append(result.group('url'))
                    #print(result.group('url'))
                    #print('---------------------')
        
    
    #词性
    word_property_list = []
    for ul in soup.find_all('ul'):
        temp_list = ul.find_all(class_="pos") 
        if len(temp_list) > 0:
            for src in temp_list:
                word_property_list.append(src.text)

    
    #翻译结果
    trans_list = []
    for temp_list in soup.find_all(class_="def"):
        trans_list.append(temp_list.text)

    if len(pronunciation_list) > 0:
        word = word + ":"
        
    for i in range(0, len(pronunciation_list)):
        word = word + (pronunciation_list[i])
        #print(mp3_list[i])
    print(word)
    for i in range(0, len(word_property_list)):
        print([word_property_list[i]], trans_list[i])
        pass
            
    #print("######################################\n")

    #发音
    try:
        if audio == 'en':
            #print(mp3_list[0])
            #play_mp3(mp3_list[0])
            play_mp3_by_process(mp3_list[0])
        elif audio == 'us':
            #play_mp3(mp3_list[1])
            play_mp3_by_process(mp3_list[1])
    except:
        print("没有语音")
        pass
        
def main():
    by_dict(sys.argv)

if __name__ == '__main__':
    main()

