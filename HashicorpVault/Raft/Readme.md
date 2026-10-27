# Hashicorp Vault Raft WIP

This section launches a Hashicorp's Vault service with Raft High Availability. 
Take into account that in Production, its recommendable to launch each vault container in a separate machine instead of 3 nodes in same compose and machine. 
Hashicorp's Vault centralizes the storage, access control and audit of secrets like passwords, API Keys, certificates and encryption keys. 

# How to start

1. Run the service

```bash
docker compose up
# Or in background mode
docker compose up -d
```

2. Login in your browser: [Localhost Vault](http://localhost:8200/)

## Configuration and managing

For further vault configuration and managing documentation, check my documentation [DOCUMENTATION - Vault](https://github.com/kupehtci/DOCUMENTATION/tree/main/Vault) hosted in GitHub.  