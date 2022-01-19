##############################################################################
# __author__ = "Roderick Fanou"
# __status__ = "Production"
# __last_modifications__ =
# by Roderick
# "2016-11-15"
##############################################################################

import copy
# !/usr/bin/python
import os.path
import sys
from datetime import datetime

import MySQLdb
import ipaddr
import pycountry
from netaddr import *


# def cidrsOverlap(cidr0, cidr1):
#    if '.' in str(cidr0[0]) and '.' in str(cidr1[0]):
#    	return cidr0[0] <= cidr1[-1] and cidr1[0] <= cidr0[-1]

def cidrsOverlap(cidr0, cidr1):
    if '.' in str(cidr0[0]) and '.' in str(cidr1[0]):
        return cidr0 in cidr1 or cidr1 in cidr0
    elif ':' in str(cidr0[0]) and ':' in str(cidr1[0]):
        return cidr0 in cidr1 or cidr1 in cidr0


## import all files in the library you need
sys.path.append('../../2_libraries/')
import DB_configuration
from define_timescales import *
from functions import *

now_datetime = str(datetime.now()).replace(' ', '_')

finish = open('finish_lastmonth_better.txt', 'w')
finish.write('started' + '; ' + now_datetime)
finish.close()

## Create a logfile:
name_log_file = 'Log_' + str(
    now_datetime) + '_' + '1_percentage_prefixes_by_country_assignment_lastmonth_better' + '.txt'
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
region = DB_configuration.region
IXP_collector = {}
IXP_CC = {}
CC_IXP = {}

## connect to the DB
Current_db = 'MergedData'
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
#### TO ENABLE LATER
output_folder = '../../Computation_outputs/5_percentage_prefixes_by_country_assignment_lastmonth_better/'
##output_folder = 'outputs/'


command = 'rm -rf ' + output_folder
os.system(command)

command = 'mkdir  ' + output_folder
os.system(command)

command = 'chmod 777 ' + output_folder
os.system(command)

filename = output_folder

#### What has AFRINIC attributed till now
### Query RIRs database

## connect to the DB
Current_db = 'RIRs'
db = MySQLdb.connect(host=DB_configuration.host, user=DB_configuration.user, passwd=DB_configuration.passwd,
                     db=Current_db)
cur = db.cursor()
print('Connected')

##Check that the dictionary is full as it should
##LET'S DO A DICTIONARY OF prefixes per continent
CC_ASNs_AFRINIC = {}
CC_ASNs_RIPE = {}
CC_ASNs_ARIN = {}
CC_ASNs_LACNIC = {}
CC_ASNs_APNIC = {}

# table_prefixes = [' IPv4_ressources_', ' IPv6_ressources_']
table_prefixes = ['IPv4_ressources_']

for tablei in table_prefixes:
    query = "select distinct NetIPaddress, NetBits, CC from " + tablei + "AFRINIC where (status = 'allocated' or status = 'assigned') and CC != '';"
    cur.execute(query)
    data = cur.fetchall()
    i = 0
    if len(data) > 0:
        while (i < len(data)):
            row = data[i]
            if '.' in row[0] or ':' in row[0]:
                asn = row[0] + '/' + row[1]
                # print 'asn =', asn
                current_CC = row[2]
                if current_CC != '':
                    if current_CC not in list(CC_ASNs_AFRINIC.keys()):
                        CC_ASNs_AFRINIC[current_CC] = []

                    if asn not in CC_ASNs_AFRINIC[current_CC]:
                        CC_ASNs_AFRINIC[current_CC].append(asn)
            i += 1

# print 'CC at AFRINIC'
# pprint(CC_ASNs_AFRINIC)


for tablei in table_prefixes:
    query = "select distinct NetIPaddress, NetBits, CC from " + tablei + "RIPE where (status = 'allocated' or status = 'assigned') and CC != '';"
    cur.execute(query)
    data = cur.fetchall()
    i = 0
    if len(data) > 0:
        while (i < len(data)):
            row = data[i]
            if '.' in row[0] or ':' in row[0]:
                asn = row[0] + '/' + row[1]  # type string
                CC = row[2]
                if CC != '':
                    if CC not in list(CC_ASNs_RIPE.keys()):
                        CC_ASNs_RIPE[CC] = []
                    if asn not in CC_ASNs_RIPE[CC]:
                        CC_ASNs_RIPE[CC].append(asn)
            i += 1

# print 'CC at RIPE',
# pprint(CC_ASNs_RIPE)


for tablei in table_prefixes:
    query = "select distinct NetIPaddress, NetBits, CC from " + tablei + "ARIN where (status = 'allocated' or status = 'assigned') and CC != '';"
    cur.execute(query)
    data = cur.fetchall()
    i = 0
    if len(data) > 0:
        while (i < len(data)):
            row = data[i]
            if '.' in row[0] or ':' in row[0]:
                asn = row[0] + '/' + row[1]  # type string
                CC = row[2]
                if CC != '':
                    if CC not in list(CC_ASNs_ARIN.keys()):
                        CC_ASNs_ARIN[CC] = []
                    if asn not in CC_ASNs_ARIN[CC]:
                        CC_ASNs_ARIN[CC].append(asn)
            i += 1

# print 'CC at ARIN',
# pprint(CC_ASNs_ARIN)


for tablei in table_prefixes:
    query = "select distinct NetIPaddress, NetBits, CC from " + tablei + "APNIC where (status = 'allocated' or status = 'assigned') and CC != '';"
    cur.execute(query)
    data = cur.fetchall()
    i = 0
    if len(data) > 0:
        while (i < len(data)):
            row = data[i]
            if '.' in row[0] or ':' in row[0]:
                asn = row[0] + '/' + row[1]  # type string
                CC = row[2]
                if CC != '':
                    if CC not in list(CC_ASNs_APNIC.keys()):
                        CC_ASNs_APNIC[CC] = []
                    if asn not in CC_ASNs_APNIC[CC]:
                        CC_ASNs_APNIC[CC].append(asn)
            i += 1

