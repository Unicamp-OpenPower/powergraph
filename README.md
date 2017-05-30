# PowerGraph

A simple tool to analyse the energy use of a server trought IPMI.

## Requirements
To use this software, you'll have to install ```ipmitool``` and ```python 2.7```.
Besides, you can install all the python dependencies running pip as it follows:

```
 sudo pip install -r requirements.txt
```

## Running
In order to run the script, use ```python 2.7``` as it follows:

```
python2.7 powergraph.py --host="server address" --port="server port" --user="allowed user" --passwd="password for this user"
```
You can use the optional parameter ```--store``` in order to save
the infos as json on tinydb. Without this parameter, the script will
print on the terminal. Besides, you can use ```--feedback``` with store
in order to see the measures status. If you want to set the time interval that a new csv file is 
generated, you can use the flag ```--csv_interval```. The 
```--tail_length``` is used to set the number of lines the csv
file will have.

Run ```csvcreator.py``` like this:

```
python2.7 csvcreator.py --jsonfile="generated_json_name"
```

There are two optional arguments: ```--date```, to create the csv only with
the data from a specific day and ```--name```, with the name you want your
```csv``` file.

The ```graph_csv.py``` runs the ```powergraph.py``` and, from time
to time, creates a new csv file, with the latest measures. To run it,
type:

```
python2.7 graph_csv.py --host="server address" --port="server port" --user="allowed user" --passwd="password for this user 
--jsonfile="path to bd jsonfile"
```

Besides, you can use the following optional arguments:
- interval: interval between each ipmi measure (default=10)
- nread: number of ipmi measures to be done (default=infinity)
- csv_interval: interval that a new csv file is made (deafult=300s)
- tail_length: size of the csv files (default=300)
