#!/usr/bin/env python

from netmiko import ConnectHandler 
from datetime import datetime
#import time
import sys
import getpass
import re
 
 #######################################################################
 # Warnings module needed to be imported to solve a connection mode    #
 # deprecated warning that I was getting when trying to connect to the #
 # juniper switches                                                    #
 #######################################################################

import warnings
warnings.filterwarnings(action='ignore',module='.*paramiko.*')

########################################################################

username = 'dsantos'
password = getpass.getpass()

def ntmk_aruba(command):
    net_connect.send_command(command, expect_string=r"#")

########################################################################
    

with open('CON-ARUBA-01.txt') as file: # This opens the text file with the BGP parameters in csv format
    parameters = file.read().splitlines() # The file is loaded into the "parameters" variable and splited into lines
    
for line in parameters:
    attribute_per_device = line.split(',') # This is to split each element of a line on the csv files to objects on a list

    # A dictionary will be created based on the objects of each line of the list (for loop will be in charge of looping
    # through all lines in the csv / txt file
    dictionary = {'HOSTNAME':attribute_per_device[0],
                  'IP':attribute_per_device[1],
                  'SECRET':attribute_per_device[2],                
                 }            
    
    print('#' * 60 + '\n' + 'Establishing connection to ' + dictionary['HOSTNAME'] + '.')    
    
    start_time = datetime.now()
    print(str(start_time.strftime("%Y-%m-%d %H:%M:%S")))
    
    net_connect = ConnectHandler(device_type='hp_procurve', ip=dictionary['IP'], username=username, password=password, global_delay_factor=3.0)
  
    print('Connected to ' + dictionary['HOSTNAME'] + '. Applying configuration script.')
    
    net_connect.send_command('\n')
    net_connect.send_command('conf t', expect_string=r'#')
    net_connect.send_command('hostname ' + dictionary['HOSTNAME'], expect_string=r'#')
    net_connect.send_command('no aaa authentication local-user "zalandoadmin" group "Level-15"', expect_string=r'#')
    net_connect.send_command('password manager plaintext ' + dictionary['SECRET'], expect_string=r'#')
    net_connect.send_command('encrypt-credential', expect_string=r'(y/n)?')
    net_connect.send_command('y', expect_string=r'#')
    net_connect.send_command('exit', expect_string=r'#')#

    print('\nSaving changes to ' + dictionary['HOSTNAME'])#

    net_connect.send_command('write memory', expect_string=r'#')    

    print('Changes saved.')
  
    end_time = datetime.now()
    
    print('\nTotal time: {}'.format(end_time - start_time) +'\n' + '#' * 60)