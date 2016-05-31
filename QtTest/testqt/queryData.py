# -*- coding: utf-8 -*-
import mysql.connector
from PyPDF2 import PdfFileWriter,PdfFileReader
import os

dictQueryResult={}
stopWords=[]
def loadedStopWords(): #加载停用词
    global stopWord
    with open( 'stop.txt' ) as f:
        for ln in f:
            stopWords.append(ln[:-2])
    # print stopWords
# loadedStopWords()
def showPdfWhenButtonClicked(tup,pdfId=1):#当点击按钮时，产生该按钮对应的dictQueryResult中的对应位置的项,enumerate后该项变为元组
    #但还是原来的字典数据 只生成一份pdf文件，所以相比queryResultParse，不需要再进行
    pageIdList = tup[1]
    if isinstance(pageIdList,list):
        print 'pdfId',pdfId
        generatePdf(str(pdfId),pageIdList)

def getPDF(dictPdfFileAndPage,keyWords): # keyWords格式化处理后,即pdf文件名
    # 相差一页自动合并稍后在该函数中实现即可
    output = PdfFileWriter( )
    # print dictPdfFileAndPage

    for k,v in dictPdfFileAndPage.items():
        pdfPath = getpath(k)
        print 'pdfPath',pdfPath
        # pdfReader = PdfFileReader( open( "{0}".format(pdfPath.decode('gbk').encode('utf-8')), "rb" ) )#读取PDF文件
        pdfReader = PdfFileReader(open(u"{}".format(pdfPath), "rb"))
        for el in v:
            output.addPage(pdfReader.getPage(el))
    # if not os.path.exists(inputPdfPath):
    #     print "the pdf file:{0} not exist".format(inputPdfPath)
    #     return 0
    outputPdfPath = keyWords+'.pdf'
    print "outputPdfPath",outputPdfPath

    outputStream = file(u"{0}".format(outputPdfPath),"wb")
    output.write(outputStream)
    # os.system( "open " + outPdfPath )#这里改成以浏览器打开


# getPDF()

# config = {
#     'user': 'root',
#     'password': '123456',
#     'database': 'testdb',
#     'raise_on_warnings': True,
# }
# cnx = mysql.connector.connect(**config)
# cursor = cnx.cursor()
# # query = "SELECT * FROM instructor limit 0,1000;"
# #" where keyWords like {0}"
# query = "select * from testdb.instructor where keyWords like  '%工具%'"
# data = '\'%控制%\''
# tmp = query.format(data)
# # print tmp
# # print query ,data
# cursor.execute(query) # 构造格式化数据并查询
# # print int(cursor.rowcount)
# # listTmp = cursor.fetchall()
#
# for (pageOfKey,keyWords) in cursor:
#     print "{},{}".format(pageOfKey,keyWords.encode('utf-8'))
#
#
# cursor.close()
# cnx.close

def queryData(keyWord='工具'): #查询数据库,并将查询结果以{key:list(pageID)}的方式添加入查询结果字典中
    # print 'keyWords',keyWord
    global dictQueryResult
    query="select * from testdb.instructor where keyWords like  '%{0}%'".format(keyWord)
    config = {
        'user': 'root',
        'password': '123456',
        'database': 'testdb',
        'raise_on_warnings': True,
    }
    cnx = mysql.connector.connect( **config )
    cursor = cnx.cursor( )
    cursor.execute( query )  # 构造格式化数据并查询
    listPageOfKey = []
    for (pageOfKey, keyWords) in cursor:
        # print "{},{}".format( pageOfKey, keyWords.encode( 'utf-8' ) )
        listPageOfKey.append(pageOfKey)

    cursor.close( )
    cnx.close
    if len(listPageOfKey):#查询结果至少有一个有效页面
        dictQueryResult[keyWord] = listPageOfKey

    return 0

# print queryData()
# dictQueryResult=queryData()
# for key,value in dictQueryResult.items():
#     print key,value

def mergeQueryResult(keyWordList): # 输入为语音识别后,然后经过简单分词以及停用词过滤后生成的关键词list
 # 作用:对于一次语音识别得到的关键词列表,逐个查询(queryData())逐个填充dictQueryResult,然后将其所有页码合成为一个mergeList
 # 输出为所有关键词搜索后的页码组成的列表,然后经过简单的非0过滤后合成一个mergeList
    global dictQueryResult
    mergeList = []
    for el in keyWordList:
        queryData(el)

    for k, v in dictQueryResult.items( ):
        for el in v:

            mergeList.append( el )
    return mergeList



def calculate(pageId):#统计字典中某个页码(页码中出现的关键词数>1)对应于哪些关键词,返回{合并关键字串:对应页码}的字典
    global dictQueryResult
    words = []
    for k,v in dictQueryResult.items():
        if pageId in v:
            words.append(k)

    if len(words)>1:#至少应该有两个关键词出现在同一页
        word = ' '.join(words)# 将多个关键字合并成一个字符串
        # print 'word',word
        dictQueryResult[word] = pageId#当某页出现关键字>=2时,将合并的关键字串以及页码添加入结果字典

