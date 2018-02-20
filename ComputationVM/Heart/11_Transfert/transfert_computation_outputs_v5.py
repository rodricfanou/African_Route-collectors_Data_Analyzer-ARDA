## ARDA Application released on: April 21, 2017
## Last review: February 19, 2018
## Author: Roderick Fanou
## Alert: Cron edition
#Update every 60mn the computations outputs in the visualization folder ARP_visual
#by moving the last results from the computation VM to the visualisation VM
#*/59 * * * * cd African_Route-collectors_Data_Analyzer-ARDA/ComputationVM/Heart/11_Transfert && python update_list_IXP_v2.py

import sys, os
from glob import glob
from datetime import date
from datetime import datetime


def run_fonction(execution_directory, directory, destination, op):
    command = 'chmod -R 777 ' + directory
    os.system(command)
    os.walk(directory)
    
    List_folders = next(os.walk(execution_directory))[1]
    for folder_to_move in List_folders:
        print
        print folder_to_move
        
        ## find all the files *.txt
        print execution_directory +'/'+ folder_to_move + '/*.txt'
        path = glob(execution_directory + '/'+ folder_to_move + '/*.txt')
        
        number_to_reach = len(path)
        print path, number_to_reach
        
        i = 0
        tab_total = []
        for file in path:
            with open(file, 'r') as fg:
                for line in fg:
                    if 'ended' in line:
                        i += 1
                        tab = line.split(';')
                        tab_total.append (str(tab[1]).strip())
    
    
        if i == number_to_reach:
            print 'We can move the results of ', execution_directory + '/'+ folder_to_move
            for folder in tab_total:
                #print 'We can move the results of ', execution_directory + '/'+ folder_to_move
                
                if op == 'IXPView':
                    print 'rm ' + destination + folder[folder.find('Computation_outputs')+20:]+ '*'
                    command =  'rm ' + destination + folder[folder.find('Computation_outputs')+20:]+ '*'
                    os.system (command)
                    print 'We shall cp -r ' , folder
                    print 'send it to ', destination +folder[folder.find('Computation_outputs')+20:]
                    command = 'cp -r '+ folder + ' ' + destination 
                    os.system (command)
                    print command
        
        
                if op == 'RegView':
                    
                    print 'rm ' + destination + folder[folder.find('Computation_outputs_Regional_View')+20:]+ '*'
                    command =  'rm ' + destination + folder[folder.find('Computation_outputs_Regional_View')+20:]+ '*'
                    os.system (command)

                    print 'We shall cp -r ' , folder
                    print 'send it to ', destination +folder[folder.find('Computation_outputs_Regional_View')+20:]

                    command = 'cp -r '+ folder + ' ' + destination
                    os.system (command)
                    print command


                if op == 'NatView':
    
                    print 'rm ' + destination + folder[folder.find('Computation_outputs_National_View')+20:]+ '*'
                    command =  'rm ' + destination + folder[folder.find('Computation_outputs_National_View')+20:]+ '*'
                    os.system (command)
                
                    print 'We shall cp -r ' , folder
                    print 'send it to ', destination +folder[folder.find('Computation_outputs_National_View')+20:]
                    
                    command = 'cp -r '+ folder + ' ' + destination
                    os.system (command)
                    print command
    
        else:
            print 'We can NOT move the results of ', execution_directory + '/'+ folder_to_move

    command = 'chmod -R 777 ' + destination
    os.system(command)


########## Beg Execution
now_datetime = str(datetime.now()).replace(' ', '_')

finish = open ('transfert_finished.txt', 'w')
finish.write('started' + '; '  + now_datetime)
finish.close()


############## Update IXP View data
op = 'IXPView'
execution_directory = '/African_Route-collectors_Data_Analyzer-ARDA/ComputationVM/Heart/3_IXPView'
directory = '/African_Route-collectors_Data_Analyzer-ARDA/ComputationVM/Heart/Computation_outputs'
##path to the location of the outputs of the IXP view computations in the /var directory
destination = '/var/www/html/.../outputs/'
run_fonction(execution_directory, directory, destination, op)


############## Update Regional View data
op = 'RegView'
execution_directory = '/African_Route-collectors_Data_Analyzer-ARDA/ComputationVM/Heart/5_RegionalView'
directory = '/African_Route-collectors_Data_Analyzer-ARDA/ComputationVM/Heart/Computation_outputs_Regional_View'
##path to the location of the outputs of the Regional view computations in the /var directory
destination = '/var/www/html/.../outputs_Regional_View/'
run_fonction(execution_directory, directory, destination, op)


############## Update National View data
op = 'NatView'
execution_directory = '/African_Route-collectors_Data_Analyzer-ARDA/ComputationVM/Heart/4_NationalView'
directory = '/African_Route-collectors_Data_Analyzer-ARDA/ComputationVM/Heart/Computation_outputs_National_View'
##path to the location of the outputs of the National view computations in the /var directory
destination = '/var/www/html/.../outputs_National_View/'
run_fonction(execution_directory, directory, destination, op)


########## End Execution
now_datetime = str(datetime.now()).replace(' ', '_')
finish = open ('transfert_finished.txt', 'w')
finish.write('ended' + '; '  + now_datetime)
finish.close()
