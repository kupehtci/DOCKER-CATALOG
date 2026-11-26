import logging
import os
import platform
from datetime import datetime, timezone

from flask import Flask, jsonify

logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO").upper(),
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)
logger = logging.getLogger("python-application")

app = Flask(__name__)

APP_NAME = os.getenv("APP_NAME", "python-application")
APP_ENV = os.getenv("APP_ENV", "production")


@app.route("/")
def hello():
    logger.info("Request to /")
    return jsonify(
        message="Hello from a custom Python image!",
        app=APP_NAME,
        environment=APP_ENV,
    )


@app.route("/health")
def health():
    return jsonify(status="ok", time=datetime.now(timezone.utc).isoformat())


@app.route("/info")
def info():
    return jsonify(
        app=APP_NAME,
        environment=APP_ENV,
        python=platform.python_version(),
        hostname=platform.node(),
    )


if __name__ == "__main__":
    # Development server only. In the container the app is served by gunicorn.
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "8080")), debug=APP_ENV == "development")
