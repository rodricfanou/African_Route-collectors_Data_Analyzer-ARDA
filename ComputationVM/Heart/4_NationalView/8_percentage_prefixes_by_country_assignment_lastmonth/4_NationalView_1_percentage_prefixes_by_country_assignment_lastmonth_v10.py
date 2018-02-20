##############################################################################
#__author__ = "Roderick Fanou"
#__email__ = "roderick.fanou@imdea.org"
#__status__ = "Production"
#__last_modifications__ =
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
from netaddr import *
import pycountry


def cidrsOverlap(cidr0, cidr1):
    return cidr0 in cidr1 or cidr1 in cidr0

## import all files in the library you need
sys.path.append('../../2_libraries/')
import ipaddress
import DB_configuration
import bgp_rib
from define_timescales import *
from functions import *


now_datetime = str(datetime.now()).replace(' ', '_')

finish = open ('finish_lastmonth_better.txt', 'w')
finish.write('started' + '; ' + now_datetime)
finish.close()

## Create a logfile:
name_log_file = 'Log_'+str(now_datetime) + '_' + 'National_View_1_percentage_prefixes_by_country_assignment_lastmonth_better' + '.txt'
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
region = DB_configuration.region
IXP_collector = {}
IXP_CC = {}
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
        IXP_CC[row[0]] = row[2]
    
    if row[2] not in CC_IXP.keys():
        CC_IXP[row[2]] = []

    if row[0] not in CC_IXP[row[2]]:
        CC_IXP[row[2]].append(row[0])
    
    IXP_collector[row[0]].append(row[1])
    i+=1

print IXP_collector
root_folder = '/home/roderick/Heart/'
output_folder = '../../Computation_outputs_National_View/8_percentage_prefixes_by_country_assignment_lastmonth_better/'



command = 'rm -rf ' + output_folder
os.system(command)

command = 'mkdir  ' + output_folder
os.system(command)

command = 'mkdir  -p ' + output_folder + 'List_prefixes_visibles_at_all_IXPs_of_a_country/'
os.system(command)

command = 'mkdir  -p ' + output_folder + 'List_prefixes_assigned_by_RIRs/'
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


query = "select distinct NetIPaddress, NetBits, CC from IPv4_ressources_AFRINIC where status = 'allocated' or status = 'assigned' and CC != '';"
cur.execute (query)
data = cur.fetchall()
i = 0


if len(data)>0:
    while (i<len(data)):
        row = data[i]
        asn = row[0]+'/'+row[1]
        current_CC = row[2]
        if current_CC != '':
            if current_CC not in CC_ASNs_AFRINIC.keys():
                CC_ASNs_AFRINIC[current_CC] = []
            
            if asn not in CC_ASNs_AFRINIC[current_CC]:
                CC_ASNs_AFRINIC[current_CC].append(asn)
        i += 1


pprint(CC_ASNs_AFRINIC)

filename_output_ASNs_by_AFRINIC = output_folder + 'Number_prefixes_assigned_by_Afrinic.txt'
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
week_prefix = {}


### splitted into weeks over the last month
#print lastMonthList[0][0], lastMonthList[0][1]


if len(List_all_tables) > 0:
    
    ### Using sliding period
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
    
    List_beg_end_each_week = [str(timestamp_one_month_before ) + '__' +   str(timestamp_now)  + '__'    + str(date_one_month_bef) + '  00:00:00__'  +  '__' +  str(date_now) + ' 00:00:00']
    
    print 'List_beg_end_each_week = ', List_beg_end_each_week
    
    print couples_year_month



    for ixp in IXP_collector.keys():
        
      CC_key = IXP_CC[ixp]
        
      if CC_key not in week_prefix.keys():
        week_prefix[CC_key] = []

      for window in couples_year_month:
    
        query = "select distinct Network  from Data__"+str(int(window[0]))+"_"+str(int(window[1])) + " where Timestamp >= %s and Timestamp <= %s  and ("
        
        k = 0
        while k < len(IXP_collector[ixp]) -1:
            k+=1
            query += " RouteCollector = %s or "
        
        query += " RouteCollector = %s)"

        print 'start_query :', datetime.now(), query
        print datetime.now(), 'week fetching data from ', ixp

        couple_timestamp = List_beg_end_each_week[0]

        list_variables = []
        tab = str(couple_timestamp).split('__')

        list_variables = [float(tab[0]), float(tab[1])] + IXP_collector[ixp]

        #if 1:
        #try:

        cur.execute(query, list_variables)
        
        log_file_instance.write(str(datetime.now())+ ' Fetching data from IXP '+ ixp + '\n')

        print 'Here is the query ', cur._executed
        data = cur.fetchall()

        print 'end_query :', datetime.now() #, data
        
        #except:
            #data = []

        i = 0

        if len(data)>0:
            
            while (i<len(data)):
                
                row = data[i]
                
                prefix = row[0]
                        
                if prefix not in week_prefix[CC_key]:
                            
                    week_prefix[CC_key].append(prefix)
                
                i+=1

    print ixp, 'len(week_prefix[CC_key]) = ' , len(week_prefix[CC_key])



