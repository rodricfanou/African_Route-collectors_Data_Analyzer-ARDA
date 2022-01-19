##############################################################################
# __author__ = "Roderick Fanou"
# __status__ = "Production"
# __description__ = "This script generates "
##############################################################################

# !/usr/bin/python
import os.path
import sys
from datetime import datetime

import MySQLdb
from netaddr import *

## import all files in the library you need
sys.path.append('../../2_libraries/')
import DB_configuration
from define_timescales import *
from functions import *

##
now_datetime = str(datetime.now()).replace(' ', '_')

finish = open('finish_lastyear.txt', 'w')
finish.write('started; ' + now_datetime)
finish.close()

## Create a logfile:
name_log_file = 'Log_' + str(now_datetime) + '_' + '9_Number_IPv6_vs_IPv4_prefixes_multiyear' + '.txt'
location_logfile = create_Logfiles_folder()

### Define timelines and timescales
## multi-years splitted into years
yearList = multiyear()
yearList.sort()
print(yearList)

## last month (Now - 4weeks) splitted into weeks
lastYearList = lastyear()
print(lastYearList)
lastYearList.sort()

## last month (Now - 4weeks) splitted into weeks
lastMonthList = lastmonth()
print(lastMonthList)
lastMonthList.sort()

## Other initialisations
continent = DB_configuration.continent
IXP_collector = {}
IXP_CC = {}
Current_db = 'MergedData'
CC_IXP = {}

## connect to the DB
db = MySQLdb.connect(host="localhost", user="", passwd="", db=Current_db)
cur = db.cursor()
print('Connected')

query = "select IXP, RouteCollector, CC from AllRouteCollectors where Continent = '" + continent + "';"
cur.execute(query)
data = cur.fetchall()
i = 0
while (i < len(data)):
    row = data[i]
    if row[0] not in list(IXP_collector.keys()):
        IXP_collector[row[0]] = []
        IXP_CC[row[2]] = row[0]

    if row[2] not in list(CC_IXP.keys()):
        CC_IXP[row[2]] = []
    if row[0] not in CC_IXP[row[2]]:
        CC_IXP[row[2]].append(row[0])

    IXP_collector[row[0]].append(row[1])
    i += 1

print(IXP_collector)
root_folder = '/home/arda/African_Route-collectors_Data_Analyzer-ARDA/ComputationVM/Heart/'
output_folder = '../../Computation_outputs/9_Number_IPv6_vs_IPv4_prefixes_multiyear/'

command = 'rm -rf ' + output_folder
os.system(command)

command = 'mkdir ' + output_folder
os.system(command)

command = 'chmod 777 ' + output_folder
os.system(command)

###Current list of all tables;
query = "SHOW TABLES LIKE 'Data__%%' "
cur.execute(query)
data = cur.fetchall()
List_all_tables = []
if len(data) > 0:
    for elmt in data:
        List_all_tables.append(elmt[0])
##print List_all_tables


## multi-year and last year
if List_all_tables > 0:

    prefix_year = {}
    year_prefix = {}

    month_prefix = {}
    prefix_month = {}

    month_prefix_bogon = {}
    year_prefix_bogon = {}

    for ixp in list(IXP_collector.keys()):

        log_file_instance = open(location_logfile + '/' + name_log_file, 'a')

        if ixp not in list(year_prefix.keys()):
            year_prefix[ixp] = {}

        if ixp not in list(year_prefix_bogon.keys()):
            year_prefix_bogon[ixp] = {}

        if ixp not in list(month_prefix.keys()):
            month_prefix[ixp] = {}

        if ixp not in list(month_prefix_bogon.keys()):
            month_prefix_bogon[ixp] = {}

        for year in yearList:

            if year not in list(year_prefix[ixp].keys()):
                year_prefix[ixp][year] = {}

            for month in range(1, 13):
                if 'Data__' + str(year) + "_" + str(month) in List_all_tables:
                    # print
                    print()
                    # print IXP_collector[ixp]

                    # query = "select count(*) from Data__"+str(year)+"_"+str(month) + " ;"
                    # cur.execute(query)
                    # data = cur.fetchall()
                    # print 'number of lines in the table ', data

                    k = 0
                    query = "select distinct Network, IP_version, OriginAS, ASpath from Data__" + str(year) + "_" + str(
                        month) + " where"
                    while k < len(IXP_collector[ixp]) - 1:
                        k += 1
                        query += " RouteCollector = %s or "

                    query += """ RouteCollector = %s and (IP_version <> 'None')"""

                    print('start_query :', datetime.now(), query)
                    print()
                    print(datetime.now(), 'fetching data from ', ixp)

                    cur.execute(query, IXP_collector[ixp])
                    log_file_instance.write(
                        str(now_datetime) + ' Multi-year & last year Fetching data from IXP ' + ixp + '\n')

                    print('Here is the query ', cur._executed)
                    data = cur.fetchall()
                    print()
                    print('end_query :', datetime.now())  # , data
                    print()
                    i = 0

                    if len(data) > 0:

                        # print len(data)
                        while (i < len(data)):
                            row = data[i]
                            prefix = row[0]
                            IPversion = row[1]
                            ASpath = row[3]

                            if '{' not in ASpath and '}' not in ASpath:
                                try:
                                    OriginAS = int(row[2])
                                except:
                                    pass

                            else:
                                # print year_prefix[ixp]
                                tabbbb = ASpath.split(' ')

                                try:
                                    OriginAS = int(str(tabbbb[-2]).strip())
                                except:
                                    pass

                            # print prefix, IPversion, OriginAS, ASpath

                            ### ASNs Origin of prefixes  ranged per year
                            if IPversion not in list(year_prefix[ixp][year].keys()):
                                year_prefix[ixp][year][IPversion] = []

                            # year_prefix[ixp][year][IPversion].append(prefix)
                            if OriginAS not in year_prefix[ixp][year][IPversion]:
                                year_prefix[ixp][year][IPversion].append(OriginAS)

                            ## ASNs Origin of prefixes: Check if we are in the last year and proceed for lastyear
                            if (year, month) in lastYearList:

                                if str(month) + '-' + str(year) not in list(month_prefix[ixp].keys()):
                                    month_prefix[ixp][str(month) + '-' + str(year)] = {}

                                if IPversion not in month_prefix[ixp][str(month) + '-' + str(year)]:
                                    month_prefix[ixp][str(month) + '-' + str(year)][IPversion] = []

                                # month_prefix[ixp][str(month)+'-'+str(year)][IPversion].append(prefix)
                                # create_output_lastyear.write(str(month)+'-'+str(year)+ '; '+ str(prefix) + '\n')

                                if OriginAS not in month_prefix[ixp][str(month) + '-' + str(year)][IPversion]:
                                    month_prefix[ixp][str(month) + '-' + str(year)][IPversion].append(OriginAS)

                            i += 1

                    else:
                        print('No prefix found for ', ixp, ' in ', 'Data__' + str(year) + '_' + str(month))

