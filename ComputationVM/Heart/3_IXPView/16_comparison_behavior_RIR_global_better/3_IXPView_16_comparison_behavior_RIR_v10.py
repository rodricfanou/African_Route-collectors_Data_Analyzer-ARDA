##############################################################################
#__author__ = "Roderick Fanou"
#__status__ = "Production"
#__last_modifications__ =
# by Roderick
# "2016-06-26"
# 1- script edition
# 2- for optimizing the queries we perform 4 queries per IXP (1 per week),
# all route collectors considered
# 3- store the prefixes while they are found.
# 4- "after line 246": improve the output for number of prefixes
# "2016-06-27"
# 1- include bogons prefixes detection
#__date_last_modif__ = "2016-06-27"
#__description__ = "This script generates for last month (Now - 4weeks ) the
#distinct list of prefixes seen during last month splitted into weeks
#The term "Unique prefixes" refers to the list of distinct prefixes present in
#the list of all prefixes in the considered timeline.
##############################################################################


#!/usr/bin/python
import os, re, sys, copy, csv, os.path
import MySQLdb
import json, copy, time, datetime, math
import subprocess, threading
from pprint import pprint
from random import choice
from time import sleep
from collections import Counter
import select, socket
import urllib2, urllib
import GeoIP
import ipaddr, logging
import gzip
from datetime import date
from datetime import datetime
from netaddr import IPNetwork, IPAddress


## import all files in the library you need
sys.path.append('../../2_libraries/')
import ipaddress
import DB_configuration
import bgp_rib
from define_timescales import *
from functions import *
import urllib2


def cidrsOverlap(cidr0, cidr1):
    return cidr0 in cidr1 or cidr1 in cidr0


def build_list_ASNs_allocated_by_RIRs_till (current_year, current_month, dict_ASNs_alloc):
    epoch = datetime(1970, 1, 1)
    d = datetime(current_year, current_month, 1)
    date_combo = (d - epoch).total_seconds()
    Dict_sortie = {}
    
    for timestamp_key in dict_ASNs_alloc.keys():
        if timestamp_key < date_combo:
            for CC in dict_ASNs_alloc[timestamp_key].keys():
                if CC not in Dict_sortie.keys():
                    Dict_sortie[CC] = []
                Dict_sortie[CC] += dict_ASNs_alloc[timestamp_key][CC]

    return Dict_sortie




root_folder = '/home/African_Route-collectors_Data_Analyzer-ARDA/ComputationVM/Heart/'
output_folder = '../../Computation_outputs/16_comparison_behavior_lastmonth_better/'
command = 'rm -rf ' + output_folder
os.system(command)

command = 'mkdir  ' + output_folder
os.system(command)

command = 'chmod 777 ' + output_folder
os.system(command)




now_datetime = str(datetime.now()).replace(' ', '_')
finish = open ('finish_lastmonth.txt', 'w')
finish.write('started; ' + now_datetime)
finish.close()





### Download Jeff'Hudson  Data

## DIX-IE 'http://thyme.rand.apnic.net/current/data-raw-table'

Prefixes_on_the_internet = {}

target_url = 'http://thyme.rand.apnic.net/current/data-raw-table'

Prefixes_on_the_internet['Japan_DIXIE'] = []
    
data = urllib2.urlopen(target_url) # it's a file like object and works just like a file
    
for line in data: # files are iterable

    line = line.strip()

    tab = line.split('	')

    #print line, tab

    if tab[0] not in Prefixes_on_the_internet['Japan_DIXIE'] :
        
        Prefixes_on_the_internet['Japan_DIXIE'].append(tab[0])

        with open(output_folder + 'Prefixes_on_the_internet___Japan_DIXIE.txt', 'a') as fgh:

            fgh.write('%s\n' %(tab[0]))


Prefixes_on_the_internet['Japan_DIXIE'] = []

#pprint(Prefixes_on_the_internet['Japan_DIXIE'])





##London http://thyme.rand.apnic.net/london/data-raw-table

target_url = 'http://thyme.rand.apnic.net/london/data-raw-table'

Prefixes_on_the_internet['London_LINX'] = []

data = urllib2.urlopen(target_url) # it's a file like object and works just like a file

for line in data: # files are iterable
    
    line = line.strip()
    
    tab = line.split('	')
    
    #print line, tab
    
    if tab[0] not in Prefixes_on_the_internet['London_LINX'] :
        
        Prefixes_on_the_internet['London_LINX'].append(tab[0])

        with open(output_folder + 'Prefixes_on_the_internet___London_LINX.txt', 'a') as fgh:
    
            fgh.write('%s\n' %(tab[0]))


