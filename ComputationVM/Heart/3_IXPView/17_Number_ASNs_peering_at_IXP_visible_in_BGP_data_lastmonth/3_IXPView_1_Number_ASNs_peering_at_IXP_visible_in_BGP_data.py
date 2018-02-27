### This is a modified version of the script 1_Number_Origin_ASNs_visible_at_an_IXP_last_month_v7.py

##############################################################################
#__author__ = "Roderick Fanou"
#__email__ = "roderick.fanou@imdea.org"
#__status__ = "Production"
#__description__ = "This script generates "
#__last_modifications__ =
# by Roderick
#"2016-10-05"
#1- Fetching continent from the configuration file
#2- detail what every column represents in the output files
##############################################################################

finish = open ('finish_lastmonth.txt', 'w')
finish.write('started')
finish.close()


#!/usr/bin/python
import os, re, sys, copy, csv, os.path
import MySQLdb
import json, copy, time, datetime, math
import subprocess, threading
from pprint import pprint
from random import choice
#from time import sleep
from collections import Counter
import select, socket
import urllib2, urllib
import GeoIP
import ipaddr, logging
import gzip
from datetime import date
from datetime import datetime
from time import mktime as mktime
#import time


#import collections, sys, os, time, re, string
from netaddr import *
#from operator import itemgetter
#import json, copy, math, time
#from pprint import pprint
#from random import choice
#from pprint import pprint
#import select, socket, time, sys
#import urllib2, urllib, glob


## import all files in the library you need
sys.path.append('../../2_libraries/')
import ipaddress
import DB_configuration
import bgp_rib
from define_timescales import *
from functions import *



## Split the date rage into the numbers of interval you want:  Ex List_weeks = list(date_range('20170301', '20170320', 4))
def date_range(start, end, intv):
    from datetime import datetime
    start = datetime.strptime(start,"%Y%m%d")
    end = datetime.strptime(end,"%Y%m%d")
    diff = (end  - start ) / intv
    for i in range(intv):
        yield (start + diff * i).strftime("%Y%m%d")
    yield end.strftime("%Y%m%d")




now_datetime = str(datetime.now()).replace(' ', '_')

## Create a logfile:
name_log_file = 'Log_'+str(now_datetime) + '_' + '17_Number_ASNs_peering_at_IXP_visible_in_BGP_data_lastmonth' + '.txt'
location_logfile = create_Logfiles_folder()

### Define timelines and timescales
## multi-years splitted into years
yearList = multiyear()
print yearList

## last month (Now - 4weeks) splitted into weeks
lastYearList = lastyear()
print lastYearList

## last month (Now - 4weeks) splitted into weeks
lastMonthList = lastmonth()
print lastMonthList


## Other initialisations
continent = DB_configuration.continent
IXP_collector = {}
IXP_CC = {}
Current_db = 'MergedData'
## connect to the DB
db = MySQLdb.connect(host = DB_configuration.host, user = DB_configuration.user, passwd = DB_configuration.passwd,  db = Current_db)
cur = db.cursor()
print 'Connected'

query = "select IXP, RouteCollector, CC from AllRouteCollectors where Continent = '"+continent+"';"
cur.execute(query)
data = cur.fetchall()
i = 0
while (i<len(data)):
    row = data[i]
    if row[0] not in IXP_collector.keys():
        IXP_collector[row[0]] = []
        IXP_CC[row[0]] = row[2]
    IXP_collector[row[0]].append(row[1])
    i+=1

print IXP_collector
root_folder = '/home/African_Route-collectors_Data_Analyzer-ARDA/ComputationVM/Heart/'
output_folder = '../../Computation_outputs/17_Number_ASNs_peering_at_IXP_visible_in_BGP_data_lastmonth/'

command = 'rm -rf ' + output_folder
os.system(command)

command = 'mkdir  ' + output_folder
os.system(command)

command = 'chmod 777 ' + output_folder
os.system(command)

###Current list of all tables;
query = "SHOW TABLES LIKE 'Data__%%' "
cur.execute (query)
data = cur.fetchall()
List_all_tables = []
if len(data)>0:
    for elmt in data:
        List_all_tables.append(elmt[0])
