# -*- coding: utf-8 -*-
import mysql.connector
from mysql.connector import errorcode


# cnx = mysql.connector.connect(user='root', password='123456', host='127.0.0.1', database='testdb')
# cnx.close()


# try:
#     cnx = mysql.connector.connect(user='root', password='123456', host='127.0.0.1', database='testdb')
# except mysql.connector.Error as err:
#   if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
#     print("Something is wrong with your user name or password")
#   elif err.errno == errorcode.ER_BAD_DB_ERROR:
#     print("Database does not exist")
#   else:
#     print(err)
# else:
#   cnx.close()

config = {
  'user':'root',
  'password':'123456',
  'database':'testdb',
  'raise_on_warnings': True,
}
cnx = mysql.connector.connect(**config)
cnx.close()
