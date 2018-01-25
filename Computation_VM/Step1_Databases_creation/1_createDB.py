## Creation of the Database in which will be store all the collected data.
import MySQLdb

db1 = MySQLdb.connect(host="localhost",user="",passwd="")

cursor = db1.cursor()
sql = 'CREATE DATABASE MergedData'
cursor.execute(sql)
