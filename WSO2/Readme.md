# WSO2

WSO2 is an middleware platform that integrates API management, integrations, identity and access management (authentication and authorization) and streaming in a self-hosted platform. 

The API Management requires a relational database (In this case MySQL) for persistent state across restarts of the service. 

## How to authenticate

Once the services are up and running, in order to login into WSO2, enter `admin` for both username and password in `https://localhost:9443`.

# Docker compose file

This docker compose file sets an environment for WSO2 API Manager with the MySQL persistence.
It defines 2 services: `wso2-apim` as the WSO2 API Manager and `mysql` for the MySQL database.  

## WSO2 API Manager

Official WSO2 image for the API manager server. 
Exposes ports: 
* `9443`: WSO2 Management console. 
* `8243`: HTTPs gateway for API and browser testing. 
* `8280`: `HTTP gateway for API and browser testing.

Port `9743` its not exposed, as its only used for the health check and can be used for internal WSO2 API. 

Points to the MySQL host, port and credentials so the data source is automatically configured for data persistence. 

The volume `apim_conf` allows to mount custom configurations in TOML format at runtime. 

## MySQL

Using official MySQL image, configured for integrating it with WSO2, sets up a functional DB. 

Exposes ports: 
* `3306`: for external database access. 

Also configures initially the database, setting the root password and creating wso2_db database for this service. 

The volume `mysql_data` persist the database files. 

Healthcheck is configured to ping the MySQL each 30s to confirm that the DB is ready.

