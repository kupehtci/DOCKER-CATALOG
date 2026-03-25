# SonarQube

SonarQube is a platform for continuous code quality analisis to detect bugs, vulnerabilities, code smells and security issues.
This service is under `/ProductionReady` folder as configured with an external **PostgreSQL** DB that maintain data persistency for production environments.  

## SonarQube documentation

Take a look into my own documentation about SonarQube at Github:  [SonarQube Documentation](https://github.com/kupehtci/DOCUMENTATION/tree/main/SonarQube)

## How to start

In order to start the SonarQube service: 
```bash
docker compose up -d
```

And then open the browser at `http://localhost:9000`

## Docker compose file

The docker compose file runs a SonarQube service using `sonarqube:community` together with a production ready Database.  

SonarQube requires **ports**: 
* `9000`: maps port 9000 to port 9000 inside the container for the SonarQube web interface

The docker mounts the following **volumes**: 
* sonarqube_data → /opt/sonarqube/data for database files and configuration data
* sonarqube_logs → /opt/sonarqube/logs for application logs
* sonarqube_extensions → /opt/sonarqube/extensions for plugins and custom extensions

### Database

By default, SonarQube doesn't require a DB for development, as runs an internal H2. 
For production environments, a Database is required, being PostgreSQL the most recommended and most suitable choice. 

The DB service mounts a lightweight alpine PostgreSQL version `postgres:16-alpine` for efficiency. 
It mounts a **volume** `postgres_data` for data persistency of the DB contents.
It configures a **healthcheck** over `pg_isready` every 10 seconds to check if the database is ready. 

Its also configured to **automatically restart** unless is manually stopped. 

#### Credentials

The credentials in the docker file needs to be configured equally in: 
* `SONAR_JDBC_USERNAME` and `SONAR_JDBC_PASSWORD` in SonarQube service. 
* `POSTGRES_DB`, `POSTGRES_USER` and `POSTGRES_PASSWORD` in PostgreSQL service. 

> Note!: Change `sonar_password` in production for a more suitable password for the DB. 