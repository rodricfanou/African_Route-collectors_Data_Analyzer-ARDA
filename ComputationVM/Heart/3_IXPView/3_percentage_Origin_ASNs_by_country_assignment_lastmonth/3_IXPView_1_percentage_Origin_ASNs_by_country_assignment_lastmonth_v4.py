#1st graph : We keep the pie chart in the application (added below), but we compute
#it only for last month, and consider distinct ASNs as defined in point 2.

##############################################################################
#__author__ = "Roderick Fanou"
#__status__ = "Production"
# Last modification date = October 18, 2016
#__Modifications__ =
## local afrinic added to the classification of the Origine ASes
## Line 660 ; error in coding Listrest_ASes instead of CC_ASNs_RIPE[cc_region]
## Continent and region fetched from configuration file
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
from datetime import datetime, timedelta
import time
import pycountry

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


now_datetime = str(datetime.now()).replace(' ', '_')

finish = open ('finish_lastmonth.txt', 'w')
finish.write('started; ' + now_datetime )
finish.close()

## Create a logfile:
name_log_file = 'Log_'+str(now_datetime) + '_' + '1_Number_Origin_ASNs_visible_at_an_IXP_lastmonth' + '.txt'
location_logfile = create_Logfiles_folder()

### Define timelines and timescales
## multi-years splitted into years
yearList = multiyear()
print yearList

## last month (Now - 4weeks) splitted into weeks
lastYearList = lastyear()
print lastYearList

## last month (Now - 4weeks) splitted into weeks
#lastMonthList = lastmonth()
#print lastMonthList


## Other initialisations
continent = DB_configuration.continent
IXP_collector = {}
IXP_CC = {}
region = DB_configuration.region
CC_ASNs_AFRINIC = {}
CC_IXP = {}



## connect to the DB
Current_db = 'MergedData'
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
        IXP_CC[row[2]] = row[0]
    
    if row[2] not in CC_IXP.keys():
        CC_IXP[row[2]] = []
    if row[0] not in CC_IXP[row[2]]:
        CC_IXP[row[2]].append(row[0])
    
    IXP_collector[row[0]].append(row[1])
    i+=1

print IXP_collector

root_folder = '/home/African_Route-collectors_Data_Analyzer-ARDA/ComputationVM/Heart/'
output_folder = '../../Computation_outputs/3_percentage_Origin_ASNs_by_country_assignment_lastmonth/'

command = 'rm -rf ' + output_folder
os.system(command)

command = 'mkdir  ' + output_folder
os.system(command)

command = 'chmod 777 ' + output_folder
os.system(command)

filename = output_folder


#### What has AFRINIC attributed till now
### Query RIRs database

## connect to the DB
Current_db = 'RIRs'
db = MySQLdb.connect(host = DB_configuration.host, user = DB_configuration.user, passwd= DB_configuration.passwd,  db = Current_db)
cur = db.cursor()

query = "select distinct ASN, CC from ASNs_"+region+" where (status = 'allocated' or status = 'assigned') ;"
print 'query = ',  query
cur.execute (query)
data = cur.fetchall()
i = 0

#print 'len table', len(data)
if len(data)>0:
    while (i<len(data)):
        row = data[i]
        print row
        asn = row[0] #type string
        current_CC = row[1]
        
        if '.' in asn: #conversion to 2Byte format
            #print '4B format:',asn
            tab = asn.split('.')
            asn = int(tab[0])*65536 + int(tab[1])
        
        asn = int(asn) #format int
        if current_CC not in  CC_ASNs_AFRINIC.keys():
            CC_ASNs_AFRINIC[current_CC] = []
        
        if asn not in CC_ASNs_AFRINIC[current_CC]:
            CC_ASNs_AFRINIC[current_CC].append(asn)
        i +=1

pprint(CC_ASNs_AFRINIC)

filename_output_ASNs_by_AFRINIC = output_folder + 'Number_ASNs_assigned_by_Afrinic.txt'
with open (filename_output_ASNs_by_AFRINIC, 'a') as fg:
    for CC in CC_ASNs_AFRINIC.keys():
        fg.write('%s;%s\n' %(CC, len(CC_ASNs_AFRINIC[CC])))


