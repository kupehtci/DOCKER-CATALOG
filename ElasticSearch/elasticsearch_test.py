import os
from datetime import datetime, timezone
from pathlib import Path

from elasticsearch import Elasticsearch
from elasticsearch.exceptions import ApiError, TransportError


def load_env_file(path):
    """Load KEY=VALUE pairs from a .env file without overriding existing variables."""
    if not path.is_file():
        return
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith('#') or '=' not in line:
            continue
        key, value = line.split('=', 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


# Reuse the same .env file as docker-compose.yaml
load_env_file(Path(__file__).parent / '.env')

# Elasticsearch connection details (from the docker-compose.yaml)
# They can be overridden with environment variables.
URL = os.getenv('ELASTICSEARCH_URL', 'http://localhost:9200')
USERNAME = os.getenv('ELASTICSEARCH_USERNAME', 'elastic')
PASSWORD = os.getenv('ELASTIC_PASSWORD')
INDEX = 'test-index'

if not PASSWORD:
    raise SystemExit("ELASTIC_PASSWORD is not set. Define it in .env or as an environment variable.")

client = Elasticsearch(URL, basic_auth=(USERNAME, PASSWORD), request_timeout=10)

try:
    info = client.info()
    print("✅ Connected successfully to Elasticsearch!")
    print(f"Cluster: {info['cluster_name']} - Version: {info['version']['number']}")

    # Cluster health
    health = client.cluster.health()
    print(f"Cluster health: {health['status']}")

    # Create an example index (no replicas, as this is a single node)
    if not client.indices.exists(index=INDEX):
        client.indices.create(
            index=INDEX,
            settings={'number_of_shards': 1, 'number_of_replicas': 0},
        )
        print(f"Created index: {INDEX}")

    # Insert an example document (refresh so it is searchable right away)
    doc = {
        'message': 'Hello Elasticsearch',
        'level': 'INFO',
        'timestamp': datetime.now(timezone.utc).isoformat(),
    }
    result = client.index(index=INDEX, document=doc, refresh='wait_for')
    print(f"Inserted document ID: {result['_id']}")

    # Search the inserted documents
    response = client.search(index=INDEX, query={'match': {'message': 'Hello'}})
    hits = response['hits']['hits']
    print(f"Found {response['hits']['total']['value']} documents:")
    for hit in hits:
        print(f"  {hit['_id']}: {hit['_source']}")

except (ApiError, TransportError) as e:
    print(f"Connection failed: {e}")
finally:
    client.close()
    print("Connection closed.")
