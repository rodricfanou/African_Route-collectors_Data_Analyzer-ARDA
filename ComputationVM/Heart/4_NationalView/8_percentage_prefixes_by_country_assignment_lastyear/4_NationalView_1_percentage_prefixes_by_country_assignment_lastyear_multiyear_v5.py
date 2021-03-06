
##############################################################################
#__author__ = "Roderick Fanou"
#__status__ = "Production"
##############################################################################


#!/usr/bin/python
import random
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

finish = open ('finish_lastyear_better.txt', 'w')
finish.write('started; ' + now_datetime)
finish.close()

## Create a logfile:
name_log_file = 'Log_'+str(now_datetime) + '_' + '4_NationalView_5_Number_prefixes_visible_at_an_IXP_multiyear_lastyear_better' + '.txt'
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
region = DB_configuration.region
IXP_collector = {}
IXP_CC = {}
Current_db = 'MergedData'
CC_IXP = {}


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
    
    if row[2] not in CC_IXP.keys():
        CC_IXP[row[2]] = []
    if row[0] not in CC_IXP[row[2]]:
        CC_IXP[row[2]].append(row[0])
    
    IXP_collector[row[0]].append(row[1])
    i+=1




print IXP_collector
root_folder = '/home/African_Route-collectors_Data_Analyzer-ARDA/ComputationVM/Heart/'
output_folder = '../../Computation_outputs_National_View/8_percentage_prefixes_by_country_assignment_lastyear_better/'

command = 'rm -rf ' + output_folder
os.system(command)

command = 'mkdir ' + output_folder
os.system(command)

command = 'chmod 777 ' + output_folder
os.system(command)

command = 'mkdir ' + output_folder + 'files_prefixes/'
os.system(command)


command = 'mkdir ' + output_folder + 'List_prefixes_assigned_by_RIRs/'
os.system(command)

command = 'chmod 777 ' + output_folder
os.system(command)



###Current list of all tables;
query = "SHOW TABLES LIKE 'Data__%%' "
cur.execute (query)
data = cur.fetchall()
List_all_tables = []
if len(data) > 0:
    for elmt in data:
        List_all_tables.append(elmt[0])
##print List_all_tables



## multi-year and last year
if len(List_all_tables) >0:
    prefix_year = {}
    year_prefix = {}
        
    month_prefix = {}
    prefix_month = {}
    
    month_prefix_bogon = {}
    year_prefix_bogon = {}

    #CC_done = []
    
    for ixp in IXP_collector.keys():

              
        CC_key = IXP_CC[ixp]
      
     # if CC_key not in CC_done:

        #CC_done.append(CC_key)
  
        log_file_instance = open(location_logfile+'/'+name_log_file, 'a')
        
        create_output_lastyear =  open(output_folder + 'LastYear__list_visible_prefixes_at_IXP_' + CC_key + '.txt', 'a')
        
        create_output_lastyear.write('Month-Year; ' + 'Prefixes Visible' + '\n')
        
        create_output_MultiYear =  open(output_folder + 'MultiYear__list_visible_prefixes_at_IXP_'+CC_key +'.txt', 'a')
        
        create_output_MultiYear.write('Year; ' + 'Prefixes Visible' + '\n')
        
        
        if CC_key not in year_prefix.keys():
            
            year_prefix[CC_key] = {}

        
        if CC_key not in month_prefix.keys():
            month_prefix[CC_key] = {}

        
        
        for year in yearList:
            
            if year not in year_prefix[CC_key].keys():
                year_prefix[CC_key][year] = []



            for month in xrange(1,13):
                if 'Data__' + str(year) + "_" + str(month) in List_all_tables:
                    #print
                    #print
                    #print IXP_collector[ixp]
                    
                    #query = "select count(*) from Data__"+str(year)+"_"+str(month) + " ;"
                    #cur.execute(query)
                    #data = cur.fetchall()
                    #print 'number of lines in the table ', data
                    
                    k = 0
                    query = "select distinct Network from Data__"+str(year)+"_"+str(month) + " where"
                    while k< len(IXP_collector[ixp]) -1:
                        k+=1
                        query += " RouteCollector = %s or "
                    
                    query += " RouteCollector = %s limit 10"
                    
                    print 'start_query :', datetime.now(), query
                    print
                    print datetime.now(), 'fetching data from ', ixp
                    
                    cur.execute(query, IXP_collector[ixp])
                    log_file_instance.write(str(now_datetime)+ ' Multi-year & last year Fetching data from IXP '+ ixp + '\n')
                    
                    print 'Here is the query ', cur._executed
                    data = cur.fetchall()
                    print
                    print 'end_query :', datetime.now() #, data
                    print
                    print
                    i = 0
                    
                    if len(data)>0:
                        
                        while (i<len(data)):
                            row = data[i]
                            prefix = row[0]

                            if prefix not in year_prefix[CC_key][year]:
                                year_prefix[CC_key][year].append(prefix)
                                create_output_MultiYear.write(str(year)+ '; '+ str(prefix) + '\n')
                                    
                                    
                            ## Check if we are in the last year and proceed for lastyear
                            if (year, month) in lastYearList:
                                
                                if str(month)+'-'+str(year) not in month_prefix[CC_key].keys():
                                    month_prefix[CC_key][str(month)+'-'+str(year)] = []

                                if prefix not in month_prefix[CC_key][str(month)+'-'+str(year)]:
                                    month_prefix[CC_key][str(month)+'-'+str(year)].append(prefix)
                                    create_output_lastyear.write(str(month)+'-'+str(year)+ '; '+ str(prefix) + '\n')
                            i += 1

                    else:
                        print 'No prefix found for ', ixp, ' in ' , 'Data__'+str(year)+'_'+str(month)




