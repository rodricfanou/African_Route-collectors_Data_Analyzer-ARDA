## ARDA Application released on: April 21, 2017
## Last review: February 19, 2018
# On the Computation VM (VM1)
# Goal: Create the database MergedData destined to host the routing data collected from all selected route-collectors.
import MySQLdb
import sys
import time
import datetime

## Fill line with necessary infos for connecting to the database.
#+----------------------+
#| Tables_in_MergedData |
#+----------------------+
#| AllRouteCollectors   |
#| Data__2003_1         |
#| Data__2003_10        |
#| Data__2012_9         |
#| Data__2013_1         |
#| Data__2013_10        |
#...
#| Data__2015_3         |
#| Data__2015_4         |
#| Data__2015_5         |
#| Data__2016_10        |
#| Data__2016_11        |
#...
#| Data__2017_7         |
#| Data__2017_8         |
#| Data__2017_9         |
#| Data__2018_1         |
#+----------------------+

db1 = MySQLdb.connect(host="localhost",user="",passwd="")
cursor = db1.cursor()
sql = 'CREATE DATABASE IF NOT EXISTS MergedData'
cursor.execute(sql)


## Goal: Create table AllRouteCollectors destined to host infos concerning all the route collectors
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


## Goal: Create tables Data__'''+year+'''_'''+month+''', which host the routing data split per month from 2003 to current date.
now = datetime.datetime.now()

year = int(now.year);

print year

