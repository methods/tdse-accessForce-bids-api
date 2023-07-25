"""

This script creates sample data for the MongoDB database.

"""

import os
import json
import sys
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URL") or "mongodb://localhost:27017/bidsAPI"


def populate_bids():
    """
    Populates the MongoDB database with sample bids data from bids.json file.
    """
    try:
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=10000)
        data_base = client["bidsAPI"]
        collection = data_base["bids"]

        # Get the current script's directory
        current_dir = os.path.dirname(os.path.abspath(__file__))

        # Construct the file path to bids.json
        file_path = os.path.join(current_dir, "test_data", "bids.json")

        # Read bids data from JSON file
        with open(file_path, encoding="utf-8") as bids_file:
            bids_data = json.load(bids_file)

        # Insert bids into the database
        for bid in bids_data["items"]:
            # Check if the bid already exists in the database
            existing_bid = collection.find_one({"_id": bid["_id"]})
            if existing_bid:
                print(f"Skipping existing bid with _id: {bid['_id']}")
            else:
                collection.insert_one(bid)
                print(f"Inserted bid with _id: {bid['_id']}")

    except ConnectionFailure as error:
        print(f"Error: {error}")
        sys.exit(1)

    finally:
        # Close the MongoDB connection
        client.close()


if __name__ == "__main__":
    populate_bids()
    sys.exit(0)
