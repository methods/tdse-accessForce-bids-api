"""

This script creates sample data for the MongoDB database.

"""

from pymongo import MongoClient
from dotenv import load_dotenv
import os
import json

load_dotenv()

MONGO_URI = os.getenv("MONGO_URL") or "mongodb://localhost:27017/bidsAPI"


def populate_bids():
    try:
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=10000)
        db = client["bidsAPI"]
        collection = db["bids"]

        # Get the current script's directory
        current_dir = os.path.dirname(os.path.abspath(__file__))

        # Construct the file path to bids.json
        file_path = os.path.join(current_dir, "test_data", "bids.json")

        # Read bids data from JSON file
        with open(file_path) as bids_file:
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

    except Exception as e:
        print(f"Error: {e}")
        exit(1)

    finally:
        # Close the MongoDB connection
        client.close()


if __name__ == "__main__":
    populate_bids()
    exit(0)
