#powergraph

A simple tool to analyse the energy use of a server trought IPMI.

## Requirements
To use this software, you'll have to install ```ipmitool``` and ```python 2.7```.
Besides, you can install all the python dependencies running pip as it follows:

```
pip install -r requirements.txt
```

## Running
In order to run the script, use ```python 2.7``` as it follows:

```
python2.7 powergraph.py --host="server address" --port="server port" --user="allowed user" --passwd="password for this user"
```
