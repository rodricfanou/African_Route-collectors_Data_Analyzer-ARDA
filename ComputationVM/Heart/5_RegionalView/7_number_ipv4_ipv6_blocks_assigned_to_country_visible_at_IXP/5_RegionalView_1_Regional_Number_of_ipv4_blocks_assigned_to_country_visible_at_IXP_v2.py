
##############################################################################
#__author__ = "Roderick Fanou"
#__status__ = "Production"
#__description__ = "This script generates "
#__last_modifications__ = by Roderick on "2016-10-25"
## description:
## Extracts Percentage of v4 prefixes attributed by AFRINIC seen at 1 or more IXP in Africa
## Extracts Percentage of v6 prefixes attributed by AFRINIC seen at 1 or more IXP in Africa
## Modifications
#1- Fetching continent from the configuration file
#2- detail what every column represents in the output files
##############################################################################

finish = open ('finish.txt', 'w')
finish.write('started')
finish.close()


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
import urllib.request, urllib.error, urllib.parse, urllib.request, urllib.parse, urllib.error
import GeoIP
import ipaddr, logging
import gzip
from datetime import date
from datetime import datetime
from netaddr import *


## import all files in the library you need
sys.path.append('../../2_libraries/')
import ipaddress
import DB_configuration
import bgp_rib
from define_timescales import *
from functions import *



now_datetime = str(datetime.now()).replace(' ', '_')

## Create a logfile:
name_log_file = 'Log_'+str(now_datetime) + '_' + '1_RegionalView_Number_of_ipv4_blocks_assigned_to_country_visible_at_IXP' + '.txt'
location_logfile = create_Logfiles_folder()

### Define timelines and timescales
## multi-years splitted into years
yearList = multiyear()
print(yearList)

## last month (Now - 12Months) splitted into months
lastYearList = lastyear()
print(lastYearList)

## last month (Now - 4weeks) splitted into months
lastMonthList = lastmonth()
print(lastMonthList)


## Other initialisations
continent = DB_configuration.continent
IXP_collector = {}
IXP_CC = {}



Current_db = 'MergedData'
## connect to the DB
db = MySQLdb.connect(host = "localhost", user = "", passwd = "",  db = Current_db)
cur = db.cursor()
print('Connected')

query = "select IXP, RouteCollector, CC from AllRouteCollectors where Continent = '"+continent+"';"
cur.execute(query)
data = cur.fetchall()
i = 0
while (i<len(data)):
    row = data[i]
    if row[0] not in list(IXP_collector.keys()):
        IXP_collector[row[0]] = []
        IXP_CC[row[0]] = row[2]
    IXP_collector[row[0]].append(row[1])
    i+=1



print(IXP_collector)

print()

#print IXP_CC

root_folder = '/home/arda/African_Route-collectors_Data_Analyzer-ARDA/ComputationVM/Heart/'

output_folder = '../../Computation_outputs_Regional_View/7_number_ipv4_ipv6_blocks_assigned_to_country_visible_at_IXP/'

## Update the folder with the selected repository
IXPView_output_folder = '/var/www/html/.../outputs/7_percentage_IP_blocks_assigned_to_country_visible_at_IXP/'

command = 'rm -rf ' + output_folder
os.system(command)

command = 'mkdir  ' + output_folder
os.system(command)

command = 'chmod 777 ' + output_folder
os.system(command)


List_prefixes_v4_all = []

List_prefixes_v6_all = []


if os.listdir(IXPView_output_folder) != []:
 
    folder_v4 = IXPView_output_folder + 'Percentage_IPv4_assigned_to_country_appearing_per_IXP/'

    folder_v6 = IXPView_output_folder + 'Percentage_IPv6_assigned_to_country_appearing_per_IXP/'
    
    #print folder_v4

    #print folder_v6

    for ixp in list(IXP_CC.keys()):
        
        filename_v4 = folder_v4 + 'List_prefixes_assigned_advertised_' + ixp + '_' + IXP_CC[ixp] + '.txt'
        
        filename_v6 = folder_v6 + 'List_prefixes_assigned_advertised_' + ixp + '_' + IXP_CC[ixp] + '.txt'

        #print ixp, IXP_CC
        
        if os.path.exists(filename_v4):

            with open (filename_v4, 'r') as fgh:

                for line in fgh:

                    line = line.strip()

                    if line not in List_prefixes_v4_all:
        
                        List_prefixes_v4_all.append(line)


        if os.path.exists(filename_v6):

            with open (filename_v6, 'r') as fgh:
        
                for line in fgh:
            
                    line = line.strip()
                
                    if line not in List_prefixes_v6_all:

                        List_prefixes_v6_all.append(line)



