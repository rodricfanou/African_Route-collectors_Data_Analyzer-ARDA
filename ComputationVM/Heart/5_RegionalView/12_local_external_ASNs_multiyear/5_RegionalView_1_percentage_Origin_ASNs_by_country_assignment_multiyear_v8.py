#1st graph : We keep the pie chart in the application (added below), but we compute
#it only for last month, and consider distinct ASNs as defined in point 2.

##############################################################################
#__author__ = "Roderick Fanou"
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
#from time import sleep
from collections import Counter
import select, socket
import urllib2, urllib
import GeoIP
import ipaddr, logging
import gzip
from datetime import date
from datetime import datetime, timedelta
import pycountry
import datetime
import time

from netaddr import *

## import all files in the library you need
sys.path.append('../../2_libraries/')
import ipaddress
import DB_configuration
import bgp_rib
from define_timescales import *
from functions import *



now_datetime = str(datetime.now()).replace(' ', '_')

finish = open ('finish_multiyear.txt', 'w')
finish.write('started; ' + now_datetime )
finish.close()

## Create a logfile:
name_log_file = 'Log_'+str(now_datetime) + '_' + '5_RegionalView_1_Number_Origin_ASNs_visible_at_an_IXP_multiyear.txt'
location_logfile = create_Logfiles_folder()

### Define timelines and timescales
## multi-years splitted into years
yearList = multiyear()
yearList.sort()
print yearList

## last month (Now - 4weeks) splitted into weeks
lastYearList = lastyear()
print lastYearList
lastYearList.sort()

## last month (Now - 4weeks) splitted into weeks
lastMonthList = lastmonth()
print lastMonthList
lastMonthList.sort()


## Other initialisations
continent = 'AF'
IXP_collector = {}
IXP_CC = {}
region = 'AFRINIC'
CC_ASNs_AFRINIC = {}
CC_IXP = {}



## connect to the DB
Current_db = 'MergedData'
db = MySQLdb.connect(host="localhost",user="",passwd="",  db = Current_db)
cur = db.cursor()
print 'Connected'

query = "select IXP, RouteCollector, CC from AllRouteCollectors where Continent = '"+continent+"';"
cur.execute(query)
data = cur.fetchall()


i = 0
while (i<len(data)):
    row = data[i]
    if row[2] not in CC_IXP.keys():
        CC_IXP[row[2]] = []
    
    if row[0] not in IXP_collector.keys():
        IXP_collector[row[0]] = []
        IXP_CC[row[0]]= row[2]
    
    if row[0] not in CC_IXP[row[2]]:
        CC_IXP[row[2]].append(row[0])
    
    IXP_collector[row[0]].append(row[1])
    i+=1


print IXP_collector
root_folder = '/home/African_Route-collectors_Data_Analyzer-ARDA/ComputationVM/Heart/'

output_folder = '../../Computation_outputs_Regional_View/12_local_external_ASNs_multiyear/'

output_folder_IXP_View = '../../Computation_outputs/12_local_external_ASNs_multiyear/'

command = 'rm -rf ' + output_folder
os.system(command)

command = 'mkdir  ' + output_folder
os.system(command)

command = 'chmod 777 ' + output_folder
os.system(command)

filename = output_folder



#### What has AFRINIC attributed till now
### Query RIRs database

## fetch all distinct prefixes corresponding to each routecollector in each IXP list contained in the
## dictionnary IXP_collector
log_file_instance = open(location_logfile+'/'+name_log_file, 'a')


## Initialisation
Current_db = 'MergedData'
db = MySQLdb.connect(host = DB_configuration.host, user = DB_configuration.user, passwd= DB_configuration.passwd,  db = Current_db)
cur = db.cursor()
### splitted into weeks over the last month
#print lastMonthList[0][0], lastMonthList[0][1]



###Current list of all tables;
query = "SHOW TABLES LIKE 'Data__%%' "
cur.execute (query)
data = cur.fetchall()
List_all_tables = []
if len(data)>0:
    for elmt in data:
        List_all_tables.append(elmt[0])


