##############################################################################
# __author__ = "Roderick Fanou"
# __status__ = "Production"
# __description__ = "This script generates "
# __last_modifications__ =
# by Roderick
# "2016-11-28"
##############################################################################

finish = open('finish_lastyear.txt', 'w')
finish.write('started')
finish.close()


def cidrsOverlap(cidr0, cidr1):
    return cidr0 in cidr1 or cidr1 in cidr0


# !/usr/bin/python
import re, sys, csv
import MySQLdb
from pprint import pprint
from time import sleep
from datetime import datetime
import os.path

# import collections, sys, os, time, re, string
from netaddr import *

# from operator import itemgetter
# import json, copy, math, time
# from pprint import pprint
# from random import choice
# from pprint import pprint
# import select, socket, time, sys
# import urllib2, urllib, glob


## import all files in the library you need
sys.path.append('../../2_libraries/')
import DB_configuration
from define_timescales import *
from functions import *

now_datetime = str(datetime.now()).replace(' ', '_')

## Create a logfile:
name_log_file = 'Log_' + str(
    now_datetime) + '_' + 'RegionalView_1_Number_prefixes_visible_at_an_IXP_lastmonth_each_country' + '.txt'
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
month_prefix = {}
month_prefix_bogon = {}

Current_db = 'MergedData'
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

    if row[2] not in list(month_prefix.keys()):
        month_prefix[row[2]] = {}
        month_prefix_bogon[row[2]] = {}

    IXP_collector[row[0]].append(row[1])
    i += 1

print('IXP_collector = ', IXP_collector)
print()
print('IXP_CC = ', IXP_CC)
print()
print('month_ASN = ', month_prefix)

root_folder = '/home/arda/African_Route-collectors_Data_Analyzer-ARDA/ComputationVM/Heart/'

output_folder = '../../Computation_outputs_National_View/3_Number_unique_prefixes_visibles_at_all_IXP_of_a_country_lastyear/'

## Update the folder with the selected repository
IXPView_output_folder = '/var/www/html/.../outputs/1_Number_prefixes_visibles_at_an_IXP_multiyear_lastyear/'

command = 'rm -rf ' + output_folder
os.system(command)

command = 'mkdir  ' + output_folder
os.system(command)

command = 'chmod 777 ' + output_folder
os.system(command)

if os.listdir(IXPView_output_folder) != []:

    for ixp in list(IXP_collector.keys()):

        CC_to_consider = IXP_CC[ixp]

        filename = IXPView_output_folder + """LastYear__list_visible_prefixes_at_IXP_""" + ixp + '.txt'

        if os.path.isfile(filename):

            with open(filename, 'r') as fg:

                for line in fg:

                    line = line.strip()

                    print(line)

                    tab = line.split('; ')

                    if '#' not in line:

                        if '/' in tab[-1]:

                            prefix_to_add = tab[-1]

                            del (tab[1])

                            couple_timestamp = '; '.join(tab)

                            if couple_timestamp not in month_prefix[CC_to_consider]:
                                month_prefix[CC_to_consider][couple_timestamp] = []

                            ## make sure the prefixes do not overlap

                            if prefix_to_add not in month_prefix[CC_to_consider][couple_timestamp]:
                                month_prefix[CC_to_consider][couple_timestamp].append(prefix_to_add)




                        elif 'Bogon' in tab[-1] or 'bogon' in tab[-1]:

                            prefix_to_add_bogon = tab[-2]

                            print('Bogon prefix = ', prefix_to_add_bogon)

                            del (tab[-1])

                            del (tab[-1])

                            couple_timestamp_bogon = '; '.join(tab)

                            print('couple_timestamp = ', couple_timestamp_bogon)

                            if CC_to_consider not in list(month_prefix.keys()):
                                month_prefix[CC_to_consider] = {}

                            if CC_to_consider not in list(month_prefix_bogon.keys()):
                                month_prefix_bogon[CC_to_consider] = {}

                            if couple_timestamp_bogon not in list(month_prefix[CC_to_consider].keys()):
                                month_prefix[CC_to_consider][couple_timestamp_bogon] = []

                            if couple_timestamp_bogon not in list(month_prefix_bogon[CC_to_consider].keys()):
                                month_prefix_bogon[CC_to_consider][couple_timestamp_bogon] = []

                            ## make sure the prefixes do not overlap

                            if prefix_to_add_bogon not in month_prefix[CC_to_consider][couple_timestamp_bogon]:
                                month_prefix[CC_to_consider][couple_timestamp_bogon].append(prefix_to_add_bogon)

                            if prefix_to_add_bogon not in month_prefix_bogon[CC_to_consider][couple_timestamp_bogon]:
                                month_prefix_bogon[CC_to_consider][couple_timestamp_bogon].append(prefix_to_add_bogon)




                        else:

                            while '/' not in tab[-1] and len(tab) >= 1:
                                del (tab[-1])

                            if '/' in tab[-1]:

                                prefix_to_add = tab[-1]

                                print('prefix = ', prefix_to_add)

                                del (tab[-1])

                                couple_timestamp = '; '.join(tab)

                                print('couple_timestamp = ', couple_timestamp)

                                print()

                                if CC_to_consider not in list(month_prefix.keys()):
                                    month_prefix[CC_to_consider] = {}

                                if couple_timestamp not in list(month_prefix[CC_to_consider].keys()):
                                    month_prefix[CC_to_consider][couple_timestamp] = []

                                ## make sure the prefixes do not overlap

                                if prefix_to_add not in month_prefix[CC_to_consider][couple_timestamp]:
                                    month_prefix[CC_to_consider][couple_timestamp].append(prefix_to_add)

