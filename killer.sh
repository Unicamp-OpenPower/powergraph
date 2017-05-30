#!/bin/bash

#script made to make sure the ipmi data collector is running.
#used alongside with crontab

#name of the process that can be running to get data
threads=('powergraph.py' 'graph_csv.py')

#get size of the threads array
size=$(echo ${#threads[@]})
size=$(echo "$size-1" | bc)

for i in $(seq 0 $size); do
    #if the number of procees running are only one, so its the grep itself
    #and nedd to be restarted
    ps_size=$(ps aux | grep ${threads[i]} | wc -l)
    if [ "$ps_size" == 1 ]; then
        for i in $(seq 0 $size); do
            for pid in $(pgrep -f ${threads[i]}); do
                kill $pid
            done
        done
        #comando to launch the data getter again
        python2.7 graph_csv.py --host='<YOUR_HOST>' --port='<YOUR_PORT>' \
            --user='<YOUR_USER>' --passwd='<YOUR_PASS'> \
            --interval=1 --jsonfile=powerdata.json &
    fi
done
