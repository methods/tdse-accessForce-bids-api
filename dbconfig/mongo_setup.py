"""
This file contains the configuration for the MongoDB database.
"""

from pymongo import MongoClient


# Create new client, connect to server and return db instance
def get_db(DB_HOST, DB_PORT, DB_NAME):
    client = MongoClient(DB_HOST, DB_PORT, serverSelectionTimeoutMS=10000)
    return client[DB_NAME]
