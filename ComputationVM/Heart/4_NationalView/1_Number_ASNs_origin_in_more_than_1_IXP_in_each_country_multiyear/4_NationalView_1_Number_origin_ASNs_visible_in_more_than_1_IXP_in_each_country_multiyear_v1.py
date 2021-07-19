
##############################################################################
#__author__ = "Roderick Fanou"
#__status__ = "Production"
#__description__ = "This script generates "
#__last_modifications__ =
# by Roderick
#"2016-10-05"
#1- Fetching continent from the configuration file
#2- detail what every column represents in the output files
##############################################################################

finish = open ('finish_multiyear.txt', 'w')
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
name_log_file = 'Log_'+str(now_datetime) + '_' + 'RegionalView_1_Number_origin_ASNs_visible_at_an_IXP_lastyear_each_country' + '.txt'
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
IXP_collector = {}
IXP_CC = {}
week_ASN = {}
week_ASN_2bytes = {}
week_ASN_4bytes = {}


Current_db = 'MergedData'
## connect to the DB
db = MySQLdb.connect(host="localhost",user="",passwd="",  db = Current_db)
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
    
    if row[2] not in week_ASN.keys():
        week_ASN[row[2]] = {}
        week_ASN_2bytes[row[2]] = {}
        week_ASN_4bytes[row[2]] = {}
    
    IXP_collector[row[0]].append(row[1])
    i+=1



print 'IXP_collector = ', IXP_collector

print

print 'IXP_CC = ', IXP_CC

print

print 'week_ASN = ', week_ASN

root_folder = '/home/African_Route-collectors_Data_Analyzer-ARDA/ComputationVM/Heart/'

output_folder = '../../Computation_outputs_National_View/1_Number_ASNs_origin_in_more_than_1_IXP_per_country_multiyear/'

## Update the folder with the selected repository
IXPView_output_folder = '/var/www/html/.../outputs/2_Number_Origin_ASNs_visibles_at_an_IXP_multiyear_lastyear/'


command = 'rm -rf ' + output_folder
os.system(command)

command = 'mkdir  ' + output_folder
os.system(command)

command = 'chmod 777 ' + output_folder
os.system(command)



if os.listdir(IXPView_output_folder) != []:
    
    for ixp in IXP_collector.keys():
        
        CC_to_consider = IXP_CC[ixp]
        
        filename = IXPView_output_folder + """MultiYear__list_visible_ASNs_at_IXP_""" + ixp + '.txt'

        if os.path.isfile(filename):
        
            with open(filename, 'r') as fg:
                
                for line in fg:
                    
                    line = line.strip()
                    
                    tab = line.split('; ')
                    
                    couple_timestamp = '; '.join( tab )
                    
                    if '#' not in line:
                            
                        ASN_to_add = int(tab[-1])
                    
                        del(tab[-1])
            
                        couple_timestamp = '; '.join( tab )
                        
                        if couple_timestamp not in week_ASN[CC_to_consider]:
                            
                            week_ASN[CC_to_consider][couple_timestamp] = []

                        if ASN_to_add not in week_ASN[CC_to_consider][couple_timestamp]:

                            week_ASN[CC_to_consider][couple_timestamp].append(ASN_to_add)


    
#print 'week_ASN = '
#pprint(week_ASN)



####### 2 bytes ASNs

for CC in week_ASN:
    
    with open (output_folder +'MultiYear__list_visible_ASNs_origin_at_IXP_' + CC + '.txt', 'a') as fh:
    
        fh.write('%s\n' %("""###Year; Visible origin ASNs at the IXP"""))
    
    for couple_timestamp in week_ASN[CC].keys():
        
        for elmt in week_ASN[CC][couple_timestamp]:

            with open (output_folder +'MultiYear__list_visible_ASNs_origin_at_IXP_' + CC + '.txt', 'a') as fh:
        
                fh.write('%s; %s\n' %(couple_timestamp, str(elmt) ))



### Compute the unique total number of Origin_ASNs that are 2bytes  per week over the last month



