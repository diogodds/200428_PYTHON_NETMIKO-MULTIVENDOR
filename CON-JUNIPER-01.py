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
password = getpass.getpass()


########################################################################
    

with open('CON-JUNIPER-01.txt') as file: # This opens the text file with the BGP parameters in csv format
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
    
    net_connect = ConnectHandler(device_type='juniper_junos', ip=dictionary['IP'], username=username, password=password, global_delay_factor=2.0)
  
    print('Connected to ' + dictionary['HOSTNAME'] + '. Applying configuration script.')
    
    net_connect.send_command('\n')
    net_connect.send_command('configure', expect_string=r'#')
    output = net_connect.send_command('set system root-authentication plain-text-password', expect_string=r'word:')
    print('Changing password for root user')
    output = net_connect.send_command(dictionary['SECRET'], expect_string=r'word:')
    print(output)
    output = net_connect.send_command(dictionary['SECRET'], expect_string=r'#')
    print(output)
    print('###### Deleting old TACACS+ servers 10.160.18.57 and 10.160.19.14. ######\n')
    output = net_connect.send_command('delete system tacplus-server 10.160.18.57', expect_string=r'#')
    output = net_connect.send_command('delete system tacplus-server 10.160.19.14', expect_string=r'#')
    print('###### Deleting ZALANDOAMIN user. ######\n')
    output = net_connect.send_command('del system login user zalandoadmin', expect_string=r'#')
    print('###### Creating MANAGER local-user and setting up a password for it ###### \n')
    output = net_connect.send_command('set system login user manager uid 2000', expect_string=r'#')
    output = net_connect.send_command('set system login user manager class super-user', expect_string=r'#')
    output = net_connect.send_command('set system login user manager authentication plain-text-password', expect_string=r'word:')
    output = net_connect.send_command(dictionary['SECRET'], expect_string=r'word:')
    print(output)
    output = net_connect.send_command(dictionary['SECRET'], expect_string=r'#')
    print(output)    
    output = net_connect.send_command('show | compare', expect_string=r'#')
    print(output)

    print('###### Commiting changes to ' + dictionary['HOSTNAME'] + '. ######\n')

    output = net_connect.commit()
    print(output)

  
    end_time = datetime.now()
    
    print('\nTotal time: {}'.format(end_time - start_time) +'\n' + '#' * 60)