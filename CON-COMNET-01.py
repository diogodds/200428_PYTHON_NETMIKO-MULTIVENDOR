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

#timestr = time.strftime('%Y%m%d-%H%M%S')

username = 'dsantos'
#password = getpass.getpass()
password = '/v5196S#'

########################################################################
    

with open('CON-COMNET-01.txt') as file: # This opens the text file with the BGP parameters in csv format
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
    
    net_connect = ConnectHandler(device_type='cisco_ios', ip=dictionary['IP'], username=username, password=password, global_delay_factor=2.0)
  
    print('Connected to ' + dictionary['HOSTNAME'] + '. Applying configuration script.')
    
    net_connect.send_command('\n')
    net_connect.send_command('conf t', expect_string=r'#')

    print('>>> no username zalandoadmin')
    output = net_connect.send_command('no username zalandoadmin', expect_string=r'#')
    print(output)
    
    print('>>> username manager privilege 15 password unencrypted ' + dictionary['SECRET'])
    output = net_connect.send_command('username manager privilege 15 password unencrypted ' + dictionary['SECRET'], expect_string=r'#')
    print(output)
    
    print('>>> exit')
    output = net_connect.send_command('exit', expect_string=r'#')
    print(output)

    print('\nSaving changes to ' + dictionary['HOSTNAME'])#

    output = net_connect.send_command('copy running-config startup-config', expect_string=r'#')
    print(output)    
    
    print('Changes saved.')
  
    end_time = datetime.now()
    
    print('\nTotal time: {}'.format(end_time - start_time) +'\n' + '#' * 60)