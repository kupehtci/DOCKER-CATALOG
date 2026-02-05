# OracleDB Docker

This folder contains a docker compose file that deploys a testing Oracle DB for developing. 

Also provides a `oracle_access.py` python script that checks the connection to the container from the local host and extract some DB information. 

## How to start

1. Start the docker compose for starting the DB: 
```bash
docker compose up
```

2. Test the DB with Python
```bash
# (optional) create python3 environment
 python3 -m venv .venv  
source ./.env/bin/activate

# Install oracledb module
pip install oracledb

# Run the script
python3 oracle_access.py
```

## Notes

The service name of the free OracleDB is `FREE`. 