Prefixes_on_the_internet['London_LINX'] = []

#pprint(Prefixes_on_the_internet['London_LINX'])




## US http://thyme.rand.apnic.net/us/data-raw-table

target_url = 'http://thyme.rand.apnic.net/us/data-raw-table'

Prefixes_on_the_internet['Washington_US'] = []

data = urllib2.urlopen(target_url) # it's a file like object and works just like a file

for line in data: # files are iterable
    
    line = line.strip()
    
    tab = line.split('	')
    
    #print line, tab
    
    if tab[0] not in Prefixes_on_the_internet['Washington_US'] :
        
        Prefixes_on_the_internet['Washington_US'].append(tab[0])

        with open(output_folder + 'Prefixes_on_the_internet___Washington_US.txt', 'a') as fgh:
    
            fgh.write('%s\n' %(tab[0]))


Prefixes_on_the_internet['Washington_US'] = []

#pprint(Prefixes_on_the_internet['Washington_US'])



##########


## Create a logfile:
name_log_file = 'Log_'+str(now_datetime) + '_' + '16_comparison_behavior_RIR_better_' + '.txt'
location_logfile = create_Logfiles_folder()
log_file_instance = open(location_logfile+'/'+name_log_file, 'a')
log_file_instance.write('startdate:' + now_datetime)


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
db = MySQLdb.connect(host="localhost",user="",passwd="",  db = Current_db)
cur = db.cursor()
#print 'Connected'


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




Current_db = 'RIRs'
## connect to the DB
db = MySQLdb.connect(host="localhost",user="",passwd="",  db = Current_db)
cur = db.cursor()


List_RIRs_prefixes = ['IPv4_ressources_AFRINIC',  'IPv4_ressources_ARIN', 'IPv4_ressources_APNIC', 'IPv4_ressources_LACNIC']

RIRs_prefixes = {}
    

for RIRs_prefix_table in List_RIRs_prefixes:

    query = "select distinct NetIPaddress, NetBits, CC, date from " + RIRs_prefix_table  + " where status = 'allocated' or status = 'assigned' and CC != '' ;"
    cur.execute (query)
    data = cur.fetchall()
    i = 0

    #RIRs_prefix_table = 'IPv4_ressources_AFRINIC'

    if len(data)>0:
        
        while (i<len(data)):
            
          row = data[i]
          #print row
          if '.' in row[0] or ':' in row[0]:  
            alloc_prefix = row[0]+'/'+row[1]
            current_CC = row[2]
            
            if '-' in row[3]:
                date_row = row[3].split('-') #type_string need to be converted into timestamp
                year_row = date_row[0]
                month_row = date_row[1]
                day_row = date_row[2]
            
            else:
                date_row = row[3] #type_string need to be converted into timestamp
                year_row = date_row[:4]
                month_row = date_row[4:6]
                day_row = date_row[6:8]
            
            
            if year_row == '0000' or year_row == '':
                year_row = '1970'
                month_row = '01'
                day_row = '01'

	    
		
            
            print 'row = ', row,  date_row[:4] + '_' + date_row[4:6] + '_' + date_row[6:8]
            date_combo = date_row[:4] + '_' + date_row[4:6] + '_' + date_row[6:8]
            
            epoch = datetime(1970, 1, 1)
            d = datetime(int(year_row), int(month_row), int(day_row))
            
            date_combo = (d - epoch).total_seconds()
            
            tab_RIR = RIRs_prefix_table.split('_')
            
            if current_CC != '':
                if alloc_prefix not in RIRs_prefixes.keys():
                    RIRs_prefixes[alloc_prefix] = {}
                    RIRs_prefixes[alloc_prefix]['Date_alloc'] = date_combo
                    RIRs_prefixes[alloc_prefix]['RIR'] = tab_RIR[-1]
                    RIRs_prefixes[alloc_prefix]['CC'] = current_CC
                else:
                    if RIRs_prefixes[alloc_prefix]['Date_alloc'] < date_combo:
                        RIRs_prefixes[alloc_prefix]['Date_alloc'] = date_combo
                        RIRs_prefixes[alloc_prefix]['CC'] = current_CC
        
          i += 1



### RIPE
query = "select distinct NetIPaddress, NetBits, CC, date from IPv4_ressources_RIPE where status = 'allocated' or status = 'assigned' and CC != '';"
cur.execute (query)
data = cur.fetchall()
i = 0