## Saving week_ASNs in a file

for CC in week_prefix.keys():
    
    with open(output_folder + 'List_prefixes_visibles_at_all_IXPs_of_a_country/List_of_prefixes_visibles_in_IXPs_of_' + CC + '.txt', 'a') as fg:
        
        for elmt in week_prefix[CC]:
            
            fg.write('%s; %s\n' %(CC, elmt))



with open (output_folder + '/1_percentage_of_allocated_prefixes_seen_at_all_IXPs_of_each_country.txt', 'a') as fd:
    fd.write('%s; %s; %s; %s; %s\n'%('##Country', 'Number of Origin ASNs found', 'Common ASNs to Origin ASNs and Assigned ASNs ', 'ASNs Assigned by Afrinic',  'Percentage of Origin ASes at the IXP assigned by Afrinic'))
    fd.close()




### Compute the percentage of assigned prefixes by Afrinic that are seen at the ASN.

for cc in CC_IXP.keys():
    
    if cc in week_prefix.keys():
            
            print
            print 'Number of ASNs allocated to CC:', len(CC_ASNs_AFRINIC[cc])
            #print 'Number of Origin ASNs seen at the IXP:', len(list(set(week_prefix[ixp])))


            intersection = []
            rest = []
            
            for prefix_adv in week_prefix[ cc]:
                if prefix_adv != '0.0.0.0/0':
                    prefix_AF_adv = ipaddr.IPNetwork(str(prefix_adv))
                    for prefix_assigned in list(set(CC_ASNs_AFRINIC[cc])):
                        if prefix_assigned not in intersection and prefix_assigned != '0.0.0.0/0':
                            prefix_AF_assigned = ipaddr.IPNetwork(str(prefix_assigned))

                            if cidrsOverlap(prefix_AF_adv, prefix_AF_assigned):
                            #if prefix_AF_adv.overlaps(prefix_AF_assigned):
                                print 'Filling the file 1_percentage_of_allocated_prefixes_seen_at_all_IXPs_of_each_country.txt', prefix_AF_adv, ' overlaps ', prefix_AF_assigned
                                intersection.append(prefix_assigned)
        
        
            if '0.0.0.0/0' in intersection:
                intersection.remove('0.0.0.0/0')
                
            if '0.0.0.0/0' in CC_ASNs_AFRINIC[cc]:
                CC_ASNs_AFRINIC[cc].remove('0.0.0.0/0')
        
            rest = list(set(CC_ASNs_AFRINIC[cc]) - set(intersection))
            
            current_filename = output_folder + '/Prefix_assigned_to_country_seen_at_'+ cc+'.txt'
            
            if len(intersection) > 0:
                with open(current_filename, 'a') as fd:
                    for elmt in intersection :
                        fd.write('%s\n'%(elmt))
    
            current_filename = output_folder + '/Prefix_assigned_to_country_Not_seen_at_'+ cc+'.txt'
            if len(rest) > 0:
                with open(current_filename, 'a') as fd:
                    for elmt in rest :
                        fd.write('%s\n'%(elmt))

            percentage_found = 100*(float(len(intersection))/float(len(CC_ASNs_AFRINIC[cc])))
            print 'intersection ', len(intersection)
            print 'percentage in % for Prefixes: ', ixp, len(list(set(week_prefix[cc]))), len(intersection), len(CC_ASNs_AFRINIC[cc]), percentage_found
            
            with open (output_folder + '/1_percentage_of_allocated_prefixes_seen_at_all_IXPs_of_each_country.txt', 'a') as fd:
                fd.write('%s; %s; %s; %s; %s\n'%(ixp, len(list(set(week_prefix[cc]))), len(intersection), len(CC_ASNs_AFRINIC[cc]), percentage_found))
                fd.close()




## connect to the DB
Current_db = 'RIRs'
db = MySQLdb.connect(host = DB_configuration.host, user = DB_configuration.user, passwd = DB_configuration.passwd, db = Current_db)
cur = db.cursor()
print 'Connected'


##Check that the dictionary is full as it should
##LET'S DO A DICTIONARY OF prefixes per continent
CC_ASNs_RIPE = {}
CC_ASNs_ARIN = {}
CC_ASNs_LACNIC = {}
CC_ASNs_APNIC = {}