### cross check in each list if there are duplicates

List_prefixes_v4_all_cross_check = copy.deepcopy(List_prefixes_v4_all)

for ip_prefix in List_prefixes_v4_all:

    ip_prefix_IX_o = ipaddr.IPNetwork(str(ip_prefix))
    
    for ip_prefix1 in List_prefixes_v4_all:
        
        if ip_prefix != ip_prefix1:
        
            ip_prefix_IX_o1 = ipaddr.IPNetwork(str(ip_prefix1))
                
            if ip_prefix_IX_o.overlaps(ip_prefix_IX_o1) and ip_prefix != '0.0.0.0/0':
                
                print(ip_prefix_IX_o, ' overlaps ', ip_prefix_IX_o1)
                
                if ip_prefix in List_prefixes_v4_all_cross_check:
                    
                    List_prefixes_v4_all_cross_check.remove(ip_prefix)


print('len( List_prefixes_v4_all_cross_check) =', len( List_prefixes_v4_all_cross_check))
print()


List_prefixes_v6_all_cross_check = copy.deepcopy(List_prefixes_v6_all)

for ip_prefix in List_prefixes_v6_all:
    
    ip_prefix_IX_o = ipaddr.IPNetwork(str(ip_prefix))
    
    for ip_prefix1 in List_prefixes_v6_all:
        
        if ip_prefix != ip_prefix1:
        
            ip_prefix_IX_o1 = ipaddr.IPNetwork(str(ip_prefix1))
            
            if ip_prefix_IX_o.overlaps(ip_prefix_IX_o1) and ip_prefix != '0.0.0.0/0':
                
                print(ip_prefix_IX_o, ' overlaps ', ip_prefix_IX_o1)
                
                if ip_prefix in List_prefixes_v6_all_cross_check:
                    
                    List_prefixes_v6_all_cross_check.remove(ip_prefix)


print('len(List_prefixes_v6_all_cross_check) =', len(List_prefixes_v6_all_cross_check))
print()


### list all prefixes in output.

with open (output_folder +'List_v4_prefixes_assigned_advertised_at_1IXP_or_more.txt', 'a') as fgh:
    
    for prefixes in List_prefixes_v4_all_cross_check:
    
        fgh.write('%s\n' %(prefixes))



with open (output_folder +'List_v6_prefixes_assigned_advertised_at_1IXP_or_more.txt', 'a') as fgh:
    
    for prefixes in List_prefixes_v6_all_cross_check:
        
        fgh.write('%s\n' %(prefixes))



CC_prefixes_AFRINIC = {}
CC_prefixes_AFRINIC['v4'] = {}
CC_prefixes_AFRINIC['v6'] = {}

## Get all the prefixes from AFRINIC

## collecting AFRINIC Assigned prefixes

Current_db = 'RIRs'
## connect to the DB
db = MySQLdb.connect(host = "localhost", user = "", passwd = "",  db = Current_db)
cur = db.cursor()

Unik_List_prefixes_Afrinic_v4 =  []
## v4
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
            
            if current_CC not in list(CC_prefixes_AFRINIC['v4'].keys()):
                CC_prefixes_AFRINIC['v4'][current_CC] = []
            
            if asn not in CC_prefixes_AFRINIC['v4'][current_CC]:
                CC_prefixes_AFRINIC['v4'][current_CC].append(asn)
    
            if asn not in Unik_List_prefixes_Afrinic_v4:
                Unik_List_prefixes_Afrinic_v4.append(asn)
        i +=1


##v6
query = "select distinct NetIPaddress, NetBits, CC from IPv6_ressources_AFRINIC where status = 'allocated' or status = 'assigned' and CC != '';"
cur.execute (query)
data = cur.fetchall()
i = 0

Unik_List_prefixes_Afrinic_v6 = []

if len(data)>0:
    while (i<len(data)):
        row = data[i]
        asn = row[0]+'/'+row[1]
        current_CC = row[2]
        
        if current_CC != '':
            
            if current_CC not in list(CC_prefixes_AFRINIC['v6'].keys()):
                CC_prefixes_AFRINIC['v6'][current_CC] = []
            
            if asn not in CC_prefixes_AFRINIC['v6'][current_CC]:
                CC_prefixes_AFRINIC['v6'][current_CC].append(asn)
    
            if asn not in Unik_List_prefixes_Afrinic_v6:
                Unik_List_prefixes_Afrinic_v6.append(asn)
                    
        i +=1