RIRs_prefix_table = 'IPv4_ressources_RIPE'

if len(data)>0:
    while (i<len(data)):
      row = data[i]
      if '.' in row[0] or ':' in row[0] :
        alloc_prefix = row[0]+'/'+row[1]
        current_CC = row[2]
        
        #print row[3]
        if '-' in row[3]:
            date_row = row[3].split('-') #type_string need to be converted into timestamp
            year_row = date_row[0]
            month_row = date_row[1]
            day_row = date_row[2]
        
        else:
            date_row = row[3] #type_string need to be converted into timestamp
            year_row = date_row[:4]
            month_row = date_row[4:6]
            day_row = date_row[6:8]
        
        
        if year_row == '0000' or month_row == '00' or day_row == '00':
            year_row = '1970'
            month_row = '01'
            day_row = '01'
    
        print 'row = ', row,  year_row + '_' + month_row + '_' + day_row
        
        
        epoch = datetime(1970, 1, 1)
        d = datetime(int(year_row), int(month_row), int(day_row))
        
        date_combo = (d - epoch).total_seconds()
        
        tab_RIR = RIRs_prefix_table.split('_')
        
        if current_CC != '':
            
            if alloc_prefix not in RIRs_prefixes.keys():
                RIRs_prefixes[alloc_prefix] = {}
                RIRs_prefixes[alloc_prefix]['Date_alloc'] = date_combo
                RIRs_prefixes[alloc_prefix]['RIR'] = tab_RIR[-1]
                RIRs_prefixes[alloc_prefix]['CC'] = current_CC
            
            else:
                if RIRs_prefixes[alloc_prefix]['Date_alloc'] < date_combo:
                    RIRs_prefixes[alloc_prefix]['Date_alloc'] = date_combo
                    RIRs_prefixes[alloc_prefix]['CC'] = current_CC
        
      i += 1


#pprint(RIRs_prefixes)
Keep_all_prefixes = copy.deepcopy(RIRs_prefixes.keys())


### ALERT: CAN BE SUPPRESSED LATER
#RIRs_prefixes = {}

### Which ones of those prefixes appear during the period ?
Current_db = 'MergedData'
## connect to the DB
db = MySQLdb.connect(host="localhost",user="",passwd="",  db = Current_db)
cur = db.cursor()





#### More or less OK

### splitted into weeks over the last month

if len(List_all_tables) > 0:
    
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
    #timestamp_one_month_before = int(timestamp_now) - 2592000
    #timestamp_one_month_before = int(timestamp_now) - 604800
    timestamp_one_month_before = int(timestamp_now) - 86400


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

    print 'List_beg_end_each_week = ', List_beg_end_each_week

    print 'couples_year_month = ', couples_year_month

    ## Commented because we do not need it right now
    #prefix_week = {}
    week_prefix = {}



    for ixp in IXP_collector.keys():
        
      #create_output = open(output_folder+'LastMonth__list_visible_prefixes_at_IXP_'+ixp+'.txt', 'a')
        
      if ixp not in week_prefix.keys():
          
        week_prefix[ixp] = []
      
      for window in couples_year_month:
    
        query = "select distinct Network from Data__" + str(int(window[0]))+"_"+str(int(window[1])) + " where Timestamp >= %s and Timestamp <= %s  and ("
        
        print
        print
        
        k = 0
        while k < len(IXP_collector[ixp]) -1:
            k+=1
            query += " RouteCollector = %s or "
        
        query += " RouteCollector = %s) and TypeRC = 'PCH' "  ## ALERT: limit 2 TO SUPPRESS AFTER.

        print 'start_query :', now_datetime, query

        print datetime.now(), 'week fetching data from ', ixp

        for couple_timestamp in List_beg_end_each_week:
            
            list_variables = []
            
            tab = str(couple_timestamp).split('__')
            
            list_variables = [float(tab[0]), float(tab[1])] + IXP_collector[ixp]

            
            try:
                cur.execute(query, list_variables)
                
                print 'Running query for ', ixp , ' and variables ', IXP_collector[ixp]
                
                #log_file_instance.write(str(now_datetime)+ ' Fetching data from IXP '+ ixp + '\n')

                print 'Here is the query ', cur._executed
                data = cur.fetchall()

                print 'end_query :', now_datetime #, data
            
            except:
                
                print 'Alert table ', "Data__"+str(lastMonthList[0][0])+"_"+str(lastMonthList[0][1]),  ' does not exist yet'
                
                data = []
            

            i = 0
            
            if len(data)>0:
                
                while (i<len(data)):
                    
                  row = data[i]
                  
                  prefix = row[0]
                  
                  ## Make sure prefix is v4 or prefix is v6 by doing an try                  
                      
                  if 'None' not in prefix:
                        
                        test = 'OK'
                        
                        try:
                        
                            ip = IPNetwork(prefix)
                        
                        except:
                            test = 'KO'

                        
                        if test == 'OK' and ip.size > 0:
                        
                            try:
                                selected_ip = ip[1]
                            except:
				try:
                                	selected_ip = ip[5]
				except:
					try:
						selected_ip = ip[2]
					except:
						pass

                            check_bogon = check_if_bogon(selected_ip)
                                
                            if check_bogon:
                                
                                print 'Pass because bogon'
                            
                            else:
                                
                                if prefix not in week_prefix[ixp]:
                                    
                                    ## check if it matches with any
                                    
                                    j = 0

                                    while j < len(Keep_all_prefixes) :
                                    
                                        prefix_IX = ipaddr.IPNetwork(str( prefix ))
                                        
                                        prefix_RIR = ipaddr.IPNetwork(str( Keep_all_prefixes[j] ))
                                        
                                        
                                        #if prefix_IX.overlaps(prefix_RIR) and prefix_IX  != '0.0.0.0/0':
                                        
                                        if cidrsOverlap(prefix_IX, prefix_RIR) :
                                            
                                            print
                                            
                                            print prefix_IX, ' overlaps ', prefix_RIR
                                            
                                            week_prefix[ixp].append(prefix)
                                            
                                            with open (output_folder+'Output_Intersection_week_prefix___' + ixp + '.txt', 'a') as fgg:
                                                
                                                fgg.write('%s\n' %(prefix))
                                            
                                                print 'We added prefix ', prefix, ' to ', output_folder+'Output_Intersection_week_prefix___' + ixp + '.txt'
                                    
                                            j = len(Keep_all_prefixes)
            
                                        j += 1


                  i += 1


