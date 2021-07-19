
##############################################################################
#__author__ = "Roderick Fanou"
#__status__ = "Production"
#__description__ = "This script generates "
#__last_modifications__ =
# by Roderick
#"2016-11-28"
##############################################################################

from datetime import date
from datetime import datetime


finish = open ('finish_lastmonth.txt', 'w')
finish.write('started')
finish.close()



def cidrsOverlap(cidr0, cidr1):
    return cidr0 in cidr1 or cidr1 in cidr0



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
name_log_file = 'Log_'+str(now_datetime) + '_' + 'RegionalView_1_Number_prefixes_visible_at_an_IXP_lastmonth_each_country' + '.txt'
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
week_prefix = {}
week_prefix_bogon = {}

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
    
    if row[2] not in week_prefix.keys():
        week_prefix[row[2]] = {}
        week_prefix_bogon[row[2]] = {}

    
    IXP_collector[row[0]].append(row[1])
    i+=1



print 'IXP_collector = ', IXP_collector
print
print 'IXP_CC = ', IXP_CC
print
print 'week_ASN = ', week_prefix

root_folder = '/home/African_Route-collectors_Data_Analyzer-ARDA/ComputationVM/Heart/'

output_folder = '../../Computation_outputs_National_View/3_Number_unique_prefixes_visibles_at_all_IXP_of_a_country_lastmonth/'

## Update the folder with the selected repository
IXPView_output_folder = '/var/www/html/.../outputs/1_Number_prefixes_visibles_at_an_IXP_lastmonth/'



command = 'rm -rf ' + output_folder
os.system(command)

command = 'mkdir  ' + output_folder
os.system(command)

command = 'chmod 777 ' + output_folder
os.system(command)






#num_ixp = 0

if os.listdir(IXPView_output_folder) != []:
    
    for ixp in IXP_collector.keys():
        
        print ixp
        
        #num_ixp += 1
        
        CC_to_consider = IXP_CC[ixp]
        
        filename = IXPView_output_folder + """LastMonth__list_visible_prefixes_at_IXP_""" + ixp + '.txt'

        if os.path.isfile(filename):
            
            with open(filename, 'r') as fg:
                
                for line in fg:
                    
                    line = line.strip()
                        
                    tab = line.split('; ')
                    
                    print tab
                            
                    if '#' not in line:

                        if '/' in tab[-1]:
                            
                            prefix_to_add = tab[-1]
                        
                            print 'prefix = ', prefix_to_add

                            del(tab[-1])
        
                            couple_timestamp = '; '.join( tab )
                            
                            print 'couple_timestamp = ', couple_timestamp
                            
                            print
                            
                            if CC_to_consider not in week_prefix.keys():
                                
                                week_prefix[CC_to_consider] = {}

                            if couple_timestamp not in week_prefix[CC_to_consider].keys():
        
                                week_prefix[CC_to_consider][couple_timestamp] = []
                            
                                ## make sure the prefixes do not overlap
            
                            if prefix_to_add not in week_prefix[CC_to_consider][couple_timestamp]:
                
                                week_prefix[CC_to_consider][couple_timestamp].append(prefix_to_add)


                        elif 'Bogon' in tab[-1] or 'bogon' in tab[-1]:

                            prefix_to_add_bogon = tab[-2]
    
                            print 'Bogon prefix = ', prefix_to_add_bogon
        
                            del(tab[-1])
                            
                            del(tab[-1])
            
                            couple_timestamp_bogon = '; '.join(tab)
                
                            print 'couple_timestamp = ', couple_timestamp_bogon
                    
                            print
                        
                            if CC_to_consider not in week_prefix.keys():
                            
                                week_prefix[CC_to_consider] = {}
                                
                            if CC_to_consider not in week_prefix_bogon.keys():
                            
                                week_prefix_bogon[CC_to_consider] = {}
                            
                            if couple_timestamp_bogon not in week_prefix[CC_to_consider].keys():
                                
                                week_prefix[CC_to_consider][couple_timestamp_bogon] = []
                                
                            if couple_timestamp_bogon not in week_prefix_bogon[CC_to_consider].keys():
                            
                                week_prefix_bogon[CC_to_consider][couple_timestamp_bogon] = []
                        
                                ## make sure the prefixes do not overlap
                            
                            if prefix_to_add_bogon not in week_prefix[CC_to_consider][couple_timestamp_bogon]:
                                
                                week_prefix[CC_to_consider][couple_timestamp_bogon].append(prefix_to_add_bogon)
                                
                            if prefix_to_add_bogon not in week_prefix_bogon[CC_to_consider][couple_timestamp_bogon]:

                                week_prefix_bogon[CC_to_consider][couple_timestamp_bogon].append(prefix_to_add_bogon)


                        else:

                            while '/' not in tab[-1] and len(tab) >= 1:

                                del(tab[-1])

                            if '/' in tab[-1]:
    
                                prefix_to_add = tab[-1]
        
                                print 'prefix = ', prefix_to_add
            
                                del(tab[-1])
                
                                couple_timestamp = '; '.join( tab )
                    
                                print 'couple_timestamp = ', couple_timestamp
                        
                                print
                            
                            if CC_to_consider not in week_prefix.keys():
                                
                                week_prefix[CC_to_consider] = {}
                    
                            if couple_timestamp not in week_prefix[CC_to_consider].keys():
                            
                                week_prefix[CC_to_consider][couple_timestamp] = []
                            
                                ## make sure the prefixes do not overlap
                            
                            if prefix_to_add not in week_prefix[CC_to_consider][couple_timestamp]:
                                
                                week_prefix[CC_to_consider][couple_timestamp].append(prefix_to_add)


                print 'The IXP I treat is ', ixp, ' in ', CC_to_consider

                #if num_ixp == 3:
                    
                #    break





