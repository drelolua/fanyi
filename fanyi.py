#!/usr/local/bin/python2
#-*-coding:utf-8-*-
#autho:Tony Cui
#email:cuisc13@gmail.com

import json
import sys
import os
import urllib2
import sqlite3
import time

url = "https://sp1.baidu.com/5b11fzupBgM18t7jm9iCKT-xh_/sensearch/selecttext"
home = os.environ['HOME']
db_path = home+"/.config/fanyi/fanyi.db"

def fanyi(q):
    q = q
    res = urllib2.urlopen(url+'?q=%s' % q)
    jso = res.read().decode('utf8')
    jso = json.loads(jso)

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

def query(q,qargs):
    s = ''
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

    t = time.time()
    data = {
        'key':qargs.decode('utf8'),
        'resp':s,
        'resp_jso':json.dumps(jso),
        'at_int':int(t),
        'at_str':time.strftime(u"%Y-%m-%d %H:%M:%S", time.localtime(t))

    }
    save(data)
    return s

def ifalready_translated(q):
    already = False
    resp = None

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    sql = 'select resp from log where keyword = "%s";' % q
    #print(sql)
    cur.execute(sql)

    res = cur.fetchall()

    cur.close()
    conn.commit()
    conn.close()

    if len(res) > 0:
        already = True
        resp = res[0][0]
        #print("Already faned, resp is: %s" %resp)


    return already,resp


if __name__ == '__main__':
    q = ''
    qargs = ''
    s = ''
    try:
        qargs = sys.argv[1]
        q = '+'.join(qargs.split(' '))
    except IndexError:
        s = 'No word to fanyi'
    already,s = ifalready_translated(qargs)
    if not already:
        s = query(q,qargs)

    print(s)