Current_db = 'MergedData'
db = MySQLdb.connect(host = DB_configuration.host, user = DB_configuration.user, passwd= DB_configuration.passwd,  db = Current_db)
cur = db.cursor()



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


## Initialisation
week_ASN = {}



### splitted into weeks over the last month
#print lastMonthList[0][0], lastMonthList[0][1]

#print List_all_tables


if len(List_all_tables) > 0:
    
    tab = str(datetime.now()).split(' ')
    #tab = ['2017-01-20']
    tab1 = tab[0].split('-')
    timestamp_now = (datetime(int(tab1[0]), int(tab1[1]), int(tab1[2])) - datetime(1970, 1, 1)).total_seconds()
    date_now  = datetime.fromtimestamp(int(timestamp_now)).strftime('%Y-%m-%d')
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

    List_beg_end_each_week = [ str(timestamp_one_month_before ) + '__' +   str(timestamp_now)  + '__'    + str(date_one_month_bef) + '  00:00:00__'  +  '__' +  str(date_now) + ' 00:00:00']

    print 'List_beg_end_each_week = ', List_beg_end_each_week

    print couples_year_month



    for ixp in IXP_collector.keys():
        print
        print
        
        if ixp not in week_ASN.keys():
            week_ASN[ixp] = []
        
        for window in couples_year_month:

            query = "select distinct OriginAS, ASPath from Data__" + str(int(window[0])) + "_" + str(int(window[1])) + " where Timestamp >= %s and Timestamp <= %s  and ("
            k = 0
            if len(IXP_collector[ixp]) > 1:
                while k < len(IXP_collector[ixp]) -1:
                    k+=1
                    query += " RouteCollector = %s or "

            query += " RouteCollector = %s) and (OriginAS != 'None' and OriginAS is not NULL and OriginAS != 'NULL')  "
        
            print 'start_query :', now_datetime, query
            print datetime.now(), 'week fetching data from ', ixp


            couple_timestamp = List_beg_end_each_week[0]
    
            list_variables = []
            tab = str(couple_timestamp).split('__')
            
            list_variables = [float(tab[0]), float(tab[1])] + IXP_collector[ixp]

            try:
                cur.execute(query, list_variables)
                
                log_file_instance.write(str(now_datetime)+ ' Fetching data from IXP '+ ixp + '\n')
                
                print 'Here is the query ', cur._executed
                data = cur.fetchall()
                print 'end_query :', now_datetime #, data
    
            except:
                data = []


            i = 0
            if len(data)>0:
                while (i<len(data)):
                    row = data[i]
                    
                    OriginASNs = []
                    ## Extract the origin AS
                    if '{' not in row[0] and ',' not in row[0] and '}' not in row[0]:
                        
                        try:
                            OriginASNs.append(int(row[0]))
                        except:
                            print 'Case 1: Alert We pass for this path ', row[1]
            
                    else:
                    
                        path = row[1].split(' ')
                        try:
                            OriginASNs.append(int(str(path[-2]).strip()))
                            #print row[1], '; ',  row[0], '; ', int(path[-2])
                        except:
                            print 'Case 2: Alert We pass for this path ', row[1]
                        
                    #print OriginASNs
                    
                    for OriginASNs_elmt in OriginASNs :
                        
                        if OriginASNs_elmt not in week_ASN[ixp]:
                            
                            week_ASN[ixp].append(OriginASNs_elmt)
                    
                    i+=1

        print ixp, 'len(week_ASN[ixp]) = ' , len(week_ASN[ixp])





with open (output_folder + '/1_percentage_of_allocated_ASNs_seen_as_origin_ASNs_at_an_IXP.txt', 'a') as fd:
    fd.write('%s; %s; %s; %s; %s\n'%('##IXP', 'Number of Origin ASNs found', 'Common ASNs to Origin ASNs and Assigned ASNs ', 'ASNs Assigned by Afrinic',  'Percentage of Origin ASes at the IXP assigned by Afrinic'))
    fd.close()


