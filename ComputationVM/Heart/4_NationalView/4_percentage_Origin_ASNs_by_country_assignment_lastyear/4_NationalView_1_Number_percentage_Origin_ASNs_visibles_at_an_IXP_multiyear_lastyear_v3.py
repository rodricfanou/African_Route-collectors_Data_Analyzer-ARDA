##############################################################################
# __author__ = "Roderick Fanou"
# __status__ = "Production"
# __Last modification date__ = October 24, 2016
##############################################################################


import copy
# !/usr/bin/python
import os.path
import sys
from datetime import datetime

import MySQLdb
import pycountry
from netaddr import *

## import all files in the library you need
sys.path.append('../../2_libraries/')
import DB_configuration
from define_timescales import *
from functions import *

now_datetime = str(datetime.now()).replace(' ', '_')

finish = open('finish_lastyear.txt', 'w')
finish.write('started; ' + now_datetime)
finish.close()

## Create a logfile:
name_log_file = 'Log_' + str(
    now_datetime) + '_' + '4_NationalView_1_Number_Origin_ASNs_visibles_at_an_IXP_multiyear_lastyear' + '.txt'
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
CC_ASNs_AFRINIC = {}
CC_IXP = {}
region = DB_configuration.region

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
        IXP_CC[row[0]] = row[2]

    if row[2] not in list(CC_IXP.keys()):
        CC_IXP[row[2]] = []
    if row[0] not in CC_IXP[row[2]]:
        CC_IXP[row[2]].append(row[0])

    IXP_collector[row[0]].append(row[1])
    i += 1

print(IXP_collector)
root_folder = '/home/arda/African_Route-collectors_Data_Analyzer-ARDA/ComputationVM/Heart/'

output_folder = '../../Computation_outputs_National_View/4_percentage_Origin_by_country_assignment_lastyear_multiyear/'

command = 'rm -rf ' + output_folder
os.system(command)

command = 'mkdir ' + output_folder
os.system(command)

command = 'mkdir  -p ' + output_folder + 'List_ASNs_visibles_at_all_IXPs_of_a_country/'
os.system(command)

command = 'mkdir  -p ' + output_folder + 'List_ASNs_assigned_by_RIRs/'
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
    ASN_year = {}
    year_ASN = {}

    month_ASN = {}
    ASN_month = {}

    for ixp in list(IXP_collector.keys()):

        CC_key = IXP_CC[ixp]

        log_file_instance = open(location_logfile + '/' + name_log_file, 'a')

        create_output_lastyear = open(output_folder + 'LastYear__list_visible_ASNs_at_IXP_' + CC_key + '.txt', 'a')

        create_output_lastyear.write('Month-Year; ' + 'Origin ASN Visible' + '\n')

        create_output_MultiYear = open(output_folder + 'MultiYear__list_visible_ASNs_at_IXP_' + CC_key + '.txt', 'a')

        create_output_MultiYear.write('Year; ' + 'Origin ASN Visible' + '\n')

        if CC_key not in list(year_ASN.keys()):
            year_ASN[CC_key] = {}

        if CC_key not in list(month_ASN.keys()):
            month_ASN[CC_key] = {}

        for year in yearList:

            if year not in list(year_ASN[CC_key].keys()):
                year_ASN[CC_key][year] = []

            for month in range(1, 13):
                if 'Data__' + str(year) + "_" + str(month) in List_all_tables:

                    # print IXP_collector[ixp]

                    # query = "select count(*) from Data__"+str(year)+"_"+str(month) + " ;"
                    # cur.execute(query)
                    # data = cur.fetchall()
                    # print 'number of lines in the table ', data

                    k = 0
                    query = "select distinct OriginAS, ASPath from Data__" + str(year) + "_" + str(month) + " where"

                    if len(IXP_collector[ixp]) > 1:
                        while k < len(IXP_collector[ixp]) - 1:
                            k += 1
                            query += " RouteCollector = %s or "

                    query += " RouteCollector = %s and (OriginAS != 'None' and OriginAS is not NULL and OriginAS != 'NULL')"

                    print('start_query :', now_datetime, query)
                    print(datetime.now(), 'fetching data from ', ixp)

                    cur.execute(query, IXP_collector[ixp])
                    log_file_instance.write(
                        str(now_datetime) + ' Multi-year & last year Fetching data from IXP ' + ixp + '\n')

                    print('Here is the query ', cur._executed)
                    data = cur.fetchall()

                    print('end_query :', now_datetime)  # , data

                    i = 0

                    if len(data) > 0:

                        while (i < len(data)):
                            row = data[i]

                            OriginASNs = []
                            ## Extract the origin AS
                            if '{' not in row[0] and ',' not in row[0] and '}' not in row[0]:

                                try:
                                    OriginASNs.append(int(row[0]))
                                except:
                                    print('Case 1: Alert We pass for this path ', row[1])

                            else:

                                path = row[1].split(' ')

                                try:
                                    OriginASNs.append(int(str(path[-2]).strip()))
                                except:
                                    print('Case 2: Alert We pass for this path ', row[1])

                            for OriginASNs_elmt in OriginASNs:

                                if OriginASNs_elmt not in year_ASN[CC_key][year]:
                                    year_ASN[CC_key][year].append(OriginASNs_elmt)
                                    create_output_MultiYear.write(str(year) + '; ' + str(OriginASNs_elmt) + '\n')

                                ## Check if we are in the last year and proceed for lastyear
                                if (year, month) in lastYearList:

                                    if str(month) + '-' + str(year) not in list(month_ASN[CC_key].keys()):
                                        month_ASN[CC_key][str(month) + '-' + str(year)] = []

                                    if OriginASNs_elmt not in month_ASN[CC_key][str(month) + '-' + str(year)]:
                                        month_ASN[CC_key][str(month) + '-' + str(year)].append(OriginASNs_elmt)
                                        create_output_lastyear.write(
                                            str(month) + '-' + str(year) + '; ' + str(OriginASNs_elmt) + '\n')

                            i += 1

                    else:
                        print('No ASN found for ', CC_key, ' in ', 'Data__' + str(year) + '_' + str(month))

