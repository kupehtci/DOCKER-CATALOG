# Nexus

This sections contains a Docker compose file for launching a develop Nexus repository.

## Production configuration

For production configuration, mount a persistent volume that references a local path instead of temporal storage. 

Also, consider incrementing the RAM available by changing: 
```yaml
INSTALL4J_ADD_VM_PARAMS=-Xms2g -Xmx4g -XX:MaxDirectMemorySize=8g  # 8g instead of 2g
```

## How to start

Launch the docker compose file: 
```bash
docker compose up -d
```

This will launch the vault service accessible at [localhost:8081](http://localhost:8081)

## How to access

The first time, you will need to use a generated password that is generated inside the container. 

In order to obtain it: 

```bash
docker debug nexus

cat /nexus-data/admin.password
```

And then login using `admin` user and the password in the `admin.password` file. 