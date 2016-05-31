# -*- coding: utf-8 -*-
# 下面的脚本将在明天给所有在2000年加入公司而且现在仍然在公司的人加薪15%,为了重复操作这些雇员我们使用buffered cursors
# (A buffered cursor fetches and buffers the rows of a result set after executing a query;
# see Section 10.6.1, “cursor.MySQLCursorBuffered Class”.)它在执行query操作之后会获取和缓存结果的列,
# 而且如果这样的话,就没必要用一些新的变量来获取这些列了,因为我们可以以用iterator的方式来用cursor(生成器)

from decimal import Decimal
from datetime import datetime, date, timedelta
import mysql.connector
# Connect with the MySQL Server
config = {
  'user':'root',
  'password':'123456',
  'database':'testdb',
  'raise_on_warnings': True,
}
cnx = mysql.connector.connect(**config)# 两个星号表示参数是字典类型 ,首先创建了一个MySQL服务器的链接--cnx
# Get two buffered cursors
curA = cnx.cursor(buffered=True)
curB = cnx.cursor(buffered=True)
today = date.today()
tomorrow = today
print today,tomorrow
# Query to get employees who joined in a period defined by two dates
query = (
  "SELECT s.emp_no, salary, from_date, to_date FROM employees AS e "
  "LEFT JOIN salaries AS s USING (emp_no) "
  "WHERE to_date = DATE('9999-01-01')"
  "AND e.hire_date BETWEEN DATE(%s) AND DATE(%s)")
# UPDATE and INSERT statements for the old and new salary
update_old_salary = (
  "UPDATE salaries SET to_date = %s "
  "WHERE emp_no = %s AND from_date = %s")
insert_new_salary = (
  "INSERT INTO salaries (emp_no, from_date, to_date, salary) "
  "VALUES (%s, %s, %s, %s)")
# Select the employees getting a raise
curA.execute(query, (date(2000, 1, 1), date(2000, 12, 31)))
# Iterate through the result of curA
for (emp_no, salary, from_date, to_date) in curA:
  # Update the old and insert the new salary
  new_salary = int(round(salary * Decimal('1.15')))
  curB.execute(update_old_salary, (tomorrow, emp_no, from_date))
  curB.execute(insert_new_salary,
               (emp_no, tomorrow, date(9999, 1, 1,), new_salary))

  # Commit the changes
  cnx.commit( )
cnx.close( )