### compute the percentage of assigned ASes by Afrinic that are origin ASes.
for cc in CC_IXP:
    
    for ixp in CC_IXP[cc]:
        
        if ixp in week_ASN.keys():
        
                print
                print
                
                print 'Number of ASNs allocated to CC:', len(CC_ASNs_AFRINIC[cc])
                
                print 'Number of Origin ASNs seen at the IXP:', len(list(set(week_ASN[ixp])))
                
                diff = list(set(week_ASN[ixp]) - set(CC_ASNs_AFRINIC[cc]))
                intersection = list(set(week_ASN[ixp]) & set(CC_ASNs_AFRINIC[cc]))
                rest = list(set(CC_ASNs_AFRINIC[cc]) - set(intersection))
                
                current_filename = output_folder + '/Origin_ASNs_assigned_to_country_seen_at_'+ixp+'.txt'
                if len(intersection) > 0:
                    with open(current_filename, 'a') as fd:
                        for elmt in intersection :
                            fd.write('%s\n'%( elmt))

            
                current_filename = output_folder + '/Origin_ASNs_assigned_to_country_Not_seen_at_'+ixp+'.txt'
                if len(rest) > 0:
                    with open(current_filename, 'a') as fd:
                        for elmt in rest :
                            fd.write('%s\n'%(elmt))
    
                                                 
                percentage_found = float(len(intersection))/float(len(CC_ASNs_AFRINIC[cc]))*100
                print 'diff', len(diff)
                print 'intersection', len(intersection)
                print 'percentage in % for Origin ASes:',  ixp, len(list(set(week_ASN[ixp]))), len(intersection), len(CC_ASNs_AFRINIC[cc]),  percentage_found


                with open (output_folder + '/1_percentage_of_allocated_ASNs_seen_as_origin_ASNs_at_an_IXP.txt', 'a') as fd:
                    fd.write('%s; %s; %s; %s; %s\n'%(ixp, len(list(set(week_ASN[ixp]))), len(intersection), len(CC_ASNs_AFRINIC[cc]),  percentage_found))
                    fd.close()





## connect to the DB
Current_db = 'RIRs'
db = MySQLdb.connect(host = DB_configuration.host, user = DB_configuration.user, passwd= DB_configuration.passwd,  db = Current_db)
cur = db.cursor()

##### Fetching list of all ASNs in each region
CC_ASNs_RIPE = {}
CC_ASNs_ARIN = {}
CC_ASNs_LACNIC = {}
CC_ASNs_APNIC = {}


query = "select distinct ASN, CC from ASNs_RIPE where status = 'allocated' or status = 'assigned';"
cur.execute (query)
data = cur.fetchall()
i = 0
if len(data)>0:
    while (i<len(data)):
        row = data[i]
        asn = row[0] #type string
        CC = row[1]
        if CC not in CC_ASNs_RIPE.keys() and CC != '':
            CC_ASNs_RIPE[CC] = []
        if '.' in asn: #conversion to 2Byte format
            asn = int(asn[:asn.find('.')])*65536 + int(asn[asn.find('.')+1:])
        asn = int(asn) #format int
        if asn not in CC_ASNs_RIPE[CC]:
            CC_ASNs_RIPE[CC].append(asn)
        i +=1
print 'CC at RIPE', CC_ASNs_RIPE.keys()
print


query = "select distinct ASN, CC from ASNs_ARIN where status = 'allocated' or status = 'assigned';"
cur.execute (query)
data = cur.fetchall()
i = 0
if len(data)>0:
    while (i<len(data)):
        row = data[i]
        asn = row[0] #type string
        CC = row[1]
        if CC not in CC_ASNs_ARIN.keys() and CC != '':
            CC_ASNs_ARIN[CC] = []
        if '.' in asn: #conversion to 2Byte format
            asn = int(asn[:asn.find('.')])*65536 + int(asn[asn.find('.')+1:])
        asn = int(asn)
        if asn not in CC_ASNs_ARIN[CC]:
            CC_ASNs_ARIN[CC].append(asn)
        i +=1
print 'CC at ARIN', CC_ASNs_ARIN.keys()
print


