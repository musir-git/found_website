# !/usr/bin/python 
# -*- coding: utf-8 -*- 

import urllib
import urllib2
import re
import bs4
import HTMLParser
import html5lib
import time
import Login
import cookielib
import base64
import json
import hashlib
import urlparse
import random
import codecs

weibos = []

def has_nickname(tag):
    return tag.has_key('nick-name')

def getInformation(text):
    re_h=re.compile('</?\w+[^>]*>')
    
    soup=bs4.BeautifulSoup(text)
    t=soup.select("script")
    s =''
    for text in t:
        if str(text).find('"pid":"pl_weibo_feedlist"')>0:
            s=str(text)
            break

    start=s.find("html")
    start+=7
    html_parser = HTMLParser.HTMLParser()
    s = html_parser.unescape(s[start:-12])
    end=s.find("<!--")
    s=s[:end]
    s=re.sub(r"\\\/","/",s)
    s=s.decode("unicode_escape")

    
    soup1=bs4.BeautifulSoup(s,"html5lib")

    contents=soup1.find_all("dl",{"class":"feed_list"})
 
    for i in contents:
        soup2=bs4.BeautifulSoup(str(i),from_encoding="utf-8")
        
        weibo = []

        
        if soup2.dl.has_key("isforward"):
            continue


        
        mid=soup2.dl["mid"]
        weibo.append( mid )      #0: weibo ID

        
        date=soup2.find_all('a','date')[-1]['title']
        weibo.append( date )        #1:发微博的时间
        
        
        author=soup2.findAll(has_nickname)[0].string
        weibo.append( author )  #2:微博作者

        
        authorhref=soup2.findAll('a')[1]['href']
        weibo.append( authorhref )   #3:作者主页链接
        
        
        tweet=soup2.findAll('em') 
        tweetContent=re_h.sub('',str(tweet[0]))
        weibo.append( tweetContent )   #4:微博内容
        
        
        imgs = soup2.findAll('img', 'bigcursor');
        picture = []
        for tag in imgs:
            picture.append( tag['src'] )
        weibo.append( picture )     #5:微博作者头像
        
        
        face=soup2.find_all("dt", {"class":"face"})[0]
        soup3=bs4.BeautifulSoup(str(face),from_encoding="utf-8")
        picturehref=soup3.find("img")['src']
        weibo.append( picturehref )      #6所有的附加链接
        
        weibos.append( weibo )

'''用于按时间排序的函数'''
def my_cmp( W1, W2 ):
    if W1[1] == W2[1]:
        return cmp( W1[0], W2[0] )
    else:
        return -cmp( W1[1], W2[1] )


def dealwithdata():
    global weibos
    weibos.sort( my_cmp )

    '''将获取到的数据按指定格式写入到weibo.txt文件中'''
    fout = codecs.open("data/weibo.txt",'w',encoding = 'utf-8')
    fout.write( u'\r\n' )
    l1 = len(weibos)
    if l1 > 200:
        l1 = 201
    for i in range(0, l1):
        if i!=0 and weibos[i][0] == weibos[i-1][0]:
            continue
        
        l2 = len( weibos[i] )
        for j in range(1, l2):
            if j==l2-3:
                fout.write( weibos[i][j].decode('utf8') + u'\r\n'  )
                continue
            if j ==l2-2:
                for url in weibos[i][j]:
                    fout.write( (url+' '))
                fout.write( u'\r\n' )
                continue
            fout.write( weibos[i][j] +u'\r\n' )

    fout.close()

def main():
    '''选取的一些关键词，两两组合爬取数据'''
    keyword1 = ["中大Din", "中大寻物", "中大", "中大南校", "中珠", "中大 东校区"]
    keyword2 = ["捡到", "拾到", "丢失", "丢了"]

    ct = 1
    for key1 in keyword1:
        for key2 in keyword2:
            keyword = key1 + " " + key2
            keyword = urllib.quote( str(keyword) )
            url='http://s.weibo.com/weibo/%s&page=%s' % ( keyword, str(1) )

            mt = urllib2.urlopen( url )
            s = mt.read()
            c = str(s)

            if ct == 1:
                fout = open('pincode.html', 'w')
                fout.write( c )
                fout.close()
                ct = 0
            
            getInformation( c )
            
    dealwithdata()
    
    print "success"
    
if __name__ == '__main__':
    users = [ '479021795@qq.com', '15889962394', '15902055133' ]
    pwds = [ 'crawler123456', '19910912', 'crawler123456' ]
    '''以上为申请的三个用于爬取数据的微博账号，可交替登陆'''

    l = len(users)
    num = random.randint(0, l-1)
    username = users[num]
    pwd = pwds[num]
    #如果登录成功就爬取数据
    if Login.login( username, pwd ):
        main()

