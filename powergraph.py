#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Copyright (C) 2017 Unicamp-OpenPower
Licensed under the Apache License, Version 2.0 (the “License”);
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an “AS IS” BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

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
        if 'Instantaneous power reading' in a or 'timestamp' in a:
            print a.replace(' ', '')
    i+=1
    sleep(2)
