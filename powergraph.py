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

import sys
import time
import subprocess
import argparse

INTERVAL = 10
NREAD = 10


def formated_print(dic):
    """
    Pretty print the output of the IPMI execution
    """
    print dic['Year'] + '/' + get_month_numner(dic['Month']) + '/' + \
        dic['Day'] + ' | ' + dic['Hour'] + ':' + dic['Min'] + ':' + \
        dic['Seg'] + ' | ' + dic['Energy'] + ' Watts'


def get_month_numner(month):
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
    parser = argparse.ArgumentParser(description='IPMI Parameters')
    parser.add_argument('--host', help='adress of the host')
    parser.add_argument('--port', help='port of IPMI host')
    parser.add_argument('--user', help='user allowed to acces IPMI')
    parser.add_argument('--passwd', help='password for the specific user')
    parser.add_argument('--interval', help='interval between data reading')
    parser.add_argument('--nread', help='number of time to collect data')
    args = parser.parse_args()
    return args, parser


def build_command(args, parser):
    """
    Build the string of the IPMI command for execution
    """
    cmd = "sudo ipmitool -I lanplus"
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
    return cmd


def run_ipmi(command):
    nread_counter = 0
    try:
        while int(nread_counter) < int(NREAD):
            result = execute_stdout(command)
            aux = result[1].split('\n')
            print str(nread_counter + 1) + ' |',
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
                    formated_print(infos)
            nread_counter += 1
            time.sleep(float(INTERVAL))
    except KeyboardInterrupt:
        print "\nExecution cancelled. Bye!"
        sys.exit(1)


def main():
    run_ipmi(build_command(get_input()[0], get_input()[1]))


if __name__ == "__main__":
    """
    Invoking the main exection function.
    """
    main()
