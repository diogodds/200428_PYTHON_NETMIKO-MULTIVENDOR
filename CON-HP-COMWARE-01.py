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

########################################################################
    

with open('CON-HP-COMWARE-01.txt') as file: # This opens the text file with the BGP parameters in csv format
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
    
    net_connect = ConnectHandler(device_type='hp_comware', ip=dictionary['IP'], username=username, password=password, global_delay_factor=2.0)
  
    print('Connected to ' + dictionary['HOSTNAME'] + '. Applying configuration script.')
    
    net_connect.send_command('\n')
    net_connect.send_command('system-view', expect_string=r']')
    
    print('>>>> undo local-user zalandoadmin class manage')
    output = net_connect.send_command('undo local-user zalandoadmin class manage', expect_string=r']')
    print(output)

    print('>>>> local-user manager class manage')
    output = net_connect.send_command('local-user manager class manage', expect_string=r']')
    print(output)

    print('>>>> password simple ' + dictionary['SECRET'])
    output = net_connect.send_command('password simple ' + dictionary['SECRET'], expect_string=r']')
    print(output)
    
    print('>>>> authorization-attribute level 3')
    output = net_connect.send_command('authorization-attribute level 3', expect_string=r']')
    print(output)

    print('>>>> service-type ssh terminal')
    output = net_connect.send_command('service-type ssh terminal', expect_string=r']')
    print(output)
    
    print('>>>> service-type web')
    output = net_connect.send_command('service-type web', expect_string=r']')
    print(output)
    
    print('>>>> service-type http')    
    output = net_connect.send_command('service-type http', expect_string=r']')
    print(output)

    print('>>>> service-type https')    
    output = net_connect.send_command('service-type https', expect_string=r']')
    print(output)

    print('>>>> authorization-attribute user-role network-admin')    
    output = net_connect.send_command('authorization-attribute user-role network-admin', expect_string=r']')
    print(output)
    
    print('>>>> authorization-attribute user-role network-operator')    
    output = net_connect.send_command('authorization-attribute user-role network-operator', expect_string=r']')
    print(output)
    
    output = net_connect.send_command('quit', expect_string=r']')
    print(output)

    print('>>>> ssh user manager service-type all authentication-type password')    
    output = net_connect.send_command('ssh user manager service-type all authentication-type password', expect_string=r']')
    print(output)
       
    print('###### Commiting changes to ' + dictionary['HOSTNAME'] + '. ######\n')
    output = net_connect.send_command('save force', expect_string=r']')
    print(output)

    end_time = datetime.now()
    
    print('\nTotal time: {}'.format(end_time - start_time) +'\n' + '#' * 60)
