# MySQL

MySQL is a relational database that uses SQL to query and modify data.

This section contains a Docker Compose file to launch a development-ready MySQL 8.0 database and a Python script to test the connection once it is deployed.

The official Docker image can be found in [Docker Hub](https://hub.docker.com/_/mysql).

## Docker Compose file configuration

The `docker-compose.yaml` file defines a single `mysql` service with:

* The `mysql:8.0` image.
* Port `3306` exposed on the host.
* A named volume (`mysql_data`) to persist data.
* A healthcheck based on `mysqladmin ping`.
* The `mysql_native_password` authentication plugin, for compatibility with older clients.
* An empty SQL mode (see [SQL Mode](#sql-mode)).

### Variables

| Variable | Default value | Description |
|---|---|---|
| MYSQL_ROOT_PASSWORD | root | Password of the `root` user |
| MYSQL_DATABASE | example | Database created on first start-up |

By default, the `example` database is created. Rename it to suit your needs.

To authenticate, use the `root` user and the password set in `MYSQL_ROOT_PASSWORD`.

> Note! These variables are only applied the first time the container starts with an empty volume. If you change them later, remove the volume (`docker compose down -v`) so they take effect.

Optionally, a non-root user can be created on first start-up by adding these variables:

```yaml
environment:
  MYSQL_USER: app
  MYSQL_PASSWORD: ChangeThisPassword
```

That user is granted full privileges on `MYSQL_DATABASE`.

### Exposed ports

| Port | Usage |
|---|---|
| 3306 | MySQL client connections |

Connection string example:
```text
mysql://root:root@localhost:3306/example
```

## Start the service

```bash
docker compose up -d
```

Check the status (wait until it shows `healthy`):

```bash
docker compose ps
```

Open a MySQL shell inside the container:

```bash
docker compose exec mysql mysql -uroot -proot example
```

Run a quick query from the host:

```bash
docker compose exec mysql mysql -uroot -proot -e "SELECT VERSION(); SHOW DATABASES;"
```

## Volumes

Data is stored in the Docker volume `mysql_data`, mounted in `/var/lib/mysql`.

To inspect it:

```bash
docker volume ls
docker volume inspect mysql_mysql_data
```

> The volume name is prefixed with the Compose project name (by default, the folder name).

Databases persist even if the container is stopped or recreated.

## Common operations

View logs
```bash
docker compose logs -f mysql
```

Stop the service and keep data
```bash
docker compose down
```

Remove container and data
```bash
docker compose down -v
```

This deletes all databases stored in MySQL.

Back up a database
```bash
docker compose exec mysql mysqldump -uroot -proot example > example_backup.sql
```

Restore a database
```bash
docker compose exec -T mysql mysql -uroot -proot example < example_backup.sql
```

## Python script

The `mysql_test.py` script allows a quick check, and serves as a reference, of how to connect to the database.

The script connects to the database, prints the server version, lists the available databases, creates a `test` table (if it does not exist), inserts a row and queries it.

> Note! The credentials in the script match the ones in `docker-compose.yaml`. If you change them, either edit the script or override them with the environment variables `MYSQL_HOST`, `MYSQL_PORT`, `MYSQL_USER`, `MYSQL_PASSWORD` and `MYSQL_DATABASE`.

To execute the Python script:
```bash
pip install -r requirements.txt
python3 mysql_test.py
```

Or use a virtual environment:
```bash
python3 -m venv .venv
source ./.venv/bin/activate
pip install -r requirements.txt
python3 mysql_test.py
```

Example output:
```text
✅ Connected successfully to MySQL!
Server version: 8.0.x
Available databases: ['example', 'information_schema', 'mysql', 'performance_schema', 'sys']
Inserted row ID: 1
Found rows: ((1, 'Test', 42, datetime.datetime(...)),)
Connection closed.
```

## SQL Mode

SQL mode is set to `""`, which clears the SQL strict modes.
This is more suitable for development, but it is **risky** for production environments, because invalid or truncated values are silently accepted instead of raising errors.

To restore the MySQL 8.0 default, remove `--sql-mode=""` from the `command` in `docker-compose.yaml`.

## Security

This configuration is intended for local development only.

For production it is recommended to:
* Use a strong root password and do not commit it to Git (use a `.env` file or managed secrets, for example HashiCorp Vault).
* Create application users with least privilege instead of using `root`.
* Keep the SQL strict modes enabled.
* Not expose port 3306 directly to the Internet.
* Enable TLS for client connections.
* Configure regular backups.