### Collecting data from AFRINIC database
Current_db = 'RIRs'
## connect to the DB
db = MySQLdb.connect(host = DB_configuration.host, user = DB_configuration.user, passwd = DB_configuration.passwd,  db = Current_db)
cur = db.cursor()
print 'Connected'

query = "select distinct NetIPaddress, NetBits, CC from IPv4_ressources_AFRINIC where status = 'allocated' or status = 'assigned' and CC != '';"
cur.execute (query)
data = cur.fetchall()
i = 0

CC_ASNs_AFRINIC = {}
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
        i +=1

### Note this contains the prefixes, not the ASNs
print CC_ASNs_AFRINIC.keys()



filename_output_ASNs_by_AFRINIC = output_folder + 'Number_prefixes_assigned_by_Afrinic.txt'

with open (filename_output_ASNs_by_AFRINIC, 'a') as fg:
    
    for CC in CC_ASNs_AFRINIC.keys():
        
        fg.write('%s;%s\n' %(CC, len(CC_ASNs_AFRINIC[CC])))



with open(output_folder + 'List_prefixes_assigned_by_RIRs/List_prefixes_assigned_by_AFRINIC.txt', 'a') as fgh:
    
    for CC in CC_ASNs_AFRINIC.keys():
        
        for elmt in CC_ASNs_AFRINIC[CC]:
            
            fgh.write('%s; %s\n' %(CC, str(elmt)))



for ixp in IXP_collector.keys():
    
    CC_key = IXP_CC[ixp]
    
    filename = output_folder+'LastYear__local_vs_External_prefixes_to_the_country_hosting_IXP_visible_at_'+ CC_key+'.txt'
    
    
    if os.path.isfile(filename):
        
        print 'file exists'

    else:
        
        with open(filename, 'a') as fd:
            fd.write('%s;%s;%s;%s;%s;%s\n'%('CC',  'month-Year', 'Number of prefixes assigned to the country visibles at the IXP', 'Number of prefixes visibles at the IXP', 'Percentage of local prefixes', 'Percentage of External prefixes' ))


    filename = output_folder+'MultiYear__local_vs_External_prefixes_to_the_country_hosting_IXP_visible_at_'+ CC_key+'.txt'
    
    
    if os.path.isfile(filename):
        
        print 'file exists'

    else:
        
        with open(filename, 'a') as fd:
            
            fd.write('%s;%s;%s;%s;%s;%s\n'%('CC',  'Year', 'Number of prefixes assigned to the country visibles at the IXP', 'Number of prefixes visibles at the IXP', 'Percentage of local prefixes', 'Percentage of External prefixes' ))




#### Separating Local from External prefixes
CC_done = []

