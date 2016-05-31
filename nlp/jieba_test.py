# -*- coding: utf-8 -*-
import jieba
import sys,time
import urllib2
import nltk
import os
os.system('pwd')
def cutText(inTxt = '/Users/v_niur/Desktop/py/bb/tmp/simple.txt',outTxt = '/Users/v_niur/Desktop/py/bb/tmp/cut_simple.txt'):
    """将中文文本进行分词并导出"""
    jieba.enable_parallel(4)
    startTime = time.time()
    content = open(inTxt,"rb").read()#将该目录下的文本的内容导入为一个字符串
    words = list(jieba.cut(content))
    endTime= time.time()
    timeCost = endTime - startTime
    with open(outTxt,'w+') as f:
        for w in words:
            # print >> f,w.encode("utf-8"), "/" ,
            print >> f, w.encode( "utf-8" ),' ',
    print 'speed',len(content),"bytes/second"

# cutText(inTxt='/Users/v_niur/Desktop/py/bb/tmp/instructor.txt',outTxt='/Users/v_niur/Desktop/py/bb/tmp/cut_instructor.txt')


def filterText(inTxt = '/Users/v_niur/Desktop/py/bb/tmp/cut_simple.txt',outText = '/Users/v_niur/Desktop/py/bb/tmp/filter_cut_simple.txt'):
    """将分词后的文本进行过滤,过滤掉长度为<2以及纯数字的字符"""

    with open(inTxt) as f:
        with open(outText,'a+') as fp:
            for ln in f:
                if len(ln) > 1:
                    buff = []
                    wordList = ln.split()
                    for w in wordList:
                        if len(w) < 2 or w.isalnum() or w in ['\'','\"',',',' ']:
                            continue
                        else:
                            buff.append(w)
                            buff.append('\n')
                            fp.writelines(buff)
filterText(inTxt='/Users/v_niur/Desktop/py/bb/tmp/cut_instructor.txt',outText='/Users/v_niur/Desktop/py/bb/tmp/filter_cut_instructor.txt')

def getTfAndTF_IDF(inTxt = '/Users/v_niur/Desktop/py/bb/tmp/simple.txt',n = 5):
    """输入一个已经分好词并初过滤的文本,该模块计算字符串长度小于n的字符串并写入相应的文本"""
    locPath = '/Users/v_niur/Desktop/py/bb/tmp/'
    fileDict = {'length=1':fp.writelines,}
    with open(inTxt) as f:
        for ln in f:



    # content = open(inTxt,"rb").read()#将该目录下的文本的内容导入为一个字符串
    # print content
    frequencyDist = nltk.FreqDist(inTxt)
    # print frequencyDist
    # vocabulary = frequencyDist.keys()
    # print vocabulary
    # print frequencyDist.elements()
    frequencyDist.plot()
# getTfAndTF_IDF()


# seg_list = jieba.cut("我来到北京清华大学", cut_all=True)
# print "Full Mode:", "/ ".join(seg_list)  # 全模式
# seg_list = jieba.cut("我来到北京清华大学", cut_all=False)
# print "Default Mode:", "/ ".join(seg_list)  # 精确模式
# seg_list = jieba.cut("他来到了网易杭研大厦")  # 默认是精确模式
# print ", ".join(seg_list)
# seg_list = jieba.cut_for_search("小明硕士毕业于中国科学院计算所，后在日本京都大学深造")  # 搜索引擎模式
# print ", ".join(seg_list)
#
# with open('simple.txt') as f:
#     for ln in f:
#         if ln:
#             # print ln
#             seg_list = jieba.cut(ln,cut_all=False)
#             print '\n'.join(seg_list)
