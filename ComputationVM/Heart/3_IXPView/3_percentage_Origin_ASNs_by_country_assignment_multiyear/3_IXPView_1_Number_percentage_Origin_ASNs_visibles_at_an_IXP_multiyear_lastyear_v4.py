
##############################################################################
#__author__ = "Roderick Fanou"
#__status__ = "Production"
#__Last modification date__ = October 24, 2016
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


## import all files in the library you need
sys.path.append('../../2_libraries/')
import DB_configuration
import bgp_rib
from define_timescales import *
from functions import *

##
now_datetime = str(datetime.now()).replace(' ', '_')

finish = open ('finish_lastyear.txt', 'w')
finish.write('started; ' + now_datetime )
finish.close()

## Create a logfile:
name_log_file = 'Log_'+str(now_datetime) + '_' + '1_Number_Origin_ASNs_visibles_at_an_IXP_multiyear_lastyear' + '.txt'
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
continent = DB_configuration.continent
IXP_collector = {}
IXP_CC = {}
Current_db = 'MergedData'
CC_ASNs_AFRINIC = {}
CC_IXP = {}
region = DB_configuration.region


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
        IXP_CC[row[2]] = row[0]
    
    if row[2] not in CC_IXP.keys():
        CC_IXP[row[2]] = []
    if row[0] not in CC_IXP[row[2]]:
        CC_IXP[row[2]].append(row[0])
    
    IXP_collector[row[0]].append(row[1])
    i+=1

print IXP_collector
root_folder = '/home/African_Route-collectors_Data_Analyzer-ARDA/ComputationVM/Heart/'
output_folder = '../../Computation_outputs/3_Number_percentage_Origin_by_country_assignment_lastyear/'

command = 'rm -rf ' + output_folder
os.system(command)

command = 'mkdir ' + output_folder
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


## multi-year and last year
if List_all_tables >0:
    ASN_year = {}
    year_ASN = {}
        
    month_ASN = {}
    ASN_month = {}
    
    for ixp in IXP_collector.keys():
        
        log_file_instance = open(location_logfile+'/'+name_log_file, 'a')
       
        create_output_lastyear =  open(output_folder + 'LastYear__list_visible_ASNs_at_IXP_' + ixp + '.txt', 'a')
        
        create_output_lastyear.write('Month-Year; ' + 'Origin ASN Visible' + '\n')
        
        create_output_MultiYear =  open(output_folder + 'MultiYear__list_visible_ASNs_at_IXP_'+ixp+'.txt', 'a')
        
        create_output_MultiYear.write('Year; ' + 'Origin ASN Visible' + '\n')
        
        if ixp not in year_ASN.keys():
            
            year_ASN[ixp] = {}
        
        if ixp not in month_ASN.keys():
            month_ASN[ixp] = {}
        
        for year in yearList:
            
            if year not in year_ASN[ixp].keys():
                year_ASN[ixp][year] = []

            for month in xrange(1,13):
                if 'Data__' + str(year) + "_" + str(month) in List_all_tables:
                    print IXP_collector[ixp]
                    
                    #query = "select count(*) from Data__"+str(year)+"_"+str(month) + " ;"
                    #cur.execute(query)
                    #data = cur.fetchall()
                    #print 'number of lines in the table ', data
                    
                    k = 0
                    query = "select distinct OriginAS, ASPath from Data__"+str(year)+"_"+str(month) + " where"
                    
                    if len(IXP_collector[ixp]) > 1:
                           while k< len(IXP_collector[ixp]) -1:
                                k+=1
                                query += " RouteCollector = %s or "
                    
                    query += " RouteCollector = %s and (OriginAS != 'None' and OriginAS is not NULL and OriginAS != 'NULL') "
                    
                    
                    print 'start_query :', now_datetime, query
                    print datetime.now(), 'fetching data from ', ixp
                    
                    cur.execute(query, IXP_collector[ixp])
                    log_file_instance.write(str(now_datetime)+ ' Multi-year & last year Fetching data from IXP '+ ixp + '\n')
                    
                    print 'Here is the query ', cur._executed
                    data = cur.fetchall()

                    print 'end_query :', now_datetime #, data
                    

                    
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
                                except:
                                    print 'Case 2: Alert We pass for this path ', row[1]
                        
                            for OriginASNs_elmt in OriginASNs :
                                
                                if OriginASNs_elmt not in year_ASN[ixp][year]:
                                    year_ASN[ixp][year].append(OriginASNs_elmt)
                                    create_output_MultiYear.write(str(year)+ '; '+ str(OriginASNs_elmt) + '\n')
                            
                                ## Check if we are in the last year and proceed for lastyear
                                if (year, month) in lastYearList:
                                    
                                    if str(month)+'-'+str(year) not in month_ASN[ixp].keys():
                                        month_ASN[ixp][str(month)+'-'+str(year)] = []
                                
                                    if OriginASNs_elmt not in month_ASN[ixp][str(month)+'-'+str(year)]:
                                        month_ASN[ixp][str(month)+'-'+str(year)].append(OriginASNs_elmt)
                                        create_output_lastyear.write(str(month)+'-'+str(year)+ '; '+ str(OriginASNs_elmt) + '\n')

                            i += 1

                    else:
                        print 'No ASN found for ', ixp, ' in ' , 'Data__'+str(year)+'_'+str(month)
                            



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


