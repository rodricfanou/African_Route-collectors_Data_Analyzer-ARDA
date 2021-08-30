## ARDA Application released on: April 21, 2017
## Last review: February 19, 2018
## Author: Roderick Fanou
## Store ASNs allocated by AFRINIC to ISPs or any organization in its region
## Alert: this script may be run:
## 1 - either frequently (at least once per trimester): In this case you can comment the lines 194 up to the last line (233) as well as the while loop on line 12 and use the cron
## 2 - or run the scripts updating the RIR data one after the other: in which case you can keep the scripts as they are.

## The user should configure the cron this script so that it runs on start up
## @reboot cd /path/to/African_Route-collectors_Data_Analyzer-ARDA/ComputationVM/Step2_Fill_RIRs_database && python 2_fill_historical_AFRINIC_v3_ASNsonly.py

import MySQLdb, collections, sys, glob, math, ast, os, time, random
from math import log


## Compute the x at the power of n.
def puissance(x, n):
    res = 1
    i = 1
    while i <= n:
        res = res * x
        i = i + 1
    return res


## Which folders in a given directory?
def get_immediate_subdirectories(dir):
    return [name for name in os.listdir(dir)
            if os.path.isdir(os.path.join(dir, name))]


sys.path.append('../Heart/2_libraries/')
import DB_configuration

## Connect to MySQL DB RIRs
db = MySQLdb.connect(host="localhost", user="", passwd="", db="RIRs")
cur = db.cursor()
print 'Connected'

## Launch a script located in the same folder which removes duplicates
os.system("python2.7 1_clean_RIRs_DBs.py")

### sleep a random time before starting any operation
value = random.randint(0, 10)
time.sleep(value * random.randint(0, 3))

## RIR data extraction has been performed several times in the literature: see for instance the C++ code
## https://code.google.com/p/ip-countryside/source/browse/trunk/getDBs.sh?r=4.

website = "ftp://ftp.afrinic.net/pub/stats/afrinic/"
folder_download = "ftp.afrinic.net/pub/stats/afrinic/"
print 'Download all the folders of allocation'

command = """ wget -N -H -r --level=2 -k -p """ + website
print '\n\n command =', command
os.system(command)

## decompress
if glob.glob(folder_download + "*/*.gz"):
    command = """gunzip -r """ + folder_download + "*/*.gz"
    os.system(command)

if glob.glob(folder_download + "*/*.bz2"):
    command = """bzip2 -dk """ + folder_download + "*/*.bz2"
    os.system(command)

    ## remove
    command = """ rm -f """ + folder_download + "*/*.bz2"
    os.system(command)

## Remove unuseful files.
if glob.glob(folder_download + "*/*.md5"):
    command = """ rm -f """ + folder_download + "*/*.md5"
    os.system(command)

if glob.glob(folder_download + "*/*.asc"):
    command = """ rm -f """ + folder_download + "*/*.asc"
    os.system(command)

if glob.glob(folder_download + "*/*.gz.bck"):
    command = """ rm -f """ + folder_download + "*/*.gz.bck"
    os.system(command)

if glob.glob(folder_download + "*/*.asc.gz"):
    command = """ rm -f """ + folder_download + "*/*.asc.gz"
    os.system(command)

if glob.glob(folder_download + "*/*.md5.gz"):
    command = """ rm -f """ + folder_download + "*/*.md5.gz"
    os.system(command)

## Which are the folders containing useful information after download:
folders = []
List_possible_folder_download = ['ftp.afrinic.net/pub/stats/afrinic/', 'ftp.afrinic.net/pub/stats/']
for folder_download in List_possible_folder_download:
    folders += get_immediate_subdirectories(folder_download)
