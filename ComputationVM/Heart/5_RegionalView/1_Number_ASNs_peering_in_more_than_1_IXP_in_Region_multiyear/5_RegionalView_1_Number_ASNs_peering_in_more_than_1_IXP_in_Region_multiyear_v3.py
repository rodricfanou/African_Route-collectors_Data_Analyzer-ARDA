
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
name_log_file = 'Log_'+str(now_datetime) + '_' + 'RegionalView_1_Number_Peering_ASNs_visible_at_an_IXP_multiyear' + '.txt'
location_logfile = create_Logfiles_folder()


### Define timelines and timescales
## multi-years splitted into years
yearList = multiyear()
print yearList

## last year splitted into months
lastYearList = lastyear()
print lastYearList

## last month (Now - 4weeks) splitted into weeks
lastMonthList = lastmonth()
print lastMonthList


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

output_folder = '../../Computation_outputs_Regional_View/1_Number_ASNs_peering_in_more_than_1_IXP_in_Region_multiyear/'

## Update the folder with the selected repository
IXPView_output_folder =  '/var/www/html/.../outputs/17_Number_ASNs_peering_at_IXP_visible_in_BGP_data/'


command = 'rm -rf ' + output_folder
os.system(command)

command = 'mkdir  ' + output_folder
os.system(command)

command = 'chmod 777 ' + output_folder
os.system(command)


