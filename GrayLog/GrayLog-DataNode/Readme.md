# GrayLog using Data Node

This docker-compose file deploys a GrayLog using GrayLog Data Node instead of separately managed OpenSearch container. 

The architecture is composed of three services: 
* `graylog`: Provides the GrayLog web interface, APIs, Ingestion endpoints and the setup flow. 
* `mongodb`: stores the graylog metadata and configurations. 
* `datanode`: replaces a self-managed opensearch service and manages the GrayLog's search backend. 

The required files are: 
* `docker-compose.yaml` defines the services. 
* `.env`:  stores `GRAYLOG_PASSWORD_SECRET` and `GRAYLOG_ROOT_PASSWORD_SHA2` that the docker-compose file expects to be provided separately for security reasons. 

## Prerequisites 

GrayLog require for production to have docker and docker compose installed and set `vm.max_map_count` to at least `262144`: 
```bash
sudo sysctl -w vm.max_map_count=262144
```

To make the kernel setting persistent across reboots, add it to /etc/sysctl.conf or a file under /etc/sysctl.d/, then reload sysctl settings.


## Environmental variables

GrayLog requires a password secret and an SHA-256 hash for the root password, that is stored in the separated `.env` files. 
To generate them: 
```bash
# Generate the password secret
< /dev/urandom tr -dc A-Z-a-z-0-9 | head -c96 ; echo

# Genrate the root password hash
echo -n 'YourAdminPassword' | sha256sum | cut -d' ' -f1
```

# Deployment

Start the docker compose with: 
```bash
docker compose up -d
```
Docker container stage
```bash
docker compose ps
```

And to follow the logs during the start up: 
```bash
docker compose logs -f
```

## First login

For Data Node-based setups, Graylog starts with a preflight UI. The initial login details are printed in the GrayLog container logs the first time the stack starts: 
```bash
# Extract the graylog's container logs. 
docker compose logs graylog
```

After preflight provisioning, sign in with the root password whose SHA-256 hash you placed in `.env` as `GRAYLOG_ROOT_PASSWORD_SHA2`. 