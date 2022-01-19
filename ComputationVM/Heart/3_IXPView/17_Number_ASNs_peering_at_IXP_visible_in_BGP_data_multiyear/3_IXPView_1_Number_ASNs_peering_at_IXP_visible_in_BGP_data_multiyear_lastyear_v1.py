# The term Unique ASNs refers to the list of distinct ASNs present in the list of all ASNs in the considered timeline. (Note that there is a similarity with point 1 above.)

# We suppress the item ASNs and Prefix growth.
# The evolution of ASNs is plotted as an area graph. We plot on the same graph the evolution of private/reserved #ASNs as an area graph as well.
# On the Y axis, we have the number of unique ASNs counted as explained above. In total, we plan to have 3 graphs with the following timelines on the X axis:
#	last month (Now - 4weeks)  splitted into weeks
#	last year (Now - 12months) splitted into months
#	multiple-years splitted into years


##############################################################################
# __author__ = "Roderick Fanou"
# __status__ = "Production"
# __description__ = "This script generates "
##############################################################################


finish = open('finish_lastyear.txt', 'w')
finish.write('started')
finish.close()

# !/usr/bin/python
import sys, os.path
import MySQLdb
from datetime import datetime
from netaddr import *

## import all files in the library you need
sys.path.append('../../2_libraries/')
import DB_configuration
from define_timescales import *
from functions import *

##
now_datetime = str(datetime.now()).replace(' ', '_')

## Create a logfile:
name_log_file = 'Log_' + str(now_datetime) + '_' + '17_Number_ASNs_peering_at_IXP_visible_in_BGP_data' + '.txt'
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
    IXP_collector[row[0]].append(row[1])
    i += 1

