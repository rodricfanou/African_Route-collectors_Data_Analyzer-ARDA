#!/usr/bin/env python
import MySQLdb
import datetime
import sys
import time
import urllib.request, urllib.error, urllib.parse, urllib.request, urllib.parse, urllib.error, glob, re
from _pybgpstream import BGPStream, BGPRecord, BGPElem
import smtplib
from smtplib import SMTPException
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import yagmail
import os
sys.path.append('../Heart/2_libraries/')
import DB_configuration

def is_valid_v4(ip):
    """Validates IPv4 addresses.
        """
    pattern = re.compile(r"""
        ^
        (?:
        # Dotted variants:
        (?:
        # Decimal 1-255 (no leading 0's)
        [3-9]\d?|2(?:5[0-5]|[0-4]?\d)?|1\d{0,2}
        |
        0x0*[0-9a-f]{1,2}  # Hexadecimal 0x0 - 0xFF (possible leading 0's)
        |
        0+[1-3]?[0-7]{0,2} # Octal 0 - 0377 (possible leading 0's)
        )
        (?:                  # Repeat 0-3 times, separated by a dot
        \.
        (?:
        [3-9]\d?|2(?:5[0-5]|[0-4]?\d)?|1\d{0,2}
        |
        0x0*[0-9a-f]{1,2}
        |
        0+[1-3]?[0-7]{0,2}
        )
        ){0,3}
        |
        0x0*[0-9a-f]{1,8}    # Hexadecimal notation, 0x0 - 0xffffffff
        |
        0+[0-3]?[0-7]{0,10}  # Octal notation, 0 - 037777777777
        |
        # Decimal notation, 1-4294967295:
        429496729[0-5]|42949672[0-8]\d|4294967[01]\d\d|429496[0-6]\d{3}|
        42949[0-5]\d{4}|4294[0-8]\d{5}|429[0-3]\d{6}|42[0-8]\d{7}|
        4[01]\d{8}|[1-3]\d{0,9}|[4-9]\d{0,8}
        )
        $
        """, re.VERBOSE | re.IGNORECASE)
    return pattern.match(ip) is not None


def is_valid_v6(ip):
    """Validates IPv6 addresses.
        """
    pattern = re.compile(r"""
        ^
        \s*                         # Leading whitespace
        (?!.*::.*::)                # Only a single whildcard allowed
        (?:(?!:)|:(?=:))            # Colon iff it would be part of a wildcard
        (?:                         # Repeat 6 times:
        [0-9a-f]{0,4}           #   A group of at most four hexadecimal digits
        (?:(?<=::)|(?<!::):)    #   Colon unless preceeded by wildcard
        ){6}                        #
        (?:                         # Either
        [0-9a-f]{0,4}           #   Another group
        (?:(?<=::)|(?<!::):)    #   Colon unless preceeded by wildcard
        [0-9a-f]{0,4}           #   Last group
        (?: (?<=::)             #   Colon iff preceeded by exacly one colon
        |  (?<!:)              #
        |  (?<=:) (?<!::) :    #
        )                      # OR
        |                          #   A v4 address with NO leading zeros
        (?:25[0-4]|2[0-4]\d|1\d\d|[1-9]?\d)
        (?: \.
        (?:25[0-4]|2[0-4]\d|1\d\d|[1-9]?\d)
        ){3}
        )
        \s*                         # Trailing whitespace
        $
        """, re.VERBOSE | re.IGNORECASE | re.DOTALL)
    return pattern.match(ip) is not None

lines = {}
today = datetime.date.today()

actualTimeStamp = time.time()
#actualTimeStamp = 1468317600
beg_timestamp = actualTimeStamp - 1 * 60 * 60
#beg_timestamp = 1468314000
#actualTimeStamp = 1457481600
#beg_timestamp = 1457395200
number_of_lines = 1000

idx = 0
actualYear = datetime.datetime.fromtimestamp(int(beg_timestamp)).strftime('%Y')
actualMonth = int(datetime.datetime.fromtimestamp(int(beg_timestamp)).strftime('%m'))

db = MySQLdb.connect(host = "localhost", user = "", passwd = "", db="MergedData") # name of the data base

cur = db.cursor()
curMail = db.cursor()

query = "select RouteCollector from AllRouteCollectors where Continent = 'AF' and TypeRC = 'RV';"
cur.execute(query)
route_all_collectors = cur.fetchall()