query = "select distinct ASN, CC from ASNs_APNIC where status = 'allocated' or status = 'assigned';"
cur.execute (query)
data = cur.fetchall()
i = 0
if len(data)>0:
    while (i<len(data)):
        row = data[i]
        asn = row[0] #type string
        CC = row[1]
        if CC not in CC_ASNs_APNIC.keys() and CC != '':
            CC_ASNs_APNIC[CC] = []
        if '.' in asn: #conversion to 2Byte format
            asn = int(asn[:asn.find('.')])*65536 + int(asn[asn.find('.')+1:])
        asn = int(asn)
        if asn not in CC_ASNs_APNIC[CC]:
            CC_ASNs_APNIC[CC].append(asn)
        i +=1
print  'CC at APNIC',CC_ASNs_APNIC.keys()
print


query = "select distinct ASN, CC from ASNs_LACNIC where status = 'allocated' or status = 'assigned';"
cur.execute (query)
data = cur.fetchall()
i = 0
if len(data)>0:
    while (i<len(data)):
        row = data[i]
        asn = row[0] #type string
        CC = row[1]
        if CC not in CC_ASNs_LACNIC.keys() and CC != '':
            CC_ASNs_LACNIC[CC] = []
        if '.' in asn: #conversion to 2Byte format
            asn = int(asn[:asn.find('.')])*65536 + int(asn[asn.find('.')+1:])
        asn = int(asn)
        if asn not in CC_ASNs_LACNIC[CC]:
            CC_ASNs_LACNIC[CC].append(asn)
        i +=1
print 'CC at LACNIC',  CC_ASNs_LACNIC.keys()
print


#### Classify by type of Origin AS
##### Classifying them into local or external

command = 'mkdir  ' + output_folder + 'files_origin/'
os.system(command)


update = 0

IXP_OriginASes = {}

IXP_OriginASes = copy.deepcopy(week_ASN)

