# Nexus with NGINX

This folder runs Sonatype Nexus Repository behind an NGINX reverse proxy that handles HTTPS. Nexus has no published ports: all traffic goes through NGINX.

What NGINX adds on top of [`../Standalone`](../Standalone):

* **HTTPS** with a self-signed certificate generated automatically, or your own certificate.
* **HTTP → HTTPS redirect**.
* **Docker registry on its own host name** (`registry.nexus.localhost`) on port 443, so clients run `docker login registry.nexus.localhost` with no extra port.
* **No upload size limit** and streaming of uploads and downloads, needed for large artifacts and Docker layers.
* **Long timeouts** (15 minutes) for big transfers.
* **Gzip compression** of the UI and repository metadata.
* A **"Nexus is starting" message** instead of a raw error while Nexus boots.
* Hidden NGINX version and an optional IP allow-list.

## Architecture

```
Client                                 NGINX (:80, :443)      Nexus (internal only)
──────                                 ─────────────────      ─────────────────────
http://<any host>              :80  →  301 to HTTPS
https://nexus.localhost        :443 →  proxy            →     nexus:8081  (UI, API, repos)
https://registry.nexus.localhost :443 → proxy           →     nexus:8082  (Docker repo connector)
```

## Files

| File | Purpose |
|---|---|
| `docker-compose.yaml` | Services `certs`, `nexus` and `nginx`. |
| `.env.example` | Example configuration with test values. |
| `nginx/templates/default.conf.template` | NGINX server blocks. The nginx image fills in the `${VARIABLES}` at startup. |
| `nginx/snippets/nexus-proxy.conf` | Proxy headers, body size and timeouts shared by every location. |
| `nginx/generate-certs.sh` | Creates a self-signed certificate in `./certs` if none exists. |
| `certs/` | Generated at first start. Ignored by git. |

## How to start

1. Create your `.env` from the example (defaults are ready for a local test):
   ```bash
   cp .env.example .env
   ```

2. Make the host names resolve to your machine. Add this line to `/etc/hosts` (needs `sudo`):
   ```
   127.0.0.1 nexus.localhost registry.nexus.localhost
   ```

3. Launch the services:
   ```bash
   docker compose up -d
   ```

   On the first start, the `certs` service creates `certs/nexus.crt` and `certs/nexus.key`, then exits. NGINX starts right away; Nexus takes around 3 minutes. Follow it with:
   ```bash
   docker compose logs -f nexus
   ```

4. Open [https://nexus.localhost](https://nexus.localhost). The browser will warn about the self-signed certificate: accept it for local tests.

To stop everything (data is kept in the volume):
```bash
docker compose down
```

## How to access

Get the initial `admin` password:
```bash
docker exec nexus cat /nexus-data/admin.password
```

Log in with user `admin` and that password, then follow the setup wizard to change the password and choose whether to allow anonymous access.

### Set the Base URL

So that Nexus generates links with the public HTTPS address, go to *Administration → System → Capabilities → Create capability → Base URL* and set it to `https://nexus.localhost` (or your `NEXUS_HOST`).

## Docker registry

NGINX forwards `https://registry.nexus.localhost` to port `8082` of Nexus. You must create the repository in Nexus that listens on that port:

1. *Administration → Repository → Repositories → Create repository → docker (hosted)*.
2. Under *Repository Connectors*, enable **HTTP** and set port `8082` (or your `REGISTRY_PORT`).
3. *Administration → Security → Realms*: add **Docker Bearer Token Realm** to the active list.

### Trust the certificate in Docker

Docker requires a trusted certificate for any registry that is not `localhost`. With the self-signed certificate, copy it where Docker looks for registry CAs:

* **Linux**:
  ```bash
  sudo mkdir -p /etc/docker/certs.d/registry.nexus.localhost
  sudo cp certs/nexus.crt /etc/docker/certs.d/registry.nexus.localhost/ca.crt
  ```
* **macOS / Windows (Docker Desktop)**:
  ```bash
  mkdir -p ~/.docker/certs.d/registry.nexus.localhost
  cp certs/nexus.crt ~/.docker/certs.d/registry.nexus.localhost/ca.crt
  ```
  Then restart Docker Desktop.

### Push an image

```bash
docker login registry.nexus.localhost
```

```bash
docker tag alpine:latest registry.nexus.localhost/alpine:test
```

```bash
docker push registry.nexus.localhost/alpine:test
```

To add more Docker repositories (for example a proxy of Docker Hub or a group), give each one its own HTTP connector port in Nexus, add the port to `expose` in the `nexus` service and copy the registry `server` block in the template with a new host name.

## Configuration variables

| Variable | Default | Description |
|---|---|---|
| `NEXUS_VERSION` | `3.98.1` | `sonatype/nexus3` image tag. |
| `NEXUS_HEAP` | `2g` | JVM heap size (`-Xms` and `-Xmx`). |
| `NEXUS_DIRECT_MEMORY` | `2g` | JVM direct memory. |
| `NGINX_IMAGE_VERSION` | `1.30.6-alpine` | `nginx` image tag (stable branch). |
| `NGINX_HTTP_PORT` | `80` | Host port for HTTP (redirects to HTTPS). |
| `NGINX_HTTPS_PORT` | `443` | Host port for HTTPS. |
| `NEXUS_HOST` | `nexus.localhost` | Host name of the Nexus UI. |
| `REGISTRY_HOST` | `registry.nexus.localhost` | Host name of the Docker registry. |
| `REGISTRY_PORT` | `8082` | HTTP connector port of the Docker hosted repository inside Nexus. |

If you change `NEXUS_HOST` or `REGISTRY_HOST` after the first start, delete `certs/` so the certificate is generated again with the new names.

## Production configuration

* **Real certificate**: put your certificate (full chain) in `certs/nexus.crt` and the key in `certs/nexus.key` before starting. The `certs` service keeps existing files and does not overwrite them. Then uncomment the `Strict-Transport-Security` header in the template.
* **Real host names**: set `NEXUS_HOST` and `REGISTRY_HOST` to DNS names pointing to the server. You no longer need the `/etc/hosts` entry or to copy the certificate into Docker.
* **Restrict access**: uncomment the `allow` / `deny` lines in the template to limit the UI to internal networks.
* **Memory, storage, upgrades and backups**: same advice as in [`../Standalone/Readme.md`](../Standalone/Readme.md#production-configuration).

After changing the NGINX template, check and apply it without restarting Nexus:
```bash
docker compose up -d --force-recreate nginx
```
