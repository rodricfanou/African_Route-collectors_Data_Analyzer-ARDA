import MySQLdb

db1 = MySQLdb.connect(host="localhost",user="",passwd="")

cursor = db1.cursor()
sql = 'CREATE DATABASE user_register'
cursor.execute(sql)
