# PostgreSQL


## Docker Compose file

This configuration deploys PostgreSQL 16-alpine in a container named `postgresql`.

Exposed **ports**
* Port `5432` mapped to internal `5432` port for DB connection. 

Configured **volumes**:
* postgres_data → /var/lib/postgresql/data for persistent database storage

Configured a **healthcheck** using pg_isready each 10s with 5 retries. 
Configured an **Auto-restart policy** unless is manually stopped. 

### Configuration: 

Configure the following environmental variables: 
* `POSTGRES_DB`: Creates database 
* `POSTGRES_USER`: Database user
* `POSTGRES_PASSWORD`: Database password

## How to start

Launch the service. 
```bash
docker compose up -d 
```

Connect to test:
```bash
docker exec -it sonarqube-db psql -U sonar -d sonarqube
```

Or even: 
```bash
docker debug postgresql
```