def mergeResult(mergeList):#该函数的作用,首先利用集合函数拿到一个无重复的数据queryList
    # 然后找出该原数据重复>1的数据,将这些数据重新进行关键词合并(用于qt结果的优先级式的显示)
    # 返回合并的{关键词串:页码list}组成的字典,下一步合并所有结果的字典,一并解析,一并显示
    #问题是如果我这里统计出了所有页码的对应的重复数组,难道要用反向比对一遍的方式来得到所有结果么,
    # 明显很麻烦,这样的话本来对于一个关键词来讲一次搜索后有查询到结果就应该将这些内容按照一个关键词的优先级进行合并的,
    # 反向遍历一遍的话,肯定会丢失某些页面.还是逐个层次的去合并页面,这样的话会更完整一些,
    #另外 对于页面间隔小于2(即只相隔一页)的页面应该补齐,即不跳过
    global dictQueryResult
    # print "mergeList",mergeList
    querySet = set( mergeList )  # querySet里无重复 项
    for item in querySet:
        # print("the %d has found %d" % (item, mergeList.count( item )))
        count = mergeList.count(item)
        if count>1:
            calculate(item) # 合并
    return dictQueryResult

def filterStopWord(words=[]): #过滤停用词,输入为语音识别后简单分词得到的关键词list,输出为删去停用词的关键词list
    global stopWords
    if len(words):
        pass
    else:
        return # 这里默认返回NULL,下一步记得判空
    loadedStopWords()

    for el in words:
        if el in stopWords:
            words.remove(el)

    return words

def queryResultParse(): # # 将(关键字查询数据库后得到的)字典 -进行解析(包括页面包含多个关键字的情况的分析),然后生成所有pdf
    global dictQueryResult
    for k, v in dictQueryResult.items( ):
        # 这里出现v不是list类型的情况,直接就是一个string,eg:'0p15',所以添加一个检验
        if isinstance(v,list):
            generatePdf(k,v)
        else:
            generatePdf( k, [v] )



def generatePdf(k, v): # 强调一下:多个关键词属于同一页在mergeResult的函数中的calculate中已经加到全局变量进去了
    # 先用字典dict存储v的分解结果,然后解析(因为存在同一个关键词可能对应多本书以及多本书中的n多页
    # 为了便于生成pdf文档,所以必须解析为{文档名:该文档中的list[页码]}字典)
    # dict合并为pdf文档,并以k作为文件名
    dictPdfFileAndPage = {}
    page=[]
    for el in v:
        tmp = el.find( 'p' )
        # print 'el',el
        strFileId = el[:tmp]
        strPage = el[tmp + 1:]
        # page.append(int(strPage))
        # print 'strFileId',strFileId
        intFileId = int(strFileId)
        if dictPdfFileAndPage.has_key(intFileId):
            dictPdfFileAndPage[intFileId].append(int(strPage))

        else:
            dictPdfFileAndPage[intFileId]=[intFileId]

        print 'k',k
        getPDF(dictPdfFileAndPage,k)


def getpath(fileId,loadedfile='loadedFile.txt'): # 根据文本所在行,也即fileId,返回该文件名(文件地址)

    with open(loadedfile) as f:
        for index,el in enumerate(f):
            if index==fileId:
                print 'el',el
                if '\n' in el:
                    return el[:-1]+'.pdf' # 去掉换行符
                else:
                    return el + '.pdf'
# getpath(1)

def check(pageList): #对pageId组成的list进行页面相关性分析,去重,以及排序
    if isinstance(pageList,list):
        tmp = []
        pageList= list(set(pageList))#去重
        pageList.sort()#排序
        length = len(pageList)
        if length>1:
            for el in xrange(length-1):
                high = pageList[el+1]
                low = pageList[el]
                if high-low<3: #即默认页面相关性很高,中间页面不能删除
                    for i in xrange(low+1,high):
                        if i not in pageList and i not in tmp:
                            tmp.append(i)
            for ell in tmp:
                pageList.append(ell)
    return pageList




if __name__ == '__main__':
    keyWordList = ['机器人', '控制器', '电源']
    # keyWordList = filterStopWord(keyWordList)
    # dictQueryResult = mergeResult(mergeQueryResult(keyWordList))
    # # 因为当直接引用该模块的时候，不知道dictQueryResult是什么时候的dictQueryResult
    # # print dictQueryResult
    # name = "123.pdf"
    # # PdfFileReader(open(u"{}".format(name),'rb')) # open是python内建函数，但不能打开这么中文文件
    # PdfFileReader(open(u"机器人系统培训高级弧焊.pdf", 'rb'))#可以这么打开
    # # 问题出在中文名这里，getPDF同样的错误，mac平台没问题
    # # 要么文件名纯英文，要么文件名纯中文（u"中文"）可以自动转义
    # # 而且不能有任何非中文文字，否则打不开
    # queryResultParse()
    #


