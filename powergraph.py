# -*- coding: utf-8 -*-

import subprocess
from time import sleep
import argparse

def execute_stdout(command):
    """ Execute a command with its parameter and return the exit code
    and the command output """
    try:
        output = subprocess.check_output([command], stderr=subprocess.STDOUT,
                                         shell=True)
        return 0, output
    except subprocess.CalledProcessError as excp:
        return excp.returncode, excp.output


parser = argparse.ArgumentParser(description='Parameters for IPMI')
parser.add_argument('--host', help='adress of the host')
parser.add_argument('--port', help='port of IPMI host')
parser.add_argument('--user', help='user allowed to acces IPMI')
parser.add_argument('--passwd', help='password for the specific user')
args = parser.parse_args()

i=0
while i < 10:    
    command = 'sudo ipmitool -I lanplus -H '+args.host+' -p '+args.port+' -U '+args.user+' -P '+args.passwd+' dcmi power reading'
    result = execute_stdout(command)
    aux = result[1].split('\n')
    print
    for b, a in enumerate(aux):
        if 'Instantaneous power reading' in a: 
            aux = a.replace(' ', '').split(':')[1].replace('Watts','')
            print aux
        elif 'timestamp' in a:
            aux = a.replace(' ', '').split(':')
            aux = aux[1:len(aux)]
            
            infos = {}
            infos['Week'] = aux[0][0:3]
            infos['Month'] = aux[0][3:6]
            infos['Day'] = aux[0][6:8]
            infos['Hour'] = aux[0][8:10]
            infos['Min'] = aux[1]
            infos['Seg'] = aux[2][0:2]
            infos['Year'] = aux[2][2:6]
            print infos


    i+=1
    sleep(2)
