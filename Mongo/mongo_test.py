import pymongo
from pymongo.errors import ConnectionFailure, PyMongoError
import urllib.parse

# MongoDB connection details (from your docker-compose)
USERNAME = urllib.parse.quote_plus('root')
PASSWORD = urllib.parse.quote_plus('1234')
HOST = 'localhost'
PORT = 27017
DB_NAME = 'appdb'

# Connection URI (universal identifier)
uri = f"mongodb://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}?authSource=admin"

try:
    client = pymongo.MongoClient(uri)
    client.admin.command('ping')
    print("✅ Connected successfully to MongoDB!")

    # List the available databases
    dbs = client.list_database_names()
    print(f"Available databases: {dbs}")

    db = client[DB_NAME]
    collection = db['test']

    # Insert an example document
    test_doc = {'name': 'Test', 'value': 42, 'timestamp': '2026-03-11'}
    result = collection.insert_one(test_doc)
    print(f"Inserted document ID: {result.inserted_id}")

    # Query the inserted document
    docs = list(collection.find({'name': 'Test'}))
    print(f"Found documents: {docs}")

except (ConnectionFailure, PyMongoError) as e:
    print(f"Connection failed: {e}")
finally:
    client.close()
    print("Connection closed.")
