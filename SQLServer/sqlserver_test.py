import pyodbc

# Configure connection parameters
server = 'localhost, 1433'
database = 'master'
username = 'sa'
password = 'MySecureP@ssw0rd2026'

# Define the connection string
conn_str = (
    'DRIVER={ODBC Driver 17 for SQL Server};'
    f'SERVER={server};'
    f'DATABASE={database};'
    f'UID={username};'
    f'PWD={password}'
)

# Connect to database and open a cursor for a basic SQL Query
try:
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    cursor.execute('SELECT @@VERSION')
    print(cursor.fetchone())
    conn.close()
except pyodbc.Error as e:
    print(e)