for ixp in IXP_OriginASes.keys():
        ori_dict = {}
        ori_dict['RIPE'] = {}
        ori_dict['external_AFRINIC'] = {}
        ori_dict['local_AFRINIC'] = {}
        ori_dict['LACNIC'] = {}
        ori_dict['APNIC'] = {}
        ori_dict['ARIN'] = {}
        ori_dict['PRIVATE'] = []
        ori_dict['RESERVED'] =[]
        
        
        filename = output_folder + 'Percentage_Origin_ASNs_by_country_assignment_' +ixp+ '.txt'
        filename1 = output_folder + 'Percentage_Origin_ASNs_by_region_' +ixp+ '.txt'
        
        
        with open(filename, 'a') as fd:
            fd.write('%s;%s;%s;%s;%s;%s;%s\n'%('##Current_CC', 'Country name', 'Intersection OriginASNs & ASNs assigned to the country', 'num Origin ASNs seen at the IXP', 'Percentage of local ASNs compared to the ASNs seen at the IXP', 'num ASNs assigned by Afrinic to the CC', 'Percentage of ASNs assigned to the country seen at the IXP' ))


        with open (filename1, 'a') as fg:
            fg.write('%s;%s;%s\n'%('##Type of ASNs (Region)', 'len_ASNs_type', 'percentage_type'))


        for CC in CC_IXP.keys():
            for ixp1 in CC_IXP[CC]:
                if ixp == ixp1 :
                        #print ixp, CC
                        #print ixp,  IXP_OriginASes[ixp], len( IXP_OriginASes[ixp])
                        current_CC = CC
                        #print
                        
                        Listrest_ASes = copy.deepcopy(IXP_OriginASes[ixp])

                        private = []
                        reserved = []
                        for s in Listrest_ASes:
                            if 64512<=s and s<=65534 :
                                private.append(s)
                                IXP_OriginASes[ixp].remove(s)
                                ori_dict['PRIVATE'].append(s)
                            
                            elif (s==0 or s==65535) or (54272<=s and s<=64511):
                                reserved.append(s)
                                IXP_OriginASes[ixp].remove(s)
                                ori_dict['RESERVED'].append(s)
 
 
                        try:
                            percentage_private = float(len(ori_dict['PRIVATE']))/float(len(Listrest_ASes))*100
                        except:
                            percentage_private = 0.0

                        print 'private = ', len(ori_dict['PRIVATE']), percentage_private
                        if len(ori_dict['PRIVATE']) > 0:
                            current_filename = output_folder + 'files_origin/Private_ASNs_' + ixp + '.txt'
                            for elmt in ori_dict['PRIVATE']:
                                with open (current_filename, 'a') as fh:
                                    fh.write('%s\n' %(elmt))

                        with open (filename1, 'a') as fg:
                            fg.write('%s; %s\n'%('##Total number of origin ASNs found during last month = ', len(Listrest_ASes)))
        

                        with open (filename1, 'a') as fg:
                            fg.write('%s;%s;%s\n'%('Private ASNs', len(ori_dict['PRIVATE']), percentage_private))


                        try:
                            percentage_reserved = float(len(ori_dict['RESERVED']))/float(len(Listrest_ASes))*100
                        except:
                            percentage_reserved = 0.0



                        #print 'reserved =', len(ori_dict['RESERVED']), percentage_reserved
                        if len(ori_dict['RESERVED']) > 0:
                            current_filename = output_folder + 'files_origin/Reserved_ASNs_' + ixp + '.txt'
                            for elmt in ori_dict['RESERVED']:
                                with open(current_filename, 'a') as fh:
                                    fh.write('%s\n'%(elmt))
                    
                        with open (filename1, 'a') as fg:
                            fg.write('%s;%s;%s\n'%('Reserved ASNs', len(ori_dict['RESERVED']), percentage_reserved))


                        ## Local
                        intersection = list(set(IXP_OriginASes[ixp]) & set(CC_ASNs_AFRINIC[current_CC]))
    
                        if len(intersection) > 0:
                            current_filename = output_folder + 'files_origin/Local_AFRINIC_ASNs_' + ixp + '.txt'
                            for elmt in intersection :
                                with open(current_filename, 'a') as fd:
                                    fd.write('%s\n'%(elmt))
                        
                        try:
                            ## How many ASNs assigned to current country and seen @ the IXP vs. the total number of Origin ASNs seen @ the IXP
                            percentage_local_AF = float(len(intersection))/float(len(Listrest_ASes))*100
                        except:
                            percentage_local_AF = 0.0
                        
                        print 'percentage_local_AF =', percentage_local_AF
                        ori_dict['local_AFRINIC'] = {current_CC: intersection}
                        
                        
                        ## Percentage of ASNs allocated to the country visibles at the IXP
                        try:
                            ## How many ASNs assigned to current country and seen @ the IXP vs.
                            percentage_local_AF2 = float(len(intersection))/float(len(CC_ASNs_AFRINIC[current_CC]))*100
                        except:
                            percentage_local_AF2 = 0.0

                    
                        with open(filename, 'a') as fd:
                            if len(intersection) >0:
                                try:
                                    A = pycountry.countries.get(alpha2=current_CC)
                                    fd.write('%s;%s;%s;%s;%s;%s;%s;%s\n'%(current_CC, A.name, len(intersection), len(Listrest_ASes),  percentage_local_AF, len(CC_ASNs_AFRINIC[current_CC]),  percentage_local_AF2, 'AFRINIC' ))
                                except:
                                    fd.write('%s;%s;%s;%s;%s;%s;%s;%s\n'%(current_CC, '', len(intersection), len(Listrest_ASes), percentage_local_AF, len(CC_ASNs_AFRINIC[current_CC]),  percentage_local_AF2, 'AFRINIC' ))
                    
                    
                        print 'local_AFRINIC =', percentage_local_AF
                        
                        with open (filename1, 'a') as fg:
                            fg.write('%s;%s;%s\n'%('Local AFRINIC ASNs', len(intersection), percentage_local_AF))
                        
                        

