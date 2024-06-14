from db_connection import get_mongo_db
from pymongo import ASCENDING


class TaskRepository:

    def __init__(self, collection):
        db = get_mongo_db()
        self.collection = db[collection]
        
    def filter(self, username):
            return list(self.collection.find({"username": username}))