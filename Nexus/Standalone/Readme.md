# Nexus (Standalone)

Sonatype Nexus Repository is an artifact repository manager. It stores and proxies build artifacts and packages such as Maven, npm, PyPI, NuGet, Docker images and raw files, acting as a single source for dependencies in CI/CD pipelines.

This folder contains a Docker compose file that launches a single Nexus Repository instance, exposed directly on port `8081`. It is ready for development and easy to adapt for production.

To publish Nexus over HTTPS behind an NGINX reverse proxy (recommended for production and for Docker registries), use [`../WithNginx`](../WithNginx) instead.

## How to start

Create your `.env` from the provided example (the defaults are ready for a local/test environment):
```bash
cp .env.example .env
```

The `.env` file is ignored by git. It is optional: without it, the compose file uses the same defaults.

Launch the docker compose file:
```bash
docker compose up -d
```

The first startup takes around 3 minutes. Follow its progress with:
```bash
docker compose logs -f nexus
```

Nexus is ready when the log shows `Started Sonatype Nexus` and the container status is `healthy`:
```bash
docker compose ps
```

The web interface is then available at [localhost:8081](http://localhost:8081).

To stop the service (data is kept in the volume):
```bash
docker compose down
```

## How to access

On first start, Nexus generates a random password for the `admin` user and stores it inside the container. Read it with:

```bash
docker exec nexus cat /nexus-data/admin.password
```

Log in with user `admin` and that password. The setup wizard then asks you to:
1. Set a new admin password (the `admin.password` file is deleted afterwards).
2. Choose whether to allow anonymous access. Disable it unless you need public read access.

## Docker compose file

The compose file runs `sonatype/nexus3`, pinned to a specific version for reproducible deployments.

**Ports**:
* `8081`: web interface and REST API.
* `8082` / `8083` (commented out): uncomment them when using Nexus as a Docker registry. Each Docker repository needs its own HTTP connector port, set in the repository settings in the UI.

**Volumes**:
* `nexus-data` → `/nexus-data`: repositories, blob stores, configuration, embedded database and logs.

**Other settings**:
* `ulimits.nofile` set to 65536, the minimum Sonatype requires for open file descriptors.
* `stop_grace_period` of 2 minutes, so Nexus can shut down cleanly without corrupting its database.
* A **healthcheck** over `/service/rest/v1/status/writable`, which only succeeds when Nexus can accept writes.
* Log rotation (3 files of 10 MB) to stop container logs from filling the disk.
* Automatic **restart** unless manually stopped.

### Configuration variables

The compose file reads these optional variables from the environment or from a `.env` file next to it:

| Variable | Default | Description |
|---|---|---|
| `NEXUS_VERSION` | `3.98.1` | Image tag. Also available as `-alpine` and `-ubi` variants. |
| `NEXUS_PORT` | `8081` | Host port for the web interface. |
| `NEXUS_HEAP` | `2g` | JVM heap size (used for both `-Xms` and `-Xmx`). |
| `NEXUS_DIRECT_MEMORY` | `2g` | JVM direct memory (`-XX:MaxDirectMemorySize`). |

A ready-to-use example with test values is provided in [`.env.example`](.env.example). For production, raise the memory values in your `.env`, for example:
```bash
NEXUS_HEAP=4g
NEXUS_DIRECT_MEMORY=6g
```

## Production configuration

### Memory

The defaults fit a host with 8 GB of RAM or more. For production, Sonatype recommends keeping `-Xms` equal to `-Xmx` and sizing the heap and direct memory to the host. For example, on a 16 GB host:
```bash
NEXUS_HEAP=4g
NEXUS_DIRECT_MEMORY=6g
```

Leave enough RAM for the operating system: heap plus direct memory should stay well below total host memory.

### Persistent storage

The default named volume works, but for production you may prefer a bind mount to a known path on the host, so it is easy to back up and monitor. Replace the volume in `docker-compose.yaml`:
```yaml
    volumes:
      - /srv/nexus-data:/nexus-data
```

Nexus runs as user `200` inside the container, so the host directory must be owned by that user:
```bash
sudo mkdir -p /srv/nexus-data && sudo chown -R 200:200 /srv/nexus-data
```

### Upgrades

Back up `/nexus-data` first, then change `NEXUS_VERSION` and recreate the container:
```bash
docker compose pull && docker compose up -d
```

Check the [Sonatype release notes](https://help.sonatype.com/en/release-notes.html) before jumping several versions, because some upgrades include database migrations.

### Other recommendations

* Put Nexus behind a reverse proxy with HTTPS, especially when using it as a Docker registry, since Docker clients require TLS for non-local registries. The [`../WithNginx`](../WithNginx) variant does exactly this.
* Configure backup tasks in *Administration → System → Tasks*, and back up the blob stores as well.
* Change the default admin password and create dedicated users or roles for CI pipelines instead of sharing the admin account.
