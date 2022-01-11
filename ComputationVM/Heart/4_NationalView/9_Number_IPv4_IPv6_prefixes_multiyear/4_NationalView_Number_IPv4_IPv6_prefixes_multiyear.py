##############################################################################
#__author__ = "Roderick Fanou"
#__status__ = "Production"
#__description__ = "This script generates "
#__last_modifications__ =
# by Roderick
#"2016-11-28"
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
import urllib.request, urllib.error, urllib.parse, urllib.request, urllib.parse, urllib.error
import GeoIP
import ipaddr, logging
import gzip
from datetime import date
from datetime import datetime
import os.path


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

## Create a logfile:
name_log_file = 'Log_'+str(now_datetime) + '_' + 'NationalView_1_Number_ASNs_announcing_v4_v6_lastyear_each_country' + '.txt'
location_logfile = create_Logfiles_folder()


### Define timelines and timescales
## multi-years splitted into years
yearList = multiyear()
print(yearList)


## last month (Now - 4weeks) splitted into weeks
lastYearList = lastyear()
print(lastYearList)


## last month (Now - 4weeks) splitted into weeks
lastMonthList = lastmonth()
print(lastMonthList)

## Other initialisations
continent = DB_configuration.continent
IXP_collector = {}
IXP_CC = {}

week_ASN_announcing_v4 = {}
week_ASN_announcing_v6 = {}

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
    
    if row[2] not in list(week_ASN_announcing_v4.keys()):
        week_ASN_announcing_v4[row[2]] = {}
        week_ASN_announcing_v6[row[2]] = {}
    
    IXP_collector[row[0]].append(row[1])
    i+=1



print('IXP_collector = ', IXP_collector)

print()

print('IXP_CC = ', IXP_CC)



root_folder = '/home/arda/African_Route-collectors_Data_Analyzer-ARDA/ComputationVM/Heart/'

output_folder = '../../Computation_outputs_National_View/9_Number_IPv4_IPv6_prefixes_lastyear_each_country/'

## Update the folder with the selected repository
IXPView_output_folder = '/var/www/html/.../outputs/9_Number_IPv6_vs_IPv4_prefixes_multiyear/'



command = 'rm -rf ' + output_folder
os.system(command)

command = 'mkdir  ' + output_folder
os.system(command)

command = 'chmod 777 ' + output_folder
os.system(command)




if os.listdir(IXPView_output_folder) != []:
    
    #print 'folder exists'
    
    for ixp in list(IXP_collector.keys()):
        
        CC_to_consider = IXP_CC[ixp]
        
        filename = IXPView_output_folder + """MultiYear_"""+ ixp + """_List_ASNs_announcing_v4.txt"""
        
        if os.path.isfile(filename):
            
            #print 'file ', filename , ' exists'
            
            with open(filename, 'r') as fg:
                
                for line in fg:
                    
                    #print ixp, filename,  line
                    
                    line = line.strip()
                    
                    tab = line.split('; ')
                    
                    couple_timestamp = '; '.join( tab )
                    
                    if '#' not in line:
                        
                        ASN_to_add = int(tab[-1])
                        
                        del(tab[-1])
                        
                        print()
                        
                        print(tab)
                        
                        while tab[-1] == '' or tab[-1] == ';' :
                            
                            del(tab[-1])
                        
                        print(tab)
                        
                        couple_timestamp = '; '.join( tab )
                        
                        if couple_timestamp not in week_ASN_announcing_v4[CC_to_consider]:
                            
                            week_ASN_announcing_v4[CC_to_consider][couple_timestamp] = []
                    
                        if ASN_to_add not in week_ASN_announcing_v4[CC_to_consider][couple_timestamp]:
                            
                            week_ASN_announcing_v4[CC_to_consider][couple_timestamp].append(ASN_to_add)


#print
#print 'week_ASN_announcing_v4 = ', week_ASN_announcing_v4


