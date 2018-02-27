#1st graph : We keep the pie chart in the application (added below), but we compute
#it only for last month, and consider distinct ASNs as defined in point 2.

##############################################################################
#__author__ = "Roderick Fanou"
#__email__ = "roderick.fanou@imdea.org"
#__status__ = "Production"
#__last_modifications__ =
## local afrinic added to the classification of the Origine ASes
## Line 660 ; error in coding Listrest_ASes instead of CC_ASNs_RIPE[cc_region]
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

finish = open ('finish_multiyear.txt', 'w')
finish.write('started; ' + now_datetime )
finish.close()

## Create a logfile:
name_log_file = 'Log_'+str(now_datetime) + '_' + '1_Number_Origin_ASNs_visible_at_an_IXP_lastyear_multiyear' + '.txt'
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
output_folder = '../../Computation_outputs/12_local_external_ASNs_multiyear/'

#command = 'rm -rf ' + output_folder
#os.system(command)

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
        #print row
        asn = row[0] #type string
        current_CC = row[1]
        
        if '.' in asn: #conversion to 2Byte format
            #print '4B format:',asn
            tab = asn.split('.')
            asn = int(tab[0])*65536 + int(tab[1])
        
        asn = int(asn) #format int
        if current_CC not in  CC_ASNs_AFRINIC.keys() and current_CC != '' :
            CC_ASNs_AFRINIC[current_CC] = []
        
        if asn not in CC_ASNs_AFRINIC[current_CC]:
            CC_ASNs_AFRINIC[current_CC].append(asn)
        
        i +=1



pprint(CC_ASNs_AFRINIC)







#filename_output_ASNs_by_AFRINIC = output_folder + 'Number_ASNs_assigned_by_Afrinic.txt'
#with open (filename_output_ASNs_by_AFRINIC, 'a') as fg:
#    for CC in CC_ASNs_AFRINIC.keys():
#        fg.write('%s;%s\n' %(CC, len(CC_ASNs_AFRINIC[CC])))




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


if List_all_tables >0:
    

    year_ASN = {}
    
    
    for ixp in IXP_collector.keys():
        
        log_file_instance = open(location_logfile+'/'+name_log_file, 'a')
        
        if ixp not in year_ASN.keys():
            year_ASN[ixp] = {}


        for year in yearList:
    
            if year not in year_ASN[ixp].keys():
                year_ASN[ixp][year] = []
        
            for month in xrange(1,13):
                if 'Data__' + str(year) + "_" + str(month) in List_all_tables:
                    print
                    print
                    #print IXP_collector[ixp]

                    k = 0
                    query = "select distinct OriginAS, ASPath from Data__"+str(year)+"_"+str(month) + " where"
                    while k< len(IXP_collector[ixp]) -1:
                        k+=1
                        query += " RouteCollector = %s or "
                    
                    query += " RouteCollector = %s and (OriginAS != 'None' and OriginAS is not NULL and OriginAS != 'NULL') "
                    
                    print 'start_query :', datetime.now(), query
                    print
                    print datetime.now(), 'fetching data from ', ixp

                    cur.execute(query, IXP_collector[ixp])
                    
                    log_file_instance.write(str(now_datetime)+ 'Last year Fetching data from IXP '+ ixp + '\n')
                    
                    print 'Here is the query ', cur._executed
                    data = cur.fetchall()
                    print
                    print 'end_query :', datetime.now() #, data
                    i = 0
                    
                    print "we found data of length ", len(data)
                    
                    if len(data)>0:
                        
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
                                
                                if OriginASNs_elmt  not in year_ASN[ixp][year]:
                                    year_ASN[ixp][year].append(OriginASNs_elmt)
                                
                            
                            i += 1
                                
                    else:
                        print 'No prefix found for ', ixp, ' in ' , 'Data__'+str(year)+'_'+str(month)


pprint(year_ASN)



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
        asn = int(asn) #format int
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
        asn = int(asn) #format int
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
        asn = int(asn) #format int
        if asn not in CC_ASNs_LACNIC[CC]:
            CC_ASNs_LACNIC[CC].append(asn)
        i +=1
print 'CC at LACNIC',  CC_ASNs_LACNIC.keys()
print


#### Classify by type of Origin AS
##### Classifying them into local or external

command = 'mkdir  ' + output_folder + 'files_origin/'
os.system(command)


#Number_ASNs_classified = len(Listrest_ASes)

update = 0

#month_prefix[ixp][str(month)+'-'+str(year)]