query = "select distinct NetIPaddress, NetBits, CC from IPv4_ressources_RIPE where status = 'allocated' or status = 'assigned';"
cur.execute (query)
#print CC
#print query
data = cur.fetchall()
i = 0
if len(data)>0:
    while (i<len(data)):
        row = data[i]
        asn = row[0]+'/'+row[1] #type string
        CC = row[2]
        if CC not in CC_ASNs_RIPE.keys() and CC != '':
            CC_ASNs_RIPE[CC] = []
    
        if asn not in CC_ASNs_RIPE[CC]:
            CC_ASNs_RIPE[CC].append(asn)
        i +=1

print 'CC at RIPE', CC_ASNs_RIPE.keys()
print



##TAKE CARE HERE: just assigned. not allocated.
query = "select distinct NetIPaddress, NetBits, CC from IPv4_ressources_ARIN where status = 'allocated' or status = 'assigned';"
cur.execute (query)
#print CC
#print query
data = cur.fetchall()
i = 0
#print data
#print
if len(data)>0:
    while (i<len(data)):
        row = data[i]
        asn = row[0]+'/'+row[1] #type string
        CC = row[2]
        if CC not in CC_ASNs_ARIN.keys() and CC != '':
            CC_ASNs_ARIN[CC] = []
    
        if asn not in CC_ASNs_ARIN[CC]:
            CC_ASNs_ARIN[CC].append(asn)
        i +=1

print 'CC at ARIN', CC_ASNs_ARIN.keys()
print



query = "select distinct NetIPaddress, NetBits, CC from IPv4_ressources_APNIC where status = 'allocated' or status = 'assigned';"
cur.execute (query)
#print CC
#print query
data = cur.fetchall()
i = 0
#print data
#print
if len(data)>0:
    while (i<len(data)):
        row = data[i]
        asn = row[0]+'/'+row[1] #type string
        CC = row[2]
        if CC not in CC_ASNs_APNIC.keys() and CC != '':
            CC_ASNs_APNIC[CC] = []
        if asn not in CC_ASNs_APNIC[CC]:
            CC_ASNs_APNIC[CC].append(asn)
        i +=1
print  'CC at APNIC',CC_ASNs_APNIC.keys()
print



query = "select distinct NetIPaddress, NetBits, CC from IPv4_ressources_LACNIC where status = 'allocated' or status = 'assigned';"
cur.execute (query)
#print CC
#print query
data = cur.fetchall()
i = 0
#print data
#print
if len(data)>0:
    while (i<len(data)):
        row = data[i]
        asn = row[0]+'/'+row[1] #type string
        CC = row[2]
        
        if CC not in CC_ASNs_LACNIC.keys() and CC != '':
            CC_ASNs_LACNIC[CC] = []
        if asn not in CC_ASNs_LACNIC[CC]:
            CC_ASNs_LACNIC[CC].append(asn)
        i +=1

print 'CC at LACNIC',  CC_ASNs_LACNIC.keys()






### Dropping the list of ASNs assigned by each RIR in a file

with open(output_folder + 'List_prefixes_assigned_by_RIRs/List_prefixes_assigned_by_AFRINIC.txt', 'a') as fgh:
    
    for CC in CC_ASNs_AFRINIC.keys():
        
        for elmt in CC_ASNs_AFRINIC[CC]:
            
            fgh.write('%s; %s\n' %(CC, str(elmt)))



with open(output_folder + 'List_prefixes_assigned_by_RIRs/List_prefixes_assigned_by_LACNIC.txt', 'a') as fgh:
    
    for CC in CC_ASNs_LACNIC.keys():
        
        for elmt in CC_ASNs_LACNIC[CC]:
            
            fgh.write('%s; %s\n' %(CC, str(elmt)))



with open(output_folder + 'List_prefixes_assigned_by_RIRs/List_prefixes_assigned_by_RIPE.txt', 'a') as fgh:
    
    for CC in CC_ASNs_RIPE.keys():
        
        for elmt in CC_ASNs_RIPE[CC]:
            
            fgh.write('%s; %s\n' %(CC, str(elmt)))



with open(output_folder + 'List_prefixes_assigned_by_RIRs/List_prefixes_assigned_by_ARIN.txt', 'a') as fgh:
    
    for CC in CC_ASNs_ARIN.keys():
        
        for elmt in CC_ASNs_ARIN[CC]:
            
            fgh.write('%s; %s\n' %(CC, str(elmt)))



