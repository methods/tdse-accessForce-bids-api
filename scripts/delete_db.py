"""
This script deletes all bids from the MongoDB collection.

"""

import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URL") or "mongodb://localhost:27017/bidsAPI"


def delete_bids():
    try:
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=10000)
        db = client["bidsAPI"]
        collection = db["bids"]

        if collection.count_documents({}) == 0:
            print("No bids to delete.")

        delete_result = collection.delete_many({})

        # Print the number of deleted bids
        print(f"Deleted {delete_result.deleted_count} bids from the collection.")

    except Exception as e:
        print(f"Error: {e}")
        exit(1)

    finally:
        client.close()


if __name__ == "__main__":
    delete_bids()
    exit(0)
