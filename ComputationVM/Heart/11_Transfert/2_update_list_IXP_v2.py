## ARDA Application released on: April 21, 2017
## Last review: February 19, 2018
## Author: Roderick Fanou
## Alert: Cron edition
#Update every 30mn the computations outputs in the visualization folder ARP_visual
#by moving the last results from the computation VM to the visualisation VM
#*/30  * * * * cd /African_Route-collectors_Data_Analyzer-ARDA/ComputationVM/Heart/11_Transfert && python 2_update_list_IXP_v2.py

import os, sys, MySQLdb
sys.path.append('../2_libraries/')
import DB_configuration
from incf.countryutils import transformations

Current_db = 'MergedData'
db = MySQLdb.connect(host = DB_configuration.host, user = DB_configuration.user, passwd = DB_configuration.passwd,  db = Current_db)
cur = db.cursor()
continent = 'AF'

query = "select IXP, IXPName , CC from AllRouteCollectors where Continent = '"+continent+"';"
cur.execute(query)
data = cur.fetchall()
#print data

##path to the location of the outputs of the IXP view computations in the /var directory
create_folder_command = 'mkdir /var/www/html/.../outputs'
os.system(create_folder_command)

Python_list_IXPs = []
##path to the location of the final list of IXPs
IXP_list_file = open('/var/www/html/.../outputs/list_IXPs.txt', 'w')
for line in data:
    if line[0] not in Python_list_IXPs:
	country_name  = transformations.cc_to_cn(str(line[2]).strip())

	print line[2], country_name
        IXP_list_file.write(line[0]+';'+line[2]+ ';' + country_name + '\n')
        Python_list_IXPs.append(line[0])