print
for ixp in week_prefix.keys():
    week_prefix[ixp] = []
    print ' prefixes seen at the IXP ', ixp, ' = ', week_prefix[ixp]
    print
    print ixp, 'len(week_prefix[ixp]) = ', len(week_prefix[ixp])
    print
    print




######## Length shorter equal or longer; seen from each IXP
Computation_announcements = {}

for IXP_in_world in Prefixes_on_the_internet.keys():

    if IXP_in_world not in Computation_announcements.keys():

        Computation_announcements[IXP_in_world] = {}
    
    with open(output_folder + 'Prefixes_on_the_internet___' + IXP_in_world + '.txt', 'r') as fgh:
        
        for line in fgh:
        
                line = line.strip()
                
                if line not in Prefixes_on_the_internet[IXP_in_world]:
        
                    Prefixes_on_the_internet[IXP_in_world].append(line)
        


    for Global_prefix in Prefixes_on_the_internet[IXP_in_world]:
        
        for ixp in week_prefix.keys():
            
            #create_output = open(output_folder+'Comparison_members_behavior_'+ixp+'.txt', 'a')
            
            if ixp not in Computation_announcements[IXP_in_world].keys():

                Computation_announcements[IXP_in_world][ixp] = {}
            
            if 'IXPShorterThanUpstream' not in Computation_announcements[IXP_in_world][ixp].keys():
            
                Computation_announcements[IXP_in_world][ixp]['IXPShorterThanUpstream'] = []
            
            create_file1 = open(output_folder+'List_prefix_announcements_IXPShorterThanUpstream__for__'+ ixp+ '.txt', 'a')
            

            if 'IXPLongerThanUpstream' not in Computation_announcements[IXP_in_world][ixp].keys():
    
                Computation_announcements[IXP_in_world][ixp]['IXPLongerThanUpstream'] = []
            
            create_file2 = open(output_folder+'List_prefix_announcements_IXPLongerThanUpstream__for__'+ ixp+ '.txt', 'a')
            
            
            if 'IXPBalancedUpstream' not in Computation_announcements[IXP_in_world][ixp].keys():
            
                Computation_announcements[IXP_in_world][ixp]['IXPBalancedUpstream'] = []
            
            create_file3 = open(output_folder+'List_prefix_announcements_IXPBalancedUpstream__for__'+ ixp+ '.txt', 'a')
            
            
            List_prefixes_in_Output = []
                
            if os.path.exists(output_folder+'Output_Intersection_week_prefix___' + ixp + '.txt'):
            
                with open (output_folder+'Output_Intersection_week_prefix___' + ixp + '.txt', 'r') as fhhh:

                    for line in fhhh:
                
                        line1 = line.strip()
     
                        if line1 not in List_prefixes_in_Output:
                            
                            List_prefixes_in_Output.append(line1)
                        

                #for prefix_IXP in week_prefix[ixp]:
                
                for prefix_IXP in List_prefixes_in_Output:
                    
                    #create_output =  open(output_folder+'Comparison_members_behavior_'+ixp+'.txt', 'a')
                    test = 'OK'
                    ## Make sure prefix is v4 or prefix is v6 by doing a try
                    
                    try:
                        #prefix_seen_IX = ipaddr.IPNetwork( str( prefix_IXP ) )
                        prefix_seen_IX = IPNetwork( str( prefix_IXP ) )
                        #prefix_Internet = ipaddr.IPNetwork( str( Global_prefix ) )
                        prefix_Internet = IPNetwork( str( Global_prefix ) )
                    
                    except:
                        test = 'KO'
                    
                    
                    print prefix_seen_IX, prefix_Internet
                    
                    if test == 'OK':
                        
                        if cidrsOverlap(prefix_seen_IX, prefix_Internet) :

                            tab_IXP = str(prefix_IXP).split('/')

                            tab_Internet = str(Global_prefix).split('/')
                            
                            to_add = str(prefix_IXP) + '__' + str(Global_prefix)
                        
                            print prefix_seen_IX, 'overlap with ', prefix_Internet
                            
                            
                            
                            # 41.32.0.0/16 (IXP); 41.32.0.0/12 (UPSTREAM)
                            
                            if int(tab_IXP[-1]) > int(tab_Internet[-1]):
                                
                                print int(tab_IXP[-1]) , ' < ', int(tab_Internet[-1]) , ' but num host IXP > num host Internet.'
                                
                                if to_add not in Computation_announcements[IXP_in_world][ixp]['IXPShorterThanUpstream']:
                            
                                    Computation_announcements[IXP_in_world][ixp]['IXPShorterThanUpstream'].append(to_add)
                        
                                    create_file1.write( str(prefix_IXP) + ' ; ' +  str(Global_prefix) + '\n' )
                        
                        
                        
                            elif int(tab_IXP[-1]) < int(tab_Internet[-1]):
                                
                                print int(tab_IXP[-1]) , ' > ', int(tab_Internet[-1]), ' but num host IXP < num host Internet'
                            
                                if to_add not in Computation_announcements[IXP_in_world][ixp]['IXPLongerThanUpstream']:
                                
                                    Computation_announcements[IXP_in_world][ixp]['IXPLongerThanUpstream'].append(to_add)
                            
                                    create_file2.write( str(prefix_IXP) + ' ; ' +  str(Global_prefix) + '\n' )
                        
                        

                            elif int(tab_IXP[-1]) == int(tab_Internet[-1]):
                                
                                print int(tab_IXP[-1]) ,  ' == ', int(tab_Internet[-1])

                                if to_add not in Computation_announcements[IXP_in_world][ixp]['IXPBalancedUpstream']:
                                
                                    Computation_announcements[IXP_in_world][ixp]['IXPBalancedUpstream'].append(to_add)

                                    create_file3.write( str(prefix_IXP) + ' ; ' +  str(Global_prefix) + '\n' )


        Prefixes_on_the_internet[IXP_in_world] = []




for IXP_in_world in Computation_announcements.keys():
    
    for ixp in Computation_announcements[IXP_in_world].keys():
        
        create_output = open(output_folder+'Comparison_members_behavior_'+ixp+'.txt', 'a')
        

        create_output.write(str(IXP_in_world) + '; IXPShorterThanUpstream; ' + str(len(list(set(     Computation_announcements[IXP_in_world][ixp]['IXPShorterThanUpstream']    ))))  + '\n')

        create_output.write(str(IXP_in_world) + '; IXPLongerThanUpstream; ' + str(len(list(set(     Computation_announcements[IXP_in_world][ixp]['IXPLongerThanUpstream']    ))))  + '\n')

        create_output.write(str(IXP_in_world) + '; IXPBalancedUpstream; ' + str(len(list(set(     Computation_announcements[IXP_in_world][ixp]['IXPBalancedUpstream']    ))))  + '\n\n')


finish = open ('finish_lastmonth.txt', 'w')
finish.write('ended' + '; ' +  root_folder + output_folder[6:] + '; ' + now_datetime)
finish.close()

