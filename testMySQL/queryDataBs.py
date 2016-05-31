# -*- coding: utf-8 -*-
# 下面的代码演示如何用一个cursor来查询数据,并且将查询到的数据进行格式化输出
import datetime
import mysql.connector
config = {
    'user': 'root',
    'password': '123456',
    'database': 'testdb',
    'raise_on_warnings': True,
}
cnx = mysql.connector.connect(**config)
cursor = cnx.cursor()
query = ("SELECT first_name, last_name, hire_date FROM employees "
         "WHERE hire_date BETWEEN %s AND %s")
hire_start = datetime.date(1999, 1, 1)
hire_end = datetime.date(1999, 12, 31)

print query,(hire_start, hire_end)
cursor.execute(query, (hire_start, hire_end)) # 构造格式化数据并查询


for (first_name, last_name, hire_date) in cursor:
  print("{}, {} was hired on {:%d %b %Y}".format(
    last_name, first_name, hire_date))# 格式化输出
cursor.close()
cnx.close