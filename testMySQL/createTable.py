# -*- coding: utf-8 -*-
from __future__ import print_function
import mysql.connector
from mysql.connector import errorcode
DB_NAME = 'employees'


def createTable( ):
    global DB_NAME

    TABLES = {'employees': (
        "CREATE TABLE `employees` ("
        "  `emp_no` int(11) NOT NULL AUTO_INCREMENT,"
        "  `birth_date` date NOT NULL,"
        "  `first_name` varchar(14) NOT NULL,"
        "  `last_name` varchar(16) NOT NULL,"
        "  `gender` enum('M','F') NOT NULL,"
        "  `hire_date` date NOT NULL,"
        "  PRIMARY KEY (`emp_no`)"
        ") ENGINE=InnoDB"), 'departments': (
        "CREATE TABLE `departments` ("
        "  `dept_no` char(4) NOT NULL,"
        "  `dept_name` varchar(40) NOT NULL,"
        "  PRIMARY KEY (`dept_no`), UNIQUE KEY `dept_name` (`dept_name`)"
        ") ENGINE=InnoDB"), 'salaries': (
        "CREATE TABLE `salaries` ("
        "  `emp_no` int(11) NOT NULL,"
        "  `salary` int(11) NOT NULL,"
        "  `from_date` date NOT NULL,"
        "  `to_date` date NOT NULL,"
        "  PRIMARY KEY (`emp_no`,`from_date`), KEY `emp_no` (`emp_no`),"
        "  CONSTRAINT `salaries_ibfk_1` FOREIGN KEY (`emp_no`) "
        "     REFERENCES `employees` (`emp_no`) ON DELETE CASCADE"
        ") ENGINE=InnoDB"), 'dept_emp': (
        "CREATE TABLE `dept_emp` ("
        "  `emp_no` int(11) NOT NULL,"
        "  `dept_no` char(4) NOT NULL,"
        "  `from_date` date NOT NULL,"
        "  `to_date` date NOT NULL,"
        "  PRIMARY KEY (`emp_no`,`dept_no`), KEY `emp_no` (`emp_no`),"
        "  KEY `dept_no` (`dept_no`),"
        "  CONSTRAINT `dept_emp_ibfk_1` FOREIGN KEY (`emp_no`) "
        "     REFERENCES `employees` (`emp_no`) ON DELETE CASCADE,"
        "  CONSTRAINT `dept_emp_ibfk_2` FOREIGN KEY (`dept_no`) "
        "     REFERENCES `departments` (`dept_no`) ON DELETE CASCADE"
        ") ENGINE=InnoDB"), 'dept_manager': (
        "  CREATE TABLE `dept_manager` ("
        "  `dept_no` char(4) NOT NULL,"
        "  `emp_no` int(11) NOT NULL,"
        "  `from_date` date NOT NULL,"
        "  `to_date` date NOT NULL,"
        "  PRIMARY KEY (`emp_no`,`dept_no`),"
        "  KEY `emp_no` (`emp_no`),"
        "  KEY `dept_no` (`dept_no`),"
        "  CONSTRAINT `dept_manager_ibfk_1` FOREIGN KEY (`emp_no`) "
        "     REFERENCES `employees` (`emp_no`) ON DELETE CASCADE,"
        "  CONSTRAINT `dept_manager_ibfk_2` FOREIGN KEY (`dept_no`) "
        "     REFERENCES `departments` (`dept_no`) ON DELETE CASCADE"
        ") ENGINE=InnoDB"), 'titles': (
        "CREATE TABLE `titles` ("
        "  `emp_no` int(11) NOT NULL,"
        "  `title` varchar(50) NOT NULL,"
        "  `from_date` date NOT NULL,"
        "  `to_date` date DEFAULT NULL,"
        "  PRIMARY KEY (`emp_no`,`title`,`from_date`), KEY `emp_no` (`emp_no`),"
        "  CONSTRAINT `titles_ibfk_1` FOREIGN KEY (`emp_no`)"
        "     REFERENCES `employees` (`emp_no`) ON DELETE CASCADE"
        ") ENGINE=InnoDB")}
    # TABLES which is a dictionary but actually it is a Table in mysql database

    config = {
        'user': 'root',
        'password': '123456',
        'database': 'testdb',
        'raise_on_warnings': True,
    }
    cnx = mysql.connector.connect( **config )
    cursor = cnx.cursor( )


#一个MySQL服务器可以管理很多的数据库,所以,当你要操作一个MySQL服务器的数据库时,你需要具体指明具体的数据库名
#如果你并不确定你想要的数据库时存在的,你可以用下面的代码确保该数据库存在,如果数据库不存在的话创建它

def create_database(cursor):
    try:
        cursor.execute(
            "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
    except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))
        exit(1)

# *****************************************************************
# test create_database(cursor)
# config = {
#     'user': 'root',
#     'password': '123456',
#     'database': 'testdb',
#     'raise_on_warnings': True,
# }
# cnx = mysql.connector.connect( **config )
# cursor = cnx.cursor( )
#
# try:
#     cnx.database = DB_NAME
# except mysql.connector.Error as err:
#     if err.errno == errorcode.ER_BAD_DB_ERROR:
#         create_database( cursor )
#         cnx.database = DB_NAME
#     else:
#         print( err )
#         exit( 1 )
#在该程序中我们尝试通过数据库的链接对象--cnx来对一个特定的数据库进行操作,如果在该操作中存在错误,
# 我们通过错误码来检验是否是因为该数据库不存在,如果确实是因为它不存在,则创建该数据库
#*****************************************************************

#当我们成功创建目标数据库,我们通过迭代TABLE字典的项来创建表


# create_database(cursor)

# for name, ddl in TABLES.iteritems():
#     try:
#         print("Creating table {}: ".format(name), end='')
#         cursor.execute(ddl)
#     except mysql.connector.Error as err:
#         if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
#             print("already exists.")
#         else:
#             print(err.msg)
#     else:
#         print("OK")
#
# cursor.close()
# cnx.close()
