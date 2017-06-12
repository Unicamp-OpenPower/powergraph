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

import os.path
import sys
import time
import subprocess
import argparse
from tinydb import TinyDB, Query

INTERVAL = 10
NREAD = 10
INFINITY = False
STORE = False


def savedb(input):
    """
    Save the execution results in a nosql db. Each new day is represented by a
    table.
    """
    db = TinyDB('powerdata.json')
    table = db.table(input[1].replace('/', ''))
    # exec  date    time    watts
    # ['2', '2017/5/12', '23:30:22', '707']
    # we ignore the execution counter and date, given date is the table name
    table.insert({'time': input[2], 'watts': input[3]})
    db.close()


def create_string(iteration, dic):
    """
    Pretty print the output of the IPMI execution
    """
    return str(iteration) + '|' + dic['Year'] + '/' + \
        get_month_number(dic['Month']) + '/' + \
        dic['Day'] + '|' + dic['Hour'] + ':' + \
        dic['Min'] + ':' + dic['Seg'] + '|' + \
        dic['Energy']


def formated_print(dic):
    """
    Pretty print the output of the IPMI execution
    """
    print dic['Year'] + '/' + get_month_number(dic['Month']) + '/' + \
        dic['Day'] + ' | ' + dic['Hour'] + ':' + dic['Min'] + ':' + \
        dic['Seg'] + ' | ' + dic['Energy'] + ' Watts'


def get_month_number(month):
    """
    Return the month as int based its name
    """
    mDict = {'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6,
             'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12}
    if month in mDict:
        return str(mDict[month])
    else:
        return 'Month not find.'


def execute_stdout(command):
    """ Execute a command with its parameter and return the exit code
    and the command output """
    try:
        output = subprocess.check_output([command], stderr=subprocess.STDOUT,
                                         shell=True)
        return 0, output
    except subprocess.CalledProcessError as excp:
        return excp.returncode, excp.output


def get_input():
    """
    Reads the user input from command execution
    """
    parser = argparse.ArgumentParser(description='Parameters')
    parser.add_argument('--host', help='adress of the host')
    parser.add_argument('--port', help='port of IPMI host')
    parser.add_argument('--user', help='user allowed to acces IPMI')
    parser.add_argument('--passwd', help='password for the specific user')
    parser.add_argument('--interval', help='seconds between each data reading')
    parser.add_argument('--nread', help='number of time to collect data')
    parser.add_argument('--store', action='store_true',
                        help='save the data collected in a nosql db')
    args = parser.parse_args()
    return args, parser


def build_command(args, parser):
    """
    Build the string of the IPMI command for execution
    """
    cmd = "ipmitool -I lanplus"
    if not args.host:
        print "\nERROR: hostname is required.\n"
        parser.print_help()
        sys.exit(1)
    else:
        cmd += ' -H ' + args.host
    if args.port:
        cmd += ' -p ' + args.port
    if not args.user:
        print "\nERROR: username is required.\n"
        parser.print_help()
        sys.exit(1)
    else:
        cmd += ' -U ' + args.user
    if args.passwd:
        cmd += ' -P ' + args.passwd
    cmd += ' dcmi power reading'
    if args.interval:
        global INTERVAL
        INTERVAL = args.interval
    if args.nread:
        global NREAD
        NREAD = args.nread
    else:
        global INFINITY
        INFINITY = True
    if args.store:
        global STORE
        STORE = True
    return cmd


def run(command, counter):
    """
    Parsers the result of the command execution
    """
    result = execute_stdout(command)
    aux = result[1].split('\n')
    for count, entry in enumerate(aux):
        if 'Instantaneous power reading' in entry:
            energy = entry.replace(' ', '').split(':')[1]
            energy = energy.replace('Watts', '')
        elif 'timestamp' in entry:
            aux = entry.replace(' ', '').split(':')
            aux = aux[1:len(aux)]
            infos = {}
            infos['Week'] = aux[0][0:3]
            infos['Month'] = aux[0][3:6]
            infos['Day'] = aux[0][6:8]
            infos['Hour'] = aux[0][8:10]
            infos['Min'] = aux[1]
            infos['Seg'] = aux[2][0:2]
            infos['Year'] = aux[2][2:6]
            infos['Energy'] = energy
            info = create_string(counter + 1, infos)
            if not STORE:
                print info
            else:
                savedb(info.split('|'))


def run_ipmi(command):
    """
    Run IPMI command.
    """
    if not cmd_exists(command):
        print "existe"
    else:
        print "não existe"

    try:
        nread_counter = 0
        if INFINITY:
            while 1:
                run(command, nread_counter)
                nread_counter += 1
                time.sleep(float(INTERVAL))
        else:
            while int(nread_counter) < int(NREAD):
                run(command, nread_counter)
                nread_counter += 1
                time.sleep(float(INTERVAL))
    except KeyboardInterrupt:
        print "\nExecution cancelled. Bye!"
        sys.exit(1)

def cmd_exists(command):
    subp = subprocess.call("type " + command, shell=True,
			stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return subp == 0

def main():
    """
    Main execution.
    """
    run_ipmi(build_command(get_input()[0], get_input()[1]))


if __name__ == "__main__":
    """
    Invoking the main execution function.
    """
    main()
