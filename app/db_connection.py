from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import os


load_dotenv()
DB_URL = os.getenv("DB_URL")
DB_NAME = os.getenv("DB_NAME")

print(f"DB_URL: {DB_URL}")
print(f"DB_NAME: {DB_NAME}")


def get_mongo_db():
    
    uri = DB_URL
    client = MongoClient(uri, server_api=ServerApi("1"))
    db = client[DB_NAME]
    return db
