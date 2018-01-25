import MySQLdb
import sys
		
db1 = MySQLdb.connect(host="localhost",user="root",passwd="edjrosse")
cursor = db1.cursor()
sql = 'use user_register'
cursor.execute(sql)

sql2  = '''CREATE TABLE IF NOT EXISTS register(
	IDInsertion INT AUTO_INCREMENT,
	User VARCHAR(20),
	UserID VARCHAR(20),
	Time_initial VARCHAR(20),
	Date_initial VARCHAR(30),
	Time_final VARCHAR(20),
	Date_final VARCHAR(30),
	primary key (IDInsertion));'''

cursor.execute(sql2)