if len(List_all_tables) > 0:
    
    year_ASN = {}
    
    for ixp in IXP_collector.keys():
        
        Current_country_ixp = IXP_CC[ixp]
        
        log_file_instance = open(location_logfile+'/'+name_log_file, 'a')
        
        if 'Region' not in year_ASN.keys():
            year_ASN['Region'] = {}

        for year in yearList:

            if year not in year_ASN['Region'].keys():
                year_ASN['Region'][year] = []
        
            for month in xrange(1,13):
                
                if 'Data__' + str(year) + "_" + str(month) in List_all_tables:
                    print
                    print
                    #print IXP_collector[ixp]

                    k = 0
                    query = "select distinct OriginAS, ASPath from Data__"+str(year)+"_"+str(month) + " where"
                    while k < len(IXP_collector[ixp]) -1:
                        k+=1
                        query += " RouteCollector = %s or "
                    
                    query += " RouteCollector = %s and (OriginAS != 'None' and OriginAS is not NULL and OriginAS != 'NULL')"
                    
                    print 'start_query :', datetime.now(), query
                    print
                    print datetime.now(), 'fetching data from ', ixp

                    cur.execute(query, IXP_collector[ixp])
                    
                    log_file_instance.write(str(now_datetime)+ 'Last year Fetching data from IXP '+ Current_country_ixp + '\n')
                    
                    print 'Here is the query ', cur._executed
                    data = cur.fetchall()
                    print
                    print 'end_query :', datetime.now() #, data
                    i = 0
                    
                    print "we found data of length ", len(data)
                    
                    if len(data) > 0:
                        
                        while (i<len(data)):
                            
                            row = data[i]
                            
                            OriginASNs = []
                            
                            ## Extract the origin AS
                            if '{' not in row[0] and ',' not in row[0] and '}' not in row[0] and row[0] != '':
                                
                                try:
                                    OriginASNs.append(int(str(row[0]).strip()))
                                
                                except:
                                    print 'Case 1: Alert We pass for this path ', row[1]
                        
                            else:
                                
                                path = row[1].split(' ')
                                
                                try:
                                    OriginASNs.append(int(str(path[-2]).strip()))
                                    #print row[1], '; ',  row[0], '; ', int(path[-2])
                                    
                                except:
                                    print 'Case 2: Alert We pass for this path ', row[1]
                    
                    
                            for OriginASNs_elmt in OriginASNs :
                                
                                if OriginASNs_elmt  not in year_ASN['Region'][year]:
                                    year_ASN['Region'][year].append(OriginASNs_elmt)
                                
                            
                            i += 1
                                
                    else:
                        print 'No prefix found for ', Current_country_ixp, ' in ' , 'Data__'+str(year)+'_'+str(month)


pprint(year_ASN)






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
        #print row
        asn = row[0] #type string
        current_CC = row[1]
        
        if '.' in asn: #conversion to 2Byte format
            #print '4B format:',asn
            tab = asn.split('.')
            asn = int(tab[0])*65536 + int(tab[1])
        
        asn = int(asn) #format int
        if 'Region' not in  CC_ASNs_AFRINIC.keys() and current_CC != '' :
            CC_ASNs_AFRINIC['Region'] = []
        
        if asn not in CC_ASNs_AFRINIC['Region']:
            CC_ASNs_AFRINIC['Region'].append(asn)

        i +=1


pprint(CC_ASNs_AFRINIC)




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
        if 'Region' not in CC_ASNs_RIPE.keys() and CC != '':
            CC_ASNs_RIPE['Region'] = []
        if '.' in asn: #conversion to 2Byte format
            asn = int(asn[:asn.find('.')])*65536 + int(asn[asn.find('.')+1:])
        asn = int(asn) #format int
        if asn not in CC_ASNs_RIPE['Region']:
            CC_ASNs_RIPE['Region'].append(asn)
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
        if 'Region' not in CC_ASNs_ARIN.keys() and CC != '':
            CC_ASNs_ARIN['Region'] = []
        if '.' in asn: #conversion to 2Byte format
            asn = int(asn[:asn.find('.')])*65536 + int(asn[asn.find('.')+1:])
        asn = int(asn) #format int
        if asn not in CC_ASNs_ARIN['Region']:
            CC_ASNs_ARIN['Region'].append(asn)
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
        if 'Region' not in CC_ASNs_APNIC.keys() and CC != '':
            CC_ASNs_APNIC['Region'] = []
        if '.' in asn: #conversion to 2Byte format
            asn = int(asn[:asn.find('.')])*65536 + int(asn[asn.find('.')+1:])
        asn = int(asn) #format int
        if asn not in CC_ASNs_APNIC['Region']:
            CC_ASNs_APNIC['Region'].append(asn)
        i +=1
