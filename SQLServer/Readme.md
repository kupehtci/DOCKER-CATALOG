# SQL Server

This section contains a Docker Compose file to launch an development ready SQL Server and a python script for testing the connection. 

The official Microsoft's docker image can be found in [Docker Hub](https://hub.docker.com/r/microsoft/mssql-server).

## Python script

The python script allows a quick check and reference of how to connect to the database. 
A python environment is configured, so you can use it to get the neccesary modules for executing the script or import the modules manually

In order to use the python script: 
```bash
# 1. Enable the pre-configured environment
source .venv/bin/activate

# 2. If doesnt want to use the environment, install the necessary modules
pip install pyodbc

# 3. Execute the script
python3 sqlserver_test.py
# Example output:
# python sqlserver_test.py 
# ('Microsoft SQL Server 2025 (RTM-CU1) (KB5078298) - 17.0.4006.2 (X64) \n\tJan 22 2026 18:05:52 \n\tCopyright (C) 2025 Microsoft Corporation\n\tEnterprise Developer Edition (64-bit) on Linux (Ubuntu 24.04.3 LTS) <X64>',)
```

## MacOS errors

MacOS requires some drivers to be installed in order to execute msql commands:
```bash
brew tap microsoft/mssql-release https://github.com/Microsoft/homebrew-mssql-release

brew update

# install required formulas
HOMEBREW_ACCEPT_EULA=Y brew install msodbcsql17 mssql-tools18 unixodbc

# Check drivers installed, verify that Driver 17 is available
odbcinst -q -d 
# Example output: 
#[ODBC Driver 17 for SQL Server]
#[ODBC Driver 18 for SQL Server]
```

## Versions

By default, the version of the container image is settled to `2025-latest` being the most recent one updated. 
If desired, use `latest` as the docker image version. 

