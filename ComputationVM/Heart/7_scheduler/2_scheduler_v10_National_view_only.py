## ARDA Application released on: April 21, 2017
## Last review: February 19, 2018
## Author: Roderick Fanou
## Description:
## This script is run daily. => put it in the cron for everyday at 1 am, 9 am and 5pm
## Follow the 'Alert' signs within the scripts and make the suitable changes

import time, copy
from datetime import datetime
import os, sys, subprocess, glob, time, MySQLdb, random

## import all files in the library you need
sys.path.append('../2_libraries/')
import DB_configuration
from functions import *

### Check if the table to store tomorrow's data is available.

def Check_tables_for_insertions(database):
    
    import datetime
    Current_db = database
    
    ## connect to the DB
    db = MySQLdb.connect(host = "localhost", user = "", passwd = "",  db = Current_db)
    cur = db.cursor()
    print('Connected')
    
    #Create a datetime object with today's value
    today = datetime.datetime.today()
    
    #print today's date in YYYY-MM-DD format
    value1 = datetime.datetime.strftime(today,'%d-%m-%Y')
    tab1111 = value1.split('-')
    table1 = 'Data__' +str(int(tab1111[2]))+ '_' + str(int(tab1111[1]))
    
    
    #add one day to today's date
    tomorrow = today + datetime.timedelta(1)
    
    #print tomorrow's date in YYYY-MM-DD format
    value2 = datetime.datetime.strftime(tomorrow,'%d-%m-%Y')
    tab1111 = value2.split('-')
    table2 = 'Data__' +str(int(tab1111[2]))+ '_' + str(int(tab1111[1]))
    
    
    Original_table  = 'Data__2003_1'
    
    print(table1, table2)
    
    ## Check if today table exists
    
    stmt = "SHOW TABLES LIKE '" + table1 + "'"
    print(stmt)
    cur.execute(stmt)
    result = cur.fetchone()
    print(result)
    if result:
        # there is a table for today
        print('the table ', table1, ' exists')

    else:
        # there is no table for today; create it
        print('the table ', table1, ' does not exist')
        
        stmt = """CREATE TABLE """ + table1 + """ LIKE """ + Original_table ;
        cur.execute(stmt)



    stmt = "SHOW TABLES LIKE '" + table2 + "'"
    print(stmt)
    cur.execute(stmt)
    result = cur.fetchone()
    print(result)
    if result:
        # there is a table for today
        print('the table ', table2, ' exists')

    else:
        # there is no table for today; create it
        print('the table ', table2, ' does not exist')
        stmt = """CREATE TABLE """ + table2 + """ LIKE """ + Original_table ;
        cur.execute(stmt)




## Check if the table in which we have to store data for the next month is there, otherwise create it.
Check_tables_for_insertions('MergedData')


### Months and corresponding numbers.
Months = {'Jan':'01', 'Feb':'02', 'Mar':'03', 'Apr':'04', 'May':'05', 'June':'06', 'Jun':'06', 'Jul':'07', 'July':'07', 'Aug':'08', 'Sept':'09', 'Sep':'09', 'Oct':'10', 'Nov':'11', 'Dec':'12'}

number_of_script_not_to_exceed = 2

## As task, it checks which are the scripts that are currently running


## Connexion to the database MergedData_backup
## Other initialisations
continent = DB_configuration.continent
IXP_collector = {}
IXP_CC = {}
Current_db = 'MergedData_backup'
## connect to the DB
db = MySQLdb.connect(host = "localhost", user = "", passwd = "",  db = Current_db)
cur = db.cursor()
print('Connected')







### Build a file that summarizes all the scripts to run and

Final_list_of_scripts = {}

## get all the sub-folders in the folders IXP_View, National_View,

directory = ['/African_Route-collectors_Data_Analyzer-ARDA/ComputationVM/Heart/4_NationalView/']

