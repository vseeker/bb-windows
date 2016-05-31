# -*- coding:utf-8 -*-
from datetime import datetime
import wave
import urllib, urllib2, pycurl
import base64
import json
import StringIO
import smtplib
import string
import os
import time
from ftplib import FTP  # 从ftplib模块中导入FTP


def get_token():
    apiKey = "ksAE6RQ7tHNSvQI2dayBdCZZ"#百度语音开放平台申请的API Key和Secret Key
    secretKey = "a66c5e2fefff7be6f8354f567177e04f"#Secret Key

    auth_url = "https://openapi.baidu.com/oauth/2.0/token?grant_type=client_credentials&client_id="\
    + apiKey + "&client_secret=" + secretKey;#百度授权服务地址

    res = urllib2.urlopen(auth_url)
    json_data = res.read()
    return json.loads(json_data)['access_token']

def use_cloud(token, fileName):
    #fp = wave.open('login.wav', 'rb')
    fp = wave.open(fileName, 'rb')
    nf = fp.getnframes()
    f_len = nf * 2
    audio_data = fp.readframes(nf)
    cuid = "B8-88-E3-8D-0E-6C" #电脑MAC
    srv_url = 'http://vop.baidu.com/server_api' + '?cuid=' + cuid + '&token=' + token

    http_header = [
        'Content-Type: audio/pcm; rate=16000',
        'Content-Length: %d' % f_len
    ]#当音频是16K的时候rate=16000，如果音频是8K的时候rate=8000

    b = StringIO.StringIO()
    c = pycurl.Curl()
    c.setopt(pycurl.URL, str(srv_url)) #curl doesn't support unicode
    #c.setopt(c.RETURNTRANSFER, 1)
    c.setopt(c.HTTPHEADER, http_header)   #must be list, not dict
    c.setopt(c.POST, 1)
    c.setopt(c.CONNECTTIMEOUT, 30)
    c.setopt(c.TIMEOUT, 30)
    #c.setopt(c.WRITEFUNCTION, dump_res)
    c.setopt(c.WRITEFUNCTION, b.write)
    c.setopt(c.POSTFIELDS, audio_data)
    c.setopt(c.POSTFIELDSIZE, f_len)
    c.perform() #pycurl.perform() has no return val
    sentence = b.getvalue()
    return sentence

def analyzeString(sentence):
    first = sentence.find('[')
    last = sentence.find(']')
    return sentence[first+1:last]

if __name__ == '__main__':
    filename = '../QtTest/testqt/1462613764.wav'
    token = get_token()
    sentence = use_cloud(token, filename)
    result = analyzeString(sentence)
    print "ok",result