for ixp in IXP_collector.keys():
    
  CC_key = IXP_CC[ixp]
    
  if CC_key not in CC_done:

    CC_done.append(CC_key)

    current_CC = CC_key
    
    if CC_key in month_prefix.keys():
        
        filename = output_folder+'LastYear__local_vs_External_prefixes_to_the_country_hosting_IXP_visible_at_'+CC_key+'.txt'
        
        for id_month_and_year in month_prefix[CC_key].keys():
            
            print month_prefix[CC_key].keys()
            
            if len(month_prefix[CC_key][id_month_and_year]) > 0:
                #create_output_lastyear.write(elmt+ '; '+ str(len(month_prefix[ixp][elmt])) + '\n')
                set_ASNs = copy.deepcopy(month_prefix[CC_key][id_month_and_year])
                ## Classify and put numbers.
                
                
                ## Local: Allows to find all prefixes that are local the country of the IXP and assigned by Afrinic in the prefixes visiblea as the IXP;
                ## here we just consider exact prefixes advertised. What about overlaps ?
                intersection = list(set(month_prefix[CC_key][id_month_and_year]) & set(CC_ASNs_AFRINIC[current_CC]))
            
                ### We now treat all the overlaps that are not in the intersection list
                for prefix_adv in list(set(month_prefix[CC_key][id_month_and_year])):
                    if prefix_adv != '0.0.0.0/0' and 'None' not in prefix_adv:
                        if prefix_adv not in intersection:
                            prefix_AF_adv  = ipaddr.IPNetwork(str(prefix_adv))
                            try:
                                for prefix_assigned in list(set(CC_ASNs_AFRINIC[current_CC])):
                                    if prefix_assigned not in intersection and prefix_assigned != '0.0.0.0/0':
                                        prefix_AF_assigned = ipaddr.IPNetwork(str(prefix_assigned))
                                        
                                        if cidrsOverlap(prefix_AF_adv, prefix_AF_assigned):
                                        #if prefix_AF_adv.overlaps(prefix_AF_assigned):
                                            print prefix_AF_adv, ' overlaps ', prefix_AF_assigned
                                            intersection.append(prefix_assigned)
                            except:
                                pass
                    
        
                if '0.0.0.0/0' in intersection:
                    intersection.remove('0.0.0.0/0')
                                                
                if '0.0.0.0/0' in CC_ASNs_AFRINIC[current_CC]:
                    CC_ASNs_AFRINIC[current_CC].remove('0.0.0.0/0')
                                                        
                if '0.0.0.0/0' in month_prefix[CC_key][id_month_and_year]:
                    month_prefix[CC_key][id_month_and_year].remove('0.0.0.0/0')
                
                if len(intersection) > 0:
                    current_filename = output_folder + 'files_prefixes/Local_AFRINIC_prefixes_' + CC_key + '.txt'
                    for elmt in intersection :
                        with open(current_filename, 'a') as fd:
                            fd.write('%s\n'%(elmt))


                try:
                    ## How many prefixes assigned to current country and seen @ the IXP vs. the total number of Origin ASNs seen @ the IXP
                    percentage_local_AF = 100*(float(len(intersection))/float(len(month_prefix[CC_key][id_month_and_year])))
                except:
                    percentage_local_AF = 0.0
                
                with open(filename, 'a') as fd:
                    #if len(intersection) >0:
                    try:
                        A = pycountry.countries.get(alpha2=current_CC)
                        print 'Acurrent_CC = ', current_CC
                        print 'Aixp = ', ixp
                        print 'Aid_month_and_year = ', id_month_and_year
                        print 'Aintersection = ', intersection
                        print 'Amonth_prefix[ixp] = ', month_prefix[CC_key]
                        print 'Amonth_prefix[ixp][id_month_and_year] = ', month_prefix[CC_key][id_month_and_year]
                        print 'Apercentage_local_AF = ', percentage_local_AF
                        print 'A100-percentage_local_AF = ', 100-percentage_local_AF
                        
                        fd.write('%s;%s;%s;%s;%s;%s\n'%(current_CC,  id_month_and_year, len(intersection), len(month_prefix[CC_key][id_month_and_year]),  percentage_local_AF, 100-percentage_local_AF ))
                    
                    except:
                        print 'current_CC = ', current_CC
                        print 'ixp = ', ixp
                        print 'id_month_and_year = ', id_month_and_year
                        print 'intersection = ', intersection
                        print 'month_prefix[ixp] = ', month_prefix[CC_key]
                        print 'month_prefix[ixp][id_month_and_year] = ', month_prefix[CC_key][id_month_and_year]
                        print 'percentage_local_AF = ', percentage_local_AF
                        print '100-percentage_local_AF = ', 100-percentage_local_AF
                        
                        fd.write('%s;%s;%s;%s;%s;%s\n'%(current_CC, id_month_and_year, len(intersection), len(month_prefix[CC_key][id_month_and_year]),  percentage_local_AF, 100-percentage_local_AF ))





    if ixp in year_prefix.keys():
        
	#CC_key = IXP_CC[ixp]

        filename = output_folder+'MultiYear__local_vs_External_prefixes_to_the_country_hosting_IXP_visible_at_'+ CC_key +'.txt'
        
        for year in yearList:
            #create_output_MultiYear.write(str(year)+ '; '+ str(len(year_prefix[ixp][year]))  + '\n')
            
            ## Classify and put numbers.
            #if len(year_prefix[ixp][year]) > 0:
            set_ASNs = copy.deepcopy(year_prefix[CC_key][year])
                            
            ## Local: Allows to find all prefixes that are local the country of the IXP and assigned by Afrinic in the prefixes visiblea as the IXP;
            ## here we just consider exact prefixes advertised. What about overlaps ?
            intersection = list(set(year_prefix[CC_key][year]) & set(CC_ASNs_AFRINIC[current_CC]))
        
        
            ### We now treat all the overlaps that are not in the intersection list
            for prefix_adv in list(set(year_prefix[CC_key][year])):
                if prefix_adv != '0.0.0.0/0' and 'None' not in prefix_adv :
                    prefix_AF_adv = ipaddr.IPNetwork(str(prefix_adv))
                    try:
                        for prefix_assigned in list(set(CC_ASNs_AFRINIC[current_CC])):
                            if prefix_assigned not in intersection and prefix_assigned != '0.0.0.0/0':
                                prefix_AF_assigned = ipaddr.IPNetwork(str(prefix_assigned))
                                
                                if cidrsOverlap(prefix_AF_adv, prefix_AF_assigned):
                                #if prefix_AF_adv.overlaps(prefix_AF_assigned):
                                    print prefix_AF_adv, ' overlaps ', prefix_AF_assigned
                                    #if prefix_adv not in intersection:
                                    intersection.append(prefix_assigned)
                    except:
                        pass
                        
        
            if '0.0.0.0/0' in intersection:
                intersection.remove('0.0.0.0/0')
            
            if '0.0.0.0/0' in CC_ASNs_AFRINIC[current_CC]:
                CC_ASNs_AFRINIC[current_CC].remove('0.0.0.0/0')
            
            if '0.0.0.0/0' in year_prefix[CC_key][year]:
                year_prefix[CC_key][year].remove('0.0.0.0/0')
        
        
            if len(intersection) > 0:
                current_filename = output_folder + 'files_prefixes/Local_AFRINIC_prefixes_' + CC_key + '.txt'
                for elmt in intersection :
                    with open(current_filename, 'a') as fd:
                        fd.write('%s\n'%(elmt))
                            
            try:
                ## How many ASNs assigned to current country and seen @ the IXP vs. the total number of Origin ASNs seen @ the IXP
                percentage_local_AF = 100*(float(len(intersection))/float(len(year_prefix[CC_key][year])))
            except:
                percentage_local_AF = 0.0
            
            
            with open(filename, 'a') as fd:
                #if len(intersection) >0:
                    try:
                        A = pycountry.countries.get(alpha2=current_CC)
                        fd.write('%s;%s;%s;%s;%s;%s\n'%(current_CC,  year, len(intersection), len(year_prefix[CC_key][year]),  percentage_local_AF, 100-percentage_local_AF ))
                    
                    except:
                        fd.write('%s;%s;%s;%s;%s;%s\n'%(current_CC,  year, len(intersection), len(year_prefix[CC_key][year]),  percentage_local_AF, 100-percentage_local_AF ))


log_file_instance.close()
now_datetime = str(datetime.now()).replace(' ', '_')
finish = open ('finish_lastyear_better.txt', 'w')
finish.write('ended' + '; ' +  root_folder + output_folder[6:] + '; ' + now_datetime)
finish.close()