for direc in directory:
    
    if '3_IXPView' in direc:
        key_word = '3_IXPView'
    
    elif '4_NationalView' in direc:
        key_word = '4_NationalView'
    
    elif '5_RegionalView' in direc:
        key_word = '5_RegionalView'

    print()
    print(direc)

    os.walk(direc)

    sub_directories = [x[0] for x in os.walk(direc)]
    
    print(sub_directories)
    
    for sub_directory in sub_directories:
        print()
        print(sub_directory)
        os.chdir(sub_directory)
        
        List_all_files = glob.glob("*.py")
        number_files_marked = 0
        
        for file in List_all_files:
            if key_word in file:
                number_files_marked += 1
                marked_file = file
            print(file)
        
        #print number_files_marked
        if number_files_marked == 0:
            if len(List_all_files) > 1:
                indice = 0
                for file in List_all_files:
                    if '_v' in file:
                        tab = file.split('_')
                        #print tab
                        tab1 = tab[-1].split('.')
                        if tab1[0][0] == 'v':
                            #print 'tab1 = ', tab1
                            try:
                                #print int(tab1[0][1:])
                                if indice < int(tab1[0][1:]):
                                    indice = int(tab1[0][1:])
                            except:
                                pass
            
                #print 'indice = ', indice
                
                for file in List_all_files:
                    if 'v' + str(indice) + '.py' in file:
                        
                        if os.path.isfile(key_word + '_'+ file):
                            print('no need to create ' + key_word + '_'+ file + ' as it exists')
                        else:
                            command1 = "cp " + file + '  '+  key_word + '_'+ file
                            print(command1)
                        
                        Final_list_of_scripts[key_word + '_'+ file] = {}
                        Final_list_of_scripts[key_word + '_'+ file]['location'] = sub_directory
                        os.system(command1)

            else:
                for file in List_all_files:
            
                    if os.path.isfile(key_word + '_'+ file):
                        print('no need to create ' + key_word + '_'+ file + ' as it exists')
                    else:
                        command1 = "cp " + file + '  ' + key_word + '_' + file
                        os.system(command1)
                        print(command1)
            
                    Final_list_of_scripts[key_word + '_'+ file] = {}
                    Final_list_of_scripts[key_word + '_'+ file]['location'] = sub_directory


        else:
            Final_list_of_scripts[marked_file] = {}
            Final_list_of_scripts[marked_file]['location'] = sub_directory
            list_txt_files = glob.glob("*.txt")
            Final_list_of_scripts[marked_file]['txt_file'] = list_txt_files
            
            for elmt in list_txt_files:
                if elmt == 'list_cmd_dates.txt':
                    command = """rm -rf """ + elmt
                    os.system(command)
            
                else:
                    with open (elmt, 'r') as fh1:
                        print(elmt)
                        for line in fh1:
                            print(line)
                            tab = line.split(';')
                            if 'started' in line:
                                ### Final_list_of_scripts[marked_file]['launch_date'] = tab[-1]
                                ### add the date of the creation of the file.
                                import os.path, time
                                #print "last modified: %s" % time.ctime(os.path.getmtime(elmt))
                                print("created: %s" % time.ctime(os.path.getctime(elmt)))
                                date_creation = time.ctime(os.path.getctime(elmt))
                                #print date_creation
                                tab = date_creation.split(' ')
                                
                                if len(tab[-3] + '/' + Months[tab[1]] + '/' + tab[-1]) == 10:
                                    launch_date = tab[-3] + '/' + Months[tab[1]] + '/' + tab[-1]
                                    print(launch_date)
                                    Final_list_of_scripts[marked_file]['launch_exec_date'] = str(launch_date).strip()
                                    
                                    cur.execute ("""UPDATE Infos_on_all_scripts_to_run SET Last_end_execution_date=%s WHERE Script_to_execute=%s""",('Unknown',marked_file))
                                    
                                    db.commit()
                        
                        
                            elif 'ended' in line:
                                ### split the date.
                                to_add = tab[-1]
                                tab1 = to_add.split('_')
                                print('tab1 = ', tab1)
                                to_add1 = str(tab1[0]).strip()
                                tabb = to_add1.split('-')
                                try:
                                    day = int(tabb[-1])
                                    
                                    if int(tabb[-1]) < 10:
                                        value = '0'+tabb[-1]
                                    else:
                                        value = tabb[-1]
                                    
                                    end_exec_date = tabb[-1] + '/' + tabb[-2] + '/' + tabb[-3]
                                    Final_list_of_scripts[marked_file]['end_exec_date'] = end_exec_date
                                    print(Final_list_of_scripts[marked_file]['end_exec_date'])
                                
                                except:
                                    print('In the except')
                                    date_creation = time.ctime(os.path.getctime(elmt))
                                    print(date_creation)
                                    tab = date_creation.split(' ')
                                    print('tab before = ', tab)
                                    if '' in tab:
                                        for item in range(tab.count('')):
                                            tab.remove('')
                                    print('tab after = ', tab)
                                    
                                    if int(tab[-3]) < 10:
                                        value = '0'+tab[-3]
                                    else:
                                        value = tab[-3]
                                    
                                    end_exec_date = value + '/' + Months[tab[1]] + '/' + tab[-1]
                                    print('end_exec_date to update = ', end_exec_date)
                                    #time.sleep(50)
                                    Final_list_of_scripts[marked_file]['end_exec_date'] = str(end_exec_date).strip()
                                
                                
                                ##### Update all end dates.
                                if len(Final_list_of_scripts[marked_file]['end_exec_date']) == 10:
                                    
                                    cur.execute ("""UPDATE Infos_on_all_scripts_to_run SET Last_end_execution_date=%s WHERE Script_to_execute=%s""",(Final_list_of_scripts[marked_file]['end_exec_date'],marked_file))
                                    
                                    db.commit()


#print 'Final_list_of_scripts = ', Final_list_of_scripts

#### Create the table 'Infos_on_all_scripts_to_run' if it does not exist
query = "SHOW TABLES LIKE 'Infos_on_all_scripts_to_run' "
cur.execute (query)
data = cur.fetchall()
List_all_tables = []
if len(data)>0:
    for elmt in data:
        List_all_tables.append(elmt[0])


import os.path
os.chdir('/African_Route-collectors_Data_Analyzer-ARDA/ComputationVM/Heart/7_scheduler')

cwd = os.getcwd()
print(cwd)


if len(List_all_tables) == 0:

    ### the file does not exists; create it.
    
    ### if file does not exist,
    ### add them into the file if they are not; with their last date of runn and the worse and best period, and keep 5 scripts executed, in priority queue
    
    query = """CREATE TABLE Infos_on_all_scripts_to_run (
        id INT(6) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
        Item VARCHAR(400) NULL,
        Directory VARCHAR(800) NOT NULL,
        Script_to_execute VARCHAR(400) NOT NULL,
        Last_beg_execution_date VARCHAR(50),
        Last_end_execution_date VARCHAR(50),
        Best_execution_period INT(5),
        Worse_execution_period INT(5),
        Current_Status  VARCHAR(50),
        Current_Status_machine  VARCHAR(50),
        best_memory_usage FLOAT(6),
        worse_memory_usage FLOAT(6),
        best_cpu_usage FLOAT(6),
        worse_cpu_usage FLOAT(6),
        pid INT(6),
        Priority_queue VARCHAR(50)
        ) """
    
    cur.execute(query)
    print()
    print()

    for script in Final_list_of_scripts:
        directory_add = Final_list_of_scripts[script]['location']
        
        if 'launch_exec_date' in list(Final_list_of_scripts[script].keys()):
            launch_exec_date_add = Final_list_of_scripts[script]['launch_exec_date']
        else:
            launch_exec_date_add = 'Unknown'
        
        if 'end_exec_date' in list(Final_list_of_scripts[script].keys()):
            end_exec_date_add = Final_list_of_scripts[script]['end_exec_date']
        else:
            end_exec_date_add = 'Unknown'
        
        Current_Status_machine_add = ''
        best_memory_usage_add = -1
        worse_memory_usage_add = -1
        best_cpu_usage_add = -1
        worse_cpu_usage_add = -1
    
        Best_execution_period_add = -1
        Worse_execution_period_add = -1
        Priority_queue_add = 'No'
        
        
        print('',  directory_add, script, launch_exec_date_add, end_exec_date_add, Best_execution_period_add, Worse_execution_period_add, Priority_queue_add)
        cur.execute ("""INSERT INTO Infos_on_all_scripts_to_run (Item, Directory, Script_to_execute ,Last_beg_execution_date, Last_end_execution_date, Best_execution_period, Worse_execution_period,  Current_Status_machine, best_memory_usage, worse_memory_usage, best_cpu_usage, worse_cpu_usage,    Priority_queue) VALUES (%s, %s,  %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) """, ('',  directory_add, script, launch_exec_date_add, end_exec_date_add, Best_execution_period_add, Worse_execution_period_add,  Current_Status_machine_add,   best_memory_usage_add, worse_memory_usage_add, best_cpu_usage_add,  worse_cpu_usage_add,   Priority_queue_add))
        
        db.commit()


