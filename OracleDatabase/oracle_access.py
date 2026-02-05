import oracledb

## Connect to database
try: 
    connection = oracledb.connect(
        user="SYSTEM",
        password="Pass123",     # Password needs to be the same as Docker compose file one
        dsn="localhost:1521/FREE"   
    )

    # Check the connection
    if not connection.is_healthy(): 
        print("Error in the connection. Review the configuration and the database")
        exit    
    
    cursor = connection.cursor()
    
    cursor.execute("SELECT USER FROM DUAL")
    print(f"Connected as: {cursor.fetchone()[0]}")
    
    cursor.execute("SELECT table_name FROM user_tables")
    
    # Fetch all users
    print("Users: ")
    cursor.execute("SELECT username, account_status FROM dba_users")
    rows = cursor.fetchall()
    for row in rows: 
        print(str(row))

    cursor.close() 
    connection.close()

except Exception as e: 
    print(f"Exception: {e}")