if os.listdir(IXPView_output_folder) != []:
    
    List_years_clone  = copy.copy(yearList)
    
    ### Last year
    #del(List_years_clone[-1])
    
    ## run this for each list except the last one:
    
    for Current_Year in List_years_clone:

        print 'Computation for Current_Year = ', Current_Year
        
        ## Get list ASNs appearing for each IXP
        Last_year_ASN = {}
        
        Total_number_Origin_ASNs = []
        
        Pie_chart__lastyear = {}
        Pie_chart__lastyear["0% to less than 20%"] = []
        Pie_chart__lastyear["20% to less than 40%"] = []
        Pie_chart__lastyear["40% to less than 60%"] = []
        Pie_chart__lastyear["60% to less than 80%"] = []
        Pie_chart__lastyear["80% or more"] = []
        
        for ixp in IXP_collector.keys():
            
            filename = IXPView_output_folder+ """MultiYear__list_visible_ASNs_at_IXP_""" + ixp + '.txt'
            List_ASNs = []
            
            print 'parsing ', filename
                
            try:
                
                with open(filename, 'r') as fg:
                    for line in fg:
                        line = line.strip()
                        tab = line.split('; ')

                        if '#' not in line:
                            try:
                                
                                if int(tab[0]) == int(Current_Year):
                                    if int(tab[-1]) not in List_ASNs:
                                        List_ASNs.append(int(tab[-1]))
                            
                            except:
                                pass

                    #print ixp, len(List_ASNs)
                    if ixp not in Last_year_ASN:
                        Last_year_ASN[ixp] = {}

                    
                    Last_year_ASN[ixp] = List_ASNs

                    Total_number_Origin_ASNs = List_ASNs + Total_number_Origin_ASNs

                    Total_number_Origin_ASNs = list(set(Total_number_Origin_ASNs))
                    
                    #print 'current len( Total_number_Origin_ASNs)= ', len(Total_number_Origin_ASNs)

            except:
                print
                print 'pass for ', filename
                pass

        Appear = {}
        
        for elmt in Total_number_Origin_ASNs:
            
            kkkk = 0
            if elmt not in Appear.keys():
                Appear[elmt] = []

            for ixp in IXP_collector.keys():
                
                if elmt in Last_year_ASN[ixp]:
                    kkkk += 1
                    Appear[elmt].append(ixp)

            value = 100 * (float(len(Appear[elmt])))
            value = value / len(IXP_collector.keys())

            #print elmt, kkkk,  Appear[elmt], len(Appear[elmt]), value
            
            if value  < 20 :
                Pie_chart__lastyear["0% to less than 20%"].append(elmt)

            if value  < 40 and value  >= 20 :
                Pie_chart__lastyear["20% to less than 40%"].append(elmt)
            
            if value  < 60 and value  >= 40 :
                Pie_chart__lastyear["40% to less than 60%"].append(elmt)
            
            if value  < 80 and value  >= 60 :
                Pie_chart__lastyear["60% to less than 80%"].append(elmt)
            
            if value  <= 100 and value  > 80 :
                Pie_chart__lastyear["80% or more"].append(elmt)



        with open(output_folder + 'MultiYear__Total_Number_unique_Peering_ASNs_seen_at_1_IXP_and_more__'+ str(Current_Year) +'.txt', 'w') as fgg:
            fgg.write('%s\n' %('###Regional View -- The Total number of unique Peering ASNs seen at 1 IXP or more'))
            fgg.write('%s\n\n' %(len(Total_number_Origin_ASNs) ))
            
            fgg.write('%s\n' %('###Regional View -- Total number of IXPs'))
            fgg.write('%s\n\n' %( len(IXP_collector.keys())  ))
            
            ## Improve the computation of the total number of IXP per year.
            fgg.write('%s; %s\n' %('###Regional View -- Pie chart date', str(Current_Year) ))
            fgg.write('%s; %s\n' %('0%-20%', len( Pie_chart__lastyear["0% to less than 20%"] )  ))
            fgg.write('%s; %s\n' %('20%-40%', len( Pie_chart__lastyear["20% to less than 40%"] )  ))
            fgg.write('%s; %s\n' %('40%-60%', len( Pie_chart__lastyear["40% to less than 60%"] )  ))
            fgg.write('%s; %s\n' %('60%-80%', len( Pie_chart__lastyear["60% to less than 80%"] )  ))
            fgg.write('%s; %s\n' %('80%-100%', len( Pie_chart__lastyear["80% or more"] )  ))


        with open (output_folder +'MultiYear__List_Peering_ASNs_0percent_20percent_Year_' + str(Current_Year)+ '.txt', 'a') as fh:
            fh.write('%s\n' %("""##ASN; IXPs at which it is visible"""))
            for elmt in Pie_chart__lastyear["0% to less than 20%"]:
                fh.write('%s; %s\n' %(elmt, '; '.join(Appear[elmt])))

        with open (output_folder +'MultiYear__List_Peering_ASNs_20percent_40percent_Year_' + str(Current_Year) + '.txt', 'a') as fh:
            fh.write('%s\n' %("""##ASN; IXPs at which it is visible"""))
            for elmt in Pie_chart__lastyear["20% to less than 40%"]:
                fh.write('%s; %s\n' %(elmt, '; '.join(Appear[elmt])))

        with open (output_folder +'MultiYear__List_Peering_ASNs_40percent_60percent_' + str(Current_Year) + '.txt', 'a') as fh:
            fh.write('%s\n' %("""##ASN; IXPs at which it is visible"""))
            for elmt in Pie_chart__lastyear["40% to less than 60%"]:
                fh.write('%s; %s\n' %(elmt, '; '.join(Appear[elmt])))

        with open (output_folder +'MultiYear__List_Peering_ASNs_60percent_80percent_' + str(Current_Year) + '.txt', 'a') as fh:
            fh.write('%s \n' %("""##ASN; IXPs at which it is visible"""))
            for elmt in Pie_chart__lastyear["60% to less than 80%"]:
                fh.write('%s; %s\n' %(elmt, '; '.join(Appear[elmt])))

        with open (output_folder +'MultiYear__List_Peering_ASNs_80percent_100percent_' + str(Current_Year) + '.txt', 'a') as fh:
            fh.write('%s\n' %("""##ASN; IXPs at which it is visible"""))
            for elmt in Pie_chart__lastyear["80% or more"]:
                fh.write('%s; %s\n' %(elmt, '; '.join(Appear[elmt])))

        #print 'Step1 done'
        ##sys.exit('Step1 done')
        print


    ### Compute the unique total number of Peering_ASNs that are 2bytes per month over the last year

    Last_year_ASN_2bytes = {}

    create_output_2bytesASN_list =  open(output_folder+'MultiYear__2bytes_list_visible_Peering_ASNs_in_more_than_1_IXP.txt', 'a')
    
    create_output_2bytesASN_list.write('###Year; Visible 2bytes Peering ASNs \n')

    create_output_2bytesASN_num =  open(output_folder+'MultiYear__2bytes_number_visible_Peering_ASNs_in_more_than_1_IXP.txt', 'a')
    
    create_output_2bytesASN_num.write('###Year; Number Visible 2bytes Peering ASNs \n')

    for ixp in IXP_collector.keys():
        
        filename = IXPView_output_folder+ """MultiYear__2bytes_list_visible_ASNs_peering_at_IXP_""" + ixp + '.txt'
        
        print 'parsing ', filename
        
        try:
        
            with open(filename, 'r') as fg:
                
                for line in fg:
                    line = line.strip()
                    tab = line.split('; ')
                    
                    if "#" not in line:
                    
                        #try:
                            
                            ASN_2bytes = int(tab[-1])
                            del(tab[-1])
                            key_timestamp = '; '.join(tab)
                        
                            if key_timestamp not in Last_year_ASN_2bytes.keys():
                                Last_year_ASN_2bytes[key_timestamp] = []

                            if ASN_2bytes not in Last_year_ASN_2bytes[key_timestamp]:
                                Last_year_ASN_2bytes[key_timestamp].append(ASN_2bytes)
                                to_add  = str(key_timestamp) + '; ' + str(ASN_2bytes) + '\n'
                                create_output_2bytesASN_list.write(to_add)

                        #except:
                        #    pass

        except:
            print
            print 'pass for ', filename
            pass


    for key_timestamp in Last_year_ASN_2bytes:
        
        to_add = str(key_timestamp) + '; ' + str(len(Last_year_ASN_2bytes[key_timestamp])) + '\n'
        
        create_output_2bytesASN_num.write( to_add )


    #print 'Step2 done'
    print


    ### Compute the unique total number of Peering_ASNs that are 4bytes per month over the last year

    Last_year_ASN_4bytes = {}
    
    create_output_4bytesASN_list =  open(output_folder+'MultiYear__4bytes_list_visible_Peering_ASNs_in_more_than_1_IXP.txt', 'a')
    
    create_output_4bytesASN_list.write('###Year; Visible 4bytes Peering ASNs \n')
    
    create_output_4bytesASN_num =  open(output_folder+'MultiYear__4bytes_number_visible_Peering_ASNs_in_more_than_1_IXP.txt', 'a')
    
    create_output_4bytesASN_num.write('###Year; Number Visible 4bytes Peering ASNs \n')



    for ixp in IXP_collector.keys():
        
        filename = IXPView_output_folder+ """MultiYear__4bytes_list_visible_ASNs_peering_at_IXP_""" + ixp + '.txt'
        
        print 'parsing ', filename
        
        try:
        
            with open(filename, 'r') as fg:
                for line in fg:
                    line = line.strip()
                    tab = line.split('; ')
                    
                    if "#" not in line:
                        
                        #try:
                        
                            ASN_4bytes = int(tab[-1])
                            del(tab[-1])
                            key_timestamp = '; '.join(tab)
                            
                            if key_timestamp not in Last_year_ASN_4bytes.keys():
                                Last_year_ASN_4bytes[key_timestamp] = []
                            
                            if ASN_4bytes not in Last_year_ASN_4bytes[key_timestamp]:
                                Last_year_ASN_4bytes[key_timestamp].append(ASN_4bytes)
                                to_add  = str(key_timestamp) + '; ' + str(ASN_4bytes) + '\n'
                                create_output_4bytesASN_list.write(to_add)

                        #except:
                        #    pass

        except:
            print
            print 'pass for ', filename
            pass


    for key_timestamp in Last_year_ASN_4bytes:
        to_add = str(key_timestamp) + '; ' + str(len(Last_year_ASN_4bytes[key_timestamp])) + '\n'
        create_output_4bytesASN_num.write( to_add )

    #print 'Step3 done'


with open (output_folder + 'MultiYear__2and4bytes_number_visible_Peering_ASNs_in_more_than_1_IXP.txt', 'a') as fg:
    fg.write('%s\n' %("""###Year; Number of Visible Peering 2bytes ASNs; Number of Visible Peering 4bytes ASNs;"""))
    for key_timestamp in Last_year_ASN_2bytes.keys():
        try:
            fg.write('%s; %s; %s\n' %(key_timestamp, len(Last_year_ASN_2bytes[key_timestamp]), len(Last_year_ASN_4bytes[key_timestamp])))
        except:
            fg.write('%s; %s; %s\n' %(key_timestamp, len(Last_year_ASN_2bytes[key_timestamp]), 0))




now_datetime = str(datetime.now()).replace(' ', '_')
finish = open ('finish_multiyear.txt', 'w')
finish.write('ended' + '; ' +  root_folder + output_folder[6:] + '; ' + now_datetime)
finish.close()
