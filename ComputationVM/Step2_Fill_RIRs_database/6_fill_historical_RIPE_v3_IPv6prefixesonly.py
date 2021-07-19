## ARDA Application released on: April 21, 2017
## Last review: February 19, 2018
## Filling historical RIPE ressources attributions
## Store IPv6 prefixes allocated by RIPE to ISPs or any organization in its region
## Alert: this script may be run:
## 1 - either frequently (at least once per trimester): In this case you can comment the lines 194 up to the last line (233) and use the cron of script 2_fill_historical_AFRINIC_v3_ASNsonly.py
## 2 - or run the scripts updating the RIR data one after the other: in which case you can keep the scripts as they are.

import MySQLdb, collections, sys, glob, math,  ast, os, time, random
from math import log

## Compute the x at the power of n.
def puissance ( x, n) :
	res = 1
	i = 1
	while i<=n:
		res = res * x
		i = i + 1
	return res

## Which folders in a given directory dir?
def get_immediate_subdirectories(dir):
    return [name for name in os.listdir(dir)
            if os.path.isdir(os.path.join(dir, name))]

sys.path.append('../Heart/2_libraries/')
import DB_configuration

## Connect to MySQL DB RIRs
db = MySQLdb.connect(host="localhost",user="",passwd="",  db ="RIRs")
cur = db.cursor()
print 'Connected'

#os.system("python 1_clean_RIRs_DBs.py")

### Sleep a random time before starting any operation
value = random.randint(0,10)
time.sleep(value * random.randint(0,3))

## RIR data extraction has been performed several times in the literature: see for instance the C++ code
## https://code.google.com/p/ip-countryside/source/browse/trunk/getDBs.sh?r=4.

website = "ftp://ftp.ripe.net/ripe/stats/"
folder_download = "ftp.ripe.net/ripe/stats/"

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
List_possible_folder_download = ['ftp.ripe.net/pub/stats/ripe/', 'ftp.ripe.net/pub/stats/']
for folder_download in List_possible_folder_download:
    folders += get_immediate_subdirectories(folder_download)
folders += ['ripe/']


for folder in folders:
    print folder
    list_of_files = []
    command2 = 'cd ' + folder_download + str(folder).strip() + ' ; gunzip *.gz'
    print 'command2 =', command2
    os.system(command2)


    filename = folder_download + str(folder).strip() + '/*'
    filename_md5 = folder_download + str(folder).strip() + '/*.md5'
    filename_asc = folder_download + str(folder).strip() + '/*.asc'
    filename_txt1 = folder_download + str(folder).strip() + '/*.txt'
    filename_txt2 = folder_download + str(folder).strip() + '/*.TXT'
    filename_without_txt = folder_download + str(folder).strip() + '/delegated-ripencc-*'
    filename_without_txt1 = folder_download + str(folder).strip() + '/legacy-ripencc-*'
    filename_txt3 = []
    filename_txt3.append(str(folder_download + str(folder).strip() + '/test').strip())
    filename_without_txt_direct = folder_download + '/delegated-ripencc-*'
    filename_without_txt1_direct = folder_download + '/legacy-ripencc-*'
    filename_md5_direct = folder_download + '/*.md5'
    filename_asc_direct = folder_download + '/*.asc'
    filename_txt1_direct = folder_download + '/*.txt'
    filename_txt2_direct  = folder_download + '/*.TXT'

    the_whole_list = glob.glob(filename) + glob.glob(filename_without_txt) + glob.glob(filename_without_txt1) + glob.glob(filename_without_txt_direct) + glob.glob(filename_without_txt1_direct)
    #print  the_whole_list
    
    the_whole_list_of_md5 = glob.glob(filename_md5) +  glob.glob(filename_md5_direct)
    #print  the_whole_list_of_md5
    
    the_whole_list_of_asc = glob.glob(filename_asc) +  glob.glob(filename_asc_direct)
    #print the_whole_list_of_asc
    
    the_whole_list_of_txt = glob.glob(filename_txt1) + glob.glob(filename_txt2) + filename_txt3 + glob.glob(filename_txt2_direct)  + glob.glob(filename_txt1_direct)
    
    
    ## Suppressing all .md5, .asc, or .txt
    for elmt in the_whole_list:
        if elmt not in the_whole_list_of_md5 and elmt not in the_whole_list_of_asc and elmt not in the_whole_list_of_txt :
            list_of_files.append(elmt)
    print '\n\n\n', 'Allocations ', folder, '\n'
    #print list_of_files


    ### Build a check list
    Check_list = []

    sql_command = """select * from IPv6_ressources_RIPE"""
    cur.execute(sql_command)
    db_dump2 = cur.fetchall()
    for elmt in db_dump2:
        value = elmt[1] +  '_'+ elmt[3] + '_' + elmt[4].upper() + '_' + elmt[5] + '_' + elmt[6]
        if value not in Check_list:
                Check_list.append(value)

    print 'len(Check_list) =', len(Check_list), 'len(db_dump2) =' , len(db_dump2)

    
    ## Files treatment and data storage    
    for filei in list_of_files :
        if os.path.exists(filei) and os.path.isfile(filei):
            
	    k_insertion = 0
            with open (filei, 'r') as fk:
		print 'IPv6 prefixes: We are in folder', folder , 'file', filei, 'which is the num', list_of_files.index(filei)
                for lines in fk:
                    line = lines.strip()
                    line = line.split('|')
                    
            
                    if line != '' and 'ipv6' in line and '*' not in line:
                        try:
				if ':' in line[3].strip():
					#afrinic|TN|ipv6|2001:970::|32|20021024|allocated
                           		NetBits = str(line[4].strip())
                            		CCf = line[1].strip()
                          	  	CCf = CCf.upper()

					value1 = str(line[3])  + '_' + str(NetBits) + '_' + str(CCf) + '_'+ str(line[6]) + '_' + str(line[5])
                            		print value1

                            		if value1 not in Check_list:
                                		# IPv6 prefixes details insertions
                                		sql_commandb = """ INSERT INTO IPv6_ressources_RIPE (NetIPaddress, NetBits, CC, Status, date) VALUES (%s,%s,%s,%s,%s);"""
                                		cur.execute(sql_commandb, ( line[3].strip(),  NetBits, CCf, line[6].strip(), line[5].strip()))
                                		print 'insertion of', line[3].strip(),'with a /', NetBits , 'needed in IPv6'
                   				db.commit()
						Check_list.append(value1)             
						k_insertion += 1
                            		else:
                                		print 'We do not insert ', line[3].strip(),'/', NetBits, ' anymore'

					print                                                                		
                        except:
                        	pass
		   
	    with open ('record_files_parsed_by_1_fill_historical_RIPE_v3_IPv6prefixesonly.txt', 'a') as fg:
                fg.write('%s; %s\n ' %(filei, k_insertion))