for CC in week_prefix.keys():
    
    with open (output_folder +'LastMonth__list_unique_prefixes_at_IXP_' + CC + '.txt', 'a') as fh:
        
        fh.write('%s\n' %("""###Num Week; Timestamp beginning;  Timestamp end;  Datetime  beginning;  Datetime end; Visible prefixes at the IXP; Bogon?"""))

    for couple_timestamp1 in week_prefix[CC].keys():
        
        for elmt in week_prefix[CC][couple_timestamp1]:
            
            k = 0
            
            if couple_timestamp1 in week_prefix_bogon[CC].keys():
            
                if elmt in week_prefix_bogon[CC][couple_timestamp1]:
            
                    with open (output_folder +'LastMonth__list_unique_prefixes_at_IXP_' + CC + '.txt', 'a') as fh:
                
                        fh.write('%s; %s; %s\n' %(couple_timestamp1, str(elmt), 'bogon'))

                        k = 1
        
            if k == 0:

                with open (output_folder +'LastMonth__list_unique_prefixes_at_IXP_' + CC + '.txt', 'a') as fh:
                
                    fh.write('%s; %s\n' %(couple_timestamp1, str(elmt)))





#### Collect timestamps from number files for CC where there is no info.

if os.listdir(IXPView_output_folder) != []:
    
    for ixp in IXP_collector.keys():
        
        CC_to_consider = IXP_CC[ixp]
        
        if len(week_prefix[CC_to_consider]) == 0:
        
            filename = IXPView_output_folder + """LastMonth__number_visible_prefixes_at_IXP_""" + ixp + '.txt'
            
            if os.path.isfile(filename):
                
                with open(filename, 'r') as fg:
                    
                    for line in fg:
                        
                        if '#' not in line:
                            
                            tab = line.split(';')
                            
                            del(tab[-1])
                            
                            del(tab[-1])
                            
                            
                            couple_timestamp = '; '.join( tab )
                            
                            print 'couple_timestamp = ', couple_timestamp
                            
                            print
                            
                            if CC_to_consider not in week_prefix.keys():
                                
                                week_prefix[CC_to_consider] = {}
                            
                            if couple_timestamp not in week_prefix[CC_to_consider].keys():
                                
                                week_prefix[CC_to_consider][couple_timestamp] = []





for CC in week_prefix.keys():
    
    with open (output_folder +'LastMonth__number_unique_prefixes_at_IXP_' + CC + '.txt', 'a') as fh1:
    
        fh1.write('%s\n' %("""###Num Week; Timestamp beginning;  Timestamp end;  Datetime  beginning;  Datetime end; Number of Visible prefixes at the IXP; Number of Visible Bogon prefixes"""))
    
    for couple_timestamp11 in week_prefix[CC].keys():
        
        if couple_timestamp11 in week_prefix_bogon[CC].keys():
            
            with open (output_folder +'LastMonth__number_unique_prefixes_at_IXP_' + CC + '.txt', 'a') as fh1:
        
                fh1.write('%s; %s; %s\n' %(couple_timestamp11, str(len(week_prefix[CC][couple_timestamp11])), str(len(week_prefix_bogon[CC][couple_timestamp11]))))

        else:

            with open (output_folder +'LastMonth__number_unique_prefixes_at_IXP_' + CC + '.txt', 'a') as fh1:
    
                fh1.write('%s; %s; %s\n' %(couple_timestamp11, str(len(week_prefix[CC][couple_timestamp11])), '0'))





now_datetime = str(datetime.now()).replace(' ', '_')
finish = open ('finish_lastmonth.txt', 'w')
finish.write('ended' + '; ' +  root_folder + output_folder[6:] + '; ' + now_datetime)
finish.close()