with open(output_folder + 'List_prefixes_assigned_by_RIRs/List_prefixes_assigned_by_APNIC.txt', 'a') as fgh:
    
    for CC in CC_ASNs_APNIC.keys():
        
        for elmt in CC_ASNs_APNIC[CC]:
            
            fgh.write('%s; %s\n' %(CC, str(elmt)))








#### Classify by type of Origin AS
##### Classifying them into local or external

command = 'mkdir  ' + output_folder + 'files_prefixes/'
os.system(command)

update = 0

IXP_OriginASes = {}

IXP_OriginASes = copy.deepcopy(week_prefix)

### compute the percentage of assigned ASes by Afrinic that are origin ASes.


for CC_key in IXP_OriginASes.keys():
    
    print
    print
    
    ori_dict = {}
    ori_dict['RIPE'] = {}
    ori_dict['external_AFRINIC'] = {}
    ori_dict['local_AFRINIC'] = {}
    ori_dict['LACNIC'] = {}
    ori_dict['APNIC'] = {}
    ori_dict['ARIN'] = {}
    ori_dict['PRIVATE'] = []
    ori_dict['RESERVED'] =[]
    
    filename = output_folder + 'Percentage_prefixes_by_country_assignment_' + CC_key + '.txt'
    filename1 = output_folder + 'Percentage_prefixes_by_region_' + CC_key + '.txt'
    
    
    with open(filename, 'a') as fd:
        fd.write('%s;%s;%s;%s;%s;%s;%s\n'%('##Current_CC', 'Country name', 'Intersection visible prefixes & prefixes assigned to the country', 'num prefixes seen at the IXP', 'Percentage_local_AF', 'num prefixes assigned by Afrinic to the CC', 'Percentage_local_AF2' ))
    
    with open (filename1, 'a') as fg:
        fg.write('%s;%s;%s\n'%('##Type of ASNs (Region)', 'len_prefixes_Type', 'percentage_type'))
    
    for CC in CC_IXP.keys():
        
        if CC == CC_key:
        
                current_CC = CC
                print

                ## Listrest_ASes contains allthe prefixes corresponding to that country found in the database
                Listrest_ASes = copy.deepcopy(IXP_OriginASes[current_CC])
            
                ## Local: Allows to find all prefixes that are local to AFRINIC and the country found in the advertised prefixes; here we just consider exact prefixes advertised. What $
                intersection = list(set(IXP_OriginASes[current_CC]) & set(CC_ASNs_AFRINIC[current_CC]))

                if len(intersection) > 0:
                    current_filename =  output_folder + 'files_prefixes/Local_AFRINIC_prefixes_' + current_CC + '.txt'
                    for elmt in intersection :
                        with open(current_filename, 'a') as fd:
                            fd.write('%s\n'%(elmt))


                for prefix_adv in list(set(IXP_OriginASes[current_CC])):
                    if prefix_adv != '0.0.0.0/0' and 'None' not in prefix_adv:
                        prefix_AF_adv = ipaddr.IPNetwork(str(prefix_adv))
                        for prefix_assigned in list(set(CC_ASNs_AFRINIC[current_CC])):
                            
                            if prefix_assigned not in intersection and prefix_assigned != '0.0.0.0/0':
                                prefix_AF_assigned = ipaddr.IPNetwork(str(prefix_assigned))
                                
                                if cidrsOverlap(prefix_AF_adv, prefix_AF_assigned):
                                #if prefix_AF_adv.overlaps(prefix_AF_assigned):
                                    print prefix_AF_adv, ' overlaps ', prefix_AF_assigned
                                    intersection.append(prefix_assigned)



                if '0.0.0.0/0' in intersection:
                    intersection.remove('0.0.0.0/0')
                
                if  '0.0.0.0/0' in CC_ASNs_AFRINIC[current_CC]:
                    CC_ASNs_AFRINIC[current_CC].remove('0.0.0.0/0')
                
                if '0.0.0.0/0' in IXP_OriginASes[current_CC]:
                    IXP_OriginASes[current_CC].remove('0.0.0.0/0')


                try:
                    percentage_local_AF = 100*(float(len(intersection))/float(len(Listrest_ASes)))
                except:
                    percentage_local_AF = 0.0
            
                print 'percentage_local_AF =', percentage_local_AF
                ori_dict['local_AFRINIC'] = {current_CC: intersection}


                ## Percentage of ASNs allocated to the country visibles at the IXP
                try:
                    percentage_local_AF2 = 100*(float(len(intersection))/float(len( CC_ASNs_AFRINIC[current_CC] )))
                except:
                    percentage_local_AF2 = 0.0
            
            
                with open(filename, 'a') as fd:
                    if len(intersection) >0:
                        try:
                            A = pycountry.countries.get(alpha2=current_CC)
                            fd.write('%s;%s;%s;%s;%s;%s;%s\n'%(current_CC, A.name, len(intersection), len(IXP_OriginASes[current_CC]), percentage_local_AF, len( CC_ASNs_AFRINIC[current_CC] ), percentage_local_AF2))
                        
                        except:
                            fd.write('%s;%s;%s;%s;%s;%s;%s\n'%(current_CC, '', len(intersection), len(IXP_OriginASes[current_CC]), percentage_local_AF, len(CC_ASNs_AFRINIC[current_CC]), percentage_local_AF2 ))


                print 'local_AFRINIC =', percentage_local_AF

                with open (filename1, 'a') as fg:
                    fg.write('%s;%s;%s\n'%('Local AFRINIC prefixes', len(intersection), percentage_local_AF))