# print 'CC at APNIC',
# pprint(CC_ASNs_APNIC)


for tablei in table_prefixes:
    query = "select distinct NetIPaddress, NetBits, CC from " + tablei + "LACNIC where (status = 'allocated' or status = 'assigned') and CC != '';"
    cur.execute(query)
    data = cur.fetchall()
    i = 0
    if len(data) > 0:
        while (i < len(data)):
            row = data[i]
            if '.' in row[0] or ':' in row[0]:
                asn = row[0] + '/' + row[1]  # type string
                CC = row[2]
                if CC != '':
                    if CC not in list(CC_ASNs_LACNIC.keys()):
                        CC_ASNs_LACNIC[CC] = []
                    if asn not in CC_ASNs_LACNIC[CC]:
                        CC_ASNs_LACNIC[CC].append(asn)
            i += 1

# print 'CC at LACNIC',
# pprint(CC_ASNs_LACNIC)


### Directing the outputs in a file
filename_output_ASNs_by_AFRINIC = output_folder + 'Number_prefixes_assigned_by_AFRINIC.txt'
with open(filename_output_ASNs_by_AFRINIC, 'a') as fg:
    for CC in list(CC_ASNs_AFRINIC.keys()):
        fg.write('%s;%s\n' % (CC, len(CC_ASNs_AFRINIC[CC])))

        with open(output_folder + 'List_prefixes_allocated_by_AFRINIC.txt', 'a') as fh:
            for pref in CC_ASNs_AFRINIC[CC]:
                fh.write('%s; %s\n' % (CC, pref))

### Directing the outputs in a file
filename_output_ASNs_by_RIPE = output_folder + 'Number_prefixes_assigned_by_RIPE.txt'
with open(filename_output_ASNs_by_RIPE, 'a') as fg:
    for CC in list(CC_ASNs_RIPE.keys()):
        fg.write('%s;%s\n' % (CC, len(CC_ASNs_RIPE[CC])))

        with open(output_folder + 'List_prefixes_allocated_by_RIPE.txt', 'a') as fh:
            for pref in CC_ASNs_RIPE[CC]:
                fh.write('%s; %s\n' % (CC, pref))

### Directing the outputs in a file
filename_output_ASNs_by_APNIC = output_folder + 'Number_prefixes_assigned_by_APNIC.txt'
with open(filename_output_ASNs_by_APNIC, 'a') as fg:
    for CC in list(CC_ASNs_APNIC.keys()):
        fg.write('%s;%s\n' % (CC, len(CC_ASNs_APNIC[CC])))

        with open(output_folder + 'List_prefixes_allocated_by_APNIC.txt', 'a') as fh:
            for pref in CC_ASNs_APNIC[CC]:
                fh.write('%s; %s\n' % (CC, pref))

### Directing the outputs in a file
filename_output_ASNs_by_ARIN = output_folder + 'Number_prefixes_assigned_by_ARIN.txt'
with open(filename_output_ASNs_by_ARIN, 'a') as fg:
    for CC in list(CC_ASNs_ARIN.keys()):
        fg.write('%s;%s\n' % (CC, len(CC_ASNs_ARIN[CC])))

        with open(output_folder + 'List_prefixes_allocated_by_ARIN.txt', 'a') as fh:
            for pref in CC_ASNs_ARIN[CC]:
                fh.write('%s; %s\n' % (CC, pref))

### Directing the outputs in a file
filename_output_ASNs_by_LACNIC = output_folder + 'Number_prefixes_assigned_by_LACNIC.txt'
with open(filename_output_ASNs_by_LACNIC, 'a') as fg:
    for CC in list(CC_ASNs_LACNIC.keys()):
        fg.write('%s;%s\n' % (CC, len(CC_ASNs_LACNIC[CC])))

        with open(output_folder + 'List_prefixes_allocated_by_LACNIC.txt', 'a') as fh:
            for pref in CC_ASNs_LACNIC[CC]:
                fh.write('%s; %s\n' % (CC, pref))

Current_db = 'MergedData'
db = MySQLdb.connect(host=DB_configuration.host, user=DB_configuration.user, passwd=DB_configuration.passwd,
                     db=Current_db)
cur = db.cursor()

###Current list of all tables;
query = "SHOW TABLES LIKE 'Data__%%' "
cur.execute(query)
data = cur.fetchall()
List_all_tables = []
if len(data) > 0:
    for elmt in data:
        List_all_tables.append(elmt[0])

##print List_all_tables

## fetch all distinct prefixes corresponding to each routecollector in each IXP list contained in the
## dictionnary IXP_collector

log_file_instance = open(location_logfile + '/' + name_log_file, 'a')

## Initialisation
week_prefix = {}

### splitted into weeks over the last month
# print lastMonthList[0][0], lastMonthList[0][1]


