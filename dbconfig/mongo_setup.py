import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URL") or "mongodb://localhost:27017/bidsAPI"


# Create a new client and connect to the server
client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=10000)
db = client["bidsAPI"]
