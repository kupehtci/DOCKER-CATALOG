# GrayLog using Data Node

This docker-compose file deploys a GrayLog using GrayLog Data Node instead of separately managed OpenSearch container. 

The architecture is composed of three services: 
* `graylog`: Provides the GrayLog web interface, APIs, Ingestion endpoints and the setup flow. 
* `mongodb`: stores the graylog metadata and configurations. 
* `datanode`: replaces a self-managed opensearch service and manages the GrayLog's search backend. 

The required files are: 
* `docker-compose.yaml` defines the services. 
* `.env`:  stores `GRAYLOG_PASSWORD_SECRET` and `GRAYLOG_ROOT_PASSWORD_SHA2` that the docker-compose file expects to be provided separately for security reasons. It is not committed; create it from `.env.example` (see [Environmental variables](#environmental-variables)).
* `.env.example`: commented template of the `.env` file. 

## Prerequisites 

GrayLog require for production to have docker and docker compose installed and set `vm.max_map_count` to at least `262144`: 
```bash
sudo sysctl -w vm.max_map_count=262144
```

To make the kernel setting persistent across reboots, add it to /etc/sysctl.conf or a file under /etc/sysctl.d/, then reload sysctl settings.


## Environmental variables

The docker-compose file reads two values from a `.env` file placed next to it. That file is git-ignored, so create it from the template:
```bash
cp .env.example .env
```

| Variable | Used by | What it is for | What to put |
|---|---|---|---|
| `GRAYLOG_PASSWORD_SECRET` | `graylog` and `datanode` | Shared secret. Graylog uses it to encrypt/salt sensitive data stored in MongoDB (stored credentials, tokens, sessions) and the Data Node uses it to authenticate against the Graylog server. It is **not** a login password. | A random string, letters and digits, at least 16 characters (64-96 recommended). |
| `GRAYLOG_ROOT_PASSWORD_SHA2` | `graylog` | Password of the built-in `admin` user, used to log in to the web UI and the REST API after the preflight setup. | The SHA-256 hash (64 hex characters) of the password you choose, **never the plain password**. |

To generate them: 
```bash
# Generate the password secret (96 random characters)
< /dev/urandom LC_ALL=C tr -dc 'A-Za-z0-9' | head -c96 ; echo
```
```bash
# Generate the root password hash on Linux (-n avoids hashing the trailing newline)
echo -n 'YourAdminPassword' | sha256sum | cut -d' ' -f1
```
```bash
# Generate the root password hash on macOS
echo -n 'YourAdminPassword' | shasum -a 256 | cut -d' ' -f1
```

The resulting `.env` looks like this:
```
GRAYLOG_PASSWORD_SECRET=<random-string-of-96-characters>
GRAYLOG_ROOT_PASSWORD_SHA2=<sha256-hash-of-the-admin-password>
```

Notes:
* `GRAYLOG_PASSWORD_SECRET` must be the same for `graylog` and `datanode` (the compose file already passes the same variable to both). Do not change it after the first start: data encrypted with the old value becomes unreadable and the Data Node can no longer connect, so changing it means removing the volumes (`docker compose down -v`).
* `GRAYLOG_ROOT_PASSWORD_SHA2` can be changed at any time: update the hash and recreate the container with `docker compose up -d graylog`.

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