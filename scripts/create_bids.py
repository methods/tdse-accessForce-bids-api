"""

This script creates sample data for the Bids collection.

"""

import os
import json
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


def populate_bids():
    """
    Populates the MongoDB database with sample bids data from bids.json file.
    """
    try:
        client = MongoClient(DB_HOST, DB_PORT, serverSelectionTimeoutMS=10000)
        data_base = client[DB_NAME]
        collection = data_base["bids"]

        # Get the current script's directory
        current_dir = os.path.dirname(os.path.abspath(__file__))

        # Construct the file path to bids.json
        file_path = os.path.join(current_dir, "test_data", "bids.json")

        # Read bids data from JSON file
        with open(file_path, encoding="utf-8") as bids_file:
            bids_data = json.load(bids_file)

        # Insert bids into the database
        for bid in bids_data:
            # Check if the bid already exists in the database
            existing_bid = collection.find_one({"_id": bid["_id"]})
            if existing_bid:
                print(f"Skipping existing bid with _id: {bid['_id']}")
            else:
                collection.insert_one(bid)
                print(f"Inserted bid with _id: {bid['_id']}")

    except ConnectionFailure:
        print("Error: Failed to connect to database")
        sys.exit(1)

    finally:
        # Close the MongoDB connection
        client.close()


if __name__ == "__main__":
    populate_bids()
    sys.exit(0)