for ixp in IXP_collector.keys():
    
    CC_to_consider = IXP_CC[ixp]
    
    if os.path.isfile (output_folder + 'MultiYear__2bytes_list_origin_ASNs_in_more_than_1_IXP_in_' + CC_to_consider + '.txt'):
        
        create_output_2bytesASN_list = open(output_folder+'MultiYear__2bytes_list_origin_ASNs_in_more_than_1_IXP_in_' + CC_to_consider + '.txt', 'a')
    
    else:
    
        create_output_2bytesASN_list = open(output_folder+'MultiYear__2bytes_list_origin_ASNs_in_more_than_1_IXP_in_' + CC_to_consider + '.txt', 'a')
        
        create_output_2bytesASN_list.write('###Year; Visible 2bytes origin ASNs at more than 1 IXP \n')

    
    filename = IXPView_output_folder+ """MultiYear__2bytes_list_visible_ASNs_at_IXP_""" + ixp + '.txt'
    
    if os.path.isfile(filename):
    
        with open(filename, 'r') as fg:
        
            for line in fg:

                line = line.strip()

                tab = line.split('; ')
    
                couple_timestamp = '; '.join( tab )

                if '#' not in line:
                    
                    ASN_to_add  = int(tab[-1])
                    
                    del(tab[-1])
                    
                    couple_timestamp = '; '.join( tab )
                    
                    if couple_timestamp not in week_ASN_2bytes[CC_to_consider]:
                        
                        week_ASN_2bytes[CC_to_consider][couple_timestamp] = []
                
                    if ASN_to_add not in week_ASN_2bytes[CC_to_consider][couple_timestamp]:
                        
                        week_ASN_2bytes[CC_to_consider][couple_timestamp].append(ASN_to_add)
                        
                        to_add  = str(couple_timestamp) + '; ' + str(ASN_to_add) + '\n'
                        
                        create_output_2bytesASN_list.write(to_add)


print

print 'week_ASN_2bytes = '
pprint(week_ASN_2bytes)








### Compute the unique total number of Origin_ASNs that are 2bytes  per week over the last month

for ixp in IXP_collector.keys():
    
    CC_to_consider = IXP_CC[ixp]
    
    if os.path.isfile (output_folder + 'MultiYear__4bytes_list_origin_ASNs_in_more_than_1_IXP_in_' + CC_to_consider + '.txt'):
        
        create_output_4bytesASN_list = open(output_folder+'MultiYear__4bytes_list_origin_ASNs_in_more_than_1_IXP_in_' + CC_to_consider + '.txt', 'a')

    else:
        
        create_output_4bytesASN_list = open(output_folder+'MultiYear__4bytes_list_origin_ASNs_in_more_than_1_IXP_in_' + CC_to_consider + '.txt', 'a')
        
        create_output_4bytesASN_list.write('###MYear; Visible 2bytes origin ASNs at more than 1 IXP \n')


    
    filename = IXPView_output_folder+ """MultiYear__4bytes_list_visible_ASNs_at_IXP_""" + ixp + '.txt'
    
    if os.path.isfile(filename):
        
        with open(filename, 'r') as fg:
            
            for line in fg:
                
                line = line.strip()
                
                tab = line.split('; ')
                
                couple_timestamp = '; '.join( tab )
                
                if '#' not in line:
                    
                    ASN_to_add  = int(tab[-1])
                    
                    del(tab[-1])
                    
                    couple_timestamp = '; '.join( tab )
                    
                    if couple_timestamp not in week_ASN_4bytes[CC_to_consider]:
                        
                        week_ASN_4bytes[CC_to_consider][couple_timestamp] = []
                    
                    if ASN_to_add not in week_ASN_4bytes[CC_to_consider][couple_timestamp]:
                        
                        week_ASN_4bytes[CC_to_consider][couple_timestamp].append(ASN_to_add)
                        
                        to_add  = str(couple_timestamp) + '; ' + str(ASN_to_add) + '\n'
                        
                        create_output_4bytesASN_list.write(to_add)


print

print 'week_ASN_4bytes = '
pprint(week_ASN_4bytes)


for CC in week_ASN:
    
    with open (output_folder + 'MultiYear__number_visible_origin_ASNs_in_more_than_1_IXP_of_' + CC + '.txt', 'a') as fg:

        fg.write('%s\n' %("""###Year; Number of Visible origin ASNs; Number of Visible origin 2bytes ASNs; Number of Visible origin 4bytes ASNs;"""))
        
        for couple_timestamp in week_ASN[CC].keys():
            
            if couple_timestamp in week_ASN_4bytes[CC].keys() and  couple_timestamp in week_ASN_2bytes[CC].keys():
            
                fg.write('%s; %s; %s; %s\n' %( couple_timestamp, len(week_ASN[CC][couple_timestamp]), len(week_ASN_2bytes[CC][couple_timestamp]), len(week_ASN_4bytes[CC][couple_timestamp])))

            elif couple_timestamp not in week_ASN_4bytes[CC].keys() and  couple_timestamp in week_ASN_2bytes[CC].keys():
    
                fg.write('%s; %s; %s; %s\n' %( couple_timestamp, len(week_ASN[CC][couple_timestamp]), len(week_ASN_2bytes[CC][couple_timestamp]), '0'))

            elif couple_timestamp in week_ASN_4bytes[CC].keys() and  couple_timestamp not in week_ASN_2bytes[CC].keys():
    
                fg.write('%s; %s; %s; %s\n' %( couple_timestamp, len(week_ASN[CC][couple_timestamp]), '0' , len(week_ASN_4bytes[CC][couple_timestamp])))


now_datetime = str(datetime.now()).replace(' ', '_')
finish = open ('finish_multiyear.txt', 'w')
finish.write('ended' + '; ' +  root_folder + output_folder[6:] + '; ' + now_datetime )
finish.close()