##print List_all_tables


## fetch all distinct prefixes corresponding to each routecollector in each IXP list contained in the
## dictionnary IXP_collector

log_file_instance = open(location_logfile+'/'+name_log_file, 'a')


### splitted into weeks over the last month
print lastMonthList[0][0], lastMonthList[0][1]
if List_all_tables >0:
    
    ### Using sliding period
    ### what is the timestamp of today ?
    ### 1467417600 - 1464825600 = 2592000
    
    tab = str(datetime.now()).split(' ')
    #tab = ['2017-01-20']
    tab1 = tab[0].split('-')
    timestamp_now = (datetime(int(tab1[0]), int(tab1[1]), int(tab1[2])) - datetime(1970, 1, 1)).total_seconds()
    print 'timestamp = ', timestamp_now
    
    couples_year_month = [(tab1[0], tab1[1])]
    
    ## find the number of the first week of the month in the year
    week_number_last_day = find_week_num_in_year(int(tab1[0]), int(tab1[1]), int(tab1[2]))
    print 'week_number_last_day = ', week_number_last_day
    
    
    
    ### Look for date and timestamp one month before
    timestamp_one_month_before = int(timestamp_now) - 2592000
    
    ## find the number of the first week of the month in the year
    date_one_month_bef  = datetime.fromtimestamp(int(timestamp_one_month_before)).strftime('%Y-%m-%d')
    tab2 = date_one_month_bef.split('-')
    
    week_number_first_day = find_week_num_in_year(int(tab2[0]), int(tab2[1]), int(tab2[2]))
    print 'week_number_first_day = ', week_number_first_day
    
    if (tab2[0], tab2[1]) not in couples_year_month:
        couples_year_month.append( (tab2[0], tab2[1]) )
    
    ## find the beginning and the end of each week
    List_beg_end_each_week = []
    
    
    if int(tab2[0]) == int(tab1[0]):
        num = week_number_first_day
        while num < week_number_last_day+1 :
            weekbeg, weekend = weekbegend(int(tab1[0]), num)
            
            begweek = weekbeg.strftime("%s")
            endweek = weekend.strftime("%s")
            begweek1 = weekbeg.strftime("%Y-%m-%d")
            endweek1 = weekend.strftime("%Y-%m-%d")
            
            List_beg_end_each_week.append(str(begweek) + '__' + str(endweek)  + '__' + str(begweek1) + '  00:00:00__' + str(endweek1)+ '  00:00:00')
            #print begweek, endweek
            num += 1

    elif int(tab2[0]) != int(tab1[0]):
        num = week_number_last_day
        while num > 0 :
            weekbeg, weekend = weekbegend(int(tab1[0]), num)
            
            begweek = weekbeg.strftime("%s")
            endweek = weekend.strftime("%s")
            begweek1 = weekbeg.strftime("%Y-%m-%d")
            endweek1 = weekend.strftime("%Y-%m-%d")
            
            List_beg_end_each_week.insert(0, (str(begweek) + '__' + str(endweek)  + '__' + str(begweek1) + '  00:00:00__' + str(endweek1)+ '  00:00:00'))
            #print begweek, endweek
            num -= 1

        keep_tsp = int(begweek) - 86400
        #1467417600 - 1467331200
        
        print List_beg_end_each_week, 'hello second step'
        num = week_number_first_day
        
        
        ind = 0
        while int(endweek) != keep_tsp:
            weekbeg, weekend = weekbegend(int(tab2[0]), num)
            begweek = weekbeg.strftime("%s")
            endweek = weekend.strftime("%s")
            begweek1 = weekbeg.strftime("%Y-%m-%d")
            endweek1 = weekend.strftime("%Y-%m-%d")
            
            List_beg_end_each_week.insert(ind, (str(begweek) + '__' + str(endweek)  + '__' + str(begweek1) + '  00:00:00__' + str(endweek1)+ '  00:00:00'))
            #print begweek, endweek
            ind +=1
            num += 1


    print List_beg_end_each_week

    week_ASN = {}
    week_ASN_2bytes = {}
    week_ASN_4bytes = {}


    for ixp in IXP_collector.keys():
        
      create_output =  open(output_folder+'LastMonth__list_visible_ASNs_peering_at_IXP_'+ixp+'.txt', 'a')
      
      create_output.write('###Num Week; Timestamp beginning;  Timestamp end;  Datetime  beginning;  Datetime end; Visible ASNs peering at the IXP\n')
      
      create_output_2bytesASN =  open(output_folder+'LastMonth__2bytes_list_visible_ASNs_peering_at_IXP_'+ixp+'.txt', 'a')
      
      create_output_2bytesASN.write('###Num Week; Timestamp beginning;  Timestamp end;  Datetime  beginning;  Datetime end; Visible 2bytes ASNs peering at the IXP \n')
      
      create_output_4bytesASN =  open(output_folder+'LastMonth__4bytes_list_visible_ASNs_peering_at_IXP_'+ixp+'.txt', 'a')
      
      create_output_4bytesASN.write('###Num Week; Timestamp beginning;  Timestamp end;  Datetime  beginning;  Datetime end; Visible 4bytes ASNs peering at the IXP \n')
      
        
      if ixp not in week_ASN.keys():
        week_ASN[ixp] = {}
      
      if ixp not in week_ASN_2bytes.keys():
        week_ASN_2bytes[ixp] = {}

      if ixp not in week_ASN_4bytes.keys():
        week_ASN_4bytes[ixp] = {}
        
        
      for window in couples_year_month:
          
        
            
            query = "select distinct ASPath from Data__" + str(int(window[0])) + "_" + str(int(window[1])) + " where Timestamp >= %s and Timestamp <= %s  and ("
            
            k = 0
            if len(IXP_collector[ixp]) > 1:
                while k < len(IXP_collector[ixp]) -1:
                    k+=1
                    query += " RouteCollector = %s or "

            
            query += " RouteCollector = %s)  "

            print 'start_query :', now_datetime, query
            print datetime.now(), 'week fetching data from ', ixp
            
            week = 0

            for couple_timestamp in List_beg_end_each_week:
                
                ## Initialisations
                week += 1
                list_variables = []
                tab = str(couple_timestamp).split('__')
                
                if week not in week_ASN[ixp].keys():
                    week_ASN[ixp][week] = []
                    
                if week not in week_ASN_2bytes[ixp].keys():
                    week_ASN_2bytes[ixp][week] = []
            
                if week not in week_ASN_4bytes[ixp].keys():
                    week_ASN_4bytes[ixp][week] = []
                
                    
                ## Split the week into 7 days
                beginning_date = datetime.fromtimestamp(int(tab[0])).strftime('%Y%m%d')
                    
                end_date = datetime.fromtimestamp(int(tab[1])).strftime('%Y%m%d')
                        
                List_days_in_week = list(date_range(beginning_date, end_date, 7))
                
                
                            
                with open ('List_days_in_week.hola', 'a') as fjj:
                    fjj.write('%s\n' %('-'.join(List_days_in_week)))
                                    
                index_week = 0
                                        
                while index_week <= len(List_days_in_week)-2:
                                            
                                            
                    timestp_beg = mktime(datetime.strptime(List_days_in_week[index_week], "%Y%m%d").timetuple())
                    
                    timestp_end = mktime(datetime.strptime(List_days_in_week[index_week+1], "%Y%m%d").timetuple())
                
                    #list_variables = [float(tab[0]), float(tab[1])] + IXP_collector[ixp]
                    
                    list_variables = [float(timestp_beg), float(timestp_end)] + IXP_collector[ixp]

                    #try:
                    
                    cur.execute(query, list_variables)
                    
                    log_file_instance.write(str(now_datetime)+ ' Fetching data from IXP '+ ixp + '\n')
                    
                    print 'Here is the query ', cur._executed
                    data = cur.fetchall()
                    print 'end_query :', now_datetime #, data

                    #except:

                    #    data = []



                    i = 0
                    if len(data) > 0:
                        while (i<len(data)):
                          row = data[i]
                            
                          OriginASNs = []
                          ## Extract the origin AS
                
                          path = row[0].split(' ')
                          
                          if len(path) > 0:
                              
                            if path[0] != 'None' and path[0] != 'NULL':
                              
                                #try:
                                    if int(str(path[0]).strip()) not in OriginASNs:
                                        OriginASNs.append(int(str(path[0]).strip()))
                                    print "Considered AS path = ", row[0], " peering_ASN = ", path[0]
                                #except:
                                #    print 'Case 2: Alert We pass for this path ', row[0]
                                
                            
                            for OriginASNs_elmt in OriginASNs :
                                
                                if OriginASNs_elmt not in week_ASN[ixp][week]:
                                    
                                    week_ASN[ixp][week].append(OriginASNs_elmt)
                                    
                                    create_output.write(str(week) + '; ' + '; '.join(tab) +  '; '+ str(OriginASNs_elmt) + '\n')
                                    
                                    #2 bytes : AS 0 to 65535  ## Reserved: 64512 to 65534 for private; few others such as 0 and 65535
                                    if OriginASNs_elmt >= 0 and OriginASNs_elmt <= 65535 and OriginASNs_elmt not in week_ASN_2bytes[ixp][week]:
                                        
                                        week_ASN_2bytes[ixp][week].append(OriginASNs_elmt)
                                        
                                        create_output_2bytesASN.write(str(week) + '; ' + '; '.join(tab) +  '; '+ str(OriginASNs_elmt) + '\n')

                                    # 4 bytes : AS 65,536 - 4294,967,295; The first thing to notice about these numbers is that they include all of the older 2-byte ASNs, 0 through 65535
                                    # A 4-byte ASN between 0 and 65535 is called a mappable ASN
                                    if OriginASNs_elmt >= 65536 and OriginASNs_elmt <= 4294967295 and OriginASNs_elmt not in week_ASN_4bytes[ixp][week]:
                                        
                                        week_ASN_4bytes[ixp][week].append(OriginASNs_elmt)
                                        
                                        create_output_4bytesASN.write(str(week) + '; ' + '; '.join(tab) +  '; '+ str(OriginASNs_elmt) + '\n')
                            
                            
                            i+=1

                    index_week += 1

      create_output.close()

    print
    print
    print

    print 'Printing data for IXPs'
    
    for ixp in week_ASN.keys():
        
        log_file_instance.write('\n' + str(now_datetime)+ ' Debut computation '+ ixp + '\n')
        
        create_output = open(output_folder+'LastMonth__number_visible_ASNs_peering_at_IXP_' + ixp + '.txt', 'a')
        
        create_output.write('##Num Week' + '; Timestampbeg; Timestampend; Number of OriginAS; Number of 2bytes OriginAS; Number of 4bytes ASN peering at the IXP \n')
        
        for week in week_ASN[ixp].keys():
            
            #create_output =  open(output_folder+'LastMonth__number_visible_ASNs_peering_at_IXP_'+ixp+'.txt', 'a')
            
            tab = str(List_beg_end_each_week[week - 1]).split('__')
            
            try:
                Two_Bytes_ASNs = len(list(set(week_ASN_2bytes[ixp][week])))
            except:
                Two_Bytes_ASNs = 0
            
            try:
                Four_Bytes_ASNs = len(list(set(week_ASN_4bytes[ixp][week])))
            except:
                Four_Bytes_ASNs = 0
            
            
            create_output.write(str(week) + '; ' + '; '.join(tab) +  '; '+ str(len(list(set(week_ASN[ixp][week])))) + '; ' + str(Two_Bytes_ASNs) + '; ' + str(Four_Bytes_ASNs) + '\n')
            
            log_file_instance.write( str(now_datetime)+ ' End computation '+ str(ixp) + ' week ' + str(week) + '\n')

    create_output.close()

log_file_instance.close()


finish = open ('finish_lastmonth.txt', 'w')
finish.write('ended' + '; ' +  root_folder + output_folder[6:])
finish.close()


