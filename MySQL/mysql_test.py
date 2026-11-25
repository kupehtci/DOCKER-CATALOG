import os

import pymysql
from pymysql.err import MySQLError

# MySQL connection details (from the docker-compose.yaml)
# They can be overridden with environment variables.
HOST = os.getenv('MYSQL_HOST', 'localhost')
PORT = int(os.getenv('MYSQL_PORT', '3306'))
USERNAME = os.getenv('MYSQL_USER', 'root')
PASSWORD = os.getenv('MYSQL_PASSWORD', 'root')
DB_NAME = os.getenv('MYSQL_DATABASE', 'example')

conn = None
try:
    conn = pymysql.connect(
        host=HOST,
        port=PORT,
        user=USERNAME,
        password=PASSWORD,
        database=DB_NAME,
        connect_timeout=10,
    )
    print("✅ Connected successfully to MySQL!")

    with conn.cursor() as cursor:
        # Server version
        cursor.execute('SELECT VERSION()')
        print(f"Server version: {cursor.fetchone()[0]}")

        # List the available databases
        cursor.execute('SHOW DATABASES')
        dbs = [row[0] for row in cursor.fetchall()]
        print(f"Available databases: {dbs}")

        # Create an example table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS test (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                value INT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )

        # Insert an example row
        cursor.execute(
            'INSERT INTO test (name, value) VALUES (%s, %s)',
            ('Test', 42),
        )
        conn.commit()
        print(f"Inserted row ID: {cursor.lastrowid}")

        # Query the inserted rows
        cursor.execute('SELECT id, name, value, created_at FROM test WHERE name = %s', ('Test',))
        rows = cursor.fetchall()
        print(f"Found rows: {rows}")

except MySQLError as e:
    print(f"Connection failed: {e}")
finally:
    if conn is not None:
        conn.close()
        print("Connection closed.")
