"""
This script deletes all questions from the Questions collection.

"""

import os
import sys
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = 27017
DB_NAME = os.getenv("DB_NAME")

if os.environ.get("TEST_ENVIRONMENT"):
    DB_NAME = os.getenv("TEST_DB_NAME")


def delete_bids():
    """
    Deletes all bids from the MongoDB collection.
    """
    try:
        client = MongoClient(DB_HOST, DB_PORT, serverSelectionTimeoutMS=10000)
        data_base = client[DB_NAME]
        collection = data_base["questions"]

        if collection.count_documents({}) == 0:
            print("No questions to delete.")
        else:
            delete_result = collection.delete_many({})
            print(
                f"Deleted {delete_result.deleted_count} questions from the collection."
            )

    except ConnectionFailure:
        print(f"Error: Failed to connect to database")
        sys.exit(1)

    finally:
        client.close()


if __name__ == "__main__":
    delete_bids()
    sys.exit(0)
