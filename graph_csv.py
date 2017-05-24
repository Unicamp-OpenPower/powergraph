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
import argparse
import thread
import time
import os

INTERVAL = 10

def build_commands(args):
    """
    function used to build the ipmi and csv commands
    """
    year = time.strftime("%Y")
    month = int(time.strftime("%m"))
    day = int(time.strftime("%d")) 
    date=str(year)+str(month)+str(day)
    
    csv_command = 'python2.7 csvcreator.py --name=last --date='+date+' --jsonfile='
    csv_command = csv_command + args.jsonfile
    
    ipmi_command = 'python2.7 powergraph.py'
    if not args.host:
        print "\nERROR: hostname is required.\n"
        parser.print_help()
        sys.exit(1)
    else:
        ipmi_command += ' --host='+args.host
    if args.port:
        ipmi_command += ' --port='+args.port
    if not args.user:
        print "\nERROR: username is required.\n"
        parser.print_help()
        sys.exit(1)
    else:
        ipmi_command += ' --user='+args.user
    if args.passwd:
        ipmi_command += ' --passwd='+args.passwd
    if args.interval:
        ipmi_command += ' --interval='+args.interval
    else:
        ipmi_command += ' --interval=1'
    ipmi_command += ' --store'
    
    return ipmi_command,csv_command

def get_input():
    """
    function to get the arguments from the user
    """
    parser = argparse.ArgumentParser(description='Parameters')
    
    parser.add_argument('--host', help='adress of the host')
    parser.add_argument('--port', help='port of IPMI host')
    parser.add_argument('--user', help='user allowed to acces IPMI')
    parser.add_argument('--passwd', 
                        help='password for the specific user')
    parser.add_argument('--interval', 
                        help='seconds between each data reading')
    parser.add_argument('--nread', 
                        help='number of time to collect data')
    
    parser.add_argument('--jsonfile',
                        help='jsonfile to be converted as csv')
    return parser.parse_args()

def run_collector(command):
    """
    function to run the collection of data
    """
    os.system(command)

def run_csv(command):
    """
    function to run the csv generator 
    """
    while 1:
        time.sleep(300)
        os.system(command)
        os.system("tail -n 300 last.csv > aux.csv")
        os.system("mv aux.csv last.csv")

args = get_input()
ipmi_command, csv_command = build_commands(args)

thread.start_new_thread(run_collector,(ipmi_command,))
thread.start_new_thread(run_csv,(csv_command,))

while 1:
    pass