# print year_prefix

# sys.exit()

## put them all in a file first

# Team Cymru => prefixes to ASNs + count number of uniq ASNs

#### Separating Local from External prefixes


for ixp in list(IXP_collector.keys()):

    if ixp in list(month_prefix.keys()):

        entete = []

        for id_month_and_year in list(month_prefix[ixp].keys()):

            # print month_prefix[ixp].keys()

            if len(year_prefix[ixp][year]) > 0:

                for IPversion in list(month_prefix[ixp][id_month_and_year].keys()):

                    if IPversion + 'added' not in entete:
                        with open(output_folder + 'LastYear_' + ixp + '_Number_ASNs_announcing_' + IPversion + '.txt',
                                  'a') as fg1:
                            fg1.write('%s; %s\n' % ('Month-Year', 'len_ASNs_announcing_IPversion_prefixes_in_month'))

                            entete.append(IPversion + 'added')

                    with open(output_folder + 'LastYear_' + ixp + '_Number_ASNs_announcing_' + IPversion + '.txt',
                              'a') as fg1:

                        fg1.write(
                            '%s; %s\n' % (id_month_and_year, len(month_prefix[ixp][id_month_and_year][IPversion])))

                    with open(output_folder + 'LastYear_' + ixp + '_List_ASNs_announcing_' + IPversion + '.txt',
                              'a') as fg2:

                        for ASN_to_add in month_prefix[ixp][id_month_and_year][IPversion]:
                            fg2.write('%s; %s\n' % (id_month_and_year, ASN_to_add))

    if ixp in list(year_prefix.keys()):

        for year in yearList:

            if year in list(year_prefix[ixp].keys()):

                if len(year_prefix[ixp][year]) > 0:

                    for IPversion in list(year_prefix[ixp][year].keys()):

                        if IPversion + 'added' not in entete:
                            with open(
                                    output_folder + 'MultiYear_' + ixp + '_Number_ASNs_announcing_' + IPversion + '.txt',
                                    'a') as fg1:
                                fg1.write('%s; %s\n' % ('year', 'len_ASNs_announcing_IPversion_prefixes_in_year'))

                                entete.append(IPversion + 'added')

                        with open(output_folder + 'MultiYear_' + ixp + '_Number_ASNs_announcing_' + IPversion + '.txt',
                                  'a') as fg4:

                            fg4.write('%s; %s\n' % (year, len(year_prefix[ixp][year][IPversion])))

                        with open(output_folder + 'MultiYear_' + ixp + '_List_ASNs_announcing_' + IPversion + '.txt',
                                  'a') as fg3:

                            for ASN_to_add in year_prefix[ixp][year][IPversion]:
                                fg3.write('%s; %s\n' % (year, ASN_to_add))

log_file_instance.close()
now_datetime = str(datetime.now()).replace(' ', '_')
finish = open('finish_lastyear.txt', 'w')
finish.write('ended' + '; ' + root_folder + output_folder[6:] + '; ' + now_datetime)
finish.close()