#pprint(CC_prefixes_AFRINIC)

#Cross check each list and suppress overlaps

List_AF_prefixes_v4_all_cross_check = copy.deepcopy(Unik_List_prefixes_Afrinic_v4)

for ip_prefix in Unik_List_prefixes_Afrinic_v4:
    
    ip_prefix_IX_o = ipaddr.IPNetwork(str(ip_prefix))
    
    for ip_prefix1 in Unik_List_prefixes_Afrinic_v4:
        
        if ip_prefix != ip_prefix1:
        
            ip_prefix_IX_o1 = ipaddr.IPNetwork(str(ip_prefix1))
            
            if ip_prefix_IX_o.overlaps(ip_prefix_IX_o1) and ip_prefix != '0.0.0.0/0':
                
                print(ip_prefix_IX_o, ' overlaps ', ip_prefix_IX_o1)
                
                if ip_prefix in List_AF_prefixes_v4_all_cross_check:
                    
                    List_AF_prefixes_v4_all_cross_check.remove(ip_prefix)




## List v4 prefixes attributed without overlaps

with open(output_folder +'List_v4_prefixes_attributed_by_AFRINIC.txt', 'a') as fgh:

    for elmt in List_AF_prefixes_v4_all_cross_check:
    
        fgh.write('%s\n' %(elmt))




List_AF_prefixes_v6_all_cross_check = copy.deepcopy(Unik_List_prefixes_Afrinic_v6)

for ip_prefix in Unik_List_prefixes_Afrinic_v6:
    
    ip_prefix_IX_o = ipaddr.IPNetwork(str(ip_prefix))
    
    for ip_prefix1 in Unik_List_prefixes_Afrinic_v6:
        
        if ip_prefix != ip_prefix1:
        
            ip_prefix_IX_o1 = ipaddr.IPNetwork(str(ip_prefix1))
            
            if ip_prefix_IX_o.overlaps(ip_prefix_IX_o1) and ip_prefix != '0.0.0.0/0':
                
                print(ip_prefix_IX_o, ' overlaps ', ip_prefix_IX_o1)
                
                if ip_prefix in List_AF_prefixes_v6_all_cross_check:
                    
                    List_AF_prefixes_v6_all_cross_check.remove(ip_prefix)




## List v6 prefixes attributed without overlaps

with open(output_folder +'List_v6_prefixes_attributed_by_AFRINIC.txt', 'a') as fgh:
    
    for elmt in List_AF_prefixes_v6_all_cross_check:
        
        fgh.write('%s\n' %(elmt))


## Compute the percentages.
try:
    perc_IP_blocks_v4 = 100 * ( float(len( List_prefixes_v4_all_cross_check)) / float( len( List_AF_prefixes_v4_all_cross_check) ) )
except:
    perc_IP_blocks_v4 = 0


try:
    perc_IP_blocks_v6 = 100 * ( float(len(List_prefixes_v6_all_cross_check)) / float(len( List_AF_prefixes_v6_all_cross_check) ) )
except:
    perc_IP_blocks_v6 = 0


with open(output_folder + 'Results_percentages_v4_v6_prefixes.txt', 'a') as fdg:
    
    fdg.write('%s \n' %('##Label; Length List_prefixes_v4_all_cross_check, Length List_AF_prefixes_v4_all_cross_check, Percentage' ))
    
                                    
    print(str(len(List_AF_prefixes_v4_all_cross_check)))
                                    
    fdg.write('%s; %s; %s; %s \n' %('Percentage of v4 prefixes attributed by AFRINIC seen at 1 or more IXP in Africa; ', str(len(List_prefixes_v4_all_cross_check)),  str(len(List_AF_prefixes_v4_all_cross_check)), str(perc_IP_blocks_v4) ))

    print(str(len(List_AF_prefixes_v6_all_cross_check)))
                                    
    fdg.write('%s; %s; %s; %s \n' %('Percentage of v6 prefixes attributed by AFRINIC seen at 1 or more IXP in Africa; ', str(len(List_prefixes_v6_all_cross_check)), str(len(List_AF_prefixes_v6_all_cross_check)), str(perc_IP_blocks_v6)))



now_datetime = str(datetime.now()).replace(' ', '_')
finish = open ('finish.txt', 'w')
finish.write('ended' + '; ' +  root_folder + output_folder[6:] + '; ' + now_datetime)
finish.close()
