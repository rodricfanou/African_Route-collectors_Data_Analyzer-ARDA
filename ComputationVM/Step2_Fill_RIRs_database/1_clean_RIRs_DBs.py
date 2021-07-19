## ARDA Application released on: April 21, 2017
## Last review: February 19, 2018
# This script can be used to suppress the content of/dupplicates in the tables of the database RIR if needed.

import MySQLdb, collections, sys, glob, math,  ast, os, time, random
from math import log
from pprint import pprint

sys.path.append('../Heart/2_libraries/')
import DB_configuration


def puissance ( x, n) :
        res = 1
        i = 1
        while i<=n:
                res = res * x
                i = i + 1
        return res


db = MySQLdb.connect(host="localhost",user="",passwd="")
cur = db.cursor()
print 'Connected'


## Which folders ?
def get_immediate_subdirectories(dir):
    return [name for name in os.listdir(dir)
            if os.path.isdir(os.path.join(dir, name))]


### sleep a random time before starting any operation
value = random.randint(0,10)
time.sleep(value * random.randint(0,3))

print 'Download all the folders of allocation'

RIRs = ['ARIN', 'APNIC', 'LACNIC', 'RIPE', 'AFRINIC']

##suppress weird addresses
try:
#if 1:
	for RIR in RIRs:

		print 'We are on RIRv4: ', RIR 
		query = """delete from IPv4_ressources_""" + RIR + """ where NetIPaddress = ''"""
		cur.execute(query)
		db.commit()	
		print 'Done'	

		print 'We are on RIRv6: ', RIR
                query = """delete from IPv6_ressources_""" + RIR + """ where NetIPaddress = ''"""
                cur.execute(query)
                db.commit()
		print 'Done'

		## Update NumP_IPaddres  = null
		query = """update IPv6_ressources_""" + RIR + """ set Numb_IPadd = NULL """
		cur.execute(query)
		time.sleep(4)
		db.commit()
		print 'Done'
except: 
	pass


## suppress duplicates
print
print 'suppressing dupplicates'


for RIR in RIRs:
	try:
		print 'RIR6 ', RIR		
		#query = """delete n1 from IPv6_ressources_""" + RIR + """ n1, IPv6_ressources_""" + RIR + """ n2 where n1.Al_id > n2.Al_id and n1.NetIPaddress = n2.NetIPaddress and n1.NetBits = n2.NetBits and n1.CC = n2.CC and n1.Status = n2.Status and n1.date = n2.date """ 
		query = """ select * from IPv6_ressources_""" + RIR  #+ """ limit 1000 """
		print query 
		cur.execute(query)
		data = cur.fetchall()
		Check_dict = {}
		for elmt in data: 
			print elmt
			key = elmt[1] +'_' + elmt[3] + '_' + elmt[4] + '_' + elmt[5] + '_' + elmt[6]
			
			if key not in Check_dict.keys():
				Check_dict[key] = []
			Check_dict[key].append(elmt[0])
		
		pprint(Check_dict)

		for key in Check_dict.keys():
			if len(Check_dict[key]) > 1:
				print 'remove the lines ', Check_dict[key][1:], ' due to ',  Check_dict[key]
				for id_del in Check_dict[key][1:]:
					query = """delete from IPv6_ressources_""" + RIR + """ where Al_id = """+ str(id_del)
					print query
                			cur.execute(query)
                			db.commit()
                			print 'deleted'		
		print 'Done'
	except:
		pass