###### AFRINIC

                total = 0
                total1 = 0
                
                #for cc_external in CC_IXP.keys():
                for cc_external in CC_ASNs_AFRINIC.keys():
            
                    print 'external cc in AFRINIC region to make intersection with the local ASNs:', cc_external
            
                    if current_CC != cc_external:
                        if cc_external not in ori_dict['external_AFRINIC'].keys():
                            
                          if cc_external in IXP_OriginASes.keys() :
                            print 'length of ASNs in a cc_external', cc_external , ' = ', len(set(CC_ASNs_AFRINIC[cc_external]))
                            intersection2 = []

                        
                            for prefix_adv in list(set(IXP_OriginASes[current_CC])):
                                if prefix_adv != '0.0.0.0/0' and 'None' not in prefix_adv:
                                    prefix_AF_adv = ipaddr.IPNetwork(str(prefix_adv))
                                    for prefix_assigned in list(set(CC_ASNs_AFRINIC[cc_external])):
                                        if prefix_assigned not in intersection2 and prefix_assigned != '0.0.0.0/0':
                                            prefix_AF_assigned = ipaddr.IPNetwork(str(prefix_assigned))
                                            if cidrsOverlap(prefix_AF_adv, prefix_AF_assigned):
                                            #if prefix_AF_adv.overlaps(prefix_AF_assigned):
                                                print prefix_AF_adv, ' overlaps ', prefix_AF_assigned
                                                intersection2.append(prefix_assigned)



                            if '0.0.0.0/0' in intersection2:
                                intersection2.remove('0.0.0.0/0')
        
                            if '0.0.0.0/0' in CC_ASNs_AFRINIC[cc_external]:
                                CC_ASNs_AFRINIC[cc_external].remove('0.0.0.0/0')
                
                            if '0.0.0.0/0' in IXP_OriginASes[current_CC]:
                                IXP_OriginASes[current_CC].remove('0.0.0.0/0')
                            

                            if len(intersection2) > 0:
                                current_filename = output_folder +  'files_prefixes/External_AFRINIC_prefixes_' + cc_external + '.txt'
                                for elmt in intersection2 :
                                    with open(current_filename, 'a') as fd:
                                        fd.write('%s\n'%(elmt))
                            
                        
                            try:
                                percentage_external_AF = 100*(float(len(intersection2))/float(len( Listrest_ASes)))
                            except:
                                percentage_external_AF = 0.0
                                        
                            print 'percentage_external_AF =', percentage_external_AF
                                            
                            print 'length of intersection2:', len(intersection2)
                                            
                            try:
                                percentage_external_AF2 = 100*(float(len(intersection2))/float(len(CC_ASNs_AFRINIC[cc_external])))
                            except:
                                percentage_external_AF2 = 0.0

                              
                            with open(filename, 'a') as fd:
                                if len(intersection2) > 0:
                                    try:
                                        
                                        A = pycountry.countries.get(alpha2=cc_external)
                                        fd.write('%s;%s;%s;%s;%s;%s;%s\n'%(cc_external, A.name , len(intersection2), len(IXP_OriginASes[current_CC]), percentage_external_AF, len(CC_ASNs_AFRINIC[cc_external]),  percentage_external_AF2))
                                    
                                    except:
                                        fd.write('%s;%s;%s;%s;%s;%s;%s\n'%(cc_external, '' , len(intersection2), len(IXP_OriginASes[current_CC]), percentage_external_AF, len(CC_ASNs_AFRINIC[cc_external]),  percentage_external_AF2))
                              
                            ori_dict['external_AFRINIC'][current_CC] = intersection2
                              
                            total += percentage_external_AF
                            total1 += len(intersection2)
                                                                                                              
                                                                                                              
                    else:
                        pass
                              
                with open (filename1, 'a') as fg:
                    fg.write('%s;%s;%s\n'%('External AFRINIC prefixes', total1, total))




