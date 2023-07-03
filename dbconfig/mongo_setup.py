from pymongo import MongoClient

MONGO_URI = "mongodb://localhost:27017/bids"

# Create a new client and connect to the server
def dbConnection():
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=10000)
    db = client["bids"]
    return db
   