#-*-encoding:utf-8-*-

import os
import mysql.connector


def load( file):  # 将file中的数据装在入数据库,fileId是由file所对应的
    # 在loadedFile中的行号,作为主键部分的前缀
    if os.path.exists(file):
        pass
    else:
        print "the file:{0} doesn't exist".format(file)
        return 0
    buffcsv = []
    with open(file) as f:
        for ln in f:
            buffcsv.append(ln[:-1]+'.csv')

    config = {
        'user': 'root',
        'password': '123456',
        'database': 'testdb',
        'raise_on_warnings': True,
    }
    cnx = mysql.connector.connect( **config )  # 两个星号表示参数是字典类型 ,首先创建了一个MySQLdb服务器的链接--cnx
    # print cnx

    cursor = cnx.cursor( )  # 然后用cursor()方法创建一个MySQLdbCursor

    addInstructor = (
        "insert INTO instructor(pageOfKey,keyWords) VALUES (%s,%s)")

    # dataInstructor = (24,"张")
    # cursor.execute( addInstructor, dataInstructor )
    for index,el in enumerate(buffcsv):
        print "行号：{}，添加入数据库的文件名：{}".format(index ,el)
        with open(el ) as f:
            for ln in f:
                # print int(ln[:ln.find(',')]),type(ln[ln.find(',')+1:])
                # print ln.split(",")
                # print ln[:ln.find(',')],ln[ln.find(',')+1:]
                fileId = str(index)#感觉还是从1开始好一些
                tmp = ln.find( ',' )
                pageTmp = ln[:tmp]
                pageTmp = fileId + 'p' + str(pageTmp) # p作为分割符
                keyTmp = ln[tmp + 1:]
                # print "char",keyTmp.encode(encoding="utf8mb4")
                dataInstructor = (pageTmp, keyTmp)
                cursor.execute( addInstructor, dataInstructor )
                cnx.commit( )  # 一定要注意commit操作
        # cnx.commit( )  # 一定要注意commit操作

    cursor.close( )
    cnx.close( )
def search(dir="../etc/pdf",topdown=True,fileType='.pdf'):
    # 返回存有对应目录下制定文件后缀名(eg:.pdf)的所有文件的文件名的list,
    buff = []
    for root, dirs, files in os.walk(dir, topdown):
        for name in files:
            # print name
            if fileType in name:
                name = name[:-4]
                # print 'name',u"{0}".format(name) # 竟然显示中文乱码
                buff.append(name)
    with open('all.txt','w') as f:
        for el in buff:
            f.write(el+'\n')


def searchCsv(dir="../etc",topdown=True,fileType='.csv'):
    # 根据all.txt中的pdf文件名在相应目录下寻找对应的csv文件以向数据库添加数据
    buff = []
    csvbuff = []
    listFlag = [] #用于纪录哪些pdf文件所对应的csv是存在的
    with open('all.txt','r') as f:
        for el in f:
            buff.append(el[:-1])#去除换行符

    for root, dirs, files in os.walk(dir, topdown):
        for name in files:
            if fileType in name:
                csvbuff.append(name[:-4])
    # print 'csvbuff',csvbuff
    # print buff
    for index,el in enumerate(buff):
        # print el
        if el in csvbuff:
            listFlag.append(1)
        else:
            listFlag.append(0)
    # print 'listFlag',listFlag

    with open("loadedFile.txt",'w') as f: # 用于以后在数据库中查询到有效结果时,此时拿到有效搜索信息的主键
        # 然后解析该主键分为文件所在行以及该行所指的pdf的页码,在该文件中按行找到文件名,然后才能提取指定页
        for index,el in enumerate(listFlag):
            if el:
                f.write(buff[index]+'\n')



search()
searchCsv()
load('loadedFile.txt')# 将csv文件存入数据库