if List_all_tables > 0:

    ### Using sliding period
    tab = str(datetime.now()).split(' ')
    # tab = ['2017-01-20']
    tab1 = tab[0].split('-')
    timestamp_now = (datetime(int(tab1[0]), int(tab1[1]), int(tab1[2])) - datetime(1970, 1, 1)).total_seconds()
    date_now = datetime.fromtimestamp(int(timestamp_now)).strftime('%Y-%m-%d')
    print('timestamp = ', timestamp_now)

    couples_year_month = [(tab1[0], tab1[1])]

    ## find the number of the first week of the month in the year
    week_number_last_day = find_week_num_in_year(int(tab1[0]), int(tab1[1]), int(tab1[2]))
    print('week_number_last_day = ', week_number_last_day)

    ## I changed here the timelaps; check later the couples
    ### Look for date and timestamp one month before
    # timestamp_one_month_before = int(timestamp_now) - 2592000
    timestamp_one_month_before = int(timestamp_now) - 604800

    ## find the number of the first week of the month in the year
    date_one_month_bef = datetime.fromtimestamp(int(timestamp_one_month_before)).strftime('%Y-%m-%d')
    tab2 = date_one_month_bef.split('-')

    week_number_first_day = find_week_num_in_year(int(tab2[0]), int(tab2[1]), int(tab2[2]))
    print('week_number_first_day = ', week_number_first_day)

    if (tab2[0], tab2[1]) not in couples_year_month:
        couples_year_month.append((tab2[0], tab2[1]))

    ## find the beginning and the end of each week
    List_beg_end_each_week = []

    ### Look for date and timestamp one month before
    ##timestamp_one_month_before = int(timestamp_now) - 2592000

    ## find the number of the first week of the month in the year
    date_one_month_bef = datetime.fromtimestamp(int(timestamp_one_month_before)).strftime('%Y-%m-%d')
    tab2 = date_one_month_bef.split('-')

    week_number_first_day = find_week_num_in_year(int(tab2[0]), int(tab2[1]), int(tab2[2]))
    print('week_number_first_day = ', week_number_first_day)

    if (tab2[0], tab2[1]) not in couples_year_month:
        couples_year_month.append((tab2[0], tab2[1]))

    ## find the beginning and the end of each week
    List_beg_end_each_week = []

    List_beg_end_each_week = [str(timestamp_one_month_before) + '__' + str(timestamp_now) + '__' + str(
        date_one_month_bef) + '  00:00:00__' + '__' + str(date_now) + ' 00:00:00']

    print('List_beg_end_each_week = ', List_beg_end_each_week)

    print('couples_year_month = ', couples_year_month)

    # sys.exit()

    for ixp in list(IXP_collector.keys()):

        if ixp not in list(week_prefix.keys()):
            week_prefix[ixp] = []

        for window in couples_year_month:
            query = "select distinct Network  from Data__" + str(int(window[0])) + "_" + str(
                int(window[1])) + " where Timestamp >= %s and Timestamp <= %s  and ("

            k = 0
            while k < len(IXP_collector[ixp]) - 1:
                k += 1
                query += " RouteCollector = %s or "

            ## I added a limit 100 here to suppress later
            query += " RouteCollector = %s) and TypeRC = 'PCH' "

            print('start_query :', datetime.now(), query)
            print(datetime.now(), 'week fetching data from ', ixp)

            couple_timestamp = List_beg_end_each_week[0]

            list_variables = []
            tab = str(couple_timestamp).split('__')

            list_variables = [float(tab[0]), float(tab[1])] + IXP_collector[ixp]

            # if 1:
            # try:

            cur.execute(query, list_variables)

            log_file_instance.write(str(datetime.now()) + ' Fetching data from IXP ' + ixp + '\n')

            print('Here is the query ', cur._executed)
            data = cur.fetchall()

            print('end_query :', datetime.now())  # , data

            # except:
            # data = []

            i = 0

            if len(data) > 0:

                while (i < len(data)):

                    row = data[i]

                    prefix = row[0]

                    if prefix not in week_prefix[ixp]:
                        week_prefix[ixp].append(prefix)

                    i += 1

    print(ixp, 'len(week_prefix[ixp]) = ', len(week_prefix[ixp]))

# print week_prefix

# sys.exit()

### Compute the percentage of assigned prefixes by Afrinic that are seen at the ASN.

for cc in CC_IXP:

    for ixp in CC_IXP[cc]:

        if ixp in list(week_prefix.keys()):

            print()
            print('Number of ASNs allocated to CC:', len(CC_ASNs_AFRINIC[cc]))
            print('Number of Origin ASNs seen at the IXP:', len(list(set(week_prefix[ixp]))))

            intersection = []
            rest = []

            for prefix_adv in week_prefix[ixp]:
                if prefix_adv != '0.0.0.0/0':
                    prefix_AF_adv = ipaddr.IPNetwork(str(prefix_adv))
                    for prefix_assigned in CC_ASNs_AFRINIC[cc]:
                        # if prefix_assigned not in intersection and prefix_assigned != '0.0.0.0/0':
                        prefix_AF_assigned = ipaddr.IPNetwork(str(prefix_assigned))

                        if cidrsOverlap(prefix_AF_adv, prefix_AF_assigned):
                            # if prefix_AF_adv.overlaps(prefix_AF_assigned):
                            print('Filling the file 1_percentage_of_allocated_prefixes_seen_at_an_IXP.txt',
                                  prefix_AF_adv, ' overlaps ', prefix_AF_assigned)
                            if prefix_assigned not in intersection:
                                intersection.append(prefix_assigned)

            if '0.0.0.0/0' in intersection:
                intersection.remove('0.0.0.0/0')

            if '0.0.0.0/0' in CC_ASNs_AFRINIC[cc]:
                CC_ASNs_AFRINIC[cc].remove('0.0.0.0/0')

            rest = list(set(CC_ASNs_AFRINIC[cc]) - set(intersection))

            current_filename = output_folder + '/Prefix_assigned_to_country_seen_at_' + ixp + '.txt'

            if len(intersection) > 0:
                with open(current_filename, 'a') as fd:
                    for elmt in intersection:
                        fd.write('%s\n' % (elmt))

            current_filename = output_folder + '/Prefix_assigned_to_country_Not_seen_at_' + ixp + '.txt'
            if len(rest) > 0:
                with open(current_filename, 'a') as fd:
                    for elmt in rest:
                        fd.write('%s\n' % (elmt))

            percentage_found = (100 * float(len(intersection))) / float(len(CC_ASNs_AFRINIC[cc]))
            print('intersection ', len(intersection))
            print('percentage in % for Prefixes: ', ixp, len(list(set(week_prefix[ixp]))), len(intersection),
                  len(CC_ASNs_AFRINIC[cc]), percentage_found)

            with open(output_folder + '/1_percentage_of_allocated_prefixes_by_Afrinic_seen_at_an_IXP.txt', 'a') as fd:
                fd.write('%s; %s; %s; %s; %s\n' % (
                ixp, len(list(set(week_prefix[ixp]))), len(intersection), len(CC_ASNs_AFRINIC[cc]), percentage_found))
                fd.close()