sys.exit()

if 1:
    
###### I AM HERE !!

###### RIPE

                total = 0
                total1 = 0
                print "AFRINIC REGION DONE. LET'S MOVE TO RIPE"
                for cc_region in CC_ASNs_RIPE:
                    print 'CCs in other regions'
                    if current_CC != cc_region:
                            if cc_region not in ori_dict['RIPE'].keys():
                                print
                                print 'length of ASNs in a cc_region', len(set(CC_ASNs_RIPE[cc_region]))
                                intersection3 =  []
                                
                                for prefix_adv in list(set(IXP_OriginASes[current_CC])):
                                    if prefix_adv != '0.0.0.0/0' and 'None' not in prefix_adv:
                                        prefix_AF_adv  = ipaddr.IPNetwork(str(prefix_adv))
                                        for prefix_assigned in list(set(CC_ASNs_RIPE[cc_region])):
                                            if prefix_assigned not in intersection3 and prefix_assigned != '0.0.0.0/0':
                                                prefix_AF_assigned = ipaddr.IPNetwork(str(prefix_assigned))
                                                
                                                if cidrsOverlap(prefix_AF_adv, prefix_AF_assigned):
                                                #if prefix_AF_adv.overlaps(prefix_AF_assigned):
                                                    print prefix_AF_adv, ' overlaps ', prefix_AF_assigned
                                                    intersection3.append(prefix_assigned)
                            
                                if '0.0.0.0/0' in intersection3:
                                    intersection3.remove('0.0.0.0/0')
                        
                                if  '0.0.0.0/0' in CC_ASNs_RIPE[cc_region]:
                                    CC_ASNs_RIPE[cc_region].remove('0.0.0.0/0')

                                if '0.0.0.0/0' in IXP_OriginASes[current_CC]:
                                    IXP_OriginASes[current_CC].remove('0.0.0.0/0')
                                
                                
                                if len(intersection3) > 0:
                                    current_filename = output_folder +  'files_prefixes/RIPE_prefixes_' + cc_region + '.txt'
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
                                    #if len(intersection3)> 0:
                                    try:
                                        A = pycountry.countries.get(alpha2=cc_region)
                                        fd.write('%s;%s;%s;%s;%s;%s;%s\n'%(cc_region, A.name, len(intersection3), len(IXP_OriginASes[current_CC]), percentage_RIPE, len(CC_ASNs_RIPE[cc_region]),  percentage_RIPE2))
                                    except:
                                        fd.write('%s;%s;%s;%s;%s;%s;%s\n'%(cc_region, '', len(intersection3), len(IXP_OriginASes[current_CC]), percentage_RIPE, len(CC_ASNs_RIPE[cc_region]), percentage_RIPE2))
                                    
                                total += percentage_RIPE
                                total1 += len(intersection3)

                    else:
                        print '----'
                        print 'cc coincides with another in other region which is:', cc_region
                        print '----'
                                
                    
                with open (filename1, 'a') as fg:
                    fg.write('%s;%s;%s\n'%('RIPE prefixes', total1,  total))




