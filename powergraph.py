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
    return args


def build_command(args):
    """
    Build the string of the IPMI command for execution
    """
    cmd = "sudo ipmitool -I lanplus"
    if not args.host:
        print "Please, hostname is required."
        sys.exit(1)
    else:
        cmd += ' -H ' + args.host
    if args.port:
        cmd += ' -p ' + args.port
    if not args.user:
        print "Please, username is required."
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
            print "\nExecution number: " + str(nread_counter + 1)
            for b, a in enumerate(aux):
                if 'Instantaneous power reading' in a or 'timestamp' in a:
                    print a.replace(' ', '')
            nread_counter += 1
            time.sleep(float(INTERVAL))
    except KeyboardInterrupt:
        print "\nExecution cancelled. Bye!"
        sys.exit(1)


def main():
    run_ipmi(build_command(get_input()))


if __name__ == "__main__":
    """
    Invoking the main exection function.
    """
    main()