else:


    print('length different from 0; let us insert new lines. ')
    
    inserted = 0
    for script in Final_list_of_scripts:
        directory_add = Final_list_of_scripts[script]['location']
        
        if 'launch_exec_date' in list(Final_list_of_scripts[script].keys()):
            launch_exec_date_add = Final_list_of_scripts[script]['launch_exec_date']
        else:
            launch_exec_date_add = 'Unknown'
        
        if 'end_exec_date' in list(Final_list_of_scripts[script].keys()):
            end_exec_date_add = Final_list_of_scripts[script]['end_exec_date']
        else:
            end_exec_date_add = 'Unknown'
        
        Current_Status_machine_add = ''
        best_memory_usage_add = -1
        worse_memory_usage_add = -1
        best_cpu_usage_add = -1
        worse_cpu_usage_add = -1
        

    
        Best_execution_period_add = -1
        Worse_execution_period_add = -1
        Priority_queue_add = 'No'


        query =  """ select * from Infos_on_all_scripts_to_run where Directory = %s and Script_to_execute = %s """

        cur.execute(query, ( directory_add, script))
        
        output = cur.fetchall()
        
        if len(output) == 0:

            print('',  directory_add, script, launch_exec_date_add, end_exec_date_add, Best_execution_period_add, Worse_execution_period_add, Priority_queue_add)
            cur.execute ("""INSERT INTO Infos_on_all_scripts_to_run (Item, Directory, Script_to_execute ,Last_beg_execution_date, Last_end_execution_date, Best_execution_period, Worse_execution_period,  Current_Status_machine, best_memory_usage, worse_memory_usage, best_cpu_usage, worse_cpu_usage,    Priority_queue) VALUES (%s,  %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) """, ('',  directory_add, script, launch_exec_date_add, end_exec_date_add, Best_execution_period_add, Worse_execution_period_add,  Current_Status_machine_add,   best_memory_usage_add, worse_memory_usage_add, best_cpu_usage_add,  worse_cpu_usage_add,   Priority_queue_add))
        
            db.commit()
            inserted += 1
            
        else:

            print('insert nothing')

    print('Total number of New insertions = ', inserted)








Priority_queue_list = {}

## Let us consider only scripts that are in the table:
Dict_all_scripts_to_run = {}

query = """select * from Infos_on_all_scripts_to_run"""
cur.execute(query)
for row in cur.fetchall():
    #print 'row = ', row
    ## treat info and update whenever you need to
    id = row[0]
    directory_add = row[2]
    script = row[3]
    Last_beg_execution_date_add = row[4]
    Last_end_execution_date_add = row[5]
    Best_execution_period_add = row[6]
    Worse_execution_period_add = row[7]
    Status_running_add = row[8]
    Current_Status_machine_add = row[9]
    best_memory_usage_add = row[10]
    worse_memory_usage_add = row[11]
    best_cpu_usage_add  = row[12]
    worse_cpu_usage_add = row[13]
    pid_add = row[14]
    Priority_queue_add = row[15]
    
    if Priority_queue_add == 'Yes' and '4_NationalView_' in script :
        Priority_queue_list[script] = directory_add

    Dict_all_scripts_to_run[script] = [id, '', directory_add,   script, Last_beg_execution_date_add, Last_end_execution_date_add, Best_execution_period_add, Worse_execution_period_add, Status_running_add, Current_Status_machine_add,  best_memory_usage_add, worse_memory_usage_add,  best_cpu_usage_add, best_cpu_usage_add , worse_cpu_usage_add,  pid_add, Priority_queue_add ]



ps = subprocess.Popen(['ps', 'aux'], stdout=subprocess.PIPE).communicate()[0]
processes = ps.split('\n')


number_of_script_running = 0
existing_python_scripts = {}
nfields = len(processes[0].split()) - 1
for row in processes[1:]:
    #print row
    if 'python' in row:
        for script_to_run in list(Dict_all_scripts_to_run.keys()):
          if '4_NationalView_' in script_to_run:
            print()
            line_tab =  row.split(None, nfields)
            print(line_tab)
            
            if  script_to_run  in row:
                if str(line_tab[-1]).strip() == 'python ' + str(script_to_run).strip():
                    existing_python_scripts[line_tab[1]] = {}
                    existing_python_scripts[line_tab[1]]['status'] = line_tab[7]
                    existing_python_scripts[line_tab[1]]['pid'] = line_tab[1]
                    existing_python_scripts[line_tab[1]]['cpu'] = line_tab[2]
                    existing_python_scripts[line_tab[1]]['mem'] = line_tab[3]
                    existing_python_scripts[line_tab[1]]['cmd'] = line_tab[-1]
                    existing_python_scripts[line_tab[1]]['script_running'] = str(script_to_run).strip()
                    number_of_script_running += 1
        
                    if str(existing_python_scripts[line_tab[1]]['status']) == 'T':
                        command = 'kill -9 ' + str(existing_python_scripts[line_tab[1]]['pid']).strip()
                        os.system(command)
                        number_of_script_running -= 1
                
            else:
                if '4_NationalView_' in script_to_run:
                    real_name_script = script_to_run.replace('4_NationalView_',"")

                elif '3_IXPView_' in script_to_run:
                    real_name_script = script_to_run.replace('3_IXPView_',"")

                elif '5_RegionalView_' in script_to_run:
                    real_name_script = script_to_run.replace('5_RegionalView_',"")
                
                #print 'real_name_script = ' , real_name_script
                if str(line_tab[-1]).strip() == 'python ' + str(real_name_script).strip():
                    print('We are in this case with ',str(real_name_script).strip())
                    existing_python_scripts[line_tab[1]] = {}
                    existing_python_scripts[line_tab[1]]['status'] = line_tab[7]
                    existing_python_scripts[line_tab[1]]['pid'] = line_tab[1]
                    existing_python_scripts[line_tab[1]]['cpu'] = line_tab[2]
                    existing_python_scripts[line_tab[1]]['mem'] = line_tab[3]
                    existing_python_scripts[line_tab[1]]['cmd'] = line_tab[-1]
                    existing_python_scripts[line_tab[1]]['script_running'] = str(script_to_run).strip()
                    number_of_script_running += 1


                    if str(existing_python_scripts[line_tab[1]]['status']) == 'T':
                        command = 'kill -9 ' + str(existing_python_scripts[line_tab[1]]['pid']).strip()
                        os.system(command)
                        number_of_script_running -= 1