###### ARIN

                total = 0
                total1 = 0
                print "AFRINIC & RIPE REGION DONE. LET'S MOVE TO ARIN"
                for cc_region in CC_ASNs_ARIN:
                    if current_CC != cc_region:
                        if cc_region not in ori_dict['ARIN'].keys():
                            print
                            print 'length of ASNs in a cc_region', len(set(CC_ASNs_ARIN[cc_region]))
                            intersection5 =  []
                        
                            for prefix_adv in list(set(IXP_OriginASes[cc_region])):
                                if prefix_adv != '0.0.0.0/0' and 'None' not in prefix_adv:
                                    prefix_AF_adv = ipaddr.IPNetwork(str(prefix_adv))
                                    for prefix_assigned in list(set(CC_ASNs_ARIN[cc_region])):
                                        if prefix_assigned not in intersection5 and prefix_assigned != '0.0.0.0/0':
                                            prefix_AF_assigned = ipaddr.IPNetwork(str(prefix_assigned))
                                            
                                            if cidrsOverlap(prefix_AF_adv, prefix_AF_assigned):
                                            #if prefix_AF_adv.overlaps(prefix_AF_assigned):
                                                print prefix_AF_adv, ' overlaps ', prefix_AF_assigned
                                                intersection5.append(prefix_assigned)
                                            
                                            
                            if '0.0.0.0/0' in intersection5:
                                intersection5.remove('0.0.0.0/0')
                                                    
                            if '0.0.0.0/0' in CC_ASNs_ARIN[cc_region]:
                                CC_ASNs_ARIN[cc_region].remove('0.0.0.0/0')
                            
                            if '0.0.0.0/0' in IXP_OriginASes[cc_region]:
                                IXP_OriginASes[cc_region].remove('0.0.0.0/0')
                            
                            
                            
                            if len(intersection5) > 0:
                                current_filename = output_folder + 'files_prefixes/ARIN_prefixes_' + cc_region + '.txt'
                                for elmt in intersection5 :
                                    with open(current_filename, 'a') as fd:
                                        fd.write('%s\n'%(elmt))


                            try:
                                percentage_ARIN = float(len(intersection5))/float(len(Listrest_ASes))*100
                            except:
                                percentage_ARIN = 0.0
                
                            try:
                                percentage_ARIN2 = float(len(intersection5))/float(len( CC_ASNs_ARIN[cc_region]))*100
                            except:
                                percentage_ARIN2 = 0.0
                                
                            print 'length of intersection5:', len(intersection5)
                            ori_dict['ARIN'][cc_region] = intersection5
                                        
                            with open(filename, 'a') as fd:
                                if len(intersection5) > 0:
                                    try:
                                        A = pycountry.countries.get(alpha2=cc_region)
                                        fd.write('%s;%s;%s;%s;%s;%s;%s\n'%(cc_region, A.name, len(intersection5), len(IXP_OriginASes[current_CC]), percentage_ARIN, len( CC_ASNs_ARIN[cc_region]), percentage_ARIN2))
                                    except:
                                        fd.write('%s;%s;%s;%s;%s;%s;%s\n'%(cc_region, '', len(intersection5) , len(IXP_OriginASes[current_CC]) , percentage_ARIN, len( CC_ASNs_ARIN[cc_region]), percentage_ARIN2))
                                    
                                    
                            total += percentage_ARIN
                            total1 += len(intersection5)
                
                    else:
                            print '----'
                            print 'cc coincides with another in other region which is:', cc_region
                            print '----'
                            pass
                
                
                with open (filename1, 'a') as fg:
                    fg.write('%s;%s;%s\n'%('ARIN prefixes', total1, total))



###### APNIC

                total = 0
                total1 = 0
                print "AFRINIC, RIPE & ARIN REGION DONE. LET'S MOVE TO APNIC"
                for cc_region in CC_ASNs_APNIC:
                    if current_CC != cc_region:
                        if cc_region not in ori_dict['APNIC'].keys():
                            print
                            print 'length of ASNs in a cc_region', len(set(CC_ASNs_APNIC[cc_region]))
                                
                            intersection4 = []
                                    
                            if len(intersection4) > 0:
                                current_filename = output_folder + 'files_prefixes/APNIC_prefixes_' + cc_region + '.txt'
                                for elmt in intersection4 :
                                    with open(current_filename, 'a') as fd:
                                        fd.write('%s\n'%(elmt))
                        
                        
                            for prefix_adv in list(set(IXP_OriginASes[cc_region])):
                                if prefix_adv != '0.0.0.0/0' and 'None' not in prefix_adv:
                                    prefix_AF_adv = ipaddr.IPNetwork(str(prefix_adv))
                                    for prefix_assigned in list(set(CC_ASNs_APNIC[cc_region])):
                                        if prefix_assigned not in intersection3 and prefix_assigned != '0.0.0.0/0':
                                            prefix_AF_assigned = ipaddr.IPNetwork(str(prefix_assigned))
                                            
                                            if cidrsOverlap(prefix_AF_adv, prefix_AF_assigned):
                                            #if prefix_AF_adv.overlaps(prefix_AF_assigned):
                                                print prefix_AF_adv, ' overlaps ', prefix_AF_assigned
                                                intersection4.append(prefix_assigned)
                                
                            
                            if '0.0.0.0/0' in intersection4:
                                intersection4.remove('0.0.0.0/0')

                            if '0.0.0.0/0' in CC_ASNs_APNIC[cc_region]:
                                CC_ASNs_APNIC[cc_region].remove('0.0.0.0/0')
                            
                            if '0.0.0.0/0' in IXP_OriginASes[cc_region]:
                                IXP_OriginASes[cc_region].remove('0.0.0.0/0')
        
        
                            try:
                                percentage_APNIC = float(len(intersection4))/float(len(Listrest_ASes ))*100
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
                                        fd.write('%s;%s;%s;%s;%s;%s;%s\n'%(cc_region, A.name, len(intersection4), len(IXP_OriginASes[current_CC]), percentage_APNIC, len( CC_ASNs_APNIC[cc_region] ),  percentage_APNIC2))
                                    except:
                                        fd.write('%s;%s;%s;%s;%s;%s;%s\n'%(cc_region,'', len(intersection4), len(IXP_OriginASes[current_CC]) , percentage_APNIC, len(CC_ASNs_APNIC[cc_region] ), percentage_APNIC2))
                                    
                                    total += percentage_APNIC
                                    total1 += len(intersection4)
                        
                    else:
                            print '----'
                            print 'cc coincides with another in other region which is:', cc_region
                            print '----'

            
                with open (filename1, 'a') as fg:
                    fg.write('%s;%s;%s\n'%('APNIC prefixes', total1, total))