## I am here.

#### What has AFRINIC attributed till now
### Query RIRs database

## connect to the DB
Current_db = 'RIRs'
db = MySQLdb.connect(host=DB_configuration.host, user=DB_configuration.user, passwd=DB_configuration.passwd,
                     db=Current_db)
cur = db.cursor()

query = "select distinct ASN, CC from ASNs_" + region + " where (status = 'allocated' or status = 'assigned') ;"
print('query = ', query)
cur.execute(query)
data = cur.fetchall()
i = 0

# print 'len table', len(data)
if len(data) > 0:
    while (i < len(data)):
        row = data[i]
        print(row)
        asn = row[0]  # type string
        current_CC = row[1]

        if '.' in asn:  # conversion to 2Byte format
            # print '4B format:',asn
            tab = asn.split('.')
            asn = int(tab[0]) * 65536 + int(tab[1])

        asn = int(asn)  # format int
        if current_CC not in list(CC_ASNs_AFRINIC.keys()):
            CC_ASNs_AFRINIC[current_CC] = []

        if asn not in CC_ASNs_AFRINIC[current_CC]:
            CC_ASNs_AFRINIC[current_CC].append(asn)
        i += 1

# pprint(CC_ASNs_AFRINIC)

filename_output_ASNs_by_AFRINIC = output_folder + 'Number_ASNs_assigned_by_Afrinic.txt'

with open(filename_output_ASNs_by_AFRINIC, 'a') as fg:
    for CC in list(CC_ASNs_AFRINIC.keys()):
        fg.write('%s;%s\n' % (CC, len(CC_ASNs_AFRINIC[CC])))

with open(output_folder + 'List_ASNs_assigned_by_RIRs/List_ASNs_assigned_by_AFRINIC.txt', 'a') as fgh:
    for CC in list(CC_ASNs_AFRINIC.keys()):

        for elmt in CC_ASNs_AFRINIC[CC]:
            fgh.write('%s; %s\n' % (CC, str(elmt)))

