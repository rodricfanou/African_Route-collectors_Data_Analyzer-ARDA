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
                try:
                	sql2  = '''CREATE INDEX index_RouteCollector ON Data__'''+year+'''_'''+month+'''(RouteCollector);'''
                	cursor.execute(sql2)
                	print 'I have created the index of month: '+month+' and year: '+year
                except:
                	print 'The index of month: '+month+' and year:'+year+' is created'


month = int(time.strftime("%m"))+1
year = int(year) +1;
print month

for x in range(1,month):

        month = str(x)
        year  = str(year)
        try:
     		sql3  = '''CREATE INDEX index_RouteCollector ON Data__'''+year+'''_'''+month+'''(RouteCollector);'''
        	cursor.execute(sql3)
        	print 'Index the month: '+month+' of the year'+year
        except:
            print 'The index of month: '+month+' and year:'+year+' is created'


