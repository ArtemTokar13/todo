from pymongo import MongoClient


DB_URL = 'mongodb://host.docker.internal:27017'
DB_NAME = 'Todo'

def get_db():
    try:
        client = MongoClient(DB_URL)
        db = client[DB_NAME]
        yield db
    finally:
        client.close()