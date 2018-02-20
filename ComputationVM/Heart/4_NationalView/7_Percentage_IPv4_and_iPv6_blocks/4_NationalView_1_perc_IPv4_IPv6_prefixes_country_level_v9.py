## Description
## 0ne pie chart with data for the last month (day -4 weeks).
## showing the IPv4 blocks allocated by AFRINIC seen at the IXP.

##############################################################################
#__author__ = "Roderick Fanou"
#__email__ = "roderick.fanou@imdea.org"
#__status__ = "Production"
#__description__ = "This script generates "
# Last changes On October 9th by Roderick Fanou
##############################################################################


from netaddr import *
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
import os, sys, MySQLdb
from pprint import pprint


## import all files in the library you need
sys.path.append('../../2_libraries/')
import ipaddress
import DB_configuration
import bgp_rib
from define_timescales import *
from functions import *


now_datetime = str(datetime.now()).replace(' ', '_')
finish = open ('finish_lastmonth.txt', 'w')
finish.write('started; ' + now_datetime)
finish.close()


name_log_file = 'Log_'+str(now_datetime) + '_' + '7_NationalView_1_percentage_IPv4_IPv6_blocks_country_level' + '.txt'
location_logfile = create_Logfiles_folder()
log_file_instance = open(location_logfile+'/'+name_log_file, 'a')
log_file_instance.write('startdate:' + now_datetime)

## Initialisations
IXP_collector = {}
CC_IXP = {}
continent = DB_configuration.continent
region = DB_configuration.region


root_folder = '/home/roderick/Heart/'
output_folder = '../../Computation_outputs_National_View/7_percentage_IP_blocks_assigned_to_country_visible_at_IXP/'

command = 'rm -rf ' + output_folder
os.system(command)

command = 'mkdir ' + output_folder
os.system(command)

command = 'chmod 777 ' + output_folder
os.system(command)


## What about the years for which the computation will be done
yearList = []
i = 2004
current_year = date.today().year
while i < current_year:
    i+=1
    if i not in yearList:
        yearList.append(i)


## Liste route collectors
Current_db = 'MergedData'
## connect to the DB
db = MySQLdb.connect(host = DB_configuration.host, user = DB_configuration.user, passwd = DB_configuration.passwd,  db = Current_db)
cur = db.cursor()
print 'Connected'


query = "select distinct IXP, RouteCollector from AllRouteCollectors where Continent = '"+continent+"';"
cur.execute(query)
data = cur.fetchall()
i = 0

while (i<len(data)):
    row = data[i]
    if row[0] not in IXP_collector.keys():
        IXP_collector[row[0]] = []
    
    IXP_collector[row[0]].append(row[1])
    i+=1
print 'IXP_collector dictionary =',
pprint(IXP_collector)
print



###Current list of all tables;
query = "SHOW TABLES LIKE 'Data__%%' "
cur.execute (query)
data = cur.fetchall()
List_all_tables = []
if len(data)>0:
    for elmt in data:
        List_all_tables.append(elmt[0])
#print List_all_tables





## collecting AFRINIC Assigned prefixes
CC_prefixes_AFRINIC ={}
CC_prefixes_AFRINIC['v6'] = {}
CC_prefixes_AFRINIC['v4'] = {}


Current_db = 'RIRs'
## connect to the DB
db = MySQLdb.connect(host = DB_configuration.host, user = DB_configuration.user, passwd = DB_configuration.passwd,  db = Current_db)
cur = db.cursor()


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
            if current_CC not in CC_prefixes_AFRINIC['v4'].keys():
                CC_prefixes_AFRINIC['v4'][current_CC] = []
            if asn not in CC_prefixes_AFRINIC['v4'][current_CC]:
                CC_prefixes_AFRINIC['v4'][current_CC].append(asn)
        i +=1
#pprint(CC_prefixes_AFRINIC)



##v6
query = "select distinct NetIPaddress, NetBits, CC from IPv6_ressources_AFRINIC where status = 'allocated' or status = 'assigned' and CC != '';"
cur.execute (query)
data = cur.fetchall()
i = 0

if len(data)>0:
    while (i<len(data)):
        row = data[i]
        asn = row[0]+'/'+row[1]
        current_CC = row[2]
        if current_CC != '':
            if current_CC not in CC_prefixes_AFRINIC['v6'].keys():
                CC_prefixes_AFRINIC['v6'][current_CC] = []
            if asn not in CC_prefixes_AFRINIC['v6'][current_CC]:
                CC_prefixes_AFRINIC['v6'][current_CC].append(asn)
        i +=1

#pprint(CC_prefixes_AFRINIC)

#print List_all_tables


