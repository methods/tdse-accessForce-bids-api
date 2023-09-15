"""
This file contains the configuration for the MongoDB database.
"""

import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()


def get_db(DB_HOST, DB_PORT, DB_NAME):
    # DB_HOST = os.getenv("DB_HOST")
    # DB_PORT = 27017
    # DB_NAME = os.getenv("DB_NAME")

    # if os.environ.get("TESTING"):
    #     DB_NAME = os.getenv("TEST_DB_NAME")

    # Create a new client and connect to the server
    client = MongoClient(DB_HOST, DB_PORT, serverSelectionTimeoutMS=10000)
    return client[DB_NAME]
