#!/usr/bin/python
import os, re, sys, copy, csv, os.path
import MySQLdb

#Needed for fill_Open_IP, fill_location_TC, find_location_MM
import json, copy, time, datetime, math
import subprocess, threading
from pprint import pprint
from random import choice
from time import sleep
from collections import Counter
import select, socket
import urllib2, urllib
#import GeoIP
import bgp_rib, ipaddr, logging
import gzip
from datetime import date
from datetime import datetime
import DB_configuration
import time

sys.path.append('../Heart/2_libraries/')
import bgp_rib_v6

db = MySQLdb.connect(host = DB_configuration.host, user = DB_configuration.user, passwd = DB_configuration.passwd, db="MergedData")
cur = db.cursor()

#Under this format 2011, 2012, 2013...
year = str(date.today().year)
#Under this format 01, 02, 03 ....
month = str(datetime.now().strftime("%m"))
current_day = datetime.now().strftime("%d")
#current_day = '14'
#insert_only .vs check_insert
task = 'insert_only'
#Paths to some folders
path = '/home/roderick/PCH_download_v6'
debug_folder = '/home/roderick/PCH_download_v6/debug'

command = 'mkdir debug'
os.system(command)
outfile = open(debug_folder+'/Debug__'+year+'_'+month+'.txt', 'a')
outfile.write('The script has started at '+str(time.strftime("%d/%m/%Y %H:%M:%S"))+'.\n')

def parsing_data(year, month, task):
    dirs = os.listdir(str(year)+'/'+str(month))
    os.chdir(path+'/'+str(year)+'/'+str(month))
    print dirs
    for rc in dirs:
        if rc != 'index.html':

            sql_command = """select TypeRCid from AllRouteCollectors where RouteCollector = %s;"""
            cur.execute(sql_command, str(rc))
            RouteCollectorID = cur.fetchall()[0][0]

            if task == 'check_insert':
                query = ("SELECT RouteCollector, Network, Timestamp, ASpath FROM Data__"+str(year)+"_"+str(int(month))+" where RouteCollector = %s;")
                a = [str(rc)]
                cur.execute(query, a)
                Box_Data = cur.fetchall()
 
            files = os.listdir(path+'/'+str(year)+'/'+str(month)+'/'+str(rc))
            os.chdir(path+'/'+str(year)+'/'+str(month)+'/'+str(rc))
            print 'We have in ' + rc + ':'
            
            for file_to_process in files:

                print 'Parsing new files'
                print "Processing file: ",file_to_process

                #Get the day
                first = str(year)+'.'+str(month)+'.'
                last = ".gz"
                start = file_to_process.index(first) + len(first)
                end = file_to_process.index(last)
                day = file_to_process[start:end]
                if (str(day) == str(current_day)): 
                    file_date = str(year)+'.'+str(month)+'.'+str(day)
                    file_date_time = file_date + ' 00:00:00'
                    print file_date_time
                    datetime_format = datetime.strptime(file_date_time, "%Y.%m.%d %H:%M:%S")
                    time_tuple = datetime.strptime(file_date_time, "%Y.%m.%d %H:%M:%S").timetuple()
                    timestamp_format= time.mktime(time_tuple)

                    print timestamp_format
                    with gzip.open(file_to_process, 'r') as file_h:
                        bgp_entries = []
                        for entry_n, bgp_entry in enumerate(bgp_rib_v6.BGPRIB.parse_cisco_show_ip_bgp_generator(file_h)):
                            #Network
                            network = bgp_entry[0]
                            #NextHop
                            next_hop = bgp_entry[2]
                            ##metric = bgp_entry[3]
                            ##locprf = bgp_entry[4]
                            ##weight = bgp_entry[5]
                            #ASPath
                            as_path = bgp_entry[6]
                            #ASPathLength
                            as_path_length = len(as_path)
                            #NextAS
                            if as_path:
                                nextas = as_path[0]
                            else:
                                nextas = ''
                            #OriginAS	
                            if as_path:
                                originas = as_path[as_path_length -1]
                            else:
                                originas = ''
                            #Origin
                            if bgp_entry[7] == 'i': 
                                origin = "IGP"
                            elif bgp_entry[7] == 'e':
                                origin = "EGP"
                            elif bgp_entry[7] == "?":
                                origin = "INCOMPLETE"
                            else:
                                origin = "INCOMPLETE"
                                # ignore this line and continue
                                continue
                                # save information. the order for each line is:
                                #Url_Line ; Id; date; time; Year; Location; network; nh; nextas; metric; locpref; weight; ASpath  (should be as large as possible); origin; ASpathlength
                                #bgp_entries.append([folder+str(year)+'/'+loc+'/'+file_to_process+"_"+str(entry_n), index, datetime_format, timestamp_format, str(year), loc, network, next_hop, nextas, metric, locprf, weight,  " ".join(as_path), origin, as_path_length])

                            full_as_path = " ".join(as_path)
                            if len(next_hop)==0:
                                next_hop = 'NULL'
                            if len(nextas)==0:
                                nextas = 'NULL'
                            if as_path_length==0:
                                full_as_path = 'NULL'
                            else:
                                full_as_path =  " ".join(as_path)

                            if (task == 'insert_only'):
                                try:
                                    query = "insert ignore into Data__"+str(year)+"_"+str(int(month))+" (TypeRC, TypeRCid, Date, Timestamp, Year, Month, Day, RouteCollector, OriginAS, NextAS, NextHop, Network, ASPath, ASpathlength, Origin, IP_version) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
                                    cur.execute(query, ['PCH', RouteCollectorID, datetime_format, timestamp_format, str(year), str(month), str(day), str(rc), originas, nextas, next_hop, network, full_as_path, as_path_length, origin, 'v6'])
                                    #print query
                                except:
                                    pass
                            elif (task == 'check_insert'):
                                try:
                                    chunk = (str(rc),str(network),str(timestamp_format),str(full_as_path))
                                    if (chunk not in Box_Data):
                                        query = "insert ignore into Data__"+str(year)+"_"+str(int(month))+" (TypeRC, TypeRCid, Date, Timestamp, Year, Month, Day, RouteCollector, OriginAS, NextAS, NextHop, Network, ASPath, ASpathlength, Origin, IP_version) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
                                        cur.execute(query, ['PCH', RouteCollectorID, datetime_format, timestamp_format, str(year), str(month), str(day), str(rc), originas, nextas, next_hop, network, full_as_path, as_path_length, origin, 'v6'])
                                        #print query
                                except:
                                    pass

                #os.remove(path+'/'+str(year)+'/'+str(month)+'/'+str(rc)+'/'+file_to_process)
                db.commit()

        outfile.write('We have inserted RC: '+str(rc)+'.\n')
        os.chdir(path+'/'+str(year)+'/'+str(month))
        #os.rmdir(path+'/'+str(year)+'/'+str(month)+'/'+str(rc))
        #os.system(command)

    outfile.write('We have parsed the month: '+str(month)+'.\n')
    os.chdir(path+'/'+str(year))


parsing_data(year, month, task)