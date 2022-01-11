
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
import urllib.request, urllib.error, urllib.parse, urllib.request, urllib.parse, urllib.error
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




now_datetime = str(datetime.now()).replace(' ', '_')

## Create a logfile:
name_log_file = 'Log_'+str(now_datetime) + '_' + 'RegionalView_1_Number_of_prefixes_visible_at_all_IXPs_multiyear' + '.txt'
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

root_folder = '/home/arda/African_Route-collectors_Data_Analyzer-ARDA/ComputationVM/Heart/'

output_folder = '../../Computation_outputs_Regional_View/3_Number_of_prefixes_visible_at_all_IXPs_multiyear/'

## Update the folder with the selected repository
IXPView_output_folder = '/var/www/html/.../outputs/1_Number_prefixes_visibles_at_an_IXP_multiyear_lastyear/'


command = 'rm -rf ' + output_folder
os.system(command)

command = 'mkdir  ' + output_folder
os.system(command)

command = 'chmod 777 ' + output_folder
os.system(command)





if os.listdir(IXPView_output_folder) != []:

    ### Compute the unique total number of Peering_ASNs that are 2bytes per month over the last year

    year_prefixes = {}
    
    year_bogon_prefixes = {}

    create_output_prefixes_list =  open(output_folder+'MultiYear__list_prefixes_visible_at_all_IXPs.txt', 'a')
    
    create_output_prefixes_list.write('###Year; Visible prefixes at all IXPs; Bogon ? \n')

    Unique_lines = []

    for ixp in list(IXP_collector.keys()):
        
        filename = IXPView_output_folder+ """MultiYear__list_visible_prefixes_at_IXP_""" + ixp + '.txt'
        print('We are treating ', filename)
        
        with open(filename, 'r') as fg:
            for line in fg:
                prefix_to_add = ''
                bogon_to_add = ''
                to_add = line
                line = line.strip()
                tab = line.split('; ')
                tab_key = line.split('; ')
                
                if "#" not in line:
                    
                    #try:
                    
                        if to_add not in Unique_lines :
                            Unique_lines.append(to_add)
                            create_output_prefixes_list.write(to_add)


                        if len(tab_key) == 2:
                            prefix_to_add = tab_key[-1]
                            del(tab_key[-1])
                            key_timestamp = '; '.join(tab_key)
                        
                        elif len(tab_key) == 3:
                            prefix_to_add = tab_key[-2]
                            bogon_to_add = tab_key[-2]
                            del(tab_key[-1])
                            del(tab_key[-1])
                            key_timestamp = '; '.join(tab_key)
                    
                        if key_timestamp not in list(year_prefixes.keys()):
                            year_prefixes[key_timestamp] = []
                        
                        if key_timestamp not in list(year_bogon_prefixes.keys()):
                            year_bogon_prefixes[key_timestamp] = []
                        
                        if  prefix_to_add != '':
                            if prefix_to_add not in year_prefixes[key_timestamp]:
                                year_prefixes[key_timestamp].append(prefix_to_add)

                        if  bogon_to_add != '':
                            if bogon_to_add not in year_bogon_prefixes[key_timestamp]:
                                year_bogon_prefixes[key_timestamp].append(bogon_to_add)
    
                    #except:
                    #    pass



with open (output_folder + 'MultiYear__number_prefixes_visible_at_all_IXPs.txt', 'a') as fg:
    
    fg.write('%s\n' %("""###Year; Number of Visible prefixes; Number of Visible bogon prefixes;"""))
    
    for key_timestamp in list(year_prefixes.keys()):
        
        fg.write('%s; %s; %s\n' %(key_timestamp, len(year_prefixes[key_timestamp]), len(year_bogon_prefixes[key_timestamp])))


now_datetime = str(datetime.now()).replace(' ', '_')
finish = open ('finish_multiyear.txt', 'w')
finish.write('ended' + '; ' +  root_folder + output_folder[6:] + '; ' + now_datetime)
finish.close()