### AFRINIC

                        total = 0
                        total1 = 0
                        #for cc_external in CC_IXP.keys():
                        for cc_external in CC_ASNs_AFRINIC.keys():
        
                            print 'external cc in AFRINIC region to make intersection with the local ASNs:', cc_external
            
                            if current_CC != cc_external:
                                if cc_external not in ori_dict['external_AFRINIC'].keys():
                                        print 'length of ASNs in a cc_external', cc_external , ' = ', len(set(CC_ASNs_AFRINIC[cc_external]))
                                        intersection2 =  list(set(IXP_OriginASes[ixp]) & set(CC_ASNs_AFRINIC[cc_external]))
                            
                                        if len(intersection2) > 0:
                                            current_filename = output_folder + 'files_origin/External_AFRINIC_ASNs_' + ixp + '.txt'
                                            for elmt in intersection2 :
                                                with open(current_filename, 'a') as fd:
                                                    fd.write('%s\n'%(elmt))

                                        try:
                                            percentage_external_AF = float(len(intersection2))/float(len( Listrest_ASes ))*100
                                        except:
                                            percentage_external_AF = 0.0
                
                                        print 'percentage_external_AF =', percentage_external_AF
                    
                                        print 'length of intersection2:', len(intersection2)
                        
                                        try:
                                            percentage_external_AF2 = float(len(intersection2))/float(len(CC_ASNs_AFRINIC[cc_external]))*100
                                        except:
                                            percentage_external_AF2 = 0.0
                                        
                                        
                                        with open(filename, 'a') as fd:
                                            if len(intersection2) >0:
                                                try:
                                                    A = pycountry.countries.get(alpha2=cc_external)
                                                    fd.write('%s;%s;%s;%s;%s;%s;%s;%s\n'%(cc_external, A.name , len(intersection2), len(Listrest_ASes), percentage_external_AF, len(CC_ASNs_AFRINIC[cc_external]),percentage_external_AF2, 'AFRINIC'))
                                                except:
                                                    fd.write('%s;%s;%s;%s;%s;%s;%s;%s\n'%(cc_external, '' , len(intersection2), len(Listrest_ASes), percentage_external_AF, len(CC_ASNs_AFRINIC[cc_external]), percentage_external_AF2, 'AFRINIC'))
                                                                                     
                                        ori_dict['external_AFRINIC'][cc_external] = intersection2
                                                                                     
                                        total += percentage_external_AF
                                        total1 += len(intersection2)

                            else:
                                pass
                                                                                 
                        with open (filename1, 'a') as fg:
                            fg.write('%s;%s;%s\n'%('External AFRINIC ASNs', total1, total))



### RIPE NCC
                                                                                 
                        total = 0
                        total1 = 0
                        print "AFRINIC REGION DONE. LET'S MOVE TO RIPE"
                        for cc_region in CC_ASNs_RIPE:
                            print 'CCs in other regions'
                            if current_CC != cc_region:
                                if cc_region not in ori_dict['RIPE'].keys():
                                    print
                                    print 'length of ASNs in a cc_region', len(set(CC_ASNs_RIPE[cc_region]))
                                    intersection3 =  list(set(IXP_OriginASes[ixp]) & set(CC_ASNs_RIPE[cc_region]))
                                                                                 
                                    if len(intersection3) > 0:
                                        current_filename = output_folder +  'files_origin/RIPE_ASNs_' + ixp + '.txt'
                                        for elmt in intersection3 :
                                            with open(current_filename, 'a') as fd:
                                                fd.write('%s\n'%(elmt))
                                                                                 
                                    try:
                                        percentage_RIPE = float(len(intersection3))/float(len(Listrest_ASes))*100
                                    except:
                                        percentage_RIPE = 0.0
                                                                                 
                                    try:
                                        percentage_RIPE2 = float(len(intersection3))/float(len(CC_ASNs_RIPE[cc_region]))*100
                                    except:
                                        percentage_RIPE2 = 0.0
                                                                                 
                                    print 'length of intersection3:', len(intersection3)
                                    ori_dict['RIPE'][cc_region] = intersection3
                                    with open(filename, 'a') as fd:
                                        if len(intersection3)> 0:
                                            
                                            try:
                                                A = pycountry.countries.get(alpha2=cc_region)
                                                fd.write('%s;%s;%s;%s;%s;%s;%s;%s\n'%(cc_region, A.name, len(intersection3), len(Listrest_ASes), percentage_RIPE, len(CC_ASNs_RIPE[cc_region]), percentage_RIPE2, 'RIPE NCC'))
                                            except:
                                                fd.write('%s;%s;%s;%s;%s;%s;%s;%s\n'%(cc_region, '', len(intersection3), len(Listrest_ASes), percentage_RIPE, len(CC_ASNs_RIPE[cc_region]), percentage_RIPE2, 'RIPE NCC'))
                                         
                                         
                                    total += percentage_RIPE
                                    total1 += len(intersection3)

                            else:
                                print '----'
                                print 'cc coincides with another in other region which is:', cc_region
                                print '----'
                                
                                                                                 
                        with open (filename1, 'a') as fg:
                            fg.write('%s;%s;%s\n'%('RIPE ASNs', total1,  total))
    