for CC in month_prefix:

    with open(output_folder + 'LastYear__list_visible_prefixes_at_IXP_' + CC + '.txt', 'a') as fh21:

        fh21.write('%s\n' % ("""###Month-Year; Visible prefixes at the IXP; Bogon?"""))

    for couple_timestamp1 in list(month_prefix[CC].keys()):

        for elmt in month_prefix[CC][couple_timestamp1]:

            if couple_timestamp1 in list(month_prefix_bogon[CC].keys()):

                if elmt in month_prefix_bogon[CC][couple_timestamp1]:
                    with open(output_folder + 'LastYear__list_visible_prefixes_at_IXP_' + CC + '.txt', 'a') as fh21:
                        fh21.write('%s; %s; %s\n' % (couple_timestamp1, str(elmt), 'bogon'))

            else:

                with open(output_folder + 'LastYear__list_visible_prefixes_at_IXP_' + CC + '.txt', 'a') as fh21:

                    fh21.write('%s; %s\n' % (couple_timestamp1, str(elmt)))

for CC in month_prefix:

    with open(output_folder + 'LastYear__number_visible_prefixes_at_IXP_' + CC + '.txt', 'a') as fh4:

        fh4.write(
            '%s\n' % ("""###Month-Year; Number of Visible prefixes at the IXP; Number of Visible bogon prefixes"""))

    for couple_timestamp11 in list(month_prefix[CC].keys()):

        if couple_timestamp11 in list(month_prefix_bogon[CC].keys()):

            with open(output_folder + 'LastYear__number_visible_prefixes_at_IXP_' + CC + '.txt', 'a') as fh4:

                fh4.write('%s; %s; %s\n' % (couple_timestamp11, str(len(month_prefix[CC][couple_timestamp11])),
                                            str(len(month_prefix_bogon[CC][couple_timestamp11]))))

        else:

            with open(output_folder + 'LastYear__number_visible_prefixes_at_IXP_' + CC + '.txt', 'a') as fh4:

                fh4.write('%s; %s; %s\n' % (couple_timestamp11, str(len(month_prefix[CC][couple_timestamp11])), '0'))

now_datetime = str(datetime.now()).replace(' ', '_')
finish = open('finish_lastyear.txt', 'w')
finish.write('ended' + '; ' + root_folder + output_folder[6:] + '; ' + now_datetime)
finish.close()