#print existing_python_scripts
### When did each script start being executed ?
os.chdir('/African_Route-collectors_Data_Analyzer-ARDA/ComputationVM/Heart/7_scheduler')
command1 = """ps -eo pid,lstart,etime > list_cmd_dates.txt"""
os.system(command1)

with open ('list_cmd_dates.txt', 'r') as fh:
    
    for line in fh:
        
        if 'PID' not in line:
            print(line)
            line = line.strip()
            tab = line.split(' ')
            
            if str(tab[0]).strip() in list(existing_python_scripts.keys()):
                #print tab
                month_current = Months[tab[2]]
                print('tab before = ', tab)
                
                if '' in tab:
                    for item in range(tab.count('')):
                        tab.remove('')

                if int(tab[3]) < 10:
                    value = '0'+tab[3]
                else:
                    value = tab[3]
    
                date_found = value + '/'+ month_current+ '/' +  tab[5]

                print('date_found = ', date_found)
                print('tab after = ', tab)
                #time.sleep(50)
                
                tab1 = tab[-1].split('-')
                #print tab1
                if len(tab1) == 2:
                    current_period_of_execution = int(tab1[0])
                else:
                    current_period_of_execution = 0

                print(line, 'date_found = ', date_found, ' Number of executions days = ', current_period_of_execution)

                existing_python_scripts[str(tab[0]).strip()]['date_launch'] = date_found
                existing_python_scripts[str(tab[0]).strip()]['current_period_exec'] = current_period_of_execution


print()
print(existing_python_scripts)
print()
print("number_of_script_running = ", number_of_script_running)







#### Update table with all infos collected so far:

## 1- Put Running for all those running right now and not running for all those not running

## 2- Update PID and Memory (best and worse)

## 3- Update period of run

for script_to_run in list(Dict_all_scripts_to_run.keys()):
  if '4_NationalView_' in script_to_run:
    for pid_script_currently_running in list(existing_python_scripts.keys()):
    
        if existing_python_scripts[pid_script_currently_running]['script_running'] == script_to_run:
            
            Last_beg_execution_date_add = existing_python_scripts[pid_script_currently_running]['date_launch']
            Status_running_add =  'Running'
            Current_Status_machine_add = existing_python_scripts[pid_script_currently_running]['status']
            pid_add = existing_python_scripts[pid_script_currently_running]['pid']
            
            
            ## Decide (best and worse) memory
            current_best_memory_usage_add = Dict_all_scripts_to_run[script_to_run][10]
            if float(current_best_memory_usage_add) !=  float(-1) :
                if float(existing_python_scripts[pid_script_currently_running]['mem']) < float(current_best_memory_usage_add):
                    current_best_memory_usage_add = existing_python_scripts[pid_script_currently_running]['mem']
            else:
                current_best_memory_usage_add = float(existing_python_scripts[pid_script_currently_running]['mem'])
            
            
            
            current_worse_memory_usage_add = Dict_all_scripts_to_run[script_to_run][11]
            if float(Dict_all_scripts_to_run[script_to_run][10]) != float(-1):
                if float(current_worse_memory_usage_add) !=  float(-1) :
                    if float(Dict_all_scripts_to_run[script_to_run][10]) > float(current_worse_memory_usage_add):
                        current_worse_memory_usage_add = float(Dict_all_scripts_to_run[script_to_run][10])
                else:
                    current_worse_memory_usage_add = float(Dict_all_scripts_to_run[script_to_run][10])
            else:
                current_worse_memory_usage_add = float(existing_python_scripts[pid_script_currently_running]['mem'])
            
           
            
            ## Decide (best and worse) cpu
            
            current_best_cpu_usage_add = Dict_all_scripts_to_run[script_to_run][12]
            if float(current_best_cpu_usage_add) != float(-1) :
                if float(existing_python_scripts[pid_script_currently_running]['cpu']) < float(current_best_cpu_usage_add):
                    current_best_cpu_usage_add = existing_python_scripts[pid_script_currently_running]['cpu']
            else:
                current_best_cpu_usage_add = float(existing_python_scripts[pid_script_currently_running]['cpu'])
            
            
            
            current_worse_cpu_usage_add = Dict_all_scripts_to_run[script_to_run][13]

            if float(Dict_all_scripts_to_run[script_to_run][13]) != float(-1):
                
                if float(existing_python_scripts[pid_script_currently_running]['cpu']) > float(current_worse_cpu_usage_add):
                    current_worse_cpu_usage_add = float(existing_python_scripts[pid_script_currently_running]['cpu'])
                
            else:
                current_worse_cpu_usage_add = float(existing_python_scripts[pid_script_currently_running]['cpu'])


            print('After =', Last_beg_execution_date_add, Status_running_add, Current_Status_machine_add, current_best_memory_usage_add, current_worse_memory_usage_add,  current_best_cpu_usage_add, current_worse_cpu_usage_add, pid_add, script_to_run)
            cur.execute ("""UPDATE Infos_on_all_scripts_to_run SET Last_beg_execution_date=%s, Current_Status=%s, Current_Status_machine =%s,  best_memory_usage = %s, worse_memory_usage= %s, best_cpu_usage =%s, worse_cpu_usage = %s, pid =%s WHERE Script_to_execute=%s""", (Last_beg_execution_date_add, Status_running_add, Current_Status_machine_add, current_best_memory_usage_add, current_worse_memory_usage_add,  current_best_cpu_usage_add, current_worse_cpu_usage_add, pid_add, script_to_run))

            db.commit()


length = len(list(existing_python_scripts.keys()))
print('length = ', length)





