# SonarQube

SonarQube is a platform for continuous code quality analisis to detect bugs, vulnerabilities, code smells and security issues.
This service is under `/DevelopmentReady` folder as its not hardened or either configured with an external DB for production environments. 
For production, use `ProductionReady` docker file.

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

This `DevelopmentReady` SonarQube service doesn't require an external DB, as it will use the built-in H2 database suitable for development.
For production, use `ProductionReady` docker file. 