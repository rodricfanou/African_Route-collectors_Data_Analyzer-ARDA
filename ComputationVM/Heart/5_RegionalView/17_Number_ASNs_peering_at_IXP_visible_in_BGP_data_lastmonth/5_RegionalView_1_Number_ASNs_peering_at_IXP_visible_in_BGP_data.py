from __future__ import division
# Percentage of Origin/Peering ASNs assigned to the region that are visible at all IXPs: What Afrinic has given to Africa ?
# Of all these ASNs how many assigned by Afrinic is peering at at least one IXP.

# If it get to a 100% Afrinic can say that all its prefixes are visibles at an IXP in Africa.

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
from time import sleep
from collections import Counter
import select, socket
import urllib2, urllib
import GeoIP
import ipaddr, logging
import gzip
from datetime import date
from datetime import datetime


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


##
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
region = DB_configuration.region
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




root_folder = '/home/roderick/Heart/'

output_folder = '../../Computation_outputs_Regional_View/17_Number_ASNs_peering_at_IXP_visible_in_BGP_data_lastmonth/'

IXPView_output_folder = '/var/www/html/ARP/controleurs/scripts/ARP_visual/outputs/17_Number_ASNs_peering_at_IXP_visible_in_BGP_data_lastmonth/'



command = 'rm -rf ' + output_folder
os.system(command)

command = 'mkdir  ' + output_folder
os.system(command)

command = 'chmod 777 ' + output_folder
os.system(command)



log_file_instance = open(location_logfile+'/'+name_log_file, 'a')

#print IXP_collector

if os.listdir(IXPView_output_folder) != []:
    
    Unik_list_peering_ASNs = []
    
    for ixp in IXP_collector.keys():
        
        filename_peering =  'LastMonth__list_visible_ASNs_peering_at_IXP_' + ixp + '.txt'
        

        if os.path.exists(IXPView_output_folder + filename_peering) :
            
            List_timestamps = []
        
            with open(IXPView_output_folder  + filename_peering, 'r') as fd:
                
                for line in fd:
                    
                    tab = line.split('; ')
                    
                    if '###' not in line and len(tab) > 1:
                        
                        try:
                        
                            ASN = int(tab[-1])
                        
                            if int(tab[1]) not in List_timestamps:
                            
                                List_timestamps.append(tab[1])
                    
                    
                            if int(tab[2]) not in List_timestamps:
                            
                                List_timestamps.append(tab[2])
                        
                        
                            if ASN not in Unik_list_peering_ASNs:
                            
                                Unik_list_peering_ASNs.append(ASN)

                        except:

                            pass


create_output = open(output_folder + 'LastMonth__infos_peering_ASNs.txt', 'a')

print 'len(Unik_list_peering_ASNs) = ', len(Unik_list_peering_ASNs)


filename_output_ASNs = output_folder + 'List_ASNs_peering_at_an_African_IXP.txt'

with open (filename_output_ASNs, 'a') as fg:
    for elmt in Unik_list_peering_ASNs:
        fg.write('%s\n' %(elmt))


create_output.write('Number of ASNs peering at an African IXP ; ' + str(len(Unik_list_peering_ASNs)) + ' \n')


## Get list of allocated ASNs by Afrinic
## connect to the DB
Current_db = 'RIRs'
db = MySQLdb.connect(host = DB_configuration.host, user = DB_configuration.user, passwd= DB_configuration.passwd,  db = Current_db)
cur = db.cursor()

query = "select distinct ASN, CC from ASNs_"+region+" where (status = 'allocated' or status = 'assigned') ;"
print 'query = ',  query
cur.execute (query)
data = cur.fetchall()
i = 0

ASNs_AFRINIC = []

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
        
        if asn not in ASNs_AFRINIC:
            ASNs_AFRINIC.append(asn)

        i +=1





filename_output_ASNs_by_AFRINIC = output_folder + 'List_ASNs_assigned_by_Afrinic.txt'

with open (filename_output_ASNs_by_AFRINIC, 'a') as fg:
    
    for elmt in ASNs_AFRINIC:
        
        fg.write('%s\n' %(elmt))

print 'ASNs_AFRINIC = ', len(ASNs_AFRINIC)

create_output.write('Number of ASNs assigned by Afrinic ; ' + str(len(ASNs_AFRINIC)) + ' \n')




## Compute percentage

Num_identical = []

with open (output_folder + 'List_ASNs_assigned_by_Afrinic_visibles_at_IXP.txt', 'a') as fh:

    for elmt1 in Unik_list_peering_ASNs:

        if elmt1 in ASNs_AFRINIC:
            
            if elmt1 not in Num_identical:

                Num_identical.append(elmt1)

                fh.write('%s\n' %(elmt1))

percentage = (100*len(Num_identical)) / len(ASNs_AFRINIC)


print
print 'Num_identical = ', len(Num_identical)
print
print 'Percentage peering ASNs = ', percentage


log_file_instance.write( str(now_datetime)+ ' End computation \n')


date1  = datetime.fromtimestamp( int(List_timestamps[0])).strftime('%Y-%m-%d %H:%M:%S')

create_output.write('Timestamp beg ; ' + str(List_timestamps[0]) + ' ; ' + str(date1) + ' \n')

date2  = datetime.fromtimestamp( int(List_timestamps[1])).strftime('%Y-%m-%d %H:%M:%S')

create_output.write('Timestamp end ; ' + str(List_timestamps[1]) + ' ; ' + str(date2) + ' \n')

create_output.write('Number of ASNs assigned by Afrinic peering at an African IXP ; ' + str(len(Num_identical)) + ' \n')

create_output.write('Percentage ASNs assigned by Afrinic peering at an IXP ; ' + str(percentage) + ' \n')

create_output.close()

log_file_instance.close()


finish = open ('finish_lastmonth.txt', 'w')
finish.write('ended' + '; ' +  root_folder + output_folder[6:])
finish.close()


