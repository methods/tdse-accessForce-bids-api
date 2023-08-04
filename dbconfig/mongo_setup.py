"""
This file contains the configuration for the MongoDB database.
"""

import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = 27017
DB_NAME = os.getenv("DB_NAME")

if os.environ.get("TEST_ENVIRONMENT"):
    DB_NAME = os.getenv("TEST_DB_NAME")

# Create a new client and connect to the server
client = MongoClient(DB_HOST, DB_PORT, serverSelectionTimeoutMS=10000)
db = client[DB_NAME]