folders += ['afrinic/']
print 'Folders : {}'.format(folders)
for folder in folders:
    print folder
    list_of_files = []
    filename = folder_download + str(folder).strip() + '/*'
    filename_md5 = folder_download + str(folder).strip() + '/*.md5'
    filename_asc = folder_download + str(folder).strip() + '/*.asc'
    filename_txt1 = folder_download + str(folder).strip() + '/*.txt'
    filename_txt2 = folder_download + str(folder).strip() + '/*.TXT'
    filename_without_txt = folder_download + str(folder).strip() + '/delegated-afrinic-*'
    filename_without_txt1 = folder_download + str(folder).strip() + '/legacy-afrinic-*'
    filename_txt3 = []
    filename_txt3.append(str(folder_download + str(folder).strip() + '/test').strip())
    filename_without_txt_direct = folder_download + '/delegated-afrinic-*'
    filename_without_txt1_direct = folder_download + '/legacy-afrinic-*'
    filename_md5_direct = folder_download + '/*.md5'
    filename_asc_direct = folder_download + '/*.asc'
    filename_txt1_direct = folder_download + '/*.txt'
    filename_txt2_direct = folder_download + '/*.TXT'

    the_whole_list = glob.glob(filename) + glob.glob(filename_without_txt) + glob.glob(
        filename_without_txt1) + glob.glob(filename_without_txt_direct) + glob.glob(filename_without_txt1_direct)
    # print  the_whole_list

    the_whole_list_of_md5 = glob.glob(filename_md5) + glob.glob(filename_md5_direct)
    # print  the_whole_list_of_md5

    the_whole_list_of_asc = glob.glob(filename_asc) + glob.glob(filename_asc_direct)
    # print the_whole_list_of_asc

    the_whole_list_of_txt = glob.glob(filename_txt1) + glob.glob(filename_txt2) + glob.glob(
        filename_txt2_direct) + glob.glob(filename_txt1_direct) + filename_txt3

    ## Suppressing all .md5, .asc, or .txt
    for elmt in the_whole_list:
        if elmt not in the_whole_list_of_md5 and elmt not in the_whole_list_of_asc and elmt not in the_whole_list_of_txt:
            list_of_files.append(elmt)
    print '\n\n\n', 'Allocations ', folder, '\n'
    # print list_of_files

    ### Build a check list
    sql_command = """select * from ASNs_AFRINIC ;"""
    cur.execute(sql_command)
    db_dump2 = cur.fetchall()

    Check_list = []
    for elmt in db_dump2:
        value = elmt[0] + '_' + elmt[1].upper() + '_' + elmt[2] + '_' + elmt[3]
        if value not in Check_list:
            Check_list.append(value)

    print 'len(Check_list) =', len(Check_list), 'len(db_dump2) =', len(db_dump2)

    ## Files treatment and data storage
    for filei in list_of_files:
        if os.path.exists(filei) and os.path.isfile(filei):
            k_insertion = 0
            with open(filei, 'r') as fk:
                print 'ASNs parser: are in folder', folder, 'file', filei, 'which is the num', list_of_files.index(
                    filei)
                for lines in fk:
                    line = lines.strip()
                    line = line.split('|')

                    ## Inserting ASNs
                    if line != '' and 'asn' in line and '*' not in line and 'summary' not in line:
                        try:
                            # afrinic|ZA|asn|1228|1|19910301|allocated
                            print '\n', line
                            print line[3].strip()
                            ASNf = line[3].strip()
                            CCf = line[1].strip()
                            CCf = CCf.upper()
                            Datef = line[5].strip()
                            Statusf = line[6].strip()

                            value1 = ASNf + '_' + CCf + '_' + Datef + '_' + Statusf
                            print value1

                            if value1 not in Check_list:
                                sql_commandb = """ INSERT INTO ASNs_AFRINIC (ASN, CC, date, Status) VALUES (%s,%s,%s,%s);"""
                                cur.execute(sql_commandb, (ASNf, CCf, Datef, Statusf))
                                print 'insertion of', ASNf, 'with as CC ', CCf
                                db.commit()
                                Check_list.append(value1)
                                k_insertion += 1
                            else:
                                print 'We do not insert ', ASNf, ' anymore'
                        except:
                            pass

            with open('record_files_parsed_by_1_fill_historical_AFRINIC_v3_ASNsonly.txt', 'a') as fg:
                fg.write('%s; %s\n ' % (filei, k_insertion))

## Run next script
os.system("python2.7 2_fill_historical_AFRINIC_v3_IPv4prefixesonly.py")

## Run next script
os.system("python2.7 2_fill_historical_AFRINIC_v3_IPv6prefixesonly.py")

## Run next script
os.system("python2.7 3_fill_historical_APNIC_v3_ASNsonly.py")

## Run next script
os.system("python2.7 3_fill_historical_APNIC_v3_IPv4prefixesonly.py")

## Run next script
os.system("python2.7 3_fill_historical_APNIC_v3_IPv6prefixesonly.py")

## Run next script
os.system("python2.7 4_fill_historical_ARIN_v3_ASNsonly.py")

## Run next script
os.system("python2.7 4_fill_historical_ARIN_v3_IPv4prefixesonly.py")

## Run next script
os.system("python2.7 4_fill_historical_ARIN_v3_IPv6prefixesonly.py")

## Run next script
os.system("python2.7 5_fill_historical_LACNIC_v3_ASNsonly.py")

## Run next script
os.system("python2.7 5_fill_historical_LACNIC_v3_IPv4prefixesonly.py")

## Run next script
os.system("python2.7 5_fill_historical_LACNIC_v3_IPv6prefixesonly.py")

## Run next script
os.system("python2.7 6_fill_historical_RIPE_v3_ASNsonly.py")

## Run next script
os.system("python2.7 6_fill_historical_RIPE_v3_IPv4prefixesonly.py")

## Run next script
os.system("python2.7 6_fill_historical_RIPE_v3_IPv6prefixesonly.py")

time.sleep(1000)
