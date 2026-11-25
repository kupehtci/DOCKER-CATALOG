# Elasticsearch with Docker Compose
Local single-node Elasticsearch service, intended for development, testing and lab environments. Includes data persistence, a healthcheck and basic authentication through the elastic user.

## Configuration
Create a .env file in the same folder as docker-compose.yml:
```env
ELASTIC_PASSWORD=ChangeThisSecurePassword
```
Do not commit the .env file to Git. Add it to .gitignore.

## Start the service
```bash
docker compose up -d
```
Check the status:

```bash
docker compose ps
```

Check that Elasticsearch responds:

```bash
curl -u elastic:${ELASTIC_PASSWORD} http://localhost:9200
```
Example of the expected response:

```json
{
  "name": "elasticsearch",
  "cluster_name": "docker-cluster",
  "cluster_uuid": "...",
  "version": {
    "number": "8.19.0"
  },
  "tagline": "You Know, for Search"
}
```

Check cluster health
```bash
curl -u elastic:${ELASTIC_PASSWORD} \
  http://localhost:9200/_cluster/health?pretty
```

Expected status on a single node:
* **yellow**: normal, because no replicas can be allocated with a single node.
* **red**: check the logs and the state of the indices.

### Exposed ports

| Port | Usage |
|---|---|
| 9200 | Elasticsearch HTTP / REST API | 
| 9300 | Internal transport between nodes |

For access from other applications, use:
```
http://localhost:9200
```

### Variables and resources

| Variable | Default value | Description |
|---|---|---|
| ELASTIC_PASSWORD | Defined in .env | Password of the elastic user |
| ES_JAVA_OPTS | -Xms1g -Xmx1g | Memory allocated to the JVM |
| discovery.type | single-node | Single-node configuration | 
| xpack.security.enabled | true | Enables authentication and basic security | 

To increase the JVM memory, change it in docker-compose.yml:

```text
ES_JAVA_OPTS=-Xms2g -Xmx2g
```

Both values must be equal to avoid frequent JVM heap resizing.

## Volumes

Data is stored in the Docker volume:

```text
elasticsearch_data
```

To inspect it:

```bash
docker volume ls
docker volume inspect elasticsearch_data
```

Indices persist even if the container is stopped or recreated.

## Common operations

View logs
```bash
docker compose logs -f elasticsearch
```
Stop the service
```bash
docker compose down
```

Stop and keep data
```bash
docker compose down
```

The volume is not removed with down.

Remove container and data
```bash
docker compose down -v
```

This deletes all indices and documents stored in Elasticsearch.

Restart from scratch
```bash
docker compose down -v
docker compose up -d
```
Create a test index
```bash
curl -u elastic:${ELASTIC_PASSWORD} \
  -X PUT "http://localhost:9200/test-index" \
  -H "Content-Type: application/json" \
  -d '{
    "settings": {
      "number_of_shards": 1,
      "number_of_replicas": 0
    }
  }'
```

Insert a document:
```bash
curl -u elastic:${ELASTIC_PASSWORD} \
  -X POST "http://localhost:9200/test-index/_doc" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Hello Elasticsearch",
    "level": "INFO",
    "timestamp": "2026-10-21T15:00:00Z"
  }'
```

Query documents:

```bash
curl -u elastic:${ELASTIC_PASSWORD} \
  "http://localhost:9200/test-index/_search?pretty"
```

Integration with applications
Example for a .NET application:

```text
Elasticsearch__Url=http://localhost:9200
Elasticsearch__Username=elastic
Elasticsearch__Password=ChangeThisSecurePassword
```

Example for Docker Compose in another stack:

```yaml
environment:
  - ELASTICSEARCH_URL=http://elasticsearch:9200
  - ELASTICSEARCH_USERNAME=elastic
  - ELASTICSEARCH_PASSWORD=${ELASTIC_PASSWORD}
``` 
If both services are on the same Docker network, use the service name:
```text
http://elasticsearch:9200
```

## Python script

The `elasticsearch_test.py` script allows a quick check, and serves as a reference, of how to connect to Elasticsearch once it is deployed.

The script connects to the cluster, prints its name, version and health, creates the `test-index` index (if it does not exist), inserts a document and searches for it.

> Note! The script reads `ELASTIC_PASSWORD` from the same `.env` file used by `docker-compose.yaml`. The URL and user can be overridden with the environment variables `ELASTICSEARCH_URL` and `ELASTICSEARCH_USERNAME`.

The Python client major version must match the server one, so `requirements.txt` pins an `8.x` client for the `8.19.0` image.

To execute the Python script:
```bash
pip install -r requirements.txt
python3 elasticsearch_test.py
```

Or use a virtual environment:
```bash
python3 -m venv .venv
source ./.venv/bin/activate
pip install -r requirements.txt
python3 elasticsearch_test.py
```

Example output:
```text
✅ Connected successfully to Elasticsearch!
Cluster: docker-cluster - Version: 8.19.0
Cluster health: green
Created index: test-index
Inserted document ID: ...
Found 1 documents:
  ...: {'message': 'Hello Elasticsearch', 'level': 'INFO', 'timestamp': '...'}
Connection closed.
```

### Security
This configuration enables security with a username and password, but it is intended for local development.

For production it is recommended to:
* Use at least three master-eligible nodes. 
* Configure TLS for HTTP and inter-node transport. 
* Create users and roles with least privilege. 
* Not expose port 9200 directly to the Internet. 
* Configure snapshots and backups. 
* Use managed secrets, for example HashiCorp Vault, instead of .env.