filename = output_folder+'LastYear__local_vs_External_ASNs_to_the_country_hosting_IXP_visible_at_IXP_'+ixp+'.txt'
with open(filename, 'a') as fd:
    fd.write('%s;%s;%s;%s;%s;%s;%s\n'%('CC', 'IXP', 'month-Year', 'Number of Origin ASNs assigned to the country visibles at the IXP', 'Number of Origin ASNs visibles at the IXP', 'Percentage of local Origin ASNs', 'Percentage of External Origin ASNs' ))


filename = output_folder+'MultiYear__local_vs_External_ASNs_to_the_country_hosting_IXP_visible_at_IXP_'+ixp+'.txt'
with open(filename, 'a') as fd:
    fd.write('%s;%s;%s;%s;%s;%s;%s\n'%('CC', 'IXP', 'Year', 'Number of Origin ASNs assigned to the country visibles at the IXP', 'Number of Origin ASNs visibles at the IXP', 'Percentage of local Origin ASNs', 'Percentage of External Origin ASNs' ))



## Note that Local means local to the country of the IXP
for ixp in IXP_collector.keys():
    
    if ixp in month_ASN.keys():
        filename = output_folder+'LastYear__local_vs_External_ASNs_to_the_country_hosting_IXP_visible_at_IXP_'+ixp+'.txt'
        
        for elmt in month_ASN[ixp].keys():
            
            #if len(month_ASN[ixp][elmt]) > 0:
                #create_output_lastyear.write(elmt+ '; '+ str(len(month_ASN[ixp][elmt])) + '\n')
                set_ASNs = copy.deepcopy(month_ASN[ixp][elmt])
                ## Classify and put numbers.
                
                for CC in CC_IXP.keys():
                    for ixp1 in CC_IXP[CC]:
                        
                        if ixp == ixp1 :
                            current_CC = CC
                            intersection = list(set(month_ASN[ixp][elmt]) & set(CC_ASNs_AFRINIC[current_CC]))
                    
                            try:
                                ## How many ASNs assigned to current country and seen @ the IXP vs. the total number of Origin ASNs seen @ the IXP
                                percentage_local_AF = float(len(intersection))/float(len(month_ASN[ixp][elmt]))*100
                            except:
                                percentage_local_AF = 0.0
                        
                            with open(filename, 'a') as fd:
                                #if len(intersection) >0:
                                    try:
                                        A = pycountry.countries.get(alpha2=current_CC)
                                        fd.write('%s;%s;%s;%s;%s;%s;%s\n'%(current_CC, A, elmt, len(intersection), len(month_ASN[ixp][elmt]),  percentage_local_AF, 100-percentage_local_AF ))
                                    except:
                                        fd.write('%s;%s;%s;%s;%s;%s;%s\n'%(current_CC, '', elmt, len(intersection), len(month_ASN[ixp][elmt]),  percentage_local_AF, 100-percentage_local_AF ))




    if  ixp in year_ASN.keys():
        filename = output_folder+'MultiYear__local_vs_External_ASNs_to_the_country_hosting_IXP_visible_at_IXP_'+ixp+'.txt'
        for year in list(set(yearList)):
            #create_output_MultiYear.write(str(year)+ '; '+ str(len(year_ASN[ixp][year]))  + '\n')

            ## Classify and put numbers.
            #if len(year_ASN[ixp][year]) > 0:
                set_ASNs = copy.deepcopy(year_ASN[ixp][year])

                for CC in CC_IXP.keys():
                    for ixp1 in CC_IXP[CC]:
    
                        if ixp == ixp1 :
                            current_CC = CC
                            intersection = list(set(year_ASN[ixp][year]) & set(CC_ASNs_AFRINIC[current_CC]))
                
                            try:
                                ## How many ASNs assigned to current country and seen @ the IXP vs. the total number of Origin ASNs seen @ the IXP
                                percentage_local_AF = float(len(intersection))/float(len(year_ASN[ixp][year]))*100
                            except:
                                percentage_local_AF = 0.0
                                
                            with open(filename, 'a') as fd:
                                #if len(intersection) >0:
                                    try:
                                        A = pycountry.countries.get(alpha2=current_CC)
                                        fd.write('%s;%s;%s;%s;%s;%s;%s\n'%(current_CC, A, year, len(intersection), len(year_ASN[ixp][year]),  percentage_local_AF, 100-percentage_local_AF ))
                                    except:
                                        fd.write('%s;%s;%s;%s;%s;%s;%s\n'%(current_CC, '', year, len(intersection), len(year_ASN[ixp][year]),  percentage_local_AF, 100-percentage_local_AF ))





log_file_instance.close()
now_datetime = str(datetime.now()).replace(' ', '_')
finish = open ('finish_lastyear.txt', 'w')
finish.write('ended; ' + root_folder + output_folder[6:] + '; ' + now_datetime )
finish.close()