print 'CC at APNIC', CC_ASNs_APNIC.keys()
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
            CC_ASNs_LACNIC['Region'] = []
        if '.' in asn: #conversion to 2Byte format
            asn = int(asn[:asn.find('.')])*65536 + int(asn[asn.find('.')+1:])
        asn = int(asn) #format int
        if asn not in CC_ASNs_LACNIC['Region']:
            CC_ASNs_LACNIC['Region'].append(asn)
        i +=1
print 'CC at LACNIC',  CC_ASNs_LACNIC.keys()
print



#### Classify by type of Origin AS
##### Classifying them into local or external

command = 'mkdir  ' + output_folder + 'files_origin/'
os.system(command)

ori_dict = {}
ori_dict['RIPE'] = {}
ori_dict['local_AFRINIC'] = {}
ori_dict['external_AFRINIC'] = {}
ori_dict['LACNIC'] = {}
ori_dict['APNIC'] = {}
ori_dict['ARIN'] = {}
ori_dict['PRIVATE'] = {}
ori_dict['RESERVED'] ={}

######  gather ASNs from files in the output_folder_IXP_View folder = '../../Computation_outputs/12_local_external_ASNs_multiyear/'

List_possible_file_names = ['RIPE', 'Local_AFRINIC', 'External_AFRINIC', 'LACNIC', 'ARIN', 'APNIC', 'Private', 'Reserved']

for IXP_name in IXP_collector.keys():
    
    for name_file in List_possible_file_names:
        
        file_path = output_folder_IXP_View + 'files_origin/' + name_file +'_ASNs_' + IXP_name+ '.txt'
        
        ## does file exist ?
        
        if os.path.exists(file_path):
            
            with open (file_path, 'r') as fg:
                
                for line in fg:
                    
                    line = str(line).strip()
                    
                    tab = line.split('; ')
                    
                    if len(tab) > 1:
                    
                        if name_file in ori_dict.keys():
                            
                            if int(tab[0]) not in ori_dict[name_file].keys():
                                ori_dict[name_file][int(tab[0])] = []
                            
                            ori_dict[name_file][int(tab[0])].append(int(tab[1]))
                    
                        else:
                            
                            if name_file == 'Local_AFRINIC':
                                
                                name_file_store = 'local_AFRINIC'
                            
                            elif name_file == 'External_AFRINIC':
                                
                                name_file_store = 'external_AFRINIC'
                        
                            elif name_file == 'Private':
                                
                                name_file_store = 'PRIVATE'
                            
                            elif name_file == 'Reserved':
                                
                                name_file_store = 'RESERVED'
                            
                            if int(tab[0]) not in ori_dict[name_file_store].keys():
                                ori_dict[name_file_store][int(tab[0])] = []
                            
                                ori_dict[name_file_store][int(tab[0])].append(int(tab[1]))


print 'Here is the famous ori_dict = ', ori_dict