print(IXP_collector)
root_folder = '/home/arda/African_Route-collectors_Data_Analyzer-ARDA/ComputationVM/Heart/'
output_folder = '../../Computation_outputs/17_Number_ASNs_peering_at_IXP_visible_in_BGP_data/'

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
    ASN_year = {}
    year_ASN = {}
    year_ASN_2bytes = {}
    year_ASN_4bytes = {}

    month_ASN = {}
    month_ASN_2bytes = {}
    month_ASN_4bytes = {}
    ASN_month = {}

    for ixp in list(IXP_collector.keys()):

        log_file_instance = open(location_logfile + '/' + name_log_file, 'a')

        create_output_lastyear = open(output_folder + 'LastYear__list_visible_ASNs_peering_at_IXP_' + ixp + '.txt', 'a')

        create_output_lastyear.write('###Month-Year; Visible ASNs peering at IXP \n')

        create_output_lastyear_2bytesASN = open(
            output_folder + 'LastYear__2bytes_list_visible_ASNs_peering_at_IXP_' + ixp + '.txt', 'a')

        create_output_lastyear_2bytesASN.write('###Month-Year; Visible 2bytes ASNs peering at IXP \n')

        create_output_lastyear_4bytesASN = open(
            output_folder + 'LastYear__4bytes_list_visible_ASNs_peering_at_IXP_' + ixp + '.txt', 'a')

        create_output_lastyear_4bytesASN.write('###Month-Year; Visible 4bytes ASNs peering at IXP \n')

        create_output_MultiYear = open(output_folder + 'MultiYear__list_visible_ASNs_at_IXP_' + ixp + '.txt', 'a')

        create_output_MultiYear.write('###Month-Year; Visible Origin ASNs \n')

        create_output_MultiYear_2bytesASN = open(
            output_folder + 'MultiYear__2bytes_list_visible_ASNs_peering_at_IXP_' + ixp + '.txt', 'a')

        create_output_MultiYear_2bytesASN.write('###Month-Year; Visible 2bytes ASNs peering at IXP\n')

        create_output_MultiYear_4bytesASN = open(
            output_folder + 'MultiYear__4bytes_list_visible_ASNs_peering_at_IXP_' + ixp + '.txt', 'a')

        create_output_MultiYear_4bytesASN.write('###Month-Year; Visible 4bytes ASNs peering at IXP \n')

        if ixp not in list(year_ASN.keys()):
            year_ASN[ixp] = {}

        if ixp not in list(year_ASN_2bytes.keys()):
            year_ASN_2bytes[ixp] = {}

        if ixp not in list(year_ASN_4bytes.keys()):
            year_ASN_4bytes[ixp] = {}

        if ixp not in list(month_ASN.keys()):
            month_ASN[ixp] = {}

        if ixp not in list(month_ASN_2bytes.keys()):
            month_ASN_2bytes[ixp] = {}

        if ixp not in list(month_ASN_4bytes.keys()):
            month_ASN_4bytes[ixp] = {}

        for year in yearList:

            if year not in list(year_ASN[ixp].keys()):
                year_ASN[ixp][year] = []

            if year not in list(year_ASN_2bytes[ixp].keys()):
                year_ASN_2bytes[ixp][year] = []

            if year not in list(year_ASN_4bytes[ixp].keys()):
                year_ASN_4bytes[ixp][year] = []

            for month in range(1, 13):
                if 'Data__' + str(year) + "_" + str(month) in List_all_tables:
                    print()
                    print()
                    print(IXP_collector[ixp])

                    # query = "select count(*) from Data__"+str(year)+"_"+str(month) + " ;"
                    # cur.execute(query)
                    # data = cur.fetchall()
                    # print 'number of lines in the table ', data

                    k = 0
                    query = "select distinct  ASPath from Data__" + str(year) + "_" + str(month) + " where"

                    if len(IXP_collector[ixp]) > 1:
                        while k < len(IXP_collector[ixp]) - 1:
                            k += 1
                            query += " RouteCollector = %s or "

                    query += " RouteCollector = %s  and ASpath is not NULL "

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

                            path = row[0].split(' ')

                            if len(path) > 0:

                                try:
                                    if int(str(path[0]).strip()) not in OriginASNs:
                                        OriginASNs.append(int(str(path[0]).strip()))
                                    # print row[1], '; ',  row[0], '; ', int(path[-2])
                                except:
                                    print('Case 2: Alert We pass for this path ', row[0])

                                for OriginASNs_elmt in OriginASNs:

                                    # if ixp not in prefix_year.keys():
                                    #    prefix_year[ixp] = {}
                                    # if prefix not in prefix_year[ixp].keys():
                                    #    prefix_year[ixp][prefix] = []
                                    # if year not in prefix_year[ixp][prefix]:
                                    #    prefix_year[ixp][prefix].append(year)

                                    if OriginASNs_elmt not in year_ASN[ixp][year]:
                                        year_ASN[ixp][year].append(OriginASNs_elmt)
                                        create_output_MultiYear.write(str(year) + '; ' + str(OriginASNs_elmt) + '\n')

                                        # 2 bytes : AS 0 to 65535  ## Reserved: 64512 to 65534 for private; few others such as 0 and 65535
                                        if OriginASNs_elmt >= 0 and OriginASNs_elmt <= 65535 and OriginASNs_elmt not in \
                                                year_ASN_2bytes[ixp][year]:
                                            year_ASN_2bytes[ixp][year].append(OriginASNs_elmt)
                                            create_output_MultiYear_2bytesASN.write(
                                                str(year) + '; ' + str(OriginASNs_elmt) + '\n')

                                        # 4 bytes : AS 65,536 - 4294,967,295; The first thing to notice about these numbers is that they include all of the older 2-byte ASNs, 0 through 65535
                                        # A 4-byte ASN between 0 and 65535 is called a mappable ASN
                                        if OriginASNs_elmt >= 65536 and OriginASNs_elmt <= 4294967295 and OriginASNs_elmt not in \
                                                year_ASN_4bytes[ixp][year]:
                                            year_ASN_4bytes[ixp][year].append(OriginASNs_elmt)
                                            create_output_MultiYear_4bytesASN.write(
                                                str(year) + '; ' + str(OriginASNs_elmt) + '\n')

                                    ## Check if we are in the last year and proceed for lastyear
                                    if (year, month) in lastYearList:
                                        # if ixp not in prefix_month.keys():
                                        #    prefix_month[ixp] = {}
                                        # if prefix not in prefix_month[ixp].keys():
                                        #    prefix_month[ixp][prefix] = []
                                        # if str(month)+'-'+str(year) not in prefix_month[ixp][prefix]:
                                        #    prefix_year[ixp][prefix].append(str(month)+'-'+str(year))

                                        if str(month) + '-' + str(year) not in list(month_ASN[ixp].keys()):
                                            month_ASN[ixp][str(month) + '-' + str(year)] = []

                                        if OriginASNs_elmt not in month_ASN[ixp][str(month) + '-' + str(year)]:
                                            month_ASN[ixp][str(month) + '-' + str(year)].append(OriginASNs_elmt)

                                            if str(month) + '-' + str(year) not in list(month_ASN_2bytes[ixp].keys()):
                                                month_ASN_2bytes[ixp][str(month) + '-' + str(year)] = []

                                            if str(month) + '-' + str(year) not in list(month_ASN_4bytes[ixp].keys()):
                                                month_ASN_4bytes[ixp][str(month) + '-' + str(year)] = []

                                            create_output_lastyear.write(
                                                str(month) + '-' + str(year) + '; ' + str(OriginASNs_elmt) + '\n')

                                            # 2 bytes : AS 0 to 65535  ## Reserved: 64512 to 65534 for private; few others such as 0 and 65535
                                            if OriginASNs_elmt >= 0 and OriginASNs_elmt <= 65535 and OriginASNs_elmt not in \
                                                    month_ASN_2bytes[ixp][str(month) + '-' + str(year)]:
                                                month_ASN_2bytes[ixp][str(month) + '-' + str(year)].append(
                                                    OriginASNs_elmt)
                                                create_output_lastyear_2bytesASN.write(
                                                    str(str(month) + '-' + str(year)) + '; ' + str(
                                                        OriginASNs_elmt) + '\n')

                                            # 4 bytes : AS 65,536 - 4294,967,295; The first thing to notice about these numbers is that they include all of the older 2-byte ASNs, 0 through 65535
                                            # A 4-byte ASN between 0 and 65535 is called a mappable ASN
                                            if OriginASNs_elmt >= 65536 and OriginASNs_elmt <= 4294967295 and OriginASNs_elmt not in \
                                                    month_ASN_4bytes[ixp][str(month) + '-' + str(year)]:
                                                month_ASN_4bytes[ixp][str(month) + '-' + str(year)].append(
                                                    OriginASNs_elmt)
                                                create_output_lastyear_4bytesASN.write(
                                                    str(str(month) + '-' + str(year)) + '; ' + str(
                                                        OriginASNs_elmt) + '\n')

                                i += 1

                    else:
                        print('No ASN found for ', ixp, ' in ', 'Data__' + str(year) + '_' + str(month))

        # for ixp in month_prefix.keys():
        if ixp in list(month_ASN.keys()):

            create_output_lastyear = open(
                output_folder + 'LastYear__number_visible_ASNs_peering_at_IXP_' + ixp + '.txt', 'a')

            create_output_lastyear.write(
                '##Month-Year; Number of Origin ASNs; Number of 2bytes ASNs peering at IXP; Number of 4bytes ASNs peering at IXP \n')

            for elmt in list(month_ASN[ixp].keys()):
                try:
                    Two_Bytes_ASNs = len(list(set(month_ASN_2bytes[ixp][elmt])))
                except:
                    Two_Bytes_ASNs = 0

                try:
                    Four_Bytes_ASNs = len(list(set(month_ASN_4bytes[ixp][elmt])))
                except:
                    Four_Bytes_ASNs = 0

                create_output_lastyear.write(
                    elmt + '; ' + str(len(month_ASN[ixp][elmt])) + '; ' + str(Two_Bytes_ASNs) + '; ' + str(
                        Four_Bytes_ASNs) + '\n')

            # for prefix in month_prefix[ixp][elmt]:
            #    create_output_lastyear =  open('../../'+output_folder+'LastYear__list_visible_prefixes_at_IXP_'+ixp+'.txt', 'a')
            #    create_output_lastyear.write(elmt+ '; '+ str(prefix) + '\n')

        if ixp in list(year_ASN.keys()):

            create_output_MultiYear = open(
                output_folder + 'MultiYear__number_visible_ASNs_peering_at_IXP_' + ixp + '.txt', 'a')

            create_output_MultiYear.write(
                '##Year' + '; Number of OriginASNs ; Number of 2bytes ASNs peering at IXP; Number of 4bytes ASNs peering at IXP \n')

            for year in yearList:

                try:
                    Two_Bytes_ASNs = len(list(set(year_ASN_2bytes[ixp][year])))
                except:
                    Two_Bytes_ASNs = 0

                try:
                    Four_Bytes_ASNs = len(list(set(year_ASN_4bytes[ixp][year])))
                except:
                    Four_Bytes_ASNs = 0

                # for year in year_prefix[ixp].keys():
                create_output_MultiYear.write(
                    str(year) + '; ' + str(len(year_ASN[ixp][year])) + '; ' + str(Two_Bytes_ASNs) + '; ' + str(
                        Four_Bytes_ASNs) + '\n')

            # for prefix in year_prefix[ixp][year]:
            #    create_output_MultiYear =  open('../../' + output_folder+'MultiYear__list_visible_prefixes_at_IXP_'+ixp+'.txt', 'a')
            #    create_output_MultiYear.write(str(year)+ '; '+ str(prefix) + '\n')

log_file_instance.close()
now_datetime = str(datetime.now()).replace(' ', '_')
finish = open('finish_lastyear.txt', 'w')
finish.write('ended; ' + root_folder + output_folder[6:] + '; ' + now_datetime)
finish.close()
