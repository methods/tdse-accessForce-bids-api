"""
This script deletes all bids from the Bids collection.

"""

import os
import sys
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URL") or "mongodb://localhost:27017/bidsAPI"


def delete_bids():
    """
    Deletes all bids from the MongoDB collection.
    """
    try:
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=10000)
        data_base = client["bidsAPI"]
        collection = data_base["bids"]

        if collection.count_documents({}) == 0:
            print("No bids to delete.")

        delete_result = collection.delete_many({})

        print(f"Deleted {delete_result.deleted_count} bids from the collection.")

    except ConnectionFailure as error:
        print(f"Error: {error}")
        sys.exit(1)

    finally:
        client.close()


if __name__ == "__main__":
    delete_bids()
    sys.exit(0)
