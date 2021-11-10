## To Do
#The term "Unique prefixes" refers to the list of distinct prefixes present in the list of all prefixes in the considered timeline.
#We suppress the item ASNs and Prefix growth.
#The evolution of the prefixes is plotted as an area graph. We plot on the same graph the evolution of unique bogons (including private address RFC 1918) as an area graph as well.
#On the Y axis, we have the number of unique prefixes counted as explained above. In total, we plan to have 3 graphs with the following timelines on the X axis:
#	last month (Now - 4weeks) splitted into weeks
#	last year (Now - 12 months) splitted into months
#	multi-years splitted into years

##############################################################################
#__author__ = "Roderick Fanou"
#__status__ = "Production"
#__description__ = "This script generates "
#__last_modifications__ =
# by Roderick
#"2016-10-03"
#1- Fetching continent from the configuration file
#2- detail what every column represents in the output files
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
finish.write('started')
finish.close()

## Create a logfile:
name_log_file = 'Log_'+str(now_datetime) + '_' + '1_Number_prefixes_visible_at_an_IXP_multiyear_lastyear' + '.txt'
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

print IXP_collector
root_folder = '/home/African_Route-collectors_Data_Analyzer-ARDA/ComputationVM/Heart/'
output_folder = '../../Computation_outputs/1_Number_prefixes_visibles_at_an_IXP_multiyear_lastyear/'

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
    prefix_year = {}
    year_prefix = {}
        
    month_prefix = {}
    prefix_month = {}
    
    month_prefix_bogon = {}
    year_prefix_bogon = {}
    
    year_prefix_slash = {}
    month_prefix_slash = {}
    
    
    for ixp in IXP_collector.keys():
        
        log_file_instance = open(location_logfile+'/'+name_log_file, 'a')
       
        create_output_lastyear =  open(output_folder+'LastYear__list_visible_prefixes_at_IXP_'+ixp+'.txt', 'a')
        
        create_output_lastyear.write('###Month-Year;  Visible prefixes at IXP; Bogon ? \n')
        
        create_output_MultiYear =  open(output_folder+'MultiYear__list_visible_prefixes_at_IXP_'+ixp+'.txt', 'a')
        
        create_output_MultiYear.write('###Year; Visible prefixes at IXP; Bogon ? \n')
        
        
        if ixp not in year_prefix.keys():
            year_prefix[ixp] = {}
                
        if ixp not in year_prefix_bogon.keys():
            year_prefix_bogon[ixp] = {}
        
        if ixp not in month_prefix.keys():
            month_prefix[ixp] = {}
                
        if ixp not in month_prefix_bogon.keys():
            month_prefix_bogon[ixp] = {}
        
        if ixp not in year_prefix_slash.keys():
            year_prefix_slash[ixp] = {}
        
        if ixp not in month_prefix_slash.keys():
            month_prefix_slash[ixp] = {}
        
        
        
        for year in yearList:
            
            if year not in year_prefix[ixp].keys():
                year_prefix[ixp][year] = []
                    
            if year not in year_prefix_bogon[ixp].keys():
                year_prefix_bogon[ixp][year] = []
            
            if year not in year_prefix_slash[ixp].keys():
                year_prefix_slash[ixp][year] = {}
                                

            for month in xrange(1,13):
                if 'Data__' + str(year) + "_" + str(month) in List_all_tables:
                    print
                    print
                    print IXP_collector[ixp]
                    
                    #query = "select count(*) from Data__"+str(year)+"_"+str(month) + " ;"
                    #cur.execute(query)
                    #data = cur.fetchall()
                    #print 'number of lines in the table ', data
                    
                    k = 0
                    query = "select distinct Network from Data__"+str(year)+"_"+str(month) + " where"
                    while k< len(IXP_collector[ixp]) -1:
                        k+=1
                        query += " RouteCollector = %s or "
                    
                    query += " RouteCollector = %s  "
                    
                    print 'start_query :', now_datetime, query
                    print datetime.now(), 'fetching data from ', ixp
                    
                    data = []
                    #try:
                    cur.execute(query, IXP_collector[ixp])
                    log_file_instance.write(str(now_datetime)+ ' Multi-year & last year Fetching data from IXP '+ ixp + '\n')
                    print 'Here is the query ', cur._executed
                    data = cur.fetchall()
                    #except:
                    #pass
                


                    print 'end_query :', now_datetime #, data
                    
                    i = 0
                    
                    if len(data)>0:
                        
                        while (i<len(data)):
                          
                          row = data[i]
                          prefix = row[0]
                              
                          if 'None' not in prefix:
                              
                              try:
                            
                                #if ixp not in prefix_year.keys():
                                #    prefix_year[ixp] = {}
                                #if prefix not in prefix_year[ixp].keys():
                                #    prefix_year[ixp][prefix] = []
                                #if year not in prefix_year[ixp][prefix]:
                                #    prefix_year[ixp][prefix].append(year)
                                
                                
                                ip = IPNetwork(prefix)
                    
                                try:
                                    selected_ip = ip[1]
                                except:
                                    selected_ip = ip[0]
                                
                                check_bogon = check_if_bogon(selected_ip)
                                
                                ####
                                if check_bogon:
                                    
                                    if prefix not in year_prefix_bogon[ixp][year]:
                
                                        year_prefix_bogon[ixp][year].append(prefix)
                                        
                                        create_output_MultiYear.write(str(year)+ '; '+ str(prefix) + '; bogon\n')
                                        
                                        #tableau_net_pref = prefix.split('/')
                                        
                                        
                                        #if year not in year_prefix_slash[ixp].keys():
                                        #    year_prefix_slash[ixp][str(year)] = {}
                                        
                                        #if str(tableau_net_pref[-1]) not in year_prefix_slash[ixp][year].keys():
                                        #    year_prefix_slash[ixp][year][str(tableau_net_pref[-1])] = []
                                        
                                        #if str(prefix) not in year_prefix_slash[ixp][year][str(tableau_net_pref[-1])]:
                                        #    year_prefix_slash[ixp][year][str(tableau_net_pref[-1])].append(str(prefix))
                                
                                        #create_output_slash = open(output_folder+'Multiyear__list_visible_prefixes_at_IXP_'+ixp+'_with_slash_' + str(tableau_net_pref[-1]) + '.txt', 'a')
                                        #create_output_slash.write(str(year)+ '; '+ str(prefix) + '\n')
                                        #create_output_slash.close()
                                            
                                
                                    
                                if prefix not in year_prefix[ixp][year]:
                                    
                                    year_prefix[ixp][year].append(prefix)
                                    
                                    create_output_MultiYear.write(str(year)+ '; '+ str(prefix) + '\n')
                            
                              
                                ### Find out the slash (length of the network part corresponding to the prefix)
                                tableau_net_pref = prefix.split('/')
                                
                                if year not in year_prefix_slash[ixp].keys():
                                    year_prefix_slash[ixp][str(year)] = {}
                                
                                if str(tableau_net_pref[-1]) not in year_prefix_slash[ixp][year].keys():
                                    year_prefix_slash[ixp][year][str(tableau_net_pref[-1])] = []
                                
                                if str(prefix) not in year_prefix_slash[ixp][year][str(tableau_net_pref[-1])]:
                                    year_prefix_slash[ixp][year][str(tableau_net_pref[-1])].append(str(prefix))
                                
                                #with open (output_folder+'Multiyear__list_visible_prefixes_at_IXP_'+ixp+'_with_slash_' + str(tableau_net_pref[-1]) + '.txt', 'a') as fg:
                                #    fg.write('%s; %s \n' %(str(year) , str(prefix) ))
                                
                                create_output_slash = open(output_folder+'Multiyear__list_visible_prefixes_at_IXP_'+ixp+'_with_slash_' + str(tableau_net_pref[-1]) + '.txt', 'a')
                                create_output_slash.write(str(year)+ '; '+ str(prefix) + '\n')
                                create_output_slash.close()
                                
                      
                      
                                        
                                ## Check if we are in the last year and proceed for lastyear
                                if (year, month) in lastYearList:
                                    
                                    #if ixp not in prefix_month.keys():
                                    #    prefix_month[ixp] = {}
                                    #if prefix not in prefix_month[ixp].keys():
                                    #    prefix_month[ixp][prefix] = []
                                    #if str(month)+'-'+str(year) not in prefix_month[ixp][prefix]:
                                    #    prefix_year[ixp][prefix].append(str(month)+'-'+str(year))
                                    
                                    if str(month)+'-'+str(year) not in month_prefix[ixp].keys():
                                        month_prefix[ixp][str(month)+'-'+str(year)] = []
                                    
                                    if str(month)+'-'+str(year) not in month_prefix_bogon[ixp].keys():
                                        month_prefix_bogon[ixp][str(month)+'-'+str(year)] = []
                                    
                                    if str(month)+'-'+str(year) not in month_prefix_slash[ixp].keys():
                                        month_prefix_slash[ixp][str(month)+'-'+str(year)] = {}
                                    
                    
                    
                                    if prefix in year_prefix_bogon[ixp][year]:
                                        
                                        if prefix not in month_prefix_bogon[ixp][str(month)+'-'+str(year)]:
                                            
                                            month_prefix_bogon[ixp][str(month)+'-'+str(year)].append(prefix)
                                            
                                            create_output_lastyear.write(str(month)+'-'+str(year)+ '; '+ str(prefix) + '; bogon\n')
                                    
                                   
                                        
                                    if prefix not in month_prefix[ixp][str(month)+'-'+str(year)]:
                                        
                                        month_prefix[ixp][str(month)+'-'+str(year)].append(prefix)
                                        
                                        create_output_lastyear.write(str(month)+'-'+str(year)+ '; '+ str(prefix) + '\n')
                                
                                    
                                        
                                    ### Find out the slash (length of the network part corresponding to the prefix)
                                    tableau_net_pref = prefix.split('/')
                                    
                                    if str(month)+'-'+str(year) not in month_prefix_slash[ixp].keys() :
                                        month_prefix_slash[ixp][str(month)+'-'+str(year)] = {}
                                    
                                    if str(tableau_net_pref[-1]) not in month_prefix_slash[ixp][str(month)+'-'+str(year)].keys():
                                        month_prefix_slash[ixp][str(month)+'-'+str(year)][str(tableau_net_pref[-1])] = []
                                    
                                    if prefix not in month_prefix_slash[ixp][str(month)+'-'+str(year)][str(tableau_net_pref[-1])]:
                                        month_prefix_slash[ixp][str(month)+'-'+str(year)][str(tableau_net_pref[-1])].append(prefix)
                                            
                                    with open (output_folder + 'Lastyear__list_visible_prefixes_at_IXP_' + ixp + '_with_slash_' + str(tableau_net_pref[-1]) + '.txt', 'a') as fg:
                                        fg.write('%s; %s \n' %(str(month)+ '-' + str(year), str(prefix) ))
                                    
                                        
                              except:
                                
                                pass
                                    
                          i += 1

                    else:
                        
                        print 'No prefix found for ', ixp, ' in ' , 'Data__'+str(year)+'_'+str(month)






        #for ixp in month_prefix.keys():
        if ixp in month_prefix.keys():
            
            create_output_lastyear = open(output_folder+'LastYear__number_visible_prefixes_at_IXP_'+ixp+'.txt', 'a')
            
            create_output_lastyear.write('###Month-Year; number visible prefixes at IXP; number of visible bogon prefixes at IXP \n')
            

            for elmt in month_prefix[ixp].keys():
                create_output_lastyear.write(elmt+ '; '+ str(len(month_prefix[ixp][elmt])) + '; '+ str(len(month_prefix_bogon[ixp][elmt])) + '\n')
        
            print
            print month_prefix_slash[ixp]
            print
            
            create_output_lastyear_slash = open(output_folder+'LastYear__number_visible_prefixes_at_IXP_with_slash_'+ixp+'.txt', 'a')
            
            create_output_lastyear_slash.write('###Month-Year; number visible prefixes at IXP of length prefix length \n')
            
            if len(month_prefix_slash[ixp].keys()) > 0:
                
                for year in month_prefix_slash[ixp].keys():
                    
                    if len(month_prefix_slash[ixp][year]) > 0:
                    
                        for slash_prefix in month_prefix_slash[ixp][year].keys():
                            
                            create_output_lastyear_slash.write( str(year) + '; ' + str(slash_prefix) + '; '  + str(len(month_prefix_slash[ixp][year][slash_prefix]) ) + '\n')
                    
            #create_output_lastyear_slash.close()


            #for prefix in month_prefix[ixp][elmt]:
            #    create_output_lastyear =  open(output_folder+'LastYear__list_visible_prefixes_at_IXP_'+ixp+'.txt', 'a')
            #    create_output_lastyear.write(elmt+ '; '+ str(prefix) + '\n')





        if ixp in year_prefix.keys():
            
            create_output_MultiYear = open(output_folder+'MultiYear__number_visible_prefixes_at_IXP_'+ixp+'.txt', 'a')
            
            create_output_MultiYear.write('###Year;  number visible prefixes at IXP; number of visible bogon prefixes at IXP \n')
            
            for year in yearList:
                create_output_MultiYear.write(str(year)+ '; '+ str(len(year_prefix[ixp][year])) + '; ' + str(len(year_prefix_bogon[ixp][year])) + '\n')

            #print
            #print year_prefix_slash[ixp]
            #print

            create_output_Multiyear_slash = open(output_folder+'MultiYear__number_visible_prefixes_at_IXP_with_slash_'+ixp+'.txt', 'a')

            if len(year_prefix_slash[ixp].keys()) > 0:
                
                for year in year_prefix_slash[ixp].keys():
                    
                    if len(year_prefix_slash[ixp][year]) > 0:
                    
                        for slash_prefix in year_prefix_slash[ixp][year].keys():
                            
                            create_output_Multiyear_slash.write( str(year) + '; ' + str(slash_prefix) + '; '  + str(len(year_prefix_slash[ixp][year][slash_prefix])   ) + '\n')

            #create_output_Multiyear_slash.close()

            #for year in year_prefix[ixp].keys():
            #for prefix in year_prefix[ixp][year]:
            #    create_output_MultiYear =  open(output_folder+'MultiYear__list_visible_prefixes_at_IXP_'+ixp+'.txt', 'a')
            #    create_output_MultiYear.write(str(year)+ '; '+ str(prefix) + '\n')


log_file_instance.close()
now_datetime = str(datetime.now()).replace(' ', '_')
finish = open ('finish_lastyear.txt', 'w')
finish.write('ended' + '; ' +  root_folder + output_folder[6:])
finish.close()
