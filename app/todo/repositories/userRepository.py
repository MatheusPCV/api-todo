from db_connection import get_mongo_db
from pymongo import ASCENDING


class UserRepository:

    def __init__(self, collection):
        db = get_mongo_db()
        self.collection = db[collection]
        self.collection.create_index([("username", ASCENDING)], unique=True)
        self.collection.create_index([("email", ASCENDING)], unique=True)

    def insert(self, document):
        self.collection.insert_one(document)

    def get_user_by_username(self, username):
        return self.collection.find_one({"username": username})