#### Classify by type of Origin AS
##### Classifying them into local or external

command = 'mkdir  ' + output_folder + 'files_prefixes/'
os.system(command)

update = 0

IXP_OriginASes = {}

IXP_OriginASes = copy.deepcopy(week_prefix)

##### We are here now
Listrest_ASes = {}
for ixp in list(IXP_OriginASes.keys()):
    print()
    print()

    filename = output_folder + 'Percentage_prefixes_by_country_assignment_' + ixp + '.txt'
    filename1 = output_folder + 'Percentage_prefixes_by_region_' + ixp + '.txt'

    with open(filename, 'a') as fd:
        fd.write('%s;%s;%s;%s;%s;%s;%s;%s\n' % (
        '##Current_CC', 'Country name', 'Intersection visible prefixes & prefixes assigned to the country',
        'num prefixes seen at the IXP', 'Percentage_local_AF', 'num prefixes assigned by Afrinic to the CC',
        'Percentage_local_AF2', 'RIR'))

    with open(filename1, 'a') as fg:
        fg.write('%s;%s;%s\n' % ('##Type of ASNs (Region)', 'len_prefixes_Type', 'percentage_type'))

    for CC in list(CC_IXP.keys()):

        for ixp1 in CC_IXP[CC]:

            if ixp == ixp1:

                print(ixp, CC)
                print(ixp, len(IXP_OriginASes[ixp]))
                current_CC = CC
                print()

                ## Listrest_ASes contains all the prefixes seen at the IXP, and will later contain all the prefixes seen at the IXP that a matching with a prefix allocated by AFRINIC to the country.
                if ixp not in list(Listrest_ASes.keys()):
                    Listrest_ASes[ixp] = []

                Listrest_ASes[ixp] = copy.deepcopy(IXP_OriginASes[ixp])

                ## Local: Allows to find all prefixes that are local to AFRINIC and the country found in the advertised prefixes; here we just consider exact prefixes advertised. What $
                intersection = list(set(IXP_OriginASes[ixp]) & set(CC_ASNs_AFRINIC[current_CC]))
                intersection00 = copy.deepcopy(intersection)

                # for prefix_adv1 in intersection00:
                #    if prefix_adv1 in Listrest_ASes[ixp]:
                #        Listrest_ASes[ixp].remove(prefix_adv1)

                for prefix_adv in IXP_OriginASes[ixp]:
                    if prefix_adv != '0.0.0.0/0' and 'None' not in prefix_adv:
                        prefix_AF_adv = ipaddr.IPNetwork(str(prefix_adv))
                        for prefix_assigned in CC_ASNs_AFRINIC[current_CC]:

                            # if prefix_assigned not in intersection and prefix_assigned != '0.0.0.0/0':
                            prefix_AF_assigned = ipaddr.IPNetwork(str(prefix_assigned))

                            if cidrsOverlap(prefix_AF_adv, prefix_AF_assigned):
                                # if prefix_AF_adv.overlaps(prefix_AF_assigned):
                                print(prefix_AF_adv, ' overlaps ', prefix_AF_assigned)
                                if prefix_assigned not in intersection:
                                    intersection.append(prefix_assigned)

                                if prefix_adv not in intersection00 and prefix_adv != '0.0.0.0/0':
                                    intersection00.append(prefix_adv)

                                if prefix_adv in Listrest_ASes[ixp]:
                                    Listrest_ASes[ixp].remove(prefix_adv)

                if '0.0.0.0/0' in intersection:
                    intersection.remove('0.0.0.0/0')

                if '0.0.0.0/0' in CC_ASNs_AFRINIC[current_CC]:
                    CC_ASNs_AFRINIC[current_CC].remove('0.0.0.0/0')

                if '0.0.0.0/0' in IXP_OriginASes[ixp]:
                    IXP_OriginASes[ixp].remove('0.0.0.0/0')

                try:
                    percentage_local_AF = 100 * (float(len(intersection00)) / float(len(IXP_OriginASes[ixp])))

                except:
                    percentage_local_AF = 0.0

                print('percentage_local_AF =', percentage_local_AF)

                ## Percentage of ASNs allocated to the country visibles at the IXP
                try:
                    percentage_local_AF2 = 100 * (float(len(intersection)) / float(len(CC_ASNs_AFRINIC[current_CC])))
                except:
                    percentage_local_AF2 = 0.0

                with open(filename, 'a') as fd:
                    if len(intersection) > 0:
                        try:
                            A = pycountry.countries.get(alpha2=current_CC)
                            fd.write('%s;%s;%s;%s;%s;%s;%s;%s\n' % (
                            current_CC, A.name, len(intersection), len(IXP_OriginASes[ixp]), percentage_local_AF,
                            len(CC_ASNs_AFRINIC[current_CC]), percentage_local_AF2, 'AFRINIC'))
                        except:
                            fd.write('%s;%s;%s;%s;%s;%s;%s;%s\n' % (
                            current_CC, '', len(intersection), len(IXP_OriginASes[ixp]), percentage_local_AF,
                            len(CC_ASNs_AFRINIC[current_CC]), percentage_local_AF2, 'AFRINIC'))

                print('local_AFRINIC =', percentage_local_AF)
                with open(filename1, 'a') as fg:
                    fg.write('%s;%s;%s\n' % ('Local AFRINIC prefixes', len(intersection), percentage_local_AF))

                if len(intersection) > 0:
                    current_filename = output_folder + 'files_prefixes/Local_AFRINIC_prefixes_' + ixp + '.txt'
                    for elmt in intersection:
                        with open(current_filename, 'a') as fd:
                            fd.write('%s\n' % (elmt))

                # print
                # print 'I am priting the list of prefixes remaining'

                # for ixp in Listrest_ASes.keys():
                #   print ixp, len(Listrest_ASes[ixp])

                #   for elmt in Listrest_ASes[ixp]:
                #       with open(output_folder + 'Listrest_ASes_' + ixp + '.txt' , 'a') as fg:
                #            fg.write('%s\n' %(elmt))

                # sys.exit()

                # if 1:
                ###### AFRINIC: countries different from the country hosting the IXP

                total = 0
                total1 = 0

                # for cc_external in CC_IXP.keys():
                for cc_external in list(CC_ASNs_AFRINIC.keys()):

                    print('external cc in AFRINIC region to make intersection with the local ASNs:', cc_external)

                    if current_CC != cc_external:
                        print('length of ASNs in a cc_external', cc_external, ' = ',
                              len(set(CC_ASNs_AFRINIC[cc_external])))
                        intersection2 = list(set(IXP_OriginASes[ixp]) & set(CC_ASNs_AFRINIC[cc_external]))
                        intersection22 = copy.deepcopy(intersection2)

                        # for prefix_adv1 in intersection22:
                        #    if prefix_adv1 in Listrest_ASes[ixp]:
                        #        Listrest_ASes[ixp].remove(prefix_adv1)

                        for prefix_adv in IXP_OriginASes[ixp]:
                            if prefix_adv != '0.0.0.0/0' and 'None' not in prefix_adv:
                                prefix_AF_adv = ipaddr.IPNetwork(str(prefix_adv))
                                for prefix_assigned in CC_ASNs_AFRINIC[cc_external]:
                                    # if prefix_assigned not in intersection2 and prefix_assigned != '0.0.0.0/0':
                                    prefix_AF_assigned = ipaddr.IPNetwork(str(prefix_assigned))

                                    if cidrsOverlap(prefix_AF_adv, prefix_AF_assigned):
                                        # if prefix_AF_adv.overlaps(prefix_AF_assigned):
                                        print(prefix_AF_adv, ' overlaps ', prefix_AF_assigned)
                                        if prefix_assigned not in intersection2:
                                            intersection2.append(prefix_assigned)

                                        if prefix_adv not in intersection22 and prefix_adv != '0.0.0.0/0':
                                            intersection22.append(prefix_adv)

                                        if prefix_adv in Listrest_ASes[ixp]:
                                            Listrest_ASes[ixp].remove(prefix_adv)

                        if '0.0.0.0/0' in intersection2:
                            intersection2.remove('0.0.0.0/0')

                        if '0.0.0.0/0' in CC_ASNs_AFRINIC[cc_external]:
                            CC_ASNs_AFRINIC[cc_external].remove('0.0.0.0/0')

                        if '0.0.0.0/0' in IXP_OriginASes[ixp]:
                            IXP_OriginASes[ixp].remove('0.0.0.0/0')

                        if len(intersection2) > 0:
                            current_filename = output_folder + 'files_prefixes/External_AFRINIC_prefixes_' + ixp + '.txt'
                            for elmt in intersection2:
                                with open(current_filename, 'a') as fd:
                                    fd.write('%s\n' % (elmt))

                        try:
                            percentage_external_AF = 100 * (
                                        float(len(intersection22)) / float(len(IXP_OriginASes[ixp])))

                        except:
                            percentage_external_AF = 0.0

                        print('percentage_external_AF =', percentage_external_AF)

                        print('length of intersection2:', len(intersection2))

                        try:
                            percentage_external_AF2 = 100 * (
                                        float(len(intersection2)) / float(len(CC_ASNs_AFRINIC[cc_external])))

                        except:
                            percentage_external_AF2 = 0.0

                        with open(filename, 'a') as fd:
                            if len(intersection2) > 0:
                                try:
                                    A = pycountry.countries.get(alpha2=cc_external)
                                    fd.write('%s;%s;%s;%s;%s;%s;%s;%s\n' % (
                                    cc_external, A.name, len(intersection2), len(IXP_OriginASes[ixp]),
                                    percentage_external_AF, len(CC_ASNs_AFRINIC[cc_external]), percentage_external_AF2,
                                    'AFRINIC'))
                                except:
                                    fd.write('%s;%s;%s;%s;%s;%s;%s;%s\n' % (
                                    cc_external, '', len(intersection2), len(IXP_OriginASes[ixp]),
                                    percentage_external_AF, len(CC_ASNs_AFRINIC[cc_external]), percentage_external_AF2,
                                    'AFRINIC'))

                        total += percentage_external_AF
                        total1 += len(intersection22)

                    else:
                        pass

                with open(filename1, 'a') as fg:
                    fg.write('%s;%s;%s\n' % ('External AFRINIC prefixes', total1, total))

                ## Je suis ici
                # print
                # print 'I am priting the list of prefixes remaining'

                # for ixp in Listrest_ASes.keys():
                #   print ixp, len(Listrest_ASes[ixp])

                #   for elmt in Listrest_ASes[ixp]:
                #       with open(output_folder + 'Listrest_ASes_' + ixp + '.txt' , 'a') as fg:
                #            fg.write('%s\n' %(elmt))

                # sys.exit()

                # if 1:
                ###### RIPE

                total = 0
                total1 = 0
                print("AFRINIC REGION DONE. LET'S MOVE TO RIPE")
                for cc_region in CC_ASNs_RIPE:
                    print('CCs in other regions')
                    if current_CC != cc_region:

                        print()
                        print('length of ASNs in a cc_region', len(set(CC_ASNs_RIPE[cc_region])))
                        intersection3 = list(set(IXP_OriginASes[ixp]) & set(CC_ASNs_RIPE[cc_region]))
                        intersection33 = copy.deepcopy(intersection3)

                        # for prefix_adv1 in intersection33:
                        #    if prefix_adv1 in Listrest_ASes[ixp]:
                        #        Listrest_ASes[ixp].remove(prefix_adv1)

                        for prefix_adv in IXP_OriginASes[ixp]:
                            if prefix_adv != '0.0.0.0/0' and 'None' not in prefix_adv:
                                prefix_AF_adv = ipaddr.IPNetwork(str(prefix_adv))

                                for prefix_assigned in CC_ASNs_RIPE[cc_region]:

                                    # if prefix_assigned not in intersection3 and prefix_assigned != '0.0.0.0/0':
                                    prefix_AF_assigned = ipaddr.IPNetwork(str(prefix_assigned))

                                    if cidrsOverlap(prefix_AF_adv, prefix_AF_assigned):
                                        # if prefix_AF_adv.overlaps(prefix_AF_assigned):
                                        print(prefix_AF_adv, ' overlaps ', prefix_AF_assigned)

                                        if prefix_assigned not in intersection3:
                                            intersection3.append(prefix_assigned)

                                        if prefix_adv not in intersection33 and prefix_adv != '0.0.0.0/0':
                                            intersection33.append(prefix_adv)

                                        if prefix_adv in Listrest_ASes[ixp]:
                                            Listrest_ASes[ixp].remove(prefix_adv)

                        if '0.0.0.0/0' in intersection3:
                            intersection3.remove('0.0.0.0/0')

                        if '0.0.0.0/0' in CC_ASNs_RIPE[cc_region]:
                            CC_ASNs_RIPE[cc_region].remove('0.0.0.0/0')

                        if '0.0.0.0/0' in IXP_OriginASes[ixp]:
                            IXP_OriginASes[ixp].remove('0.0.0.0/0')

                        if len(intersection3) > 0:
                            current_filename = output_folder + 'files_prefixes/RIPE_prefixes_' + ixp + '.txt'
                            for elmt in intersection3:
                                with open(current_filename, 'a') as fd:
                                    fd.write('%s\n' % (elmt))

                        try:
                            percentage_RIPE = 100 * (float(len(intersection33)) / float(len(IXP_OriginASes[ixp])))

                        except:
                            percentage_RIPE = 0.0

                        try:
                            percentage_RIPE2 = 100 * (float(len(intersection3)) / float(len(CC_ASNs_RIPE[cc_region])))

                        except:
                            percentage_RIPE2 = 0.0

                        print('length of intersection3:', len(intersection3))

                        with open(filename, 'a') as fd:
                            if len(intersection3) > 0:
                                try:
                                    A = pycountry.countries.get(alpha2=cc_region)
                                    fd.write('%s;%s;%s;%s;%s;%s;%s;%s\n' % (
                                    cc_region, A.name, len(intersection3), len(IXP_OriginASes[ixp]), percentage_RIPE,
                                    len(CC_ASNs_RIPE[cc_region]), percentage_RIPE2, 'RIPE'))

                                except:
                                    fd.write('%s;%s;%s;%s;%s;%s;%s;%s\n' % (
                                    cc_region, '', len(intersection3), len(IXP_OriginASes[ixp]), percentage_RIPE,
                                    len(CC_ASNs_RIPE[cc_region]), percentage_RIPE2, 'RIPE'))

                        total += percentage_RIPE
                        total1 += len(intersection33)

                    else:
                        print('----')
                        print('cc coincides with another in other region which is:', cc_region)
                        print('----')

                with open(filename1, 'a') as fg:
                    fg.write('%s;%s;%s\n' % ('RIPE prefixes', total1, total))

                ## Je suis ici
                # print
                # print 'I am priting the list of prefixes remaining'

                # for ixp in Listrest_ASes.keys():
                #   print ixp, len(Listrest_ASes[ixp])

                #   for elmt in Listrest_ASes[ixp]:
                #       with open(output_folder + 'Listrest_ASes_' + ixp + '.txt' , 'a') as fg:
                #            fg.write('%s\n' %(elmt))

                # sys.exit()

                ###### ARIN
                # if 1:

                total = 0
                total1 = 0
                print("AFRINIC & RIPE REGION DONE. LET'S MOVE TO ARIN")
                for cc_region in CC_ASNs_ARIN:
                    if current_CC != cc_region:
                        # if cc_region not in ori_dict['ARIN'].keys():

                        print()
                        print('length of ASNs in a cc_region', len(set(CC_ASNs_ARIN[cc_region])))
                        intersection5 = list(set(IXP_OriginASes[ixp]) & set(CC_ASNs_ARIN[cc_region]))
                        intersection55 = copy.deepcopy(intersection5)

                        # for prefix_adv1 in intersection55:
                        #        if prefix_adv1 in Listrest_ASes[ixp]:
                        #            Listrest_ASes[ixp].remove(prefix_adv1)

                        for prefix_adv in IXP_OriginASes[ixp]:
                            if prefix_adv != '0.0.0.0/0' and 'None' not in prefix_adv:
                                prefix_AF_adv = ipaddr.IPNetwork(str(prefix_adv))

                                for prefix_assigned in CC_ASNs_ARIN[cc_region]:
                                    # if prefix_assigned not in intersection5 and prefix_assigned != '0.0.0.0/0':
                                    prefix_AF_assigned = ipaddr.IPNetwork(str(prefix_assigned))

                                    if cidrsOverlap(prefix_AF_adv, prefix_AF_assigned):
                                        # if prefix_AF_adv.overlaps(prefix_AF_assigned):
                                        print(prefix_AF_adv, ' overlaps ', prefix_AF_assigned)
                                        if prefix_assigned not in intersection5:
                                            intersection5.append(prefix_assigned)

                                        if prefix_adv not in intersection55 and prefix_adv != '0.0.0.0/0':
                                            intersection55.append(prefix_adv)

                                        if prefix_adv in Listrest_ASes[ixp]:
                                            Listrest_ASes[ixp].remove(prefix_adv)

                        if '0.0.0.0/0' in intersection5:
                            intersection5.remove('0.0.0.0/0')

                        if '0.0.0.0/0' in CC_ASNs_ARIN[cc_region]:
                            CC_ASNs_ARIN[cc_region].remove('0.0.0.0/0')

                        if '0.0.0.0/0' in IXP_OriginASes[ixp]:
                            IXP_OriginASes[ixp].remove('0.0.0.0/0')

                        if len(intersection5) > 0:
                            current_filename = output_folder + 'files_prefixes/ARIN_prefixes_' + ixp + '.txt'
                            for elmt in intersection5:
                                with open(current_filename, 'a') as fd:
                                    fd.write('%s\n' % (elmt))

                        try:
                            percentage_ARIN = 100 * (float(len(intersection5)) / float(len(IXP_OriginASes[ixp])))
                        except:
                            percentage_ARIN = 0.0

                        try:
                            percentage_ARIN2 = 100 * (float(len(intersection5)) / float(len(CC_ASNs_ARIN[cc_region])))
                        except:
                            percentage_ARIN2 = 0.0

                        print('length of intersection5:', len(intersection5))

                        with open(filename, 'a') as fd:
                            if len(intersection5) > 0:
                                try:
                                    A = pycountry.countries.get(alpha2=cc_region)
                                    fd.write('%s;%s;%s;%s;%s;%s;%s;%s\n' % (
                                    cc_region, A.name, len(intersection5), len(IXP_OriginASes[ixp]), percentage_ARIN,
                                    len(CC_ASNs_ARIN[cc_region]), percentage_ARIN2, 'ARIN'))
                                except:
                                    fd.write('%s;%s;%s;%s;%s;%s;%s;%s\n' % (
                                    cc_region, '', len(intersection5), len(IXP_OriginASes[ixp]), percentage_ARIN,
                                    len(CC_ASNs_ARIN[cc_region]), percentage_ARIN2, 'ARIN'))

                        total += percentage_ARIN
                        total1 += len(intersection55)

                    else:
                        print('----')
                        print('cc coincides with another in other region which is:', cc_region)
                        print('----')
                        pass

                with open(filename1, 'a') as fg:
                    fg.write('%s;%s;%s\n' % ('ARIN prefixes', total1, total))

                ## Je suis ici
                # print
                # print 'I am priting the list of prefixes remaining'

                # for ixp in Listrest_ASes.keys():
                #   print ixp, len(Listrest_ASes[ixp])

                #   for elmt in Listrest_ASes[ixp]:
                #       with open(output_folder + 'Listrest_ASes_' + ixp + '.txt' , 'a') as fg:
                #            fg.write('%s\n' %(elmt))

                # sys.exit()

                # if 1:
                ###### APNIC

                total = 0
                total1 = 0
                print("AFRINIC, RIPE & ARIN REGION DONE. LET'S MOVE TO APNIC")
                for cc_region in CC_ASNs_APNIC:
                    if current_CC != cc_region:
                        # if cc_region not in ori_dict['APNIC'].keys():
                        print()
                        print('length of ASNs in a cc_region', len(set(CC_ASNs_APNIC[cc_region])))

                        intersection4 = list(set(IXP_OriginASes[ixp]) & set(CC_ASNs_APNIC[cc_region]))
                        intersection44 = copy.deepcopy(intersection4)

                        # for prefix_adv1 in intersection44:
                        #    if prefix_adv1 in Listrest_ASes[ixp]:
                        #        Listrest_ASes[ixp].remove(prefix_adv1)

                        for prefix_adv in IXP_OriginASes[ixp]:
                            if prefix_adv != '0.0.0.0/0' and 'None' not in prefix_adv:
                                prefix_AF_adv = ipaddr.IPNetwork(str(prefix_adv))
                                for prefix_assigned in CC_ASNs_APNIC[cc_region]:
                                    # if prefix_assigned not in intersection3 and prefix_assigned != '0.0.0.0/0':
                                    prefix_AF_assigned = ipaddr.IPNetwork(str(prefix_assigned))

                                    if cidrsOverlap(prefix_AF_adv, prefix_AF_assigned):
                                        # if prefix_AF_adv.overlaps(prefix_AF_assigned):
                                        print(prefix_AF_adv, ' overlaps ', prefix_AF_assigned)

                                        if prefix_assigned not in intersection4:
                                            intersection4.append(prefix_assigned)

                                        if prefix_adv not in intersection44 and prefix_assigned != '0.0.0.0/0':
                                            intersection44.append(prefix_adv)

                                        if prefix_adv in Listrest_ASes[ixp]:
                                            Listrest_ASes[ixp].remove(prefix_adv)

                        if '0.0.0.0/0' in intersection4:
                            intersection4.remove('0.0.0.0/0')

                        if '0.0.0.0/0' in CC_ASNs_APNIC[cc_region]:
                            CC_ASNs_APNIC[cc_region].remove('0.0.0.0/0')

                        if '0.0.0.0/0' in IXP_OriginASes[ixp]:
                            IXP_OriginASes[ixp].remove('0.0.0.0/0')

                        if len(intersection4) > 0:
                            current_filename = output_folder + 'files_prefixes/APNIC_prefixes_' + ixp + '.txt'
                            for elmt in intersection4:
                                with open(current_filename, 'a') as fd:
                                    fd.write('%s\n' % (elmt))

                        try:
                            percentage_APNIC = 100 * (float(len(intersection44)) / float(len(IXP_OriginASes[ixp])))
                        except:
                            percentage_APNIC = 0.0

                        try:
                            percentage_APNIC2 = float(len(intersection4)) / float(len(CC_ASNs_APNIC[cc_region])) * 100
                        except:
                            percentage_APNIC2 = 0.0

                        print('length of intersection4:', len(intersection4))

                        with open(filename, 'a') as fd:
                            if len(intersection4) > 0:
                                try:
                                    A = pycountry.countries.get(alpha2=cc_region)
                                    fd.write('%s;%s;%s;%s;%s;%s;%s;%s\n' % (
                                    cc_region, A.name, len(intersection4), len(IXP_OriginASes[ixp]), percentage_APNIC,
                                    len(CC_ASNs_APNIC[cc_region]), percentage_APNIC2, 'APNIC'))
                                except:
                                    fd.write('%s;%s;%s;%s;%s;%s;%s;%s\n' % (
                                    cc_region, '', len(intersection4), len(IXP_OriginASes[ixp]), percentage_APNIC,
                                    len(CC_ASNs_APNIC[cc_region]), percentage_APNIC2, 'APNIC'))

                                total += percentage_APNIC
                                total1 += len(intersection44)

                    else:
                        print('----')
                        print('cc coincides with another in other region which is:', cc_region)
                        print('----')

                with open(filename1, 'a') as fg:
                    fg.write('%s;%s;%s\n' % ('APNIC prefixes', total1, total))

                ## Je suis ici
                # print
                # print 'I am priting the list of prefixes remaining'

                # for ixp in Listrest_ASes.keys():
                #   print ixp, len(Listrest_ASes[ixp])

                #   for elmt in Listrest_ASes[ixp]:
                #       with open(output_folder + 'Listrest_ASes_' + ixp + '.txt' , 'a') as fg:
                #            fg.write('%s\n' %(elmt))

                # sys.exit()

                # if 1:

                ###### LACNIC

                total = 0
                total1 = 0
                print("AFRINIC, RIPE, ARIN & APNIC REGION DONE. LET'S MOVE TO LACNIC")
                for cc_region in CC_ASNs_LACNIC:
                    if current_CC != cc_region:
                        # if cc_region not in ori_dict['LACNIC'].keys():
                        print()
                        print('length of ASNs in a cc_region', len(set(CC_ASNs_LACNIC[cc_region])))
                        intersection6 = list(set(IXP_OriginASes[ixp]) & set(CC_ASNs_LACNIC[cc_region]))
                        intersection66 = copy.deepcopy(intersection6)

                        for prefix_adv in IXP_OriginASes[ixp]:
                            if prefix_adv != '0.0.0.0/0' and 'None' not in prefix_adv:
                                prefix_AF_adv = ipaddr.IPNetwork(str(prefix_adv))
                                for prefix_assigned in CC_ASNs_LACNIC[cc_region]:
                                    # if prefix_assigned not in intersection3 and prefix_assigned != '0.0.0.0/0':
                                    prefix_AF_assigned = ipaddr.IPNetwork(str(prefix_assigned))

                                    if cidrsOverlap(prefix_AF_adv, prefix_AF_assigned):
                                        # if prefix_AF_adv.overlaps(prefix_AF_assigned):
                                        print(prefix_AF_adv, ' overlaps ', prefix_AF_assigned)
                                        if prefix_assigned not in intersection6:
                                            intersection6.append(prefix_assigned)

                                        if prefix_adv not in intersection66 and prefix_adv != '0.0.0.0/0':
                                            intersection66.append(prefix_adv)

                                        if prefix_adv in Listrest_ASes[ixp]:
                                            Listrest_ASes[ixp].remove(prefix_adv)

                        if '0.0.0.0/0' in intersection6:
                            intersection6.remove('0.0.0.0/0')

                        if '0.0.0.0/0' in CC_ASNs_LACNIC[cc_region]:
                            CC_ASNs_LACNIC[cc_region].remove('0.0.0.0/0')

                        if '0.0.0.0/0' in IXP_OriginASes[ixp]:
                            IXP_OriginASes[ixp].remove('0.0.0.0/0')

                        if len(intersection6) > 0:
                            current_filename = output_folder + 'files_prefixes/LACNIC_prefixes_' + ixp + '.txt'
                            for elmt in intersection6:
                                with open(current_filename, 'a') as fd:
                                    fd.write('%s\n' % (elmt))

                        try:
                            percentage_LACNIC = 100 * (float(len(intersection66)) / float(len(IXP_OriginASes[ixp])))
                        except:
                            percentage_LACNIC = 0.0

                        try:
                            percentage_LACNIC2 = 100 * (
                                        float(len(intersection6)) / float(len(CC_ASNs_LACNIC[cc_region])))
                        except:
                            percentage_LACNIC2 = 0.0

                        print('length of intersection6:', len(intersection6))

                        with open(filename, 'a') as fd:
                            if len(intersection6) > 0:
                                try:
                                    A = pycountry.countries.get(alpha2=cc_region)
                                    fd.write('%s;%s;%s;%s;%s;%s;%s;%s\n' % (
                                    cc_region, A.name, len(intersection6), len(IXP_OriginASes[ixp]), percentage_LACNIC,
                                    len(CC_ASNs_LACNIC[cc_region]), percentage_LACNIC2, 'LACNIC'))
                                except:
                                    fd.write('%s;%s;%s;%s;%s;%s;%s;%s\n' % (
                                    cc_region, '', len(intersection6), len(IXP_OriginASes[ixp]), percentage_LACNIC,
                                    len(CC_ASNs_LACNIC[cc_region]), percentage_LACNIC2, 'LACNIC'))

                                total += percentage_LACNIC
                                total1 += len(intersection66)

                with open(filename1, 'a') as fg:
                    fg.write('%s;%s;%s\n' % ('LACNIC prefixes', total1, total))

print()
print('I am priting the list of prefixes remaining')

for ixp in list(Listrest_ASes.keys()):
    print(ixp, len(Listrest_ASes[ixp]))
    for elmt in Listrest_ASes[ixp]:
        with open(output_folder + 'Listrest_ASes_' + ixp + '.txt', 'a') as fg:
            fg.write('%s\n' % (elmt))

now_datetime = str(datetime.now()).replace(' ', '_')
finish = open('finish_lastmonth_better.txt', 'w')
finish.write('ended' + '; ' + root_folder + output_folder[6:] + '; ' + now_datetime)
finish.close()