for ixp in year_ASN.keys():
    
    filename = output_folder + 'Percentage_Origin_ASNs_by_country_assignment_' +ixp+ '.txt'
    filename1 = output_folder + 'Percentage_Origin_ASNs_by_region_' +ixp+ '.txt'
        
    with open (filename1, 'a') as fg:
        fg.write('%s;%s;%s;%s\n' %('##month_year', 'Type of ASNs (Region)', 'len_ASNs_type', 'percentage_type'))
    
    for year_current in year_ASN[ixp].keys():
        
        
        print 'A last check on the CC_ASNs_AFRINIC we have ', CC_ASNs_AFRINIC
 
        IXP_OriginASes = []

        IXP_OriginASes = copy.deepcopy(year_ASN[ixp][year_current])
    
        #for ixp in IXP_OriginASes.keys():
        ori_dict = {}
        ori_dict['RIPE'] = {}
        ori_dict['external_AFRINIC'] = {}
        ori_dict['local_AFRINIC'] = {}
        ori_dict['LACNIC'] = {}
        ori_dict['APNIC'] = {}
        ori_dict['ARIN'] = {}
        ori_dict['PRIVATE'] = []
        ori_dict['RESERVED'] =[]
        
        for CC in CC_IXP.keys():
            
            for ixp1 in CC_IXP[CC]:
                
                if ixp == ixp1 :
                    
                        print ixp, CC
                        print ixp,  IXP_OriginASes, len( IXP_OriginASes)
                        
                        current_CC = CC
                        
                        Listrest_ASes = copy.deepcopy(IXP_OriginASes)
                        
                        intersection = []
                        private = []
                        reserved = []
                        
                        for s in Listrest_ASes:
                            
                            if 64512<=s and s<=65534 :
                                private.append(s)
                                IXP_OriginASes.remove(s)
                                ori_dict['PRIVATE'].append(s)
                            
                            
                            elif (s==0 or s==65535) or (54272<=s and s<=64511):
                                reserved.append(s)
                                IXP_OriginASes.remove(s)
                                ori_dict['RESERVED'].append(s)
                

                        try:
                            percentage_private = 100*float(len(ori_dict['PRIVATE']))/float(len(Listrest_ASes))
                        
                        except:
                            percentage_private = 0.0

                        print 'private = ', len(ori_dict['PRIVATE']), float(len(Listrest_ASes)), percentage_private
                        
                        
                        
                        if len(ori_dict['PRIVATE']) > 0:
                            current_filename = output_folder + 'files_origin/Private_ASNs_' + ixp + '.txt'
                            for elmt in ori_dict['PRIVATE']:
                                with open (current_filename, 'a') as fh:
                                    fh.write('%s;%s\n' %(year_current,elmt))


                        with open (filename1, 'a') as fg:
                            fg.write('\n%s %s %s %s\n'%('##Total number of origin ASNs found during ' , year_current, ' = ', len(Listrest_ASes)))
        

                        with open (filename1, 'a') as fg:
                            fg.write('%s; %s; %s; %s\n'%(year_current, 'Private ASNs', len(ori_dict['PRIVATE']), percentage_private))


                        try:
                            percentage_reserved = (100*float(len(ori_dict['RESERVED'])))/float(len(Listrest_ASes))

                        except:
                            percentage_reserved = 0.0


                        #print 'reserved =', len(ori_dict['RESERVED']), percentage_reserved
                        if len(ori_dict['RESERVED']) > 0:
                            current_filename = output_folder + 'files_origin/Reserved_ASNs_' + ixp + '.txt'
                            for elmt in ori_dict['RESERVED']:
                                with open(current_filename, 'a') as fh:
                                    fh.write('%s; %s\n'%(year_current,elmt))
                    
                        with open (filename1, 'a') as fg:
                            fg.write('%s;%s;%s;%s\n'%(year_current, 'Reserved ASNs', len(ori_dict['RESERVED']), percentage_reserved))


                        ## Local
                        if current_CC in CC_ASNs_AFRINIC.keys():
                            intersection = list(set(IXP_OriginASes) & set(CC_ASNs_AFRINIC[current_CC]))

                            print 'intersection =', intersection
                            print
                            print 'CC_ASNs_AFRINIC = ', CC_ASNs_AFRINIC[current_CC]


                        if len(intersection) > 0:
                            current_filename = output_folder + 'files_origin/Local_AFRINIC_ASNs_' + ixp + '.txt'
                            for elmt in intersection :
                                with open(current_filename, 'a') as fd:
                                    fd.write('%s; %s\n'%(year_current, elmt))
                        
                        try:
                            ## How many ASNs assigned to current country and seen @ the IXP vs. the total number of Origin ASNs seen @ the IXP
                            percentage_local_AF = (100*float(len(intersection)))/float(len(Listrest_ASes))
                        except:
                            
                            percentage_local_AF = 0.0
                        
                        print 'percentage_local_AF =', percentage_local_AF
                        ori_dict['local_AFRINIC'] = {current_CC: intersection}
                        
                        
                        ## Percentage of ASNs allocated to the country visibles at the IXP
                        #try:
                            ## How many ASNs assigned to current country and seen @ the IXP vs.
                            #percentage_local_AF2 = 100*float(len(intersection))/float(len(CC_ASNs_AFRINIC[current_CC]))
                        #except:
                            #percentage_local_AF2 = 0.0


                        print 'local_AFRINIC =', percentage_local_AF
                        
                        with open (filename1, 'a') as fg:
                            fg.write('%s;%s;%s;%s\n' %(year_current, 'Local AFRINIC ASNs', len(intersection), percentage_local_AF))
                        
                        

