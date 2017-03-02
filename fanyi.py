#!/usr/local/bin/python2
#-*-coding:utf-8-*-
#autho:Tony Cui
#email:cuisc13@gmail.com

import json
import sys
import urllib2
from urllib2 import HTTPError

url = "https://sp1.baidu.com/5b11fzupBgM18t7jm9iCKT-xh_/sensearch/selecttext"

def fanyi(q):
    q = q
    try:
        res = urllib2.urlopen(url+'?q=%s' % q)
        jso = res.read()
        jso = json.loads(jso)
    except HTTPError as e:
        jso = {'errno':1,'error':'Only single word supported.%s' % str(e)}

    return jso

if __name__ == '__main__':
    q = ''
    try:
        q = ' '.join(sys.argv[1:])
    except IndexError as e:
        print('No word to fanyi')
    jso = fanyi(q)
    if jso['errno']==1:
        print(jso['error'])
    else:
        result = jso['data']['result']
        #if isinstance(result,type([])):
        if jso['data']['type']==1:
            for i in result:
                print("pre.%s " % i['pre'])
                print("cont. %s\n"% i['cont'])
        else:
            print("大概要查的是: %s"% result.encode('utf-8'))
