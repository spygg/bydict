#!/usr/bin/env python
# coding=utf-8
from bs4 import BeautifulSoup
import urllib.request
import urllib.parse
import re
import getopt
import sys
from termcolor import colored

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
                    by your_word  -f (give all result of translate)
                    by -h            (for help)
                    by -a            (for my spygg's github)
                  """)

def play(filename):
    play_mp3(filename)
    
    
def by_dict(argv):
    argc = len(argv)
    if argc <= 1:
        print("必应词典,by spygg 尝试输入一点东西吧!!")
        useage()
        return

    #是否发音
    audio = ''

    #是否显示全部例句
    full = ""
    
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
        elif arg in ('-f',):
            full = 'y'    
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
        
    
    #词性(名词/动词/等....
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


    #打印输出结果
    pronunciation = ""
    for i in range(0, len(pronunciation_list)):
        pronunciation = pronunciation + (pronunciation_list[i])
        #print(mp3_list[i])
        
    print(colored('[%s]' % (word.lstrip().rstrip(),), 'blue', attrs=['bold']), colored(pronunciation, 'white', 'on_green'))
        
    for i in range(0, len(word_property_list)):
        print([word_property_list[i]], trans_list[i])
        pass
            
    #print("######################################\n")

    #双语例句
    en_sentence_list = []
    cn_sentence_list = []
    for sentence in soup.find_all(class_='sen_en'):
        #print(sentence.text)
        en_sentence_list.append(sentence.text)

    for sentence in soup.find_all(class_='sen_cn'):
        #print(sentence.text)
        cn_sentence_list.append(sentence.text)

    if len(cn_sentence_list) == len(en_sentence_list):
        print('\n' + colored("双语例句:", "yellow", attrs=['bold']))
        if full == 'y':
            length =  len(cn_sentence_list)
        else:
            length =  min(3, len(cn_sentence_list))
            
        for i in range(0, length):
            print(colored("%d." % (i + 1,) + en_sentence_list[i], 'green'))
            print(colored(cn_sentence_list[i], 'magenta'))

    if(length < len(cn_sentence_list)):
        print(colored("more....", 'white', 'on_red'))
        
    #发音
    try:
        if audio == 'en':
            #print(mp3_list[0])
            #play_mp3(mp3_list[0])
            play(mp3_list[0])
        elif audio == 'us':
            #play_mp3(mp3_list[1])
            play(mp3_list[1])
    except:
        print(colored("没有语音", 'white', 'on_red'))
        pass
    
def main():
    by_dict(sys.argv)

if __name__ == '__main__':
    main()