### AFRINIC

                        total = 0
                        total1 = 0
                        #for cc_external in CC_IXP.keys():
                        for cc_external in CC_ASNs_AFRINIC.keys():
                            intersection2 = []
                            print 'external cc in AFRINIC region to make intersection with the local ASNs:', cc_external
            
                            if current_CC != cc_external:
                                if cc_external not in ori_dict['external_AFRINIC'].keys():
                                        print 'length of ASNs in a cc_external', cc_external , ' = ', len(set(CC_ASNs_AFRINIC[cc_external]))
                                        
                                        if cc_external in CC_ASNs_AFRINIC.keys():
                                            intersection2 =  list(set(IXP_OriginASes) & set(CC_ASNs_AFRINIC[cc_external]))
                            
                                        if len(intersection2) > 0:
                                            current_filename = output_folder + 'files_origin/External_AFRINIC_ASNs_' + ixp + '.txt'
                                            for elmt in intersection2 :
                                                with open(current_filename, 'a') as fd:
                                                    fd.write('%s; %s\n'%(year_current, elmt))

                                        try:
                                            percentage_external_AF = (100*(float(len(intersection2))))/float(len( Listrest_ASes ))
                                        except:
                                            percentage_external_AF = 0.0
                
                                        print 'percentage_external_AF =', percentage_external_AF
                    
                                        print 'length of intersection2:', len(intersection2)
                        
                                        #try:
                                        #    percentage_external_AF2 = (100*float(len(intersection2)))/float(len(CC_ASNs_AFRINIC[cc_external]))
                                        #except:
                                        #    percentage_external_AF2 = 0.0
                                        
                                        ori_dict['external_AFRINIC'][cc_external] = intersection2
                                                                                     
                                        total += percentage_external_AF
                                        total1 += len(intersection2)
                        
                            else:
                                pass
                                                                                 
                        with open (filename1, 'a') as fg:
                            fg.write('%s;%s;%s;%s\n'%(year_current,'External AFRINIC ASNs', total1, total))



### RIPE NCC
                                                                                 
                        total = 0
                        total1 = 0
                        print "AFRINIC REGION DONE. LET'S MOVE TO RIPE"
                        for cc_region in CC_ASNs_RIPE:
                            
                            intersection3 = []
                            
                            print 'CCs in other regions'
                            if current_CC != cc_region:
                                if cc_region not in ori_dict['RIPE'].keys():
                                    print
                                    print 'length of ASNs in a cc_region', len(set(CC_ASNs_RIPE[cc_region]))
                                    
                                    if cc_region in CC_ASNs_RIPE.keys():
                                        intersection3 = list(set(IXP_OriginASes) & set(CC_ASNs_RIPE[cc_region]))
                                                                                 
                                    if len(intersection3) > 0:
                                        current_filename = output_folder +  'files_origin/RIPE_ASNs_' + ixp + '.txt'
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
                                    ori_dict['RIPE'][cc_region] = intersection3
                                    
                                    total += percentage_RIPE
                                    total1 += len(intersection3)

                            else:
                                print '----'
                                print 'cc coincides with another in other region which is:', cc_region
                                print '----'
                                
                                                                                 
                        with open (filename1, 'a') as fg:
                            fg.write('%s;%s;%s;%s\n'%(year_current, 'RIPE ASNs', total1,  total))


    