## fetch all distinct prefixes corresponding to each routecollector in each IXP list contained in the
## dictionnary IXP_collector


if List_all_tables > 0:
    
    ### Using sliding period
    ### what is the timestamp of today ?
    
    tab = str(datetime.now()).split(' ')
    #tab = ['2017-01-20']
    tab1 = tab[0].split('-')
    timestamp_now = (datetime(int(tab1[0]), int(tab1[1]), int(tab1[2])) - datetime(1970, 1, 1)).total_seconds()
    date_now  = datetime.fromtimestamp(int(timestamp_now)).strftime('%Y-%m-%d')
    print 'timestamp now = ', timestamp_now
    
    couples_year_month = [(tab1[0], tab1[1])]
    
    ## find the number of the first week of the month in the year
    week_number_last_day = find_week_num_in_year(int(tab1[0]), int(tab1[1]), int(tab1[2]))
    #print 'week_number_last_day = ', week_number_last_day
    
    ### Look for date and timestamp one month before
    timestamp_one_month_before = int(timestamp_now) - 2592000
    
    ## find the number of the first week of the month in the year
    date_one_month_bef  = datetime.fromtimestamp(int(timestamp_one_month_before)).strftime('%Y-%m-%d')
    tab2 = date_one_month_bef.split('-')
    
    week_number_first_day = find_week_num_in_year(int(tab2[0]), int(tab2[1]), int(tab2[2]))
    #print 'week_number_first_day = ', week_number_first_day
    
    if (tab2[0], tab2[1]) not in couples_year_month:
        couples_year_month.append( (tab2[0], tab2[1]) )

    ## find the beginning and the end of each week
    List_beg_end_each_week = []

    List_beg_end_each_week = [ str(timestamp_one_month_before ) + '__' +   str(timestamp_now)  + '__'    + str(date_one_month_bef) + '  00:00:00__'  +  '__' +  str(date_now) + ' 00:00:00']
    
    print 'List_beg_end_each_week = ', List_beg_end_each_week



    #print 'couples_year_month = ', couples_year_month

    ## Back to MergedData to fetch prefixes and make comparisons
    Current_db = 'MergedData'
    ## connect to the DB
    db = MySQLdb.connect(host = DB_configuration.host, user = DB_configuration.user, passwd = DB_configuration.passwd,  db = Current_db)
    cur = db.cursor()
    print 'Connected to the DB'

    ## Fetch info pn prefixes available in all tables
    Counter = {}

    print

    for window in couples_year_month:
        
        #query = "select distinct Network  from Data__"+str(int(window[0]))+"_"+str(int(window[1])) + " where Timestamp >= %s and Timestamp <= %s  and ("

        #print str(int(window[0])), str(int(window[1]))
        
        if  "Data__"+str(int(window[0]))+"_"+str(int(window[1])) in List_all_tables:
            
            print 'Table ',  "Data__"+str(int(window[0]))+"_"+str(int(window[1])), ' exists. ==> launch query'
                    
            query = "select distinct Data__"+str(int(window[0]))+"_"+str(int(window[1]))+".Network, Data__"+str(int(window[0]))+"_"+str(int(window[1]))+".RouteCollector, Data__"+str(int(window[0]))+"_"+str(int(window[1]))+".IP_version, AllRouteCollectors.CC from Data__"+str(int(window[0]))+"_"+str(int(window[1]))+", AllRouteCollectors where AllRouteCollectors.RouteCollector = Data__"+str(int(window[0]))+"_"+str(int(window[1]))+ ".RouteCollector and Timestamp >= %s and Timestamp <= %s and Data__"+str(int(window[0]))+"_"+str(int(window[1]))+".IP_version <> 'None' ;"
                    
            couple_timestamp = List_beg_end_each_week[0]
                    
            list_variables = []
            
            tab = str(couple_timestamp).split('__')
                    
            list_variables = [float(tab[0]), float(tab[1])]

            cur.execute(query, (list_variables))
            data = cur.fetchall()
            
            now_datetime = str(datetime.now()).replace(' ', '_')
            print now_datetime, 'Here is the query ', cur._executed
            print

            i = 0
            if len(data)>0:
            
                while (i<len(data)):
                    
                    row = data[i]
                    prefix = row[0]
                    IPversion = row[2]
                    CC = row[3]
                    route_collector_extracted = row[1]
                    
                    for ixp in IXP_collector.keys(): #delete de 2 for the complete continent
                        
                        for route_collector in IXP_collector[ixp]:  #delete de 2 for the complete continent
                            print ixp, route_collector
                
                            if str(route_collector) == str(route_collector_extracted):
                                
                                if CC not in Counter.keys():
                                    Counter[CC] = {}
                                
                                if IPversion not in Counter[CC].keys():
                                    Counter[CC][IPversion] = []
                                
                                if prefix not in Counter[CC][IPversion]:
                                    Counter[CC][IPversion].append(prefix)
                                        
                            else:
                                print 'RouteCollector ', route_collector, 'does not appear in  table Data__'+str(int(window[0]))+"_"+str(int(window[1]))

                    i += 1

        else:
            print "Table doesn't exist: Data__"+str(year)+"_"+str(month)


    command = "mkdir " + output_folder + "Percentage_IPv4_assigned_to_country_appearing_per_CC/"
    os.system(command)

    command = "mkdir " + output_folder  + "Percentage_IPv6_assigned_to_country_appearing_per_CC/"
    os.system(command)


    ## Let us check the compute the list of IPv4, IPv6 prefixes/blocks assigned to the country of the IXP that is visibles  @ the IXP ==> Listof /32 and List of IPv4 blocks
    Intersection = {}
    Intersection['v4'] = {}
    Intersection['v6'] = {}

    #pprint(Counter)



    for IPversion in CC_prefixes_AFRINIC.keys():
        
        #if IPversion == 'v4':
        for CC_AF in CC_prefixes_AFRINIC[IPversion].keys():
            
            for prefix_adv in list(set( CC_prefixes_AFRINIC[IPversion][CC_AF])):
                
                prefix_AF_adv_o = ipaddr.IPNetwork(str(prefix_adv))
                prefix_AF_adv = IPNetwork(str(prefix_adv))
                        
                
                    
                #print 'Checking IXP ', ixp
                if CC_AF in Counter.keys():

                    if CC_AF not in Intersection[IPversion].keys():
                        Intersection[IPversion][CC_AF] = []
                    
                    if IPversion in Counter[CC_AF].keys():
            
                        for prefix_assigned in list(set(Counter[CC_AF][IPversion])):
                            
                            prefix_AF_assigned_o = ipaddr.IPNetwork(str(prefix_assigned))
                            
                            prefix_AF_assigned = IPNetwork(str(prefix_assigned))
                        
                            if prefix_AF_adv_o.overlaps(prefix_AF_assigned_o) and prefix_assigned  != '0.0.0.0/0':
                                print prefix_AF_adv_o, ' overlaps ', prefix_AF_assigned_o
                                
                                if prefix_AF_adv not in Intersection[IPversion][CC_AF]:
                                    Intersection[IPversion][CC_AF].append(prefix_AF_adv)

                                    #with open (filename1, 'a') as fgh:
                                    #    fgh.write('%s' '%s\n' %(prefix_AF_adv))




    ##### compute percentages:
    ### split prefixes into /32s on both sides and computes the numbers and percentages.
    #print Intersection['v4'].keys()


    ### Check this part : why is it taking 38% of memory ?

    for IPversion in Intersection.keys():
        print
        print 'IPversion : ', IPversion
        filename =  output_folder + "Percentage_IP" + IPversion  + "_assigned_to_country_appearing_per_CC/Infos_IPblocks_per_country.txt"
        
        with open (filename, 'a') as fg:
            
            fg.write ('%s; %s; %s; %s;  %s\n' %('IPversion', 'CC_AF','percentage_IPv4_blocks_appearing_at_CC', 'len(Intersection_IPversion_blocks_appearing)', 'len(IPversion_blocks_assigned_to_country)'))

        for CC_AF in Intersection[IPversion].keys():
            
            filename1  = output_folder + "Percentage_IP" + IPversion  + "_assigned_to_country_appearing_per_CC/List_prefixes_assigned_advertised_" + CC_AF + ".txt"
            
            with open (filename, 'a') as fg:
                
                try:
                    perc_IP_blocks = 100 * ( float(len( list(set(Intersection[IPversion][CC_AF])) ))) / (float(len( list(set( CC_prefixes_AFRINIC[IPversion][CC_AF]))  )))
                except:
                    perc_IP_blocks = 0
        
                fg.write ('%s; %s; %s; %s; %s\n' %(IPversion,  CC_AF,  perc_IP_blocks, len(list(set(Intersection[IPversion][CC_AF]))), len(list(set(CC_prefixes_AFRINIC[IPversion][CC_AF])))))

            with open (filename1, 'a') as fgh:
                for line in list(set(Intersection[IPversion][CC_AF])):
                    line = str(line).strip()
                    fgh.write('%s\n' %(line))





now_datetime = str(datetime.now()).replace(' ', '_')
finish = open ('finish_lastmonth.txt', 'w')
finish.write('ended' + '; ' +  root_folder + output_folder[6:] + '; ' + now_datetime)
finish.close()
