# Python - Application

This folder contains a Dockerfile to containerize a long-running Python web application and run it with Docker Compose (Optionally).

The example application is `app.py`, a small [Flask](https://flask.palletsprojects.com/) API served by [gunicorn](https://gunicorn.org/) with the following endpoints:

| Endpoint  | Description                                          |
|-----------|------------------------------------------------------|
| `/`       | Hello message with the application name and environment |
| `/health` | Health endpoint used by the healthcheck              |
| `/info`   | Python version and container hostname                |

```
Python/Application/
├── .dockerignore
├── .env.example
├── Dockerfile
├── docker-compose.yaml
├── app.py
└── requirements.txt
```

## Dockerfile

Single-stage build over the official `python:<version>-slim` image.

**Build argument**:
* `STACK_VERSION` (default `3.12`): Python version, used as the tag of `python:${STACK_VERSION}-slim`.

**Steps**:
1. Sets the Python environmental variables:
   * `PYTHONDONTWRITEBYTECODE=1`: does not write `.pyc` files.
   * `PYTHONUNBUFFERED=1`: stdout/stderr go straight to the container logs.
   * `PIP_NO_CACHE_DIR=1` and `PIP_DISABLE_PIP_VERSION_CHECK=1`: smaller image and faster builds.
2. Creates the non-root user `app`.
3. Copies only `requirements.txt` and installs the dependencies. This layer is cached, so the packages are only downloaded again when `requirements.txt` changes.
4. Copies the rest of the code (filtered by `.dockerignore`) owned by `app`.
5. Runs as the non-root user `app`.
6. Sets `PORT=8080` and `GUNICORN_WORKERS=2`, exposes port `8080`.
7. Defines a `HEALTHCHECK` against `/health` using the Python standard library (the slim image has no `curl` nor `wget`).
8. Starts the app with `gunicorn` (production WSGI server) instead of the Flask development server.

### .dockerignore

Excludes Python caches, virtual environments, the `.env` file, IDE folders and the Docker files from the build context.

### Adapt to your application

* Add your dependencies to `requirements.txt`.
* Change `app:app` in the `CMD` to `<module>:<flask_object>` of your application.
* For a non-WSGI application (FastAPI, worker, bot...) replace the `CMD`, e.g. `uvicorn main:app --host 0.0.0.0 --port 8080` for FastAPI.
* If your dependencies need to compile native extensions (e.g. `psycopg2`, `mysqlclient`), install `build-essential` and the `-dev` libraries before `pip install`, or use a multi-stage build.

### Build and run without Compose

```bash
docker build --build-arg STACK_VERSION=3.12 -t python-application:local .
```

```bash
docker run -d --name python-application -p 8080:8080 python-application:local
```

## Docker Compose file

This configuration builds the image from the `Dockerfile` (tagged `python-application:local`) and deploys it in a container named `python-application`.

Exposed **ports**
* Port `${APP_PORT}` (default `8080`) mapped to internal `8080` port for the HTTP API.

Configured a **healthcheck** using Python against `/health` each 30s with 3 retries, a 5s timeout and a 10s start period.
Configured an **Auto-restart policy** unless is manually stopped.

### Configuration:

Copy the example file and adjust it:
```bash
cp .env.example .env
```

Build arguments:
* `STACK_VERSION`: Python version of the base image.

Configure the following environmental variables:
* `TAG`: Tag of the built image.
* `APP_PORT`: Host port.
* `APP_NAME`: Application name returned by the API.
* `APP_ENV`: Runtime environment (`production`, `development`...).
* `LOG_LEVEL`: Log level (`DEBUG`, `INFO`, `WARNING`...).
* `GUNICORN_WORKERS`: Number of gunicorn worker processes (rule of thumb: `2 x CPU + 1`).

## How to start

Build and launch the service.
```bash
docker compose up -d --build
```

Check the status (it should be `healthy`):
```bash
docker compose ps
```

Test the endpoints:
```bash
curl http://localhost:8080/
```

```bash
curl http://localhost:8080/health
```

```bash
curl http://localhost:8080/info
```

Show the logs:
```bash
docker compose logs -f python-application
```

Stop and remove the container:
```bash
docker compose down
```

## Run locally without Docker

```bash
python -m venv .venv && source .venv/bin/activate
```

```bash
pip install -r requirements.txt && python app.py
```