for ixp in list(IXP_collector.keys()):

    CC_key = IXP_CC[ixp]

    filename = output_folder + 'LastYear__local_vs_External_ASNs_to_the_country_hosting_IXP_visible_at_IXP_' + CC_key + '.txt'

    if os.path.isfile(filename):

        print('file exists')

    else:

        with open(filename, 'a') as fd:
            fd.write('%s;%s;%s;%s;%s;%s\n' % (
            'CC', 'month-Year', 'Number of Origin ASNs assigned to the country visibles at the IXP',
            'Number of Origin ASNs visibles at the IXP', 'Percentage of local Origin ASNs',
            'Percentage of External Origin ASNs'))

    filename = output_folder + 'MultiYear__local_vs_External_ASNs_to_the_country_hosting_IXP_visible_at_IXP_' + CC_key + '.txt'

    if os.path.isfile(filename):

        print('file exists')

    else:

        with open(filename, 'a') as fd:

            fd.write('%s;%s;%s;%s;%s;%s\n' % (
            'CC', 'Year', 'Number of Origin ASNs assigned to the country visibles at the IXP',
            'Number of Origin ASNs visibles at the IXP', 'Percentage of local Origin ASNs',
            'Percentage of External Origin ASNs'))

## Note that Local means local to the country of the IXP
for ixp in list(IXP_collector.keys()):

    CC_key = IXP_CC[ixp]

    current_CC = CC_key

    if CC_key in list(month_ASN.keys()):

        filename = output_folder + 'LastYear__local_vs_External_ASNs_to_the_country_hosting_IXP_visible_at_IXP_' + CC_key + '.txt'

        intersection1 = []

        for elmt in list(month_ASN[CC_key].keys()):

            set_ASNs = copy.deepcopy(month_ASN[CC_key][elmt])

            intersection1 = list(set(month_ASN[CC_key][elmt]) & set(CC_ASNs_AFRINIC[current_CC]))

            try:
                ## How many ASNs assigned t o current country and seen @ the IXP vs. the total number of Origin ASNs seen @ the IXP
                percentage_local_AF1 = 100 * (float(len(intersection1)) / float(len(month_ASN[CC_key][elmt])))
            except:
                percentage_local_AF1 = 0.0

            with open(filename, 'a') as fd:
                # if len(intersection) >0:
                try:
                    A = pycountry.countries.get(alpha2=current_CC)
                    fd.write('%s;%s;%s;%s;%s;%s\n' % (
                    current_CC, elmt, len(intersection1), len(month_ASN[CC_key][elmt]), percentage_local_AF1,
                    100 - percentage_local_AF1))
                except:
                    fd.write('%s;%s;%s;%s;%s;%s\n' % (
                    current_CC, elmt, len(intersection1), len(month_ASN[CC_key][elmt]), percentage_local_AF1,
                    100 - percentage_local_AF1))

    if CC_key in list(year_ASN.keys()):

        filename = output_folder + 'MultiYear__local_vs_External_ASNs_to_the_country_hosting_IXP_visible_at_IXP_' + CC_key + '.txt'

        intersection2 = []

        for year in yearList:

            set_ASNs = copy.deepcopy(year_ASN[CC_key][year])

            intersection2 = list(set(year_ASN[CC_key][year]) & set(CC_ASNs_AFRINIC[current_CC]))

            try:
                ## How many ASNs assigned to current country and seen @ the IXP vs. the total number of Origin ASNs seen @ the IXP
                percentage_local_AF2 = 100 * (float(len(intersection2)) / float(len(year_ASN[CC_key][year])))
            except:
                percentage_local_AF2 = 0.0

            with open(filename, 'a') as fd:
                # if len(intersection) >0:
                try:
                    A = pycountry.countries.get(alpha2=current_CC)
                    fd.write('%s;%s;%s;%s;%s;%s\n' % (
                    current_CC, year, len(intersection2), len(year_ASN[CC_key][year]), percentage_local_AF2,
                    100 - percentage_local_AF2))
                except:
                    fd.write('%s;%s;%s;%s;%s;%s\n' % (
                    current_CC, year, len(intersection2), len(year_ASN[CC_key][year]), percentage_local_AF2,
                    100 - percentage_local_AF2))

log_file_instance.close()
now_datetime = str(datetime.now()).replace(' ', '_')
finish = open('finish_lastyear.txt', 'w')
finish.write('ended; ' + root_folder + output_folder[6:] + '; ' + now_datetime)
finish.close()
