"""
This file contains the configuration for the MongoDB database.
"""

from pymongo import MongoClient


def get_db(DB_HOST, DB_PORT, DB_NAME):
    # Create a new client and connect to the server
    client = MongoClient(DB_HOST, DB_PORT, serverSelectionTimeoutMS=10000)
    return client[DB_NAME]
