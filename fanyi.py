#!/usr/local/bin/python2
#-*-coding:utf-8-*-
#autho:Tony Cui
#email:cuisc13@gmail.com

import json
import sys
import os
import urllib2
import sqlite3
from urllib2 import HTTPError
import time

url = "https://sp1.baidu.com/5b11fzupBgM18t7jm9iCKT-xh_/sensearch/selecttext"
home = os.environ['HOME']
db_path = home+"/.config/fanyi/fanyi.db"

def fanyi(q):
    q = q
    try:
        res = urllib2.urlopen(url+'?q=%s' % q)
        jso = res.read().decode('utf8')
        jso = json.loads(jso)
    except HTTPError as e:
        jso = {'errno':1,'error':'Only single word supported.%s' % str(e)}

    return jso

def save(data):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    fmt = u'''
    insert into log
    (keyword, resp, resp_jso, at_int, at_str)
    values
    ('{0[key]}', '{0[resp]}','{0[resp_jso]}', {0[at_int]}, '{0[at_str]}')
    ;
    '''
    sql = fmt.format(data)
    cur.execute(sql)
    cur.close()
    conn.commit()
    conn.close()



if __name__ == '__main__':
    q = ''
    qargs = ''
    s = ''
    t = time.time()
    try:
        qargs = sys.argv[1]
        q = '+'.join(qargs.split(' '))
    except IndexError as e:
        s = 'No word to fanyi'
    jso = fanyi(q)
    if jso['errno']==1:
        s = jso['error']
    else:
        result = jso['data']['result']
        #if isinstance(result,type([])):
        if jso['data']['type']==1:
            s = ''
            for i in result:
                s += "pre.%s \n" % i['pre']
                s += "cont. %s\n"% i['cont']
        else:
            s = "Maybe is : %s"% result
    print(s)
    data = {
        'key':qargs.decode('utf8'),
        'resp':s.replace('\n', ' '),
        'resp_jso':json.dumps(jso),
        'at_int':int(t),
        'at_str':time.strftime(u"%Y-%m-%d %H:%M:%S", time.localtime(t))

    }
    save(data)
