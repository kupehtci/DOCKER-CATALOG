# SQL Server

This section contains a Docker Compose file to launch an development ready Mongo DB. 

## Python script

The python script allows to test the connection to the MongoDB container. 

The script just generates a connection URI composed of the credentials and the database name, pings the server, list the available databases and insert + queries a single document. 

> Note! set the credentials in the script the same as the Container's ones. 

To execute the python script: 
```bash
pip install pymongo
python3 mongo_test.py
```

Or either use environment: 
```bash
python3 -m venv .venv
source ./.venv/bin/activate
pip install pymongo
python3 mongo_test.py
```



 