#### ARIN

                        total = 0
                        total1 = 0
                        print "AFRINIC & RIPE REGION DONE. LET'S MOVE TO ARIN"
                        for cc_region in CC_ASNs_ARIN:
                            if current_CC != cc_region:
                                if cc_region not in ori_dict['ARIN'].keys():
                                    print
                                    print 'length of ASNs in a cc_region', len(set(CC_ASNs_ARIN[cc_region]))
                                    intersection5 =  list(set(IXP_OriginASes[ixp]) & set(CC_ASNs_ARIN[cc_region]))
                                
                                    if len(intersection5) > 0:
                                        current_filename = output_folder +  'files_origin/ARIN_ASNs_' + ixp + '.txt'
                                        for elmt in intersection5 :
                                            with open(current_filename, 'a') as fd:
                                                fd.write('%s\n'%(elmt))
                                            
                                    try:
                                        percentage_ARIN = float(len(intersection5))/float(len( Listrest_ASes ))*100
                                    except:
                                        percentage_ARIN = 0.0
                                            
                                    try:
                                        percentage_ARIN2 = float(len(intersection5))/float(len( CC_ASNs_ARIN[cc_region]))*100
                                    except:
                                        percentage_ARIN2 = 0.0
                                            
                                    print 'length of intersection5:', len(intersection5)
                                    ori_dict['ARIN'][cc_region] = intersection5
                                            
                                    with open(filename, 'a') as fd:
                                        if len(intersection5)> 0:
                                            try:
                                                A = pycountry.countries.get(alpha2=cc_region)
                                                fd.write('%s;%s;%s;%s;%s;%s;%s;%s\n'%(cc_region, A.name, len(intersection5), len( Listrest_ASes ), percentage_ARIN, len(CC_ASNs_ARIN[cc_region]), percentage_ARIN2, 'ARIN'))
                                            except:
                                                fd.write('%s;%s;%s;%s;%s;%s;%s;%s\n'%(cc_region, '', len(intersection5),  len( Listrest_ASes ), percentage_ARIN, len(CC_ASNs_ARIN[cc_region]), percentage_ARIN2, 'ARIN'))
                                        
                                        
                                    total += percentage_ARIN
                                    total1 += len(intersection5)


                            else:
                                print '----'
                                print 'cc coincides with another in other region which is:', cc_region
                                print '----'
                    
                    
                        with open (filename1, 'a') as fg:
                            fg.write('%s;%s;%s\n'%('ARIN ASNs', total1, total))


