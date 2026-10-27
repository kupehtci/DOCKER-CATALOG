# FileBeat

FileBeat is a lightweight log shipper developed by **Elastic**.

It can run as an agent, as a sidecar, or together with an application in order to monitor the configured log files, collect new log events and forward them to a central destination like:

* Elasticsearch
* Logstash
* Kafka
* Redis
* File

It can also be used to send logs to GrayLog using its **Beats input**.

## Folder structure

```
FileBeat/
├── docker-compose.yaml   # FileBeat service
├── config/
│   └── filebeat.yml      # FileBeat configuration (inputs, processors, output)
└── logs/                 # Put here the *.log files you want to ship
    └── sample.log
```

## How to start

Launch the docker compose file:
```bash
docker compose up -d
```

By default FileBeat reads `./logs/*.log` and prints the events to the console (`output.console`), so you can check that everything works with:
```bash
docker compose logs -f filebeat
```

Add a new line to a log file and it should appear in the output:
```bash
echo "$(date '+%Y-%m-%d %H:%M:%S') INFO hello filebeat" >> logs/sample.log
```

Stop the service:
```bash
docker compose down
```

Add `-v` to also delete the `filebeat_data` volume (the registry). FileBeat will then read all files from the beginning again.

## How to configure FileBeat service

All the configuration lives in [config/filebeat.yml](config/filebeat.yml), which is mounted read-only in `/usr/share/filebeat/filebeat.yml`. After changing it, restart the container:
```bash
docker compose restart filebeat
```

Validate the configuration and the connection with the output:
```bash
docker compose exec filebeat filebeat test config --strict.perms=false
```
```bash
docker compose exec filebeat filebeat test output --strict.perms=false
```

### Environment variables

The compose file accepts these variables (set them in a `.env` file next to `docker-compose.yaml`). `filebeat.yml` reads them with the `${VAR}` syntax.

| Variable | Default | Description |
|---|---|---|
| `FILEBEAT_VERSION` | `8.15.3` | Image tag of `docker.elastic.co/beats/filebeat` |
| `LOGSTASH_HOSTS` | `graylog:5044` | Logstash / GrayLog Beats input host:port |
| `ELASTICSEARCH_HOSTS` | `http://elasticsearch:9200` | Elasticsearch URL |
| `ELASTICSEARCH_USERNAME` | `elastic` | Elasticsearch user |
| `ELASTICSEARCH_PASSWORD` | `changeme` | Elasticsearch password (change it!) |

### Inputs

Inputs define **what** FileBeat reads. The `filestream` input is the recommended one (the old `log` input is deprecated).

```yaml
filebeat.inputs:
  - type: filestream
    id: app-logs            # Must be unique per input
    paths:
      - /var/log/app/*.log  # Path INSIDE the container
    fields:
      source_type: app      # Custom fields added to every event
    fields_under_root: true
```

To ship logs from another folder of the host, mount it in `docker-compose.yaml` and add its path to `paths`:
```yaml
volumes:
  - /path/in/host/myapp:/var/log/myapp:ro
```

**Multiline logs** (Java stack traces, etc.): uncomment the `parsers.multiline` block of the `app-logs` input and adapt the `pattern` to the beginning of each new log line.

**Docker container logs** (Linux hosts only):
1. Uncomment the `/var/lib/docker/containers` volume in `docker-compose.yaml`.
2. Set `enabled: true` in the `docker-logs` input.

The `add_docker_metadata` processor will enrich each event with the container name, image and labels.

> On macOS / Windows (Docker Desktop) the container logs live inside the Docker VM, so this mount does not work. Use the `./logs` folder instead.

### Outputs

Only **one output** can be enabled at a time. Comment `output.console` and uncomment the one you need.

**GrayLog (Beats input) / Logstash**
```yaml
output.logstash:
  hosts: ["${LOGSTASH_HOSTS}"]
```
In GrayLog go to *System → Inputs*, launch a **Beats** input on port `5044` and make sure that port is exposed in the GrayLog compose. If GrayLog runs in another compose project, connect both containers to the same Docker network, for example:
```bash
docker network connect filebeat graylog
```
Or use `LOGSTASH_HOSTS=host.docker.internal:5044` when the port is published on the host.

**Elasticsearch**
```yaml
output.elasticsearch:
  hosts: ["${ELASTICSEARCH_HOSTS}"]
  username: "${ELASTICSEARCH_USERNAME}"
  password: "${ELASTICSEARCH_PASSWORD}"
```

**Kafka**
```yaml
output.kafka:
  hosts: ["kafka:9092"]
  topic: "filebeat"
```

### Registry

FileBeat stores the read offset of every file in `/usr/share/filebeat/data` (`filebeat_data` volume). This way, after a restart it continues where it stopped and does not send duplicated events.

## Troubleshooting

| Problem | Solution |
|---|---|
| `config file ("filebeat.yml") must be owned by the user identifier` | The container already runs with `--strict.perms=false`. Use this flag also in `filebeat test ...` commands. |
| No events are shipped | Check that the path in `paths` is the path inside the container and that the file has new lines. Remove the registry (`docker compose down -v`) to re-read files from the start. |
| `Failed to connect to backoff(async(tcp://graylog:5044))` | FileBeat cannot reach the output: check the host/port and that both containers share a network. |
| `permission denied` reading logs | The service runs as `root`; check the volume is mounted and readable. |

## References

* [Filebeat documentation](https://www.elastic.co/guide/en/beats/filebeat/current/index.html)
* [Run Filebeat on Docker](https://www.elastic.co/guide/en/beats/filebeat/current/running-on-docker.html)
* [filestream input](https://www.elastic.co/guide/en/beats/filebeat/current/filebeat-input-filestream.html)