###### LACNIC

                total = 0
                total1 = 0
                print "AFRINIC, RIPE, ARIN & APNIC REGION DONE. LET'S MOVE TO LACNIC"
                for cc_region in CC_ASNs_LACNIC:
                    if current_CC != cc_region:
                        if cc_region not in ori_dict['LACNIC'].keys():
                            print
                            print 'length of ASNs in a cc_region', len(set(CC_ASNs_LACNIC[cc_region]))
                            intersection6 = []
                            
                            if len(intersection6) > 0:
                                current_filename = output_folder + 'files_prefixes/LACNIC_prefixes_' + cc_region + '.txt'
                                for elmt in intersection6 :
                                    with open(current_filename, 'a') as fd:
                                        fd.write('%s\n'%(elmt))

                            for prefix_adv in list(set(IXP_OriginASes[cc_region])):
                                if prefix_adv != '0.0.0.0/0' and 'None' not in prefix_adv:
                                    prefix_AF_adv  = ipaddr.IPNetwork(str(prefix_adv))
                                    for prefix_assigned in list(set(CC_ASNs_LACNIC[cc_region])):
                                        if prefix_assigned not in intersection3 and prefix_assigned != '0.0.0.0/0':
                                            prefix_AF_assigned = ipaddr.IPNetwork(str(prefix_assigned))
                                            
                                            if cidrsOverlap(prefix_AF_adv, prefix_AF_assigned):
                                            #if prefix_AF_adv.overlaps(prefix_AF_assigned):
                                                print prefix_AF_adv, ' overlaps ', prefix_AF_assigned
                                                intersection6.append(prefix_assigned)
                            
                                    
                                
                            if '0.0.0.0/0' in intersection6:
                                intersection6.remove('0.0.0.0/0')
                                    
                            if '0.0.0.0/0' in CC_ASNs_LACNIC[cc_region]:
                                CC_ASNs_LACNIC[cc_region].remove('0.0.0.0/0')
                            
                            if '0.0.0.0/0' in IXP_OriginASes[cc_region]:
                                IXP_OriginASes[cc_region].remove('0.0.0.0/0')
                                    
                                    
                            try:
                                percentage_LACNIC = float(len(intersection6))/float(len( IXP_OriginASes[cc_region]))*100
                            except:
                                percentage_LACNIC= 0.0


                            try:
                                percentage_LACNIC2 = float(len(intersection6))/float(len( CC_ASNs_LACNIC[cc_region]))*100
                            except:
                                percentage_LACNIC2 = 0.0


                
                            print 'length of intersection6:', len(intersection6)
                            ori_dict['LACNIC'][cc_region] = intersection6
                            with open(filename, 'a') as fd:
                                if len(intersection6)>0:
                                    try:
                                        A = pycountry.countries.get(alpha2=cc_region)
                                        fd.write('%s;%s;%s;%s;%s;%s;%s\n'%(cc_region, A.name, len(intersection6), len(IXP_OriginASes[current_CC]), percentage_LACNIC, len(CC_ASNs_LACNIC[cc_region]), percentage_LACNIC2))
                                    except:
                                        fd.write('%s;%s;%s;%s;%s;%s;%s\n'%(cc_region,'', len(intersection6), len(IXP_OriginASes[current_CC]), percentage_LACNIC, len(CC_ASNs_LACNIC[cc_region]), percentage_LACNIC2))
                                            
                                    total += percentage_LACNIC
                                    total1 += len(intersection6)
                        
                        else:
                            print '----'
                            print 'cc coincides with another in other region which is:', cc_region
                            print '----'
                                
            
                    print current_CC, ori_dict,
                    print

                with open (filename1, 'a') as fg:
                    fg.write('%s;%s;%s\n'%('LACNIC prefixes', total1, total))



finish = open ('finish_lastmonth_better.txt', 'w')
finish.write('ended' + '; ' +  root_folder + output_folder[6:]+ '; ' + now_datetime)
finish.close()