for script_to_run in list(Dict_all_scripts_to_run.keys()):
  if '4_NationalView_' in script_to_run:    
    indice_numb_case_non_equal = 0
    
    for pid_script_currently_running in list(existing_python_scripts.keys()):

        if  script_to_run != existing_python_scripts[pid_script_currently_running]['script_running']:
            
            indice_numb_case_non_equal  += 1
            
    
    if indice_numb_case_non_equal  == length:
    
            ### Status == 'Not Running'

            Status_running_add =  'Not Running'
            
            cur.execute ("""UPDATE Infos_on_all_scripts_to_run SET  Current_Status=%s, Current_Status_machine = %s  WHERE Script_to_execute=%s""", (Status_running_add, '', script_to_run))
            
            ## Look for date end and compute period (best and worse)
            #print 'I am here'
            
            if Dict_all_scripts_to_run[script_to_run][4]!= 'Unknown' and Dict_all_scripts_to_run[script_to_run][5] != 'Unknown':

                print('Current values = ', Dict_all_scripts_to_run[script_to_run][4], Dict_all_scripts_to_run[script_to_run][5])
                
                date_beg = datetime.strptime(Dict_all_scripts_to_run[script_to_run][4], "%d/%m/%Y")
                date_end = datetime.strptime(Dict_all_scripts_to_run[script_to_run][5], "%d/%m/%Y")
                
                print('Date =', date_beg, date_end)

                if date_beg <= date_end :
                    
                    delta = date_end - date_beg
                    
                    print('let us extract the number of days and update periods.')
                    
                    periodd = delta.days
                    
                    Worse_execution_period_add = int(Dict_all_scripts_to_run[script_to_run][7])
                    if Worse_execution_period_add != int('-1'):
                        if periodd > Worse_execution_period_add:
                            Worse_execution_period_add = periodd
                    else:
                        Worse_execution_period_add = periodd
                    
                    
                    Best_execution_period_add = int(Dict_all_scripts_to_run[script_to_run][6])
                    if Best_execution_period_add != int('-1'):
                        if periodd < Best_execution_period_add:
                            Best_execution_period_add = periodd
                    else:
                        Best_execution_period_add = periodd

                    print(Best_execution_period_add, Worse_execution_period_add, script_to_run)
                    
                    cur.execute ("""UPDATE Infos_on_all_scripts_to_run SET  Best_execution_period=%s, Worse_execution_period=%s  WHERE Script_to_execute=%s""", (Best_execution_period_add, Worse_execution_period_add, script_to_run))

                    db.commit()





### select all lines where both begin exec date and end dates are Unknown and update end date to 1 year ago:

query = """select * from Infos_on_all_scripts_to_run where Last_end_execution_date = 'Unknown' and Last_beg_execution_date = 'Unknown' """
cur.execute(query)
for row in cur.fetchall():
    #print 'row = ', row
    ## treat info and update whenever you need to
    id = row[0]
    script = row[3]


    from datetime import date
    from dateutil.relativedelta import relativedelta

    twelve_months_ago = date.today() - relativedelta(months=+12)

    tab_date = str(twelve_months_ago).split('-')
    
    date_a_year_ago = tab_date[-1] + '/' + tab_date[-2] + '/' + tab_date[-3]

    print('Here are the date of today and 1 year ago ',  date.today(), twelve_months_ago, 'Better written for update = ', date_a_year_ago)


    cur.execute ("""UPDATE Infos_on_all_scripts_to_run SET Last_end_execution_date=%s WHERE Script_to_execute=%s and id=%s""",(date_a_year_ago, script, id))
    
    db.commit()







### Check the priority queue
#time.sleep(10)
print('Priority_queue_list = ', Priority_queue_list)

Priority_queue_list_copy = copy.deepcopy(Priority_queue_list)


