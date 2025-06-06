from pymongo import MongoClient
from flask import current_app

class Database:
    def __init__(self):
        self.client = MongoClient(current_app.config['MONGODB_URI'])
        self.db = self.client[current_app.config['DATABASE_NAME']]

    def get_collection(self, collection_name):
        return self.db[collection_name]

    def close_connection(self):
        self.client.close()