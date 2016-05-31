# -*- coding: utf-8 -*-
from datetime import date, datetime, timedelta
import mysql.connector
import os

def load(file,fileId):# 将file中的数据装在入数据库,fileId是由file所对应的在loadedFile中的行号,作为主键部分的前缀
    config = {
      'user':'root',
      'password':'123456',
      'database':'testdb',
      'raise_on_warnings': True,
    }
    cnx = mysql.connector.connect(**config)# 两个星号表示参数是字典类型 ,首先创建了一个MySQLdb服务器的链接--cnx
    # print cnx

    cursor = cnx.cursor() #然后用cursor()方法创建一个MySQLdbCursor

    addInstructor = (
    "insert INTO instructor(pageOfKey,keyWords) VALUES (%s,%s)")

    # dataInstructor = (24,"张")
    # cursor.execute( addInstructor, dataInstructor )

    with open() as f:
        counter = 0
        for ln in f:
            # print int(ln[:ln.find(',')]),type(ln[ln.find(',')+1:])
            # print ln.split(",")
            # print ln[:ln.find(',')],ln[ln.find(',')+1:]
            tmp = ln.find(',')
            pageTmp = ln[:tmp]
            keyTmp = ln[tmp+1:]
            # print "char",keyTmp.encode(encoding="utf8mb4")
            dataInstructor = (pageTmp,keyTmp)
            counter += 1
            print counter
            cursor.execute( addInstructor, dataInstructor )
            cnx.commit( )  # 一定要注意commit操作
    # cnx.commit( )  # 一定要注意commit操作

    cursor.close()
    cnx.close()