for year_current in year_ASN['Region'].keys():
   
    filename = output_folder + 'Percentage_Origin_ASNs_by_country_assignment' + '.txt'
    
    filename1 = output_folder + 'Percentage_Origin_ASNs_by_region' + '.txt'
        
    with open (filename1, 'a') as fg:
        
        fg.write('%s;%s;%s;%s\n' %('##year', 'Type of ASNs (Region)', 'len_ASNs_type', 'percentage_type'))

    IXP_OriginASes = []

    IXP_OriginASes = copy.deepcopy(year_ASN['Region'][year_current])

    Listrest_ASes = copy.deepcopy(IXP_OriginASes)

    private = []

    reserved = []

    for s in Listrest_ASes:
    
        if 64512<=s and s<=65534 :
            private.append(s)
            IXP_OriginASes.remove(s)
            if year_current not in ori_dict['PRIVATE'].keys():
                ori_dict['PRIVATE'][year_current] =[]
            ori_dict['PRIVATE'][year_current].append(s)
            
            
        elif (s==0 or s==65535) or (54272<=s and s<=64511):
            reserved.append(s)
            IXP_OriginASes.remove(s)
            if year_current not in ori_dict['RESERVED'].keys():
                ori_dict['RESERVED'][year_current] =[]
            ori_dict['RESERVED'][year_current].append(s)


    try:
        percentage_private = 100*float(len(ori_dict['PRIVATE'][year_current]))/float(len(Listrest_ASes))
                    
    except:
        percentage_private = 0.0
                            

                                

    if year_current in ori_dict['PRIVATE'].keys():
        print 'private = ', len(ori_dict['PRIVATE'][year_current]), float(len(Listrest_ASes)), percentage_private
        if len(ori_dict['PRIVATE'][year_current]) > 0:
            current_filename = output_folder + 'files_origin/Private_ASNs_all_IXPs_in_Africa.txt'
            for elmt in ori_dict['PRIVATE'][year_current]:
                with open (current_filename, 'a') as fh:
                    fh.write('%s;%s\n' %(year_current, elmt))

        with open (filename1, 'a') as fg:
            fg.write('%s; %s; %s; %s\n'%(year_current, 'Private ASNs', len(ori_dict['PRIVATE'][year_current]), percentage_private))
    
    with open (filename1, 'a') as fg:
        fg.write('\n%s %s %s %s\n'%('##Total number of origin ASNs found during ' , year_current, ' = ', len(Listrest_ASes)))
    

    try:
        percentage_reserved = (100*float(len(ori_dict['RESERVED'][year_current])))/float(len(Listrest_ASes))

    except:
        percentage_reserved = 0.0

    #print 'reserved =', len(ori_dict['RESERVED']), percentage_reserved
    if year_current in ori_dict['RESERVED'].keys():
        if len(ori_dict['RESERVED'][year_current]) > 0:
            current_filename = output_folder + 'files_origin/Reserved_ASNs_ASNs_all_IXPs_in_Africa.txt'
            for elmt in ori_dict['RESERVED'][year_current]:
                with open(current_filename, 'a') as fh:
                    fh.write('%s; %s\n'%(year_current, elmt))

        with open (filename1, 'a') as fg:
            fg.write('%s;%s;%s;%s\n'%(year_current, 'Reserved ASNs', len(ori_dict['RESERVED'][year_current]), percentage_reserved))





### Local Afrinic ASNs


    intersection = list(set(IXP_OriginASes) & set(CC_ASNs_AFRINIC['Region']))

    print 'intersection =', intersection
    print
    print 'CC_ASNs_AFRINIC = ', CC_ASNs_AFRINIC['Region']


    if len(intersection) > 0:
        current_filename = output_folder + 'files_origin/Local_AFRINIC_ASNs_all_IXPs_in_Africa.txt'
        for elmt in intersection :
            with open(current_filename, 'a') as fd:
                fd.write('%s; %s\n'%(year_current, elmt))
    
    try:
        ## How many ASNs assigned to current country and seen @ the IXP vs. the total number of Origin ASNs seen @ the IXP
        percentage_local_AF = (100*float(len(intersection)))/float(len(Listrest_ASes))

    except:
        percentage_local_AF = 0.0
                
    print 'percentage_local_AF =', percentage_local_AF
    ori_dict['local_AFRINIC'] = {year_current: intersection}
    
    
    print 'local_AFRINIC =', percentage_local_AF
                
    with open (filename1, 'a') as fg:
        fg.write('%s;%s;%s;%s\n' %(year_current, 'Local AFRINIC ASNs', len(intersection), percentage_local_AF))


#sys.exit()
    
### RIPE NCC
                                                                         
    total = 0
    total1 = 0
    print "AFRINIC REGION DONE. LET'S MOVE TO RIPE"
    
        
    intersection3 = []
    
    print 'CCs in other regions'
    
    print
    print 'length of ASNs in a cc_region', len(set(CC_ASNs_RIPE['Region']))
    

    intersection3 = list(set(IXP_OriginASes) & set(CC_ASNs_RIPE['Region']))
                                                 
    if len(intersection3) > 0:
        current_filename = output_folder +  'files_origin/RIPE_ASNs_all_IXPs_in_Africa.txt'
        for elmt in intersection3 :
            with open(current_filename, 'a') as fd:
                fd.write('%s; %s\n'%(year_current, elmt))
                                                 
    try:
        percentage_RIPE = 100*float(len(intersection3))/float(len(Listrest_ASes))
    except:
        percentage_RIPE = 0.0
                                                 
    #try:
    #    percentage_RIPE2 = 100*float(len(intersection3))/float(len(CC_ASNs_RIPE[cc_region]))
    #except:
    #    percentage_RIPE2 = 0.0
                                                 
    print 'length of intersection3:', len(intersection3)
    ori_dict['RIPE'][year_current] = intersection3
    
    total += percentage_RIPE
    total1 += len(intersection3)
                                                             
    with open (filename1, 'a') as fg:
        fg.write('%s;%s;%s;%s\n'%(year_current, 'RIPE ASNs', total1,  total))