if os.listdir(IXPView_output_folder) != []:
    
    for ixp in list(IXP_collector.keys()):
        
        CC_to_consider = IXP_CC[ixp]
        
        filename = IXPView_output_folder + """MultiYear_"""+ ixp + """_List_ASNs_announcing_v6.txt"""
        
        if os.path.isfile(filename):
            
            with open(filename, 'r') as fg:
                
                for line in fg:
                    
                    line = line.strip()
                    
                    tab = line.split('; ')
                    
                    couple_timestamp = '; '.join( tab )
                    
                    if '#' not in line:
                        
                        ASN_to_add = int(tab[-1])
                        
                        del(tab[-1])
                        
                        print()
                        
                        print(tab)
                        
                        while tab[-1] == '' or tab[-1] == ';' :
                            
                            del(tab[-1])
                        
                        print(tab)
                        
                        couple_timestamp = '; '.join( tab )
                        
                        if couple_timestamp not in week_ASN_announcing_v6[CC_to_consider]:
                            
                            week_ASN_announcing_v6[CC_to_consider][couple_timestamp] = []
                        
                        if ASN_to_add not in week_ASN_announcing_v6[CC_to_consider][couple_timestamp]:
                            
                            week_ASN_announcing_v6[CC_to_consider][couple_timestamp].append(ASN_to_add)


#print
#print 'week_ASN_announcing_v6 = ', week_ASN_announcing_v6







for CC in week_ASN_announcing_v6:
    
    
    with open (output_folder +'MultiYear__list_ASNs_announcing_v6_at_IXPs_in_' + CC + '.txt', 'a') as fh:
        
        fh.write('%s\n' %("""###Month-Year; ASNs announcing v6 prefixes"""))
    
    for couple_timestamp1 in list(week_ASN_announcing_v6[CC].keys()):
        
        for elmt2 in week_ASN_announcing_v6[CC][couple_timestamp1]:
            
            with open (output_folder +'MultiYear__list_ASNs_announcing_v6_at_IXPs_in_' + CC + '.txt', 'a') as fh:
                
                fh.write('%s; %s\n' %(couple_timestamp1, str(elmt2) ))





for CC in week_ASN_announcing_v4:
    
    
    with open (output_folder +'MultiYear__list_ASNs_announcing_v4_at_IXPs_in_' + CC + '.txt', 'a') as fh:
        
        fh.write('%s\n' %("""###Month-Year; ASNs announcing v4 prefixes"""))
    
    for couple_timestamp in list(week_ASN_announcing_v4[CC].keys()):
        
        for elmt1 in week_ASN_announcing_v4[CC][couple_timestamp]:
            
            with open (output_folder +'MultiYear__list_ASNs_announcing_v4_at_IXPs_in_' + CC + '.txt', 'a') as fh:
                
                fh.write('%s; %s\n' %(couple_timestamp, str(elmt1) ))




    with open (output_folder +'MultiYear__Number_ASNs_announcing_v4_v6_at_IXPs_in_' + CC + '.txt', 'a') as fh:
    
        fh.write('%s\n' %("""###Month-Year; Number ASNs announcing v4 prefixes; Number ASNs announcing v6 prefixes"""))
    
    for couple_timestamp in list(week_ASN_announcing_v4[CC].keys()):
        
        with open (output_folder +'MultiYear__Number_ASNs_announcing_v4_v6_at_IXPs_in_' + CC + '.txt', 'a') as fh:

            if couple_timestamp not in list(week_ASN_announcing_v6[CC].keys()):

                fh.write('%s; %s; %s\n' %(couple_timestamp, len(week_ASN_announcing_v4[CC][couple_timestamp]), ' 0' ))
                                        
            else:
                                        
                fh.write('%s; %s; %s\n' %(couple_timestamp, len(week_ASN_announcing_v4[CC][couple_timestamp]), len(week_ASN_announcing_v6[CC][couple_timestamp]) ))



finish = open ('finish_lastmonth.txt', 'w')
finish.write('ended' + '; ' +  root_folder + output_folder[6:])
finish.close()





