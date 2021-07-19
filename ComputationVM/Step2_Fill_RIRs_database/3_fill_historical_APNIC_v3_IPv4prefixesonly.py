## ARDA Application released on: April 21, 2017
## Last review: February 19, 2018
## Store IPv4 prefixes allocated by RIPE to ISPs or any organization in its region
## Alert: this script may be run:
## 1 - either frequently (at least once per trimester): In this case you can comment the lines 194 up to the last line (233) and use the cron of script 2_fill_historical_AFRINIC_v3_ASNsonly.py; The adopted frequency depends on the server's capabilities
## 2 - or run the scripts updating the RIR data one after the other: in which case you can keep the scripts as they are.


import MySQLdb, collections, sys, glob, math,  ast, os, time, random, glob
from math import log
import os.path

## Compute the x at the power of n.
def puissance ( x, n) :
	res = 1
	i = 1
	while i<=n:
		res = res * x
		i = i + 1
	return res

## Which folders in the directory?
def get_immediate_subdirectories(dir):
    return [name for name in os.listdir(dir)
            if os.path.isdir(os.path.join(dir, name))]

#os.system("python2.7 1_clean_RIRs_DBs.py")

## Consulting the main DB
sys.path.append('../Heart/2_libraries/')
import DB_configuration

db = MySQLdb.connect(host="localhost",user="",passwd="",  db ="RIRs")
cur = db.cursor()
print 'Connected'


### Sleep a random time before starting any operation
value = random.randint(0,10)
time.sleep(value * random.randint(0,3))


## RIR data extraction has been performed several times in the literature: see for instance the C++ code
## https://code.google.com/p/ip-countryside/source/browse/trunk/getDBs.sh?r=4.
website = "ftp://ftp.apnic.net/pub/stats/apnic/"
folder_download = "ftp.apnic.net/pub/stats/apnic/"

print 'Download all the folders of allocation'
    
command = """ wget -H -r --level=2 -k -p """ + website
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
List_possible_folder_download = ['ftp.apnic.net/pub/stats/apnic/', 'ftp.apnic.net/pub/stats/']
for folder_download in List_possible_folder_download:
    folders += get_immediate_subdirectories(folder_download)
folders += ['apnic/']


for folder in folders:
    print folder
    list_of_files = []
    filename = folder_download + str(folder).strip() + '/*'
    filename_md5 = folder_download + str(folder).strip() + '/*.md5'
    filename_asc = folder_download + str(folder).strip() + '/*.asc'
    filename_txt1 = folder_download + str(folder).strip() + '/*.txt'
    filename_txt2 = folder_download + str(folder).strip() + '/*.TXT'
    filename_without_txt = folder_download + str(folder).strip() + '/delegated-apnic-*'
    filename_without_txt1 = folder_download + str(folder).strip() + '/legacy-apnic-*'
    filename_txt3 = []
    filename_txt3.append(str(folder_download + str(folder).strip() + '/test').strip())
    filename_without_txt_direct = folder_download + '/delegated-apnic-*'
    filename_without_txt1_direct = folder_download + '/legacy-apnic-*'
    filename_md5_direct = folder_download + '/*.md5'
    filename_asc_direct = folder_download + '/*.asc'
    filename_txt1_direct = folder_download + '/*.txt'
    filename_txt2_direct  = folder_download + '/*.TXT'

    the_whole_list = glob.glob(filename)+ glob.glob(filename_without_txt) + glob.glob(filename_without_txt1) + glob.glob(filename_without_txt_direct) + glob.glob(filename_without_txt1_direct)
    #print  the_whole_list
    
    the_whole_list_of_md5 = glob.glob(filename_md5) + glob.glob(filename_md5_direct)
    #print  the_whole_list_of_md5
    
    the_whole_list_of_asc = glob.glob(filename_asc) + glob.glob(filename_asc_direct)
    #print the_whole_list_of_asc
    
    the_whole_list_of_txt = glob.glob(filename_txt1) + glob.glob(filename_txt2) + glob.glob(filename_txt2) + glob.glob(filename_txt2_direct) + filename_txt3 
    
    for elmt in the_whole_list:
        if elmt not in the_whole_list_of_md5 and elmt not in the_whole_list_of_asc and elmt not in the_whole_list_of_txt :
            list_of_files.append(elmt)
    print '\n\n\n', 'Allocations ', folder, '\n'
    print list_of_files
    

    ### Build a check list
    Check_list = []
    sql_command = """select * from IPv4_ressources_APNIC"""
    cur.execute(sql_command)
    db_dump2 = cur.fetchall()
    for elmt in db_dump2:
        value = elmt[1] + '_'+ elmt[2] + '_'+ elmt[3] + '_' + elmt[4].upper() + '_' + elmt[5] + '_' + elmt[6]
        if value not in Check_list:
                Check_list.append(value)
    print 'len(Check_list) = ',  len(Check_list), 'len(db_dump2) = ', len(db_dump2)


    for filei in list_of_files :
        if os.path.exists(filei) and os.path.isfile(filei):
            #print '\nASNs Checks: We are in folder', folder , 'file', filei, 'which is the num', list_of_files.index(filei)

	    k_insertion = 0
            with open (filei, 'r') as fk:
		
            	for lines in fk:
                    line = lines.strip()
                    line = line.split('|')
		    print line, '\n'
                    try:
                    	if line != '' and 'ipv4' in line and '*' not in line:
                  	   if '.' in line[3].strip():
                    		#print 'IPv4 prefix: We are in folder', folder , 'file', filei, 'which is the num', list_of_files.index(filei)
                   		NetBits = int(32 - math.log(int(line[4].strip()), 2))
                    		CCf = line[1].strip()
		    		CCf = CCf.upper()
                    		print 'CCf = ', CCf		

		    		value1 = str(line[3]) + '_' + str(line[4]) + '_' + str(NetBits) + '_' + str(CCf) + '_'+ str(line[6]) + '_' + str(line[5])
                    		print value1

                    		if value1 not in Check_list:
                        		#IPv4 prefixes details insertions
                        		sql_commandb = """ INSERT INTO IPv4_ressources_APNIC (NetIPaddress, Numb_IPadd, NetBits, CC, Status, date) VALUES (%s,%s,%s,%s,%s,%s);"""
                        		cur.execute(sql_commandb, ( line[3].strip(), line[4].strip(), NetBits, CCf, line[6].strip(), line[5].strip()))
                        		print 'insertion of', line[3].strip(),'with a /', NetBits , 'needed in IPv4'
					db.commit()
					k_insertion += 1 
					Check_list.append(value1)

                    	else:
                        	print 'We do not insert ', line[3].strip(),'/', NetBits, ' anymore'

	            except:
		        pass

        with open ('record_files_parsed_by_1_fill_historical_APNIC_v3_IPv4prefixesonly.txt', 'a') as fg:
            fg.write('%s; %s\n ' %(filei, k_insertion))




