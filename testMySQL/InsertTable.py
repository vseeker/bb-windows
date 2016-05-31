# -*- coding: utf-8 -*-
from datetime import date, datetime, timedelta
import mysql.connector

#利用Connector/Python来插入数据
#用cursor来插入或者更新数据,如果你用的存储模式是InnoDB(默认是MySQL5.5及以后),
# 在INSERT,DELETE,UPDATE一系列操作以后必需 commit
# 该示例演示怎么插入数据,插入数据语句依赖于我们创建的主键的值(决定来我们插入的数据不会重复),该例子也说明来怎么去用某些数据格式
#该任务添加了 一个男雇员从明天开始工作,薪资50000
config = {
  'user':'root',
  'password':'123456',
  'database':'testdb',
  'raise_on_warnings': True,
}
cnx = mysql.connector.connect(**config)# 两个星号表示参数是字典类型 ,首先创建了一个MySQL服务器的链接--cnx
cursor = cnx.cursor() #然后用cursor()方法创建一个MySQLCursor
tomorrow = datetime.now().date() + timedelta(days=1)#获得当前时间加上一天的偏移量

add_employee = ("INSERT INTO employees "
               "(first_name, last_name, hire_date, gender, birth_date) "
               "VALUES (%s, %s, %s, %s, %s)")
add_salary = ("INSERT INTO salaries "
              "(emp_no, salary, from_date, to_date) "
              "VALUES (%(emp_no)s, %(salary)s, %(from_date)s, %(to_date)s)")

data_employee = ('Geert', 'Vanderkelen', tomorrow, 'M', date(1977, 6, 14))
# 所有的插入操作声明都写为python的元组类型 eg:add_employee,add_salary,以及插入的数据data_employee
# Insert new employee
cursor.execute(add_employee, data_employee) # 插入操作用execute()函数来执行,参数为插入表的项以及该行的各项所对应的数据
# 内部会自动解析数据
emp_no = cursor.lastrowid #我们用cursor的lastrowid属性拿到新插入的值(因为在创建表的时候emp_no设置为AUTO_INCREMETN)
# 来查询到我们添加操作已经执行(该值已自增)
#下面我们为新的雇员添加薪水

# Insert salary information
data_salary = {
  'emp_no': emp_no,
  'salary': 50000,
  'from_date': tomorrow,
  'to_date': date(9999, 1, 1),
}
cursor.execute(add_salary, data_salary)

# Make sure data is committed to the database
cnx.commit() # 一定要注意commit操作

cursor.close()
cnx.close()
# print emp_no