#### ARIN

                        total = 0
                        total1 = 0
                        print "AFRINIC & RIPE REGION DONE. LET'S MOVE TO ARIN"
                        for cc_region in CC_ASNs_ARIN:
                            
                            intersection5 = []
                            
                            if current_CC != cc_region:
                                if cc_region not in ori_dict['ARIN'].keys():
                                    print
                                    print 'length of ASNs in a cc_region', len(set(CC_ASNs_ARIN[cc_region]))
                                    
                                    if cc_region in CC_ASNs_ARIN.keys():
                                        intersection5 =  list(set(IXP_OriginASes) & set(CC_ASNs_ARIN[cc_region]))
                                
                                    if len(intersection5) > 0:
                                        current_filename = output_folder +  'files_origin/ARIN_ASNs_' + ixp + '.txt'
                                        for elmt in intersection5 :
                                            with open(current_filename, 'a') as fd:
                                                fd.write('%s; %s\n'%(year_current, elmt))
                                            
                                    try:
                                        percentage_ARIN = 100*float(len(intersection5))/float(len( Listrest_ASes ))
                                    except:
                                        percentage_ARIN = 0.0
                                            
                                    #try:
                                    #    percentage_ARIN2 = 100*float(len(intersection5))/float(len( CC_ASNs_ARIN[cc_region]))
                                    #except:
                                    #   percentage_ARIN2 = 0.0
                                            
                                    print 'length of intersection5:', len(intersection5)
                                    ori_dict['ARIN'][cc_region] = intersection5
                                        
                                        
                                    total += percentage_ARIN
                                    total1 += len(intersection5)


                            else:
                                print '----'
                                print 'cc coincides with another in other region which is:', cc_region
                                print '----'
                    
                    
                        with open (filename1, 'a') as fg:
                            fg.write('%s;%s;%s;%s\n'%(year_current, 'ARIN ASNs', total1, total))




### APNIC

                        total = 0
                        total1 = 0
                        print "AFRINIC, RIPE & ARIN REGION DONE. LET'S MOVE TO APNIC"
                        for cc_region in CC_ASNs_APNIC:
                            
                            intersection4 = []
                            
                            if current_CC != cc_region:
                                if cc_region not in ori_dict['APNIC'].keys():
                                    print
                                    print 'length of ASNs in a cc_region', len(set(CC_ASNs_APNIC[cc_region]))
                                    
                                    if cc_region in CC_ASNs_APNIC.keys():
                                        intersection4 =  list(set(IXP_OriginASes) & set(CC_ASNs_APNIC[cc_region]))
                                    
                                    if len(intersection4) > 0:
                                        current_filename = output_folder + 'files_origin/APNIC_ASNs_' + ixp + '.txt'
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
                                    ori_dict['APNIC'][cc_region] = intersection4
                                    
                            
                                    total += percentage_APNIC
                                    total1 += len(intersection4)
                        
                            else:
                                print '----'
                                print 'cc coincides with another in other region which is:', cc_region
                                print '----'
            
                        with open (filename1, 'a') as fg:
                            fg.write('%s;%s;%s;%s\n'%(year_current, 'APNIC ASNs', total1, total))



### LACNIC

                        total = 0
                        total1 = 0
                        print "AFRINIC, RIPE, ARIN & APNIC REGION DONE. LET'S MOVE TO LACNIC"
                        for cc_region in CC_ASNs_LACNIC:
                            
                            intersection5 = []
                            
                            if current_CC != cc_region:
                                if cc_region not in ori_dict['LACNIC'].keys():
                                    print
                                    print 'length of ASNs in a cc_region', len(set(CC_ASNs_LACNIC[cc_region]))
                                    
                                    if cc_region in CC_ASNs_LACNIC.keys():
                                        intersection6 =  list(set(IXP_OriginASes) & set(CC_ASNs_LACNIC[cc_region]))
                                    
                                    if len(intersection6) > 0:
                                        current_filename = output_folder + 'files_origin/LACNIC_ASNs_' + ixp + '.txt'
                                        for elmt in intersection6 :
                                            with open(current_filename, 'a') as fd:
                                                fd.write('%s; %s\n'%(year_current, elmt))
                                        
                                    try:
                                        percentage_LACNIC = 100*float(len(intersection6))/float(len( Listrest_ASes ))
                                    except:
                                        percentage_LACNIC = 0.0
                                            
                                    #try:
                                    #    percentage_LACNIC2 = 100*float(len(intersection6))/float(len(CC_ASNs_LACNIC[cc_region]))
                                    #except:
                                    #    percentage_LACNIC2 = 0.0
                                            
                                    print 'length of intersection6:', len(intersection6)
                                    ori_dict['LACNIC'][cc_region] = intersection6
                
                                    total += percentage_LACNIC
                                    total1 += len(intersection6)
                        
                            else:
                                print '----'
                                print 'cc coincides with another in other region which is:', cc_region
                                print '----'
                        
                        with open (filename1, 'a') as fg:
                            fg.write('%s;%s;%s;%s\n'%(year_current, 'LACNIC ASNs', total1, total))



#print current_CC, ori_dict,
print


### store output into files
log_file_instance.write( str(now_datetime)+ ' End computation '+ '\n')
#create_output.close()
log_file_instance.close()


finish = open ('finish_multiyear.txt', 'w')
finish.write('ended; ' + root_folder + output_folder[6:] + '; ' + now_datetime )
finish.close()

