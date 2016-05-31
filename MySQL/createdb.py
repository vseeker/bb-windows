# -*- coding: utf-8 -*-
import mysql.connector
from mysql.connector import errorcode
# **************create database and get connected with it**********
config = {
    'user': 'root',
    'password': '123456',
    'database': 'testdb',
    'raise_on_warnings': True,
}
# cnx = mysql.connector.connect(**config)
# 返回一个 MySQLConnection object
# # 我们可以通过该对象来操作数据库
# cnx.close()

# To handle connection errors, use the try statement and catch all errors using the errors.Error exception:
try:
    cnx = mysql.connector.connect(**config)     # ** means the parameter is a  dictionary
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print "something is wrong with your user name or password"
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print "Datebase does not exist"
    else:
        print err
else:
    cnx.close()