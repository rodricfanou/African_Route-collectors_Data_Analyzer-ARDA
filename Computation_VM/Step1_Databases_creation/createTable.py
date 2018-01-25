import MySQLdb
import sys
import time
import datetime
now = datetime.datetime.now()

year = int(now.year);

print year

for x in range(2003, year):
	for y in xrange(1,13):
		
		db1 = MySQLdb.connect(host="localhost",user="",passwd="")
		cursor = db1.cursor()
		sql = 'use MergedData'
		cursor.execute(sql)

		month = str(y)
		year  = str(x)  

		sql2  = '''CREATE TABLE IF NOT EXISTS Data__'''+year+'''_'''+month+'''(
			IDInsertion INT AUTO_INCREMENT,
			TypeRC VARCHAR(5),
			TypeRCid VARCHAR(5),
			Date DATETIME,
			Timestamp INT(255),
			Year INT(100),
			Month INT(100),
			Day INT(100),
			RouteCollector VARCHAR(1000),
			OriginAS VARCHAR(500),
			NextAS VARCHAR(500),
			NextHop VARCHAR(20),
			Network VARCHAR(500),
			ASPath VARCHAR(15000),
			ASPathLength VARCHAR(100),
			Origin VARCHAR(100),
			IP_version VARCHAR(5),
			primary key (IDInsertion));'''

		cursor.execute(sql2)

month = int(time.strftime("%m"))+1
year = int(year) +1;
print month

for x in range(1,month+1):
	
	month = str(x)
	year  = str(year)  

	sql3  = '''CREATE TABLE IF NOT EXISTS Data__'''+year+'''_'''+month+'''(
		IDInsertion INT AUTO_INCREMENT,
		TypeRC VARCHAR(5),
		TypeRCid VARCHAR(5),
		Date DATETIME,
		Timestamp INT(255),
		Year INT(100),
		Month INT(100),
		Day INT(100),
		RouteCollector VARCHAR(1000),
		OriginAS VARCHAR(500),
		NextAS VARCHAR(500),
		NextHop VARCHAR(20),
		Network VARCHAR(500),
		ASPath VARCHAR(15000),
		ASPathLength VARCHAR(100),
		Origin VARCHAR(100),
		IP_version VARCHAR(5),
		primary key (IDInsertion));'''

	cursor.execute(sql3)