#### ARIN

    total = 0
    total1 = 0
    print "AFRINIC & RIPE REGION DONE. LET'S MOVE TO ARIN"
    

    intersection5 = []
    

    print 'length of ASNs in a cc_region', len(set(CC_ASNs_ARIN['Region']))

    intersection5 =  list(set(IXP_OriginASes) & set(CC_ASNs_ARIN['Region']))

    if len(intersection5) > 0:
        current_filename = output_folder +  'files_origin/ARIN_ASNs_all_IXPs_in_Africa.txt'
        for elmt in intersection5:
            with open(current_filename, 'a') as fd:
                fd.write('%s; %s\n'%(year_current, elmt))
            
    try:
        percentage_ARIN = 100*float(len(intersection5))/float(len( Listrest_ASes ))
    except:
        percentage_ARIN = 0.0
            
   
            
    print 'length of intersection5:', len(intersection5)
    ori_dict['ARIN'][year_current] = intersection5
        
        
    total += percentage_ARIN
    total1 += len(intersection5)

    with open (filename1, 'a') as fg:
        fg.write('%s;%s;%s;%s\n'%(year_current, 'ARIN ASNs', total1, total))




### APNIC

    total = 0
    total1 = 0
    print "AFRINIC, RIPE & ARIN REGION DONE. LET'S MOVE TO APNIC"

    intersection4 = []
    

    print 'length of ASNs in a cc_region', len(set(CC_ASNs_APNIC['Region']))

    intersection4 =  list(set(IXP_OriginASes) & set(CC_ASNs_APNIC['Region']))
    
    if len(intersection4) > 0:
        current_filename = output_folder + 'files_origin/APNIC_ASNs_all_IXPs_in_Africa.txt'
        for elmt in intersection4 :
            with open(current_filename, 'a') as fd:
                fd.write('%s; %s\n'%(year_current, elmt))
        
    try:
        percentage_APNIC = 100*float(len(intersection4))/float(len( Listrest_ASes ))
    except:
        percentage_APNIC = 0.0
            
    #try:
    #    percentage_APNIC2 = 100*float(len(intersection4))/float(len( CC_ASNs_APNIC[cc_region] ))
    #except:
    #    percentage_APNIC2 = 0.0
            
            
    print 'length of intersection4:', len(intersection4)
    ori_dict['APNIC'][year_current] = intersection4
    

    total += percentage_APNIC
    total1 += len(intersection4)


    with open (filename1, 'a') as fg:
        fg.write('%s;%s;%s;%s\n'%(year_current, 'APNIC ASNs', total1, total))



### LACNIC

    total = 0
    total1 = 0
    print "AFRINIC, RIPE, ARIN & APNIC REGION DONE. LET'S MOVE TO LACNIC"

        
    intersection5 = []
    

    print 'length of ASNs in a cc_region', len(set(CC_ASNs_LACNIC['Region']))
    
    intersection6 =  list(set(IXP_OriginASes) & set(CC_ASNs_LACNIC['Region']))
    
    if len(intersection6) > 0:
        current_filename = output_folder + 'files_origin/LACNIC_ASNs_all_IXPs_in_Africa.txt'
        for elmt in intersection6 :
            with open(current_filename, 'a') as fd:
                fd.write('%s; %s\n'%(year_current, elmt))
        
    try:
        percentage_LACNIC = 100*float(len(intersection6))/float(len( Listrest_ASes ))
    except:
        percentage_LACNIC = 0.0
            

            
    print 'length of intersection6:', len(intersection6)
    ori_dict['LACNIC'][year_current] = intersection6

    total += percentage_LACNIC
    total1 += len(intersection6)
    
    with open (filename1, 'a') as fg:
        fg.write('%s;%s;%s;%s\n'%(year_current, 'LACNIC ASNs', total1, total))



#print current_CC, ori_dict,
print

### store output into files
log_file_instance.write( str(now_datetime)+ ' End computation '+ '\n')
#create_output.close()
log_file_instance.close()


now_datetime = str(datetime.now()).replace(' ', '_')
finish = open ('finish_multiyear.txt', 'w')
finish.write('ended; ' + root_folder + output_folder[6:] + '; ' + now_datetime)
finish.close()

