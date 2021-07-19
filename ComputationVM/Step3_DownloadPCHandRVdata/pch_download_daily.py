#!/usr/bin/python
import sys, os, csv, glob
import time
import MySQLdb
import DB_configuration
import datetime
from datetime import date

outfile = open('Debug_time.txt', 'a')
outfile.write('The script has started at '+str(time.strftime("%d/%m/%Y %H:%M:%S"))+'.\n')

#Correctly downloaded = [2003, 2005, 2006, 2007, 2008, 2009, 2013]
#needed = 2010, 2011, 2012, 2014, 2015
yearList = [str(date.today().year)]
#monthList = ["01"]
monthList = [str(datetime.datetime.now().strftime("%m"))]
current_day = datetime.datetime.now().strftime("%d")
#current_day = '14'
Dictionary_locations = []
Dictionary_files = {}
Full_Dictionary = {}
path = "/home/roderick/PCH_download"

print "Start"

#Select only the African RouteCollector
db = MySQLdb.connect(host="localhost",user="",passwd="", db="MergedData")
cur = db.cursor()
sql_command = """select RouteCollector from AllRouteCollectors where Continent = 'AF';"""
cur.execute(sql_command)
List = cur.fetchall() 


RouteCollector_african  = []
for rc in List :
	RouteCollector_african.append(str(rc[0]).strip())

print RouteCollector_african

for elem in yearList:
    for month in monthList:
        Full_Dictionary[str(elem)] = {}
        os.chdir(path)
        command = "rm index.html"
        os.system(command)
        command = "wget https://www.pch.net/resources/Routing_Data/IPv4_daily_snapshots/" +str(elem)+"/"+str(month)+"/" 
        print "\n Executing command =", command
        os.system(command) 

        find_file = "index.html"
        print "\n find_file =", find_file

        #<a href="/resources/data.php?dir=/2003//route-views.oregon-ix.net"><strong>route-views.oregon-ix.net</strong></a>
        with open (find_file, "r") as index_file:
            print "I access to file"
            for line in index_file:
                line = line.strip()
                try:
                    first = "<strong>"
                    last = "</strong>"
                    start = line.index(first) + len(first)
                    end = line.index(last)
                    ## Extracting the url of a "location folder"
                    url_to_folder = line[start:end]
                    ##Extracting the list of locations.
                    folder_only = url_to_folder
                    if 1:
                        Dictionary_locations.append(folder_only)
                except:
                    pass

        command = "mkdir "+str(elem)
        os.system(command)
        command = "mkdir "+str(elem)+'/'+str(month)
        os.system(command) 
        print "Creating folder: ", str(month)
        os.chdir(path+"/"+str(elem)+"/"+str(month))


        ##Download the data files of the locations
        for folder_only in Dictionary_locations:
            print folder_only
            if folder_only in RouteCollector_african:
                command = "rm index.html"
                os.system(command)
                command = "mkdir " +str(folder_only)
                os.system(command)
                print 'AQUI',folder_only
                command = "wget https://www.pch.net/resources/Routing_Data/IPv4_daily_snapshots/"+str(elem)+"/"+str(month)+"/"+str(folder_only)+"/"
                print "\n I launch the command: ", command
                os.system(command) 
                print 'AQUI NO',folder_only
                os.chdir(path+"/"+str(elem)+"/"+str(month))
                find_packets = "index.html"
                Full_Dictionary[str(elem)][folder_only] = []

                with open (find_packets, 'r') as index_packets:
                    for line2 in index_packets:
                        line2 = line2.strip()
                        try:
                            first2 = '<td data-sort-value="'
                            last2 = '"><i class="fa fa-archive fa-fw">'
                            start2 = line2.index(first2) + len(first2)
                            end2 = line2.index(last2)
                            url_to_file = line2[start2:end2] 
                            ## Extracting the name of the data file
                            file_only = url_to_file
                            url_to_file = folder_only+"/"+file_only
                            os.chdir(path+"/"+str(elem)+"/"+str(month)+"/"+str(folder_only))
                            dia_de_descarga = '.'+current_day+'.gz'
                            if (dia_de_descarga in url_to_file):
                                command = " wget https://www.pch.net/resources/Routing_Data/IPv4_daily_snapshots/" + str(elem) +"/"+str(month)+"/"+url_to_file
                                os.system(command) 
                                print 'url command= ', command
                                print 'url_to_file', url_to_file
                                print 'file_only', file_only
                                print 'folder_only', folder_only
                                time.sleep(10)
                        except:
                            pass

                        os.chdir(path+"/"+str(elem)+"/"+str(month))  
os.chdir(path)                        
command = 'python daily_victor_roderick_parsing_vtest.py'
os.system(command)
outfile = open('Debug_time.txt', 'a')
outfile.write('The script has ended at '+str(time.strftime("%d/%m/%Y %H:%M:%S"))+'.\n')
