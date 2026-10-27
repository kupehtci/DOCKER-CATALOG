import argparse
import pyodbc

# Configura los parámetros de conexión
server = 'localhost, 1433'
database = 'master'
username = 'sa'
password = 'MySecureP@ssw0rd2026'

# Define la cadena de conexión
conn_str = (
    'DRIVER={ODBC Driver 17 for SQL Server};'
    f'SERVER={server};'
    f'DATABASE={database};'
    f'UID={username};'
    f'PWD={password}'
)


# Get argumentss
arg_parser = argparse.ArgumentParser()
arg_parser.add_argument('--sql_file_path', required=True, type=str)
args = arg_parser.parse_args()

try:
    # Connect to database
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()

    # Read the SQL file
    with open(args.sql_file_path, 'r', encoding='utf-8') as f:
        sql_script = f.read()

    # Execute the SQL file.
    # If the file has more than 1 statement different, separate into multiple SQL files
    cursor.execute(sql_script)

    # for a select show the results and for a DELETE and similar show the affected files
    if sql_script.strip().upper().startswith('SELECT'):
        rows = cursor.fetchall()
        for row in rows:
            print(row)
    else:
        conn.commit()
        print(f"Filas afectadas: {cursor.rowcount}")

    conn.close()
    print("Script ejecutado correctamente.")

except pyodbc.Error as e:
    print(f"Error de base de datos: {e}")
except FileNotFoundError as e:
    print(f"Error: No se encontró el archivo SQL: {e}")
except Exception as e:
    print(f"Error inesperado: {e}")