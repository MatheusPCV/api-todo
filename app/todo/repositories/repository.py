from db_connection import get_mongo_db
from bson import ObjectId


class Repository:

    def __init__(self, collection):
        db = get_mongo_db()
        self.collection = db[collection]

    def get_all(self):
        return self.collection.find()

    def get_by_id(self, id):
        return self.collection.find_one({"_id": ObjectId(id)})

    def insert(self, document):
        return self.collection.insert_one(document)

    def update(self, id, update_data):
        return self.collection.update_one({"_id": ObjectId(id)}, {"$set": update_data})

    def delete(self, id):
        return self.collection.delete_one({"_id": ObjectId(id)})
