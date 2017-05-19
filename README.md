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
print on the terminal.

Run ```csvcreator.py``` like this:

```
python2.7 csvcreator.py --jsonfile="generated_json_name"
```