for x in range(2003, year):
    for y in xrange(1,13):
        
        db1 = MySQLdb.connect(host="localhost",user="root",passwd="edjrosse")
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
            ASPath TEXT,
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
        ASPath TEXT,
        ASPathLength VARCHAR(100),
        Origin VARCHAR(100),
        IP_version VARCHAR(5),
        primary key (IDInsertion));'''
    
    cursor.execute(sql3)


## Indexing the tables Data__'''+year+'''_'''+month+''' created above
now = datetime.datetime.now()
year = int(now.year);
print year

for x in range(2003, year):
    for y in xrange(1,13):
        
        cursor = db1.cursor()
        sql = 'use MergedData'
        cursor.execute(sql)
            
        month = str(y)
        year  = str(x)
        try:
            sql2  = '''CREATE INDEX index_RouteCollector_Network ON Data__'''+year+'''_'''+month+'''(RouteCollector, Network);'''
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
            sql3  = '''CREATE INDEX index_RouteCollector_Network ON Data__'''+year+'''_'''+month+'''(RouteCollector, Network);'''
            cursor.execute(sql3)
            print 'Index the month: '+month+' of the year'+year
        except:
            print 'The index of month: '+month+' and year:'+year+' is created'






## Goal: create RIRs database destined to host data collected by the RIRs
#+-------------------------+
#| Tables_in_RIRs          |
#+-------------------------+
#| ASNs_AFRINIC            |
#| ASNs_APNIC              |
#| ASNs_ARIN               |
#| ASNs_LACNIC             |
#| ASNs_RIPE               |
#| IPv4_ressources_AFRINIC |
#| IPv4_ressources_APNIC   |
#| IPv4_ressources_ARIN    |
#| IPv4_ressources_LACNIC  |
#| IPv4_ressources_RIPE    |
#| IPv6_ressources_AFRINIC |
#| IPv6_ressources_APNIC   |
#| IPv6_ressources_ARIN    |
#| IPv6_ressources_LACNIC  |
#| IPv6_ressources_RIPE    |
#| IXPs_launch_date        |
#+-------------------------+

sql = 'CREATE DATABASE IF NOT EXISTS RIRs'
cursor.execute(sql)


sql3  = '''CREATE TABLE IF NOT EXISTS RIRs.ASNs_AFRINIC(
    ASN VARCHAR(50) NOT NULL,
    CC VARCHAR(50) NULL,
    date VARCHAR(50) NULL,
    Status VARCHAR(50) NULL,
    PRIMARY KEY (ASN));'''

cursor.execute(sql3)

sql3  = '''CREATE TABLE IF NOT EXISTS RIRs.ASNs_APNIC(
    ASN VARCHAR(50) NOT NULL,
    CC VARCHAR(50) NULL,
    date VARCHAR(50) NULL,
    Status VARCHAR(50) NULL,
    PRIMARY KEY (ASN));'''

cursor.execute(sql3)

sql3  = '''CREATE TABLE IF NOT EXISTS RIRs.ASNs_ARIN(
    ASN VARCHAR(50) NOT NULL,
    CC VARCHAR(50) NULL,
    date VARCHAR(50) NULL,
    Status VARCHAR(50) NULL,
    PRIMARY KEY (ASN));'''

cursor.execute(sql3)

sql3  = '''CREATE TABLE IF NOT EXISTS RIRs.ASNs_LACNIC(
    ASN VARCHAR(50) NOT NULL,
    CC VARCHAR(50) NULL,
    date VARCHAR(50) NULL,
    Status VARCHAR(50) NULL,
    PRIMARY KEY (ASN));'''

cursor.execute(sql3)

sql3  = '''CREATE TABLE IF NOT EXISTS RIRs.ASNs_RIPE(
    ASN VARCHAR(50) NOT NULL,
    CC VARCHAR(50) NULL,
    date VARCHAR(50) NULL,
    Status VARCHAR(50) NULL,
    PRIMARY KEY (ASN));'''

cursor.execute(sql3)

sql3  = '''CREATE TABLE IF NOT EXISTS RIRs.IPv4_ressources_AFRINIC (
    Al_id INT NOT NULL AUTO_INCREMENT,
    NetIPaddress VARCHAR(50) NOT NULL,
    Numb_IPadd VARCHAR(50) NOT NULL,
    NetBits VARCHAR(50) NOT NULL,
    CC VARCHAR(50) NULL,
    Status VARCHAR(50) NULL,
    date VARCHAR(50) NULL,
    PRIMARY KEY (Al_id));'''

cursor.execute(sql3)

sql3  = '''CREATE TABLE IF NOT EXISTS RIRs.IPv4_ressources_APNIC (
    Al_id INT NOT NULL AUTO_INCREMENT,
    NetIPaddress VARCHAR(50) NOT NULL,
    Numb_IPadd VARCHAR(50) NOT NULL,
    NetBits VARCHAR(50) NOT NULL,
    CC VARCHAR(50) NULL,
    Status VARCHAR(50) NULL,
    date VARCHAR(50) NULL,
    PRIMARY KEY (Al_id));'''

cursor.execute(sql3)

sql3  = '''CREATE TABLE IF NOT EXISTS RIRs.IPv4_ressources_LACNIC (
    Al_id INT NOT NULL AUTO_INCREMENT,
    NetIPaddress VARCHAR(50) NOT NULL,
    Numb_IPadd VARCHAR(50) NOT NULL,
    NetBits VARCHAR(50) NOT NULL,
    CC VARCHAR(50) NULL,
    Status VARCHAR(50) NULL,
    date VARCHAR(50) NULL,
    PRIMARY KEY (Al_id));'''

cursor.execute(sql3)

sql3  = '''CREATE TABLE IF NOT EXISTS RIRs.IPv4_ressources_ARIN (
    Al_id INT NOT NULL AUTO_INCREMENT,
    NetIPaddress VARCHAR(50) NOT NULL,
    Numb_IPadd VARCHAR(50) NOT NULL,
    NetBits VARCHAR(50) NOT NULL,
    CC VARCHAR(50) NULL,
    Status VARCHAR(50) NULL,
    date VARCHAR(50) NULL,
    PRIMARY KEY (Al_id));'''

cursor.execute(sql3)

sql3  = '''CREATE TABLE IF NOT EXISTS RIRs.IPv4_ressources_RIPE (
    Al_id INT NOT NULL AUTO_INCREMENT,
    NetIPaddress VARCHAR(50) NOT NULL,
    Numb_IPadd VARCHAR(50) NOT NULL,
    NetBits VARCHAR(50) NOT NULL,
    CC VARCHAR(50) NULL,
    Status VARCHAR(50) NULL,
    date VARCHAR(50) NULL,
    PRIMARY KEY (Al_id));'''

cursor.execute(sql3)

sql3  = '''CREATE TABLE IF NOT EXISTS RIRs.IPv6_ressources_AFRINIC (
    Al_id INT NOT NULL AUTO_INCREMENT,
    NetIPaddress VARCHAR(50) NOT NULL,
    Numb_IPadd VARCHAR(50) NOT NULL,
    NetBits VARCHAR(50) NOT NULL,
    CC VARCHAR(50) NULL,
    Status VARCHAR(50) NULL,
    date VARCHAR(50) NULL,
    PRIMARY KEY (Al_id));'''

cursor.execute(sql3)

sql3  = '''CREATE TABLE IF NOT EXISTS RIRs.IPv6_ressources_APNIC (
    Al_id INT NOT NULL AUTO_INCREMENT,
    NetIPaddress VARCHAR(50) NOT NULL,
    Numb_IPadd VARCHAR(50) NOT NULL,
    NetBits VARCHAR(50) NOT NULL,
    CC VARCHAR(50) NULL,
    Status VARCHAR(50) NULL,
    date VARCHAR(50) NULL,
    PRIMARY KEY (Al_id));'''

cursor.execute(sql3)

sql3  = '''CREATE TABLE IF NOT EXISTS RIRs.IPv6_ressources_LACNIC (
    Al_id INT NOT NULL AUTO_INCREMENT,
    NetIPaddress VARCHAR(50) NOT NULL,
    Numb_IPadd VARCHAR(50) NOT NULL,
    NetBits VARCHAR(50) NOT NULL,
    CC VARCHAR(50) NULL,
    Status VARCHAR(50) NULL,
    date VARCHAR(50) NULL,
    PRIMARY KEY (Al_id));'''

cursor.execute(sql3)

sql3  = '''CREATE TABLE IF NOT EXISTS RIRs.IPv6_ressources_ARIN (
    Al_id INT NOT NULL AUTO_INCREMENT,
    NetIPaddress VARCHAR(50) NOT NULL,
    Numb_IPadd VARCHAR(50) NOT NULL,
    NetBits VARCHAR(50) NOT NULL,
    CC VARCHAR(50) NULL,
    Status VARCHAR(50) NULL,
    date VARCHAR(50) NULL,
    PRIMARY KEY (Al_id));'''

cursor.execute(sql3)

sql3  = '''CREATE TABLE IF NOT EXISTS RIRs.IPv6_ressources_RIPE (
    Al_id INT NOT NULL AUTO_INCREMENT,
    NetIPaddress VARCHAR(50) NOT NULL,
    Numb_IPadd VARCHAR(50) NOT NULL,
    NetBits VARCHAR(50) NOT NULL,
    CC VARCHAR(50) NULL,
    Status VARCHAR(50) NULL,
    date VARCHAR(50) NULL,
    PRIMARY KEY (Al_id));'''

cursor.execute(sql3)


## On the Visualization VM (VM2)
#+-------------------------+
#| Tables_in_user_register |
#+-------------------------+
#| IP_user                 |
#| register                |
#+-------------------------+

sql = 'CREATE DATABASE IF NOT EXISTS user_register'
cursor.execute(sql)

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
