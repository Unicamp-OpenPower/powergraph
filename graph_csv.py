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
PYTHON_VERSION = 'python2.7'

def build_commands(args):
    """
    function used to build the ipmi and csv commands
    """
    year = time.strftime("%Y")
    month = int(time.strftime("%m"))
    day = int(time.strftime("%d")) 
    date=str(year)+str(month)+str(day)
    
    csv_command = PYTHON_VERSION + ' csvcreator.py --name=last --date=' + date + \
            ' --jsonfile='
    csv_command = csv_command + args.jsonfile
    
    if args.csv_interval:
        global CSV_INTERVAL 
        CSV_INTERVAL = args.csv_interval
    else:
        CSV_INTERVAL = 300

    powergraph_command = PYTHON_VERSION + ' powergraph.py'
    if not args.host:
        print "\nERROR: hostname is required.\n"
        parser.print_help()
        sys.exit(1)
    else:
        powergraph_command += ' --host=' + args.host
    if args.port:
        powergraph_command += ' --port=' + args.port
    if not args.user:
        print "\nERROR: username is required.\n"
        parser.print_help()
        sys.exit(1)
    else:
        powergraph_command += ' --user=' + args.user
    if args.passwd:
        powergraph_command += ' --passwd=' + args.passwd
    if args.interval:
        powergraph_command += ' --interval=' + args.interval
    else:
        powergraph_command += ' --interval=1'
    powergraph_command += ' --store'
    
    return powergraph_command,csv_command

def get_input():
    """
    function to get the arguments from the user
    """
    parser = argparse.ArgumentParser(description='Parameters')
    
    parser.add_argument('--host', 
                        help='adress of the host', required=True)
    parser.add_argument('--port', 
                        help='port of IPMI host', required=True)
    parser.add_argument('--user',
                        help='user allowed to acces IPMI', required=True)
    parser.add_argument('--passwd', 
                        help='password for the specific user', required=True)
    parser.add_argument('--interval', 
                        help='seconds between each data reading')
    parser.add_argument('--nread', 
                        help='number of time to collect data')
    
    parser.add_argument('--jsonfile',
                        help='jsonfile to be converted as csv', required=True)
    parser.add_argument('--csv_interval',
                        help='interval you want to create a new csv file')
    parser.add_argument('--tail_length',
                        help='the amount of inputs do get from the csv file '
                        'in order to create the input for the graphic '
                        'visualization',
                        default=300)

    return parser.parse_args()

def run_collector(command):
    """
    function to run the collection of data
    """
    try:
        os.system(command)
    except OSError as err:
        print ("OS erros: {0}".format(err))


def run_csv(command,tail_length):
    """
    function to run the csv generator 
    """
    while True:
        time.sleep(float(CSV_INTERVAL))
        try:
            os.system(command)
            os.system("tail -n 300 last.csv > aux.csv")
            os.system("mv -f aux.csv last.csv")
        except OSError as err:
            print("OS error: {0}".format(err))

def main():
    """
    Main execution.
    """
    args = get_input()
    powergraph_command, csv_command = build_commands(args)
    thread.start_new_thread(run_collector, (powergraph_command,))
    thread.start_new_thread(run_csv, (csv_command, args.tail_length, ))
    try:
        while True:
            pass
    except (KeyboardInterrupt, SystemExit):
        print "\nExecution cancelled. Bye!"
        sys.exit(1)


if __name__ == "__main__":
    """
    Invoking the main execution function.
    """
    main()

