# Python - SingleShot

This folder contains a Dockerfile to containerize a **single-shot** Python script: a job that runs once, does its work and exits (batch processes, migrations, reports, scheduled tasks, CI steps...). Unlike [Application](../Application), there is no server, no exposed port and no restart policy.

The example script is `main.py`: it checks a list of URLs, logs the result and writes a JSON report to `/app/output/report.json`. The **exit code** is `0` when every URL answered with a 2xx/3xx status and `1` otherwise, so the container result can be used by cron, CI pipelines or orchestrators.

```
Python/SingleShot/
├── .dockerignore
├── .env.example
├── .gitignore
├── Dockerfile
├── docker-compose.yaml
├── main.py
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
2. Creates the non-root user `app` and the `/app/output` directory owned by it.
3. Copies only `requirements.txt` and installs the dependencies. This layer is cached, so the packages are only downloaded again when `requirements.txt` changes.
4. Copies the script (filtered by `.dockerignore`) and runs as the non-root user `app`.
5. Uses `ENTRYPOINT ["python", "main.py"]` with an empty `CMD`: the script always runs and any argument given to `docker run` / `docker compose run` is passed to the script.

### .dockerignore

Excludes Python caches, virtual environments, the `output/` folder, the `.env` file, IDE folders and the Docker files from the build context.

### Adapt to your script

* Add your dependencies to `requirements.txt`.
* Replace `main.py` (or change the `ENTRYPOINT`) with your script.
* Return a non-zero exit code on failure (`sys.exit(1)`) so the caller knows the job failed.
* Read the configuration from environmental variables and/or CLI arguments.

### Build and run without Compose

```bash
docker build --build-arg STACK_VERSION=3.12 -t python-singleshot:local .
```

Run once and remove the container (`--rm`), passing the arguments to the script:
```bash
docker run --rm -v "$(pwd)/output:/app/output" python-singleshot:local --url https://www.python.org --url https://pypi.org
```

Or with environmental variables:
```bash
docker run --rm -e TARGET_URLS=https://www.python.org,https://pypi.org -v "$(pwd)/output:/app/output" python-singleshot:local
```

Check the exit code of the job:
```bash
echo $?
```

## Docker Compose file

This configuration builds the image from the `Dockerfile` (tagged `python-singleshot:local`) and runs the job once in a container named `python-singleshot`.

No **ports** are exposed.

Configured **volumes**:
* `./output` → `/app/output` to get the JSON report in the host.

Configured **restart policy** `"no"`: the container stops when the script ends and is never restarted.

### Configuration:

Copy the example file and adjust it:
```bash
cp .env.example .env
```

Build arguments:
* `STACK_VERSION`: Python version of the base image.

Configure the following environmental variables:
* `TAG`: Tag of the built image.
* `TARGET_URLS`: Comma separated list of URLs to check.
* `REQUEST_TIMEOUT`: Timeout in seconds of each request.
* `LOG_LEVEL`: Log level (`DEBUG`, `INFO`, `WARNING`...).

> **Linux hosts**: the script runs as the non-root user `app`. If the bind-mounted `./output` folder is created by Docker as `root`, the job cannot write the report. Create it beforehand with `mkdir -p output && chmod 777 output`, or add `user: "${UID}:${GID}"` to the service. Docker Desktop (macOS / Windows) does not need it.

## How to start

Build and run the job (the command ends when the script ends and returns its exit code):
```bash
docker compose up --build --abort-on-container-exit --exit-code-from python-singleshot
```

Alternatively, run it as a one-off container, overriding the arguments:
```bash
docker compose run --rm python-singleshot --url https://www.python.org --timeout 10
```

Check the report:
```bash
cat output/report.json
```

Show the logs and exit code of the last run:
```bash
docker compose logs python-singleshot
```

```bash
docker compose ps -a
```

Remove the stopped container:
```bash
docker compose down
```

### Schedule it

Since it is a single-shot job, it can be scheduled from the host, e.g. with `cron` every day at 06:00:
```
0 6 * * * cd /path/to/Python/SingleShot && docker compose run --rm python-singleshot >> /var/log/singleshot.log 2>&1
```

## Run locally without Docker

```bash
python -m venv .venv && source .venv/bin/activate
```

```bash
pip install -r requirements.txt && python main.py --url https://www.python.org --output output/report.json
```
