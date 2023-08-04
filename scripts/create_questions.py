"""

This script creates sample data for the Questions collection.

"""

import os
import json
import sys
from itertools import zip_longest
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = 27017
DB_NAME = os.getenv("DB_NAME")

if os.environ.get("TEST_ENVIRONMENT"):
    DB_NAME = os.getenv("TEST_DB_NAME")


def populate_questions():
    """
    Populates the MongoDB database with sample questions data from questions.json file.
    """
    try:
        client = MongoClient(DB_HOST, DB_PORT, serverSelectionTimeoutMS=10000)
        data_base = client[DB_NAME]
        collection = data_base["questions"]

        # Get the current script's directory
        current_dir = os.path.dirname(os.path.abspath(__file__))

        # Construct the file path to bids.json
        bids_path = os.path.join(current_dir, "test_data", "bids.json")

        # Construct the file path to questions.json
        questions_path = os.path.join(current_dir, "test_data", "questions.json")

        # Read bids data from JSON file
        with open(bids_path, encoding="utf-8") as bids_file:
            bids_data = json.load(bids_file)

        # Read bids data from JSON file
        with open(questions_path, encoding="utf-8") as questions_file:
            questions_data = json.load(questions_file)

        # Update questions data with existing bid ids from bids.json
        updated_questions = []

        bids = bids_data["items"]
        questions_groups = [
            questions_data[i : i + 3] for i in range(0, len(questions_data), 3)
        ]

        for bid, questions in zip_longest(bids, questions_groups, fillvalue=None):
            bid_url = bid["links"]["self"]

            for question in questions:
                self_url = question["links"]["self"]
                question["links"]["bid"] = bid_url
                question["links"]["self"] = f"{bid_url}{self_url}"
                updated_questions.append(question)

        # Insert questions into the database
        for question in updated_questions:
            # Check if the question already exists in the database
            existing_question = collection.find_one({"_id": question["_id"]})
            if existing_question:
                print(f"Skipping existing question with _id: {question['_id']}")
            else:
                collection.insert_one(question)
                print(f"Inserted question with _id: {question['_id']}")

    except ConnectionFailure:
        print(f"Error: Failed to connect to database")
        sys.exit(1)

    finally:
        # Close the MongoDB connection
        client.close()


if __name__ == "__main__":
    populate_questions()
    sys.exit(0)