if len(list(Priority_queue_list_copy.keys())) > 0:
    
    ## pay attention that the number of scripts running never exceeds 5; this number can be ajusted later
    if number_of_script_running <= number_of_script_not_to_exceed :
        
        ## date_now :
        from datetime import datetime
        
        
        
        ### if there is any file in that queue, launch it, sleep andcome back alive and check if that script is running.
        for script in Priority_queue_list:
            
            current_date = datetime.now().strftime('%d-%m-%Y-%H-%M-%S')
            tab111 = current_date.split('-')
            date_today = tab111[0] + '/' + tab111[1] + '/' + tab111[2]
            print('current date = ', current_date)
            
            from crontab import CronTab
            ### Alert: Put Username here
            tab = CronTab(user = 'Username')
            
            direc = Priority_queue_list[script]
            os.chdir(direc)
            
            cmd = 'cd ' + direc +  ' && ' + ' python ' + script
            cron_job = tab.new(cmd, comment='MyJob')
            print('cron_job = ', cron_job)
            value = int(tab111[4])+5
            print(value)
            
            if int(tab111[4])+5 < 59:
                cron_job.minute.on(int(tab111[4])+5)
                cron_job.hour.on(int(tab111[3]))
            
            else:
                cron_job.minute.on(int(1))
                cron_job.hour.on(int(tab111[3]) + 1)
            
            cron_job.day.on(int(tab111[0]))
            cron_job.month.on(int(tab111[1]))
            
            #writes content to crontab
            print('cron_job = ', cron_job)
            if True == cron_job.is_valid():
                print('Script added in cron')
                tab.write()
                print(tab.render())
                print('sleeping')
                if int(tab111[4])+5 < 59:
                    time.sleep(350)
                else:
                    time.sleep(600)
                print('end of sleep')
            
            for item in tab.find_comment('MyJob'):
                print('item to remove = ', item)
                tab.remove(item)
            
            tab.remove_all(comment='MyJob')
            
            #tab.remove(cron_job)

            #if len(cron_job) > 0:
            #tab.remove_all(cmd)
            #writes content to crontab
            tab.write()


            ## check if it is running
            ps = subprocess.Popen(['ps', 'aux'], stdout=subprocess.PIPE).communicate()[0]
            processes = ps.split('\n')

            existing_python_scripts_now = {}
            nfields = len(processes[0].split()) - 1
            
            for row in processes[1:]:
                if 'python' in row:

                    for script_to_run in list(Dict_all_scripts_to_run.keys()):
                      if '4_NationalView_' in script_to_run:
		        print()
                        line_tab =  row.split(None, nfields)
                        print(line_tab)
            
                        if  script_to_run  in row:
                            if str(line_tab[-1]).strip() == 'python ' + str(script_to_run).strip():
                                existing_python_scripts_now[line_tab[1]] = {}
                                existing_python_scripts_now[line_tab[1]]['status'] = line_tab[7]
                                existing_python_scripts_now[line_tab[1]]['pid'] = line_tab[1]
                                existing_python_scripts_now[line_tab[1]]['cpu'] = line_tab[2]
                                existing_python_scripts_now[line_tab[1]]['mem'] = line_tab[3]
                                existing_python_scripts_now[line_tab[1]]['cmd'] = line_tab[-1]
                                existing_python_scripts_now[line_tab[1]]['script_running'] = str(script_to_run).strip()

                
                        else:
                            if '4_NationalView_' in script_to_run:
                                real_name_script = script_to_run.replace('4_NationalView_',"")
                                
                            elif '3_IXPView_' in script_to_run:
                                real_name_script = script_to_run.replace('3_IXPView_',"")
                        
                            elif '5_RegionalView_' in script_to_run:
                                real_name_script = script_to_run.replace('5_RegionalView_',"")
                                
                            #print 'real_name_script = ' , real_name_script
                                
                            if str(line_tab[-1]).strip() == 'python ' + str(real_name_script).strip():
                                print('We are in this case with ',str(real_name_script).strip())
                                existing_python_scripts_now[line_tab[1]] = {}
                                existing_python_scripts_now[line_tab[1]]['status'] = line_tab[7]
                                existing_python_scripts_now[line_tab[1]]['pid'] = line_tab[1]
                                existing_python_scripts_now[line_tab[1]]['cpu'] = line_tab[2]
                                existing_python_scripts_now[line_tab[1]]['mem'] = line_tab[3]
                                existing_python_scripts_now[line_tab[1]]['cmd'] = line_tab[-1]
                                existing_python_scripts_now[line_tab[1]]['script_running'] = str(script_to_run).strip()
        

            ## import time
            ## print (time.strftime("%d/%m/%Y"))
            ## existing_python_scripts[line_tab[-1]]['start_date1'] = line_tab[3]

            ## Find the date of launch of that script

            for linee in existing_python_scripts_now:
                
                #if cmd in existing_python_scripts_now[linee]['cmd']:
                
                if script == existing_python_scripts_now[linee]['script_running']:

                    print('The script is running')
                    print('We can make changes.')

                    ##if yes remove the script from the list of Priority queues by updating in the table  the line corresponding to that script.
                
                    os.chdir('/African_Route-collectors_Data_Analyzer-ARDA/ComputationVM/Heart/7_scheduler')
                    command1 = """ps -eo pid,lstart,etime > list_cmd_dates.txt"""
                    os.system(command1)

                    with open ('list_cmd_dates.txt', 'r') as fh:
            
                        for line in fh:
                            
                            if 'PID' not in line:
                                #print line
                                line = line.strip()
                                tab = line.split(' ')
                                
                                if str(tab[0]).strip() in list(existing_python_scripts_now.keys()):
                                    print('I found the script in', tab)
                                    month_current = Months[tab[2]]
                                    if '' in tab:
                                        for item in range(tab.count('')):
                                            tab.remove('')
                                
                                    if int(tab[3]) < 10:
                                        value = '0'+tab[3]
                                    else:
                                        value =tab[3]
                                    
                                    date_found = value + '/'+ month_current+ '/' +  tab[5]
                                    
                                    print('date_found = ', date_found)
                                    #print tab
                                    #time.sleep(50)
                                    
                                    tab1 = tab[-1].split('-')
                                    #print tab1
                                    ## It is in days.
                                    
                                    if len(tab1) == 2:
                                        current_period_of_execution = int(tab1[0])
                                    else:
                                        current_period_of_execution = 0
                                
                                    print(line, 'date_found = ', date_found, ' Number of executions days = ', current_period_of_execution)
                                    
                                    existing_python_scripts_now[tab[0]]['date_launch'] = date_found
                                    existing_python_scripts_now[tab[0]]['current_period_exec'] = current_period_of_execution
                    
                    
                    print('existing_python_scripts_now =', existing_python_scripts_now)

                    print('before = ', Last_beg_execution_date_add)

                    if 'date_launch' in list(existing_python_scripts_now[linee].keys()):
                        print('date_launch is in existing_python_scripts_now')
                        Last_beg_execution_date_add = existing_python_scripts_now[linee]['date_launch']

                    print('after = ', Last_beg_execution_date_add)
                    

                    if float(existing_python_scripts_now[linee]['mem']) < float(best_memory_usage_add) :
                        best_memory_usage_add = float(existing_python_scripts_now[linee]['mem'])

                    elif float(existing_python_scripts_now[linee]['mem']) > float(worse_memory_usage_add) :
                        worse_memory_usage_add = float(existing_python_scripts_now[linee]['mem'])

                    Status_running_add = 'Running'

                    if float(existing_python_scripts_now[linee]['cpu']) < float(best_cpu_usage_add) :
                        best_cpu_usage_add = float(existing_python_scripts_now[linee]['cpu'])

                    elif float(existing_python_scripts_now[linee]['cpu']) > float(worse_cpu_usage_add) :
                        worse_cpu_usage_add = float(existing_python_scripts_now[linee]['cpu'])

                    print('after = ', Last_beg_execution_date_add)
                    
                    pid_add = existing_python_scripts_now[linee]['pid']

                    Current_Status_machine_add = existing_python_scripts_now[linee]['status']

                    Priority_queue_add = 'No'

                    print('after = ', Last_beg_execution_date_add)
                    
                    if Last_beg_execution_date_add == 'Unknown' and Status_running_add == 'Running':
                        Last_beg_execution_date_add = date_today
                    
                    print(direc, Last_beg_execution_date_add, best_memory_usage_add, worse_memory_usage_add,  Status_running_add, best_cpu_usage_add, worse_cpu_usage_add, pid_add, Current_Status_machine_add, Priority_queue_add)

                    ### Update table
                    ### When you restart such a script, start date should be 'Unknown'

                    Last_end_execution_date_add = 'Unknown'

                    cur.execute ("""UPDATE Infos_on_all_scripts_to_run SET Last_beg_execution_date=%s, Current_Status=%s,  Current_Status_machine=%s,  best_memory_usage = %s, worse_memory_usage=%s, pid=%s, Priority_queue=%s, best_cpu_usage=%s, worse_cpu_usage=%s, Last_end_execution_date=%s WHERE Script_to_execute =%s""", (Last_beg_execution_date_add, Status_running_add, Current_Status_machine_add, best_memory_usage_add, worse_memory_usage_add, pid_add, Priority_queue_add, best_cpu_usage_add, worse_cpu_usage_add, Last_end_execution_date_add, script))
    
                    db.commit()

                    number_of_script_running += 1


                    ## Create a priority queue from the info in the table and prioritize them while running the scripts

                    #if in the priority queue a script is executed, it dispareer from the list of scripts to reececute right now


                    del(Priority_queue_list_copy[script])


    Priority_queue_list = copy.deepcopy(Priority_queue_list_copy)


