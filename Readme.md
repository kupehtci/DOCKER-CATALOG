# DOCKER-CATALOG

Docker catalog is a collection of docker custom images and docker compose environments defined for a quick deployment of tools, DB and services for developing, testing and learning. 

Feel free to use them with attribution, learn about docker compose definitions and combine the services as needed. 

## How to start

Each folder, have a certain service / tool / application with a `docker-compose.yaml` file or a `Dockerfile`, ready to start the service with: 

```bash
# For docker compose files
docker compose up
```

For `Dockerfiles` read the `Readme.md` of the folder for further instructions. 

## How to test

Each service varies in funcionality and integrations but the services that allow an easy testing, a python script or similar is placed together with the docker files for testing. 