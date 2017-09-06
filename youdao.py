#!/usr/bin/env python
# coding=utf-8

import urllib.request
import urllib.parse
import time
import random
import hashlib
import sys

    
def tranlate(argv):
    argc = len(argv)

    sentence = ''
    if(argc <= 1):
        sentence = "人生苦短, 你需要Python!!"

    for i in range(1, argc):
        sentence = sentence + argv[i]
        
    url = r'http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule&sessionFrom=www.baidu.com'
    data = {
        'from':'AUTO',
        'to':'AUTO',
        'smartresult':'dict',
        'client':'fanyideskweb',
        'doctype':'json',
        'version':'2.1',
        'keyfrom':'fanyi.web',
        'action':'FY_BY_CLICKBUTTION',
        'typoResult':'true'
    }

##    #get data from javascript
##    para = gen_salt_sign(key)

    salt = str(int(time.time() * 1000) + random.randint(0, 9))
    sign = "fanyideskweb" + sentence + salt + "rY0D^0'nM0}g5Mm1z%1G4"
    sign = hashlib.md5(sign.encode('utf-8')).hexdigest()

    
    data['i'] = sentence
    data['salt'] = salt
    data['sign'] = sign

    headers = {
        'Host':'fanyi.youdao.com',
        'Origin':'http://fanyi.youdao.com',
        'Pragma':'no--cache',
        'Referer':'http://fanyi.youdao.com/',
        'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36',
        'X-Requested-With':'XMLHttpRequest'
    }
    
    data = urllib.parse.urlencode(data).encode('utf-8')
    request = urllib.request.Request(url = url, data = data, headers = headers, method = 'POST')
    #request = urllib.request.Request(url = url, data = data, method = 'POST')
    response = urllib.request.urlopen(request)

    print(response.read().decode('utf-8'))


if __name__ == '__main__':
    tranlate(sys.argv)

