# Nexus

Sonatype Nexus Repository is an artifact repository manager. It stores and proxies build artifacts and packages such as Maven, npm, PyPI, NuGet, Docker images and raw files, acting as a single source for dependencies in CI/CD pipelines.

Two configurations are provided, depending on the final usage:

* [`Standalone`](Standalone): Nexus alone, exposed over HTTP on port `8081`. Quick to start, for development and testing.
* [`WithNginx`](WithNginx): Nexus behind an NGINX reverse proxy with HTTPS. Nexus is not exposed directly, and the Docker registry is published on its own host name. Recommended for production or when Nexus is used as a Docker registry.

Each folder has its own `docker-compose.yaml`, `.env.example` and Readme with the steps to start it.
