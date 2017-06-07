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

import json
import csv
import sys
import argparse
import datetime
from tinydb import TinyDB, Query
from argparse import RawTextHelpFormatter


def getalltables(json_file):
    """
    Return a list of all tables in a json file.
    """
    tables = openjson(json_file).keys()
    tables.remove('_default')
    return tables


def openjson(json_file):
    """
    Opens the Json file.
    """
    if str(json_file).endswith('.json'):
        with open(json_file) as data_file:
            data = json.load(data_file)
        return data
    else:
        print 'Select the correct file and try again.'
        sys.exit(1)


def readdbtable(json_file_data, table_name):
    """
    Reads the table form the json file and returns
    a combinaton of two lists as rows of a table.
    """
    db = json_file_data[table_name]
    dbdict = {}
    timedict = {}
    timelist = list()
    wattslist = list()

    # Creates two dictionaries:
    # 1: execution_number -> time (e.g: 1, 13:01:45)
    # 2: time -> watts (e.g: 13:01:45, 300)
    for read in db:
        dbdict[int(read)] = str(db[read]['time'])
        timedict[str(db[read]['time'])] = int(db[read]['watts'])

    # Creates two separeted lists that will be the coluns in
    # the csv file. One is for the time and another for the
    # watts
    timelist.append('date')
    wattslist.append('consumption')
    for iten in dbdict:
        # print iten, dbdict[iten], timedict[dbdict[iten]]
        timelist.append(dbdict[iten])
        wattslist.append(timedict[dbdict[iten]])

    # Merge both lists
    rows = zip(timelist, wattslist)
    return rows


def createcsv(csv_file_name, data):
    """
    Creates the csv file.
    """
    try:
        with open(csv_file_name + '.csv', 'wb') as finalcsv:
            wr = csv.writer(finalcsv, quoting=csv.QUOTE_ALL)
            for row in data:
                wr.writerow(row)
    except IOError as e:
        print "I/O error({0}): {1}".format(e.errno, e.strerror)


def validate(date):
    """
    Validates the format of the date set by user.
    """
    try:
        datetime.datetime.strptime(date, '%Y%m%d')
    except ValueError:
        raise ValueError('wrong date format, should be YYYYMMDD (e.g 2017513)')
        sys.exit(1)


def table_exists(input_date, all_tables):
    """
    Verifies if a date set by user (which is the name of the table) is
    present in the list of tables.
    """
    if input_date in all_tables:
        return True
    else:
        print '\n    ERROR: Could not find the date in the database.'
        print '    Available dates: ' + ', '.join(all_tables) + '.'
        return False


def get_input():
    """
    Reads the user input from command execution
    """
    program_shortdesc = '''

    --- csv file generator (cfg) for the powergraph ---

    This auxiliary tools creates a csv file from the ouput generated
    by the powergraph tool which can be used as input for several
    tools like OpenOffice or Microsoft Office for visual graphics
    generation.
    '''
    parser = argparse.ArgumentParser(description=program_shortdesc,
                                     formatter_class=RawTextHelpFormatter)
    parser.add_argument('--name',
                        help='the name of the cvs file'
                        '\ne.g: --name=mycsv creats mycsv.csv')
    parser.add_argument('--date',
                        help='the date where the data was collected'
                        '\ne.g --date=2017513 will create a csv for the'
                        '\nmeasurement collected at May, 13 2017')
    parser.add_argument('--jsonfile', help='the .json database',
                        required=True)
    args = parser.parse_args()
    return args, parser


def main():
    """
    Main execution.
    """
    try:
        json_file = get_input()[0].jsonfile
        name = get_input()[0].name
        date = get_input()[0].date
        alltables = getalltables(json_file)

        # user sets all parameters
        if name and date:
            validate(date)
            if table_exists(date, alltables):
                createcsv(name, readdbtable(openjson(json_file), date))
        # user sets only the date
        elif not name and date:
            if table_exists(date, alltables):
                validate(date)
                createcsv(date, readdbtable(openjson(json_file), date))
        # user set only the name
        elif name and not date:
            for table in getalltables(json_file):
                createcsv(name, readdbtable(openjson(json_file),
                          str(table)))
        # user does not set any optional parameter
        else:
            for table in alltables:
                createcsv(str(table), readdbtable(openjson(json_file),
                                                  str(table)))
    except KeyboardInterrupt:
        print "\nExecution cancelled. Bye!"
        sys.exit(1)


if __name__ == "__main__":
    """
    Invoking the main execution function.
    """
    main()
