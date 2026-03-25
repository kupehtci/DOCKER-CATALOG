# SonarQube Hardened

SonarQube is a platform for continuous code quality analisis to detect bugs, vulnerabilities, code smells and security issues.
SonarQube hardened image is a secure container image that reduce vulnerabilities by not containing unnecesary components and not having elevated priviledges.

## SonarQube documentation

Take a look into my own documenation about SonarQube at Github:  [SonarQube Documentation](https://github.com/kupehtci/DOCUMENTATION/tree/main/SonarQube)

## How to start

In order to start the SonarQube service: 
```bash
docker compose up -d
```

And then open the browser at `http://localhost:9000`

> Note!: Requires to be authenticated into dhi.io with `docker login dhi.io`

## Docker compose file

The docker compose file runs a SonarQube service using `dhi.io/sonarqube:26-debian13-dev` hardened image. 

SonarQube requires **ports**: 
* `9000`: maps port 9000 to port 9000 inside the container for the SonarQube web interface

Environment requires `SONAR_ES_BOOTSTRAP_CHECKS_DISABLE` to be enabled in order to avoid elasticsearch bootstrap checks in environments with no elevated priviledges like in this case with a hardened image. 

The docker mounts the following **volumes**: 
* sonarqube_data → /opt/sonarqube/data for database files and configuration data
* sonarqube_logs → /opt/sonarqube/logs for application logs
* sonarqube_extensions → /opt/sonarqube/extensions for plugins and custom extensions