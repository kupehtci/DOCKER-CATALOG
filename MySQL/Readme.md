# MySQL

MySQL is a relational database that uses SQL to query and modify data. 

This docker compose file, sets up a MySQL database for development. 

# Docker compose file configuration

The docker compose 


By default, `MYSQL_DATABASE: example` database is created, rename it to your needs. 

In order to authenticate, use the root password settled up in `MYSQL_ROOT_PASSWORD`.

## SQL Mode

SQL Mode is settled to "", clearing the SQL strict modes. 
This is more suitable for development, but its **risky** for production environments. 