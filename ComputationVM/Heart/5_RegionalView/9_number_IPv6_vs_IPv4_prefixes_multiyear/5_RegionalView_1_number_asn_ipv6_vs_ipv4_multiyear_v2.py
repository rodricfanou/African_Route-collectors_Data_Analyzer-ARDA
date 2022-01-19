##############################################################################
# __author__ = "Roderick Fanou"
# __status__ = "Production"
# __last_modifications__ =
##############################################################################

finish = open('finish_multiyear.txt', 'w')
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

continent = DB_configuration.continent
IXP_collector = {}
IXP_CC = {}

now_datetime = str(datetime.now()).replace(' ', '_')

## Create a logfile:
name_log_file = 'Log_' + str(now_datetime) + '_' + 'Regional_9_number_IPv6_vs_IPv4_prefixes_multiyear' + '.txt'
location_logfile = create_Logfiles_folder()

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

root_folder = '/home/arda/African_Route-collectors_Data_Analyzer-ARDA/ComputationVM/Heart/'

output_folder = '../../Computation_outputs_Regional_View/9_number_asn_ipv6_vs_ipv4_multiyear/'

## Update the folder with the selected repository
IXPView_output_folder = '/var/www/html/.../output/9_Number_IPv6_vs_IPv4_prefixes_multiyear/'

command = 'rm -rf ' + output_folder
os.system(command)

command = 'mkdir  ' + output_folder
os.system(command)

command = 'chmod 777 ' + output_folder
os.system(command)

print('Hola')

if os.listdir(IXPView_output_folder) != []:

    week_ASNs_v4 = {}

    week_ASNs_v6 = {}

    Unik_list_ASNs_v4 = {}

    Unik_list_ASNs_v6 = {}

    for ixp in list(IXP_collector.keys()):

        filename_v4 = 'MultiYear_' + ixp + '_List_ASNs_announcing_v4.txt'

        print('Treating the file = ', filename_v4)

        if os.path.exists(IXPView_output_folder + filename_v4):

            with open(IXPView_output_folder + filename_v4, 'r') as fd:

                for line in fd:

                    tab = line.split('; ')

                    if '#' not in tab and len(tab) > 1:

                        ASN = tab[-1]

                        del (tab[-1])

                        key = '; '.join(tab)

                        if key not in list(Unik_list_ASNs_v4.keys()):
                            Unik_list_ASNs_v4[key] = []

                        if ASN not in Unik_list_ASNs_v4[key]:
                            Unik_list_ASNs_v4[key].append(ASN)

        filename_v6 = 'MultiYear_' + ixp + '_List_ASNs_announcing_v6.txt'

        print('Treating the file = ', filename_v6)

        if os.path.exists(IXPView_output_folder + filename_v6):

            with open(IXPView_output_folder + filename_v6, 'r') as fd:

                for line in fd:

                    tab = line.split('; ')

                    if '#' not in tab and len(tab) > 1:

                        ASN = tab[-1]

                        del (tab[-1])

                        key = '; '.join(tab)

                        if key not in list(Unik_list_ASNs_v6.keys()):
                            Unik_list_ASNs_v6[key] = []

                        if ASN not in Unik_list_ASNs_v6[key]:
                            Unik_list_ASNs_v6[key].append(ASN)

### write Unik list ASNs per week in files

with open(output_folder + 'MultiYear__list_Origin_ASNs_advertising_v4_prefixes_at_all_IXPs.txt', 'a') as fg:
    fg.write('%s' % ('###Year; Visible ASNs advertising v4 prefixes\n'))

    for week in list(Unik_list_ASNs_v4.keys()):

        for ASN in Unik_list_ASNs_v4[week]:
            fg.write('%s; %s \n' % (week, ASN))

with open(output_folder + 'MultiYear__list_Origin_ASNs_advertising_v6_prefixes_at_all_IXPs.txt', 'a') as fg:
    fg.write('%s' % ('###Year; Visible ASNs advertising v6 prefixes\n'))

    for week in list(Unik_list_ASNs_v6.keys()):

        for ASN in Unik_list_ASNs_v6[week]:
            fg.write('%s; %s \n' % (week, ASN))

with open(output_folder + 'MultiYear__number_Origin_ASNs_advertising_v4_v6_prefixes_at_all_IXPs.txt', 'a') as fg:
    fg.write('%s' % ('###Year; Number ASNs advertising v4 prefixes;  Number ASNs advertising v6 prefixes\n'))

    for week in list(Unik_list_ASNs_v4.keys()):

        if week in list(Unik_list_ASNs_v6.keys()):

            fg.write('%s; %s; %s  \n' % (week, len(Unik_list_ASNs_v4[week]), len(Unik_list_ASNs_v6[week])))

        else:

            fg.write('%s; %s; %s  \n' % (week, len(Unik_list_ASNs_v4[week]), 0))

now_datetime = str(datetime.now()).replace(' ', '_')
finish = open('finish_multiyear.txt', 'w')
finish.write('ended' + '; ' + root_folder + output_folder[6:] + '; ' + now_datetime)
finish.close()
