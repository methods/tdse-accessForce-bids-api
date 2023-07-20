from pymongo import MongoClient

MONGO_URI = "mongodb://localhost:27017/bidsAPI"


# Create a new client and connect to the server
def dbConnection():
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=10000)
    db = client["bidsAPI"]
    return db