print('The current number of total ', number_of_script_running)


#sys.exit()







if len(Priority_queue_list) == 0:
    
    # Prioritise National View and Regional View as they run Fast
    
    # Run 1 of National View and 1 of Regional View and launch 2 of IXP View,
    
    
    #Categories = [ '3_IXPView', '4_NationalView', '5_RegionalView', '3_IXPView', '3_IXPView' ]
        
    Categories = [ '4_NationalView']
    
    print('Here is Category before schuffling : ', Categories)
    
    random.shuffle(Categories)
    
    print('Here is Category after schuffling : ', Categories)
    
    for Category in Categories:
        
        ## select the info from the table
        query = """select * from Infos_on_all_scripts_to_run where Current_Status = 'Not Running' """
        cur.execute(query)
        output_query = cur.fetchall()
        
        print()
        print(Category)
        
        Old_execution_time = ''
        Script_to_be_executed = ''
        value = ''
        
        from datetime import datetime
        for row in output_query:
            #print 'row = ', row
            ## treat info and update whenever you need to
            direc = row[2]
            script = row[3]
            Last_beg_execution_date_add = row[4]
            Last_end_execution_date_add = row[5]
            row_date = ''
            
            if Category in script:
                if Last_end_execution_date_add != 'Unknown':
                    row_date = Last_end_execution_date_add
                
                elif Last_beg_execution_date_add != 'Unknwon':
                    row_date = Last_beg_execution_date_add
                
                
            
                if row_date != '' and len(row_date) == 10:
                    print(row_date)
                    considered_date = time.strptime(row_date, "%d/%m/%Y")
                    considered_directory =  direc
                    
                    if Old_execution_time == '':
                        Old_execution_time = considered_date
                        Script_to_be_executed = script
                        direc_keep = considered_directory
                    
                    else:
                        if Old_execution_time > considered_date:
                            Old_execution_time = considered_date
                            Script_to_be_executed = script
                            direc_keep = considered_directory
    
    

        print('We need to execute ', Script_to_be_executed, 'run ast time at ', Old_execution_time, direc_keep)

        ## It ensures that no more than 5 scripts are running in parallel with the background downloader.

        if number_of_script_running < number_of_script_not_to_exceed:

            current_date = datetime.now().strftime('%d-%m-%Y-%H-%M-%S')
            tab111 = current_date.split('-')
            date_today = tab111[0] + '/' + tab111[1] + '/' + tab111[2]
            print('current date = ', current_date)
            
            script = Script_to_be_executed
            
            from crontab import CronTab
            ## Alert : Put your username below
            tab = CronTab(user = 'Username')
        
            direc = direc_keep
            os.chdir(direc)
            
            cmd = 'cd ' + direc +  ' && ' + ' python ' + script
            cron_job = tab.new(cmd, comment='MyJob')
            print('cron_job = ', cron_job)
            value = int(tab111[4])+5
            print(value)
            
            if int(tab111[4])+5 < 59:
                cron_job.minute.on(int(tab111[4])+5)
                cron_job.hour.on(int(tab111[3]))
            
            else:
                cron_job.minute.on(int(1))
                cron_job.hour.on(int(tab111[3]) + 1)
            
            cron_job.day.on(int(tab111[0]))
            cron_job.month.on(int(tab111[1]))
            
            #writes content to crontab
            print('cron_job = ', cron_job)
            if True == cron_job.is_valid():
                print('Script added in cron')
                tab.write()
                print(tab.render())
                print('sleeping')
                if int(tab111[4])+5 < 59:
                    time.sleep(350)
                else:
                    time.sleep(600)
                print('end of sleep')
            
            
            for item in tab.find_comment('MyJob'):
                print('item to remove = ', item)
                tab.remove(item)
        
            tab.remove_all(comment='MyJob')

            tab.write()
            
            
            ## check if it is running
            ps = subprocess.Popen(['ps', 'aux'], stdout=subprocess.PIPE).communicate()[0]
            processes = ps.split('\n')
            
            existing_python_scripts_now = {}
            nfields = len(processes[0].split()) - 1
            
            for row in processes[1:]:
                if 'python' in row:
        
                    for script_to_run in list(Dict_all_scripts_to_run.keys()):
                      if '4_NationalView_' in script_to_run:
		        print()
                        line_tab =  row.split(None, nfields)
                        print(line_tab)
                        
                        if  script_to_run  in row:
                            if str(line_tab[-1]).strip() == 'python ' + str(script_to_run).strip():
                                existing_python_scripts_now[line_tab[1]] = {}
                                existing_python_scripts_now[line_tab[1]]['status'] = line_tab[7]
                                existing_python_scripts_now[line_tab[1]]['pid'] = line_tab[1]
                                existing_python_scripts_now[line_tab[1]]['cpu'] = line_tab[2]
                                existing_python_scripts_now[line_tab[1]]['mem'] = line_tab[3]
                                existing_python_scripts_now[line_tab[1]]['cmd'] = line_tab[-1]
                                existing_python_scripts_now[line_tab[1]]['script_running'] = str(script_to_run).strip()
                
                
                        else:
                            if '4_NationalView_' in script_to_run:
                                real_name_script = script_to_run.replace('4_NationalView_',"")
                                
                            elif '3_IXPView_' in script_to_run:
                                real_name_script = script_to_run.replace('3_IXPView_',"")
                        
                            elif '5_RegionalView_' in script_to_run:
                                real_name_script = script_to_run.replace('5_RegionalView_',"")
                                
                            #print 'real_name_script = ' , real_name_script
                                
                            if str(line_tab[-1]).strip() == 'python ' + str(real_name_script).strip():
                                print('We are in this case with ',str(real_name_script).strip())
                                existing_python_scripts_now[line_tab[1]] = {}
                                existing_python_scripts_now[line_tab[1]]['status'] = line_tab[7]
                                existing_python_scripts_now[line_tab[1]]['pid'] = line_tab[1]
                                existing_python_scripts_now[line_tab[1]]['cpu'] = line_tab[2]
                                existing_python_scripts_now[line_tab[1]]['mem'] = line_tab[3]
                                existing_python_scripts_now[line_tab[1]]['cmd'] = line_tab[-1]
                                existing_python_scripts_now[line_tab[1]]['script_running'] = str(script_to_run).strip()



            ## import time
            ## print (time.strftime("%d/%m/%Y"))
            ## existing_python_scripts[line_tab[-1]]['start_date1'] = line_tab[3]
            
            ## Find the date of launch of that script
            ## select the info from the table
            query1 = """select * from Infos_on_all_scripts_to_run where Script_to_execute = %s"""
            cur.execute(query1, script)

            for rrow in cur.fetchall():
                id = rrow[0]
                directory_add = rrow[2]
                script = rrow[3]
                Last_beg_execution_date_add = rrow[4]
                Last_end_execution_date_add = rrow[5]
                Best_execution_period_add = rrow[6]
                Worse_execution_period_add = rrow[7]
                Status_running_add = rrow[8]
                Current_Status_machine_add = rrow[9]
                best_memory_usage_add = rrow[10]
                worse_memory_usage_add = rrow[11]
                best_cpu_usage_add  = rrow[12]
                worse_cpu_usage_add = rrow[13]
                pid_add = rrow[14]
                Priority_queue_add = rrow[15]
                
                
            for linee in existing_python_scripts_now:
                
                #if cmd in existing_python_scripts_now[linee]['cmd']:
                
                if script == existing_python_scripts_now[linee]['script_running']:
                    
                    print('The script is running')
                    print('We can make changes.')
                    
                    ##if yes remove the script from the list of Priority queues by updating in the table  the line corresponding to that script.
                    os.chdir('/African_Route-collectors_Data_Analyzer-ARDA/ComputationVM/Heart/7_scheduler')
                    command1 = """ps -eo pid,lstart,etime > list_cmd_dates.txt"""
                    os.system(command1)
                    
                    with open ('list_cmd_dates.txt', 'r') as fh:
                        
                        for line in fh:
                            
                            if 'PID' not in line:
                                
                                #print line
                                line = line.strip()
                                tab = line.split(' ')
                                
                                if tab[0] in list(existing_python_scripts_now.keys()):
                                    print('I found the script in', tab)
                                    month_current = Months[tab[2]]
                                   
                                    if '' in tab:
                                        for item in range(tab.count('')):
                                            tab.remove('')

                                    if int(tab[3]) < 10:
                                        value = '0'+tab[3]
                                    else:
                                        value = tab[3]
                                    date_found = value + '/'+ month_current+ '/' +  tab[5]
                                    
                                    print('date_found = ', date_found)
                                    #print tab
                                    #time.sleep(50)

                                    tab1 = tab[-1].split('-')
                                    #print tab1
                                    ## It is in days.
                                    
                                    if len(tab1) == 2:
                                        current_period_of_execution = int(tab1[0])
                                    else:
                                        current_period_of_execution = 0
                                    
                                    print(line, 'date_found = ', date_found, ' Number of executions days = ', current_period_of_execution)
                                    
                                    existing_python_scripts_now[tab[0]]['date_launch'] = date_found
                                    existing_python_scripts_now[tab[0]]['current_period_exec'] = current_period_of_execution
                
                
                    print('existing_python_scripts_now =', existing_python_scripts_now)
                    
                    print('before = ', Last_beg_execution_date_add)
                    
                    if 'date_launch' in list(existing_python_scripts_now[linee].keys()):
                        print('date_launch is in existing_python_scripts_now')
                        Last_beg_execution_date_add = existing_python_scripts_now[linee]['date_launch']
                    
                    print('after = ', Last_beg_execution_date_add)
                    
                    if float(existing_python_scripts_now[linee]['mem']) < float(best_memory_usage_add) :
                        best_memory_usage_add = existing_python_scripts_now[linee]['mem']
                    
                    elif float(existing_python_scripts_now[linee]['mem']) > float(worse_memory_usage_add) :
                        worse_memory_usage_add = existing_python_scripts_now[linee]['mem']
                    
                    Status_running_add = 'Running'

                    if float(existing_python_scripts_now[linee]['cpu']) < float(best_cpu_usage_add) :
                        best_cpu_usage_add = float(existing_python_scripts_now[linee]['cpu'])
                    
                    elif float(existing_python_scripts_now[linee]['cpu']) > float(worse_cpu_usage_add):
                        worse_cpu_usage_add = float(existing_python_scripts_now[linee]['cpu'])
                    
                    print('after = ', Last_beg_execution_date_add)
                    
                    pid_add = existing_python_scripts_now[linee]['pid']
                    
                    Current_Status_machine_add = existing_python_scripts_now[linee]['status']

                    Priority_queue_add = 'No'
                    
                    print('after = ', Last_beg_execution_date_add)
                    
                    if Last_beg_execution_date_add == 'Unknown' and Status_running_add == 'Running':
                        Last_beg_execution_date_add = date_today
                    
                    Last_end_execution_date_add = 'Unknown'
                
                    print(direc, Last_beg_execution_date_add, best_memory_usage_add, worse_memory_usage_add,  Status_running_add, best_cpu_usage_add, worse_cpu_usage_add, pid_add, Current_Status_machine_add, Priority_queue_add)
                        
                        ### Update table
                        
                    cur.execute ("""UPDATE Infos_on_all_scripts_to_run SET Last_beg_execution_date=%s,   Current_Status=%s,  Current_Status_machine=%s,  best_memory_usage = %s, worse_memory_usage=%s, pid=%s, Priority_queue=%s, best_cpu_usage=%s, worse_cpu_usage=%s, Last_end_execution_date=%s WHERE Script_to_execute =%s""", (Last_beg_execution_date_add, Status_running_add, Current_Status_machine_add, best_memory_usage_add, worse_memory_usage_add, pid_add, Priority_queue_add, best_cpu_usage_add, worse_cpu_usage_add, Last_end_execution_date_add, script))
                        
                    db.commit()
                            
                    number_of_script_running += 1

print('number_of_script_running  = ', number_of_script_running)