# Create a new bgpstream instance and a reusable bgprecord instance

for aux in route_all_collectors:
    collector = aux[0]
    print(collector)
    sql_command = """select TypeRCid from AllRouteCollectors where RouteCollector = %s;"""
    curMail.execute(sql_command, str(collector))
    RouteCollectorID = curMail.fetchall()[0][0]
        
    route_collector = collector
    timestamp1 = int(beg_timestamp)
    timestamp2 = int(actualTimeStamp)
    TypeRC = 'RV'
    TypeRCid = RouteCollectorID

    stream = BGPStream()
    rec = BGPRecord()
    # Consider RIPE RRC 10 only
    stream.add_filter('collector',route_collector)

    # Consider this time interval:
    # Sat Aug  1 08:20:11 UTC 2015
    stream.add_interval_filter(timestamp1,timestamp2)

    # Start the stream
    stream.start()
    # Get next record
    while(stream.get_next_record(rec)):
        # Print the record information only if it is not a valid record
        if rec.status != "valid":
            print(rec.project, rec.collector, rec.type, rec.time, rec.status)
        else:
            elem = rec.get_next_elem()
            while(elem):

                # Print record and elem information
                # print rec.project, rec.collector, rec.type, rec.time, rec.status,
                Timestamp = rec.time
                Date = datetime.datetime.fromtimestamp(rec.time)
                Year = str(Date.year)
                Month = str(Date.month)
                Day = str(Date.day)

                NextAS =  elem.peer_asn

                if 'next-hop' in list(elem.fields.keys()):
                    NextHop = elem.fields['next-hop']
                else:
                    NextHop = 'None'

                if 'prefix' in list(elem.fields.keys()):
                    Network = elem.fields['prefix']
                else:
                    Network = 'None'

                if 'as-path' in list(elem.fields.keys()):
                    ASPath = elem.fields['as-path']
                    ASPathLength = str(len(elem.fields['as-path'].split(" ")))
                    OriginAS = (elem.fields['as-path'].split(" "))[int(ASPathLength)-1]
                    #print OriginAS
                else:
                    ASPath = 'None'
                    ASPathLength = 'None'
                    OriginAS = 'None'
                
                if is_valid_v4(NextHop):
                    IPversion = 'v4'
                elif is_valid_v6(NextHop):
                    IPversion = 'v6'
                else:
                    IPversion = 'None'

                #print 'We can store it in the DB'
                sql_command = """ INSERT INTO Data__"""+Year+"""_"""+Month+""" (TypeRC, TypeRCid, Date, Timestamp, Year, Month, Day, RouteCollector, OriginAS, NextAS, NextHop, Network, ASPath, ASPathLength, IP_version) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"""
                cur.execute(sql_command, (TypeRC, TypeRCid, Date, Timestamp, Date.year, Date.month, Date.day, route_collector, OriginAS, NextAS, NextHop, Network, ASPath, ASPathLength, IPversion))
                idx += 1
                if idx%number_of_lines == 0 and idx > 0:
                    db.commit()
      
                #print 'Tipo de elemento:',elem.type 
                #print 'Direccion:', elem.peer_address 
                #print 'Campos:', elem.fields
                elem = rec.get_next_elem()
    
    lines[collector] = idx
    print(idx)
    idx = 0
    db.commit()

today = datetime.date.today()
sql_command = 'SELECT table_schema "Database Name", SUM( data_length + index_length)/1024/1024 "Database Size (MB)" FROM information_schema.TABLES where table_schema = "MergedData";'
cur.execute(sql_command)
size_of_DB = cur.fetchall()[0][1]
beg_date = datetime.datetime.fromtimestamp(int(beg_timestamp)).strftime('%Y-%m-%d %H:%M:%S')
actual_date = datetime.datetime.fromtimestamp(int(actualTimeStamp)).strftime('%Y-%m-%d %H:%M:%S')
command = 'python costas_mail.py "roderick.fanou@gmail.com" "RouteViews download on '+str(today)+'" "We have downloaded RouteViews data from '+str(beg_date)+' ('+str(beg_timestamp)+') to '+str(actual_date)+' ('+str(actualTimeStamp)+')\nWe have collected '+str(lines['route-views.kixp'])+' lines for KIXP collector\nWe have collected lines for JINX collector\nThe size of the DB is '+str(size_of_DB)+' MB"'
os.system(command)
