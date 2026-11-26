ARG STACK_VERSION=3.12

FROM python:${STACK_VERSION}-slim

# Python runtime settings:
# - PYTHONDONTWRITEBYTECODE: do not write .pyc files
# - PYTHONUNBUFFERED: send stdout/stderr straight to the container logs
# - PIP_*: smaller image and no version check on build
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

# Create a non-root user and the output directory it writes to
RUN groupadd --system app \
    && useradd --system --gid app --home-dir /app --no-create-home app \
    && mkdir -p /app/output \
    && chown -R app:app /app

# Install dependencies (cached layer while requirements.txt does not change)
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the script (filtered by .dockerignore)
COPY --chown=app:app . .

USER app

# ENTRYPOINT + CMD: the script always runs, and any argument given to
# `docker run <image> ...` / `docker compose run job ...` replaces the CMD
ENTRYPOINT ["python", "main.py"]
CMD []