### APNIC

                        total = 0
                        total1 = 0
                        print "AFRINIC, RIPE & ARIN REGION DONE. LET'S MOVE TO APNIC"
                        for cc_region in CC_ASNs_APNIC:
                            if current_CC != cc_region:
                                if cc_region not in ori_dict['APNIC'].keys():
                                    print
                                    print 'length of ASNs in a cc_region', len(set(CC_ASNs_APNIC[cc_region]))
                                
                                    intersection4 =  list(set(IXP_OriginASes[ixp]) & set(CC_ASNs_APNIC[cc_region]))
                                    
                                    if len(intersection4) > 0:
                                        current_filename = output_folder + 'files_origin/APNIC_ASNs_' + ixp + '.txt'
                                        for elmt in intersection4 :
                                            with open(current_filename, 'a') as fd:
                                                fd.write('%s\n'%(elmt))
                                        
                                    try:
                                        percentage_APNIC = float(len(intersection4))/float(len( Listrest_ASes ))*100
                                    except:
                                        percentage_APNIC = 0.0
                                            
                                    try:
                                        percentage_APNIC2 = float(len(intersection4))/float(len( CC_ASNs_APNIC[cc_region] ))*100
                                    except:
                                        percentage_APNIC2 = 0.0
                                            
                                            
                                    print 'length of intersection4:', len(intersection4)
                                    ori_dict['APNIC'][cc_region] = intersection4
                                            
                                    with open(filename, 'a') as fd:
                                        if len(intersection4)>0:
                                            try:
                                                A = pycountry.countries.get(alpha2=cc_region)
                                                fd.write('%s;%s;%s;%s;%s;%s;%s;%s\n'%(cc_region, A.name, len(intersection4), len( Listrest_ASes), percentage_APNIC, len(CC_ASNs_APNIC[cc_region]), percentage_APNIC2, 'APNIC'))
                                            except:
                                                fd.write('%s;%s;%s;%s;%s;%s;%s;%s\n'%(cc_region,'', len(intersection4), len( Listrest_ASes), percentage_APNIC, len(CC_ASNs_APNIC[cc_region]), percentage_APNIC2, 'APNIC'))
                            
                                    total += percentage_APNIC
                                    total1 += len(intersection4)
                        
                            else:
                                print '----'
                                print 'cc coincides with another in other region which is:', cc_region
                                print '----'
            
                        with open (filename1, 'a') as fg:
                            fg.write('%s;%s;%s\n'%('APNIC ASNs', total1, total))



### LACNIC

                        total = 0
                        total1 = 0
                        print "AFRINIC, RIPE, ARIN & APNIC REGION DONE. LET'S MOVE TO LACNIC"
                        for cc_region in CC_ASNs_LACNIC:
                            if current_CC != cc_region:
                                if cc_region not in ori_dict['LACNIC'].keys():
                                    print
                                    print 'length of ASNs in a cc_region', len(set(CC_ASNs_LACNIC[cc_region]))
                                    intersection6 =  list(set(IXP_OriginASes[ixp]) & set(CC_ASNs_LACNIC[cc_region]))
                                    
                                    if len(intersection6) > 0:
                                        current_filename = output_folder + 'files_origin/LACNIC_ASNs_' + ixp + '.txt'
                                        for elmt in intersection6 :
                                            with open(current_filename, 'a') as fd:
                                                fd.write('%s\n'%(elmt))
                                        
                                    try:
                                        percentage_LACNIC = float(len(intersection6))/float(len( Listrest_ASes ))*100
                                    except:
                                        percentage_LACNIC = 0.0
                                            
                                    try:
                                        percentage_LACNIC2 = float(len(intersection6))/float(len(CC_ASNs_LACNIC[cc_region]))*100
                                    except:
                                        percentage_LACNIC2 = 0.0
                                            
                                    print 'length of intersection6:', len(intersection6)
                                    ori_dict['LACNIC'][cc_region] = intersection6
                                    with open(filename, 'a') as fd:
                                        if len(intersection6)>0:
                                            try:
                                                A = pycountry.countries.get(alpha2=cc_region)
                                                fd.write('%s;%s;%s;%s;%s;%s;%s;%s\n'%(cc_region, A.name, len(intersection6), len(Listrest_ASes), percentage_LACNIC, len(CC_ASNs_LACNIC[cc_region]), percentage_LACNIC2, 'LACNIC'))
                                            except:
                                                fd.write('%s;%s;%s;%s;%s;%s;%s;%s\n'%(cc_region,'', len(intersection6), len(Listrest_ASes), percentage_LACNIC, len(CC_ASNs_LACNIC[cc_region]), percentage_LACNIC2, 'LACNIC'))
                
                                    total += percentage_LACNIC
                                    total1 += len(intersection6)
                        
                            else:
                                print '----'
                                print 'cc coincides with another in other region which is:', cc_region
                                print '----'
                        
                        with open (filename1, 'a') as fg:
                            fg.write('%s;%s;%s\n'%('LACNIC ASNs', total1, total))




#print current_CC, ori_dict,
print


### store output into files
log_file_instance.write( str(now_datetime)+ ' End computation '+ '\n')
#create_output.close()
log_file_instance.close()


finish = open ('finish_lastmonth.txt', 'w')
finish.write('ended; ' + root_folder + output_folder[6:] + '; ' + now_datetime )
finish.close()

