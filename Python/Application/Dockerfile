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

# Create a non-root user to run the application
RUN groupadd --system app \
    && useradd --system --gid app --home-dir /app --no-create-home app

# Install dependencies (cached layer while requirements.txt does not change)
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the application code (filtered by .dockerignore)
COPY --chown=app:app . .

USER app

ENV PORT=8080 \
    GUNICORN_WORKERS=2

EXPOSE 8080

# Healthcheck with the standard library (the slim image has no curl nor wget)
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import os, urllib.request; urllib.request.urlopen(f'http://localhost:{os.environ.get(\"PORT\", \"8080\")}/health', timeout=4)" || exit 1

# Serve the app with gunicorn (production WSGI server). Adjust "app:app" to <module>:<flask_object>
CMD ["sh", "-c", "exec gunicorn --bind 0.0.0.0:${PORT} --workers ${GUNICORN_WORKERS} --access-logfile - app:app"]
