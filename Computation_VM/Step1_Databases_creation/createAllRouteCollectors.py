import MySQLdb

db1 = MySQLdb.connect(host="localhost",user="",passwd="")

cursor = db1.cursor()

sql = 'use MergedData' 
cursor.execute(sql)
   
sql2  = '''CREATE TABLE AllRouteCollectors(
	ID INT AUTO_INCREMENT,
	IXP VARCHAR(100),
	IXPName VARCHAR(500),
	RouteCollector VARCHAR(500),
	TypeRC VARCHAR(5),
	TypeRCid VARCHAR(5),
	SetupDate DATETIME,
	Continent VARCHAR(5),
	CC VARCHAR(5),
	Country VARCHAR(100),
	City VARCHAR(100),
	Operational VARCHAR(5),
	RIR VARCHAR(10),
	UrlToData VARCHAR(800),
	RegistrationDate DATETIME,
	primary key (ID)
	);'''
cursor.execute(sql2)

