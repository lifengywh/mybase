#!/usr/bin/env python
# -*-coding:utf-8-*-
import json
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import requests
from bs4 import BeautifulSoup
import time
import pprint
import redis

#header转化
def header_get(word):
    headers = {}
    header_list = word.strip().split("\n")
    for h in header_list:
        if 'HTTP/' in h:
            pass
        else:
            h_k,h_v = h.split(':',1)
            headers[h_k.strip()] = h_v.strip()
    pprint.pprint(headers)
    return headers

#cookie转化
def cookie_get(word):
    cookies = {}
    cookie_list = word.split(";")
    for c in cookie_list:
        c_k,c_v = c.split("=",1)
        cookies[c_k.strip()] = c_v.strip()
    pprint.pprint(cookies)
    return cookies

#去除文件空格
def space_delete(file_old,file_new):
    f = open(file_old).readlines()
    for i in f:
        if i == '\n':
            pass
        else:
            ff = open(file_new,'a')
            ff.write(i)
            ff.close()

def art_get(url):
    while 1:
        try:
            r = requests.get(url,timeout=3)
            return r
        except Exception,e:
            print 'get message lose',Exception,e,url
            time.sleep(1)

def soup_get(content):
    soup = BeautifulSoup(content,'lxml')
    return soup

#文本写入
def txt_write(file,word,word_num=0):
    if len(word) > word_num:
        f = open(file,'a+')
        f.write(word + '\n')
        f.close()

#文本去重
def txt_remove_duplicate(file_from,file_to):
    f = open(file_from,'r').readlines()
    print '>>> the old txt :',len(f)
    ff = list(set(f))
    print '>>> the new txt :',len(ff)
    for i in ff:
        txt_write(file_to,i.strip())

#免费代理获取，存入本机redis
def proxy_free_get(num,url,redis_l_name):
    redis_conn = redis.Redis(host = 'localhost', port = 6379, db = 0)
    ip_url = 'http://127.0.0.1:8000/?types=0&count=' + str(num) + '&country=中国'
    r = requests.get(ip_url)
    ip_ports = json.loads(r.text)
    proxyies_list = []
    for i in ip_ports:
        ip = i[0]
        port = i[1]
        proxies={
            'http':'http://%s:%s'%(ip,port),
            'https':'http://%s:%s'%(ip,port)
        }
        proxyies_list.append(proxies)
    a = 0
    for ip in proxyies_list:
        print ip
        try:
            r_con = requests.get(url,proxies=ip,timeout=4)
            print r_con.status_code
            if r_con.status_code == 200:
                redis_conn.lpush(redis_l_name,ip)
                print '>>> add ip success the num is: ',a
                a += 1
        except:
            pass
    return True

#无忧动态代理获取
def proxy_wuyou_get():
    r = requests.get('http://api.ip.data5u.com/dynamic/get.html?order=44683b56c4c364f479437869bba97ebd')
    proxies={
        'http':'http://%s'%(r.content.strip()),
        'https':'http://%s'%(r.content.strip())
    }
    return proxies