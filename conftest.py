"""
This file contains fixtures that are used by multiple tests.
"""

import jwt
import logging
import os
import pytest
from app import app
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = 27017
DB_NAME = os.getenv("TEST_DB_NAME")
test_data = [
    {
        "_id": "be15c306-c85b-4e67-a9f6-682553c065a1",
        "alias": "ONS",
        "bid_date": "2023-06-23",
        "bid_folder_url": "https://organisation.sharepoint.com/Docs/dummyfolder",
        "client": "Office for National Statistics",
        "failed": {"has_score": True, "out_of": 36, "phase": 2, "score": 20},
        "feedback": {
            "description": "Feedback from client in detail",
            "url": "https://organisation.sharepoint.com/Docs/dummyfolder/feedback",
        },
        "last_updated": "2023-07-20T17:00:40.510224",
        "links": {
            "questions": "/api/bids/be15c306-c85b-4e67-a9f6-682553c065a1/questions",
            "self": "/api/bids/be15c306-c85b-4e67-a9f6-682553c065a1",
        },
        "status": "in_progress",
        "success": [{"has_score": True, "out_of": 36, "phase": 1, "score": 30}],
        "tender": "Business Intelligence and Data Warehousing",
        "was_successful": False,
    },
    {
        "_id": "a5e8f31b-d848-4e87-b5c9-8db5a9d72bc7",
        "alias": "ACME",
        "bid_date": "2023-07-05",
        "bid_folder_url": "https://organisation.sharepoint.com/Docs/dummyfolder",
        "client": "ACME Corporation",
        "failed": {"has_score": True, "out_of": 36, "phase": 2, "score": 15},
        "feedback": {
            "description": "Feedback from client in detail",
            "url": "https://organisation.sharepoint.com/Docs/dummyfolder/feedback",
        },
        "last_updated": "2023-08-01T14:30:20.123456",
        "links": {
            "questions": "/api/bids/a5e8f31b-d848-4e87-b5c9-8db5a9d72bc7/questions",
            "self": "/api/bids/a5e8f31b-d848-4e87-b5c9-8db5a9d72bc7",
        },
        "status": "in_progress",
        "success": [{"has_score": True, "out_of": 36, "phase": 1, "score": 28}],
        "tender": "Data Analytics Solution",
        "was_successful": False,
    },
]


@pytest.fixture
def integration_setup_and_teardown():
    client = MongoClient(DB_HOST, DB_PORT, serverSelectionTimeoutMS=10000)
    data_base = client[DB_NAME]
    collection = data_base["bids"]
    collection.insert_many(test_data)
    yield
    collection.delete_many({})


@pytest.fixture(autouse=True)
def pause_logging():
    logging.disable(logging.CRITICAL)
    print("----------Logging disabled----------")
    yield
    logging.disable(logging.NOTSET)
    print("----------Logging re-enabled----------")


@pytest.fixture(scope="session")
def test_client():
    os.environ["TEST_ENVIRONMENT"] = "True"
    with app.test_client() as client:
        yield client
    os.environ.pop("TEST_ENVIRONMENT")


@pytest.fixture(scope="session")
def api_key():
    api_key = os.getenv("API_KEY")
    return api_key


@pytest.fixture(scope="session")
def basic_jwt():
    payload = {"username": "User McTestface", "admin": False}
    key = os.getenv("SECRET_KEY")
    token = jwt.encode(payload=payload, key=key)
    return token


@pytest.fixture(scope="session")
def admin_jwt():
    payload = {"username": "Admin McTestface", "admin": True}
    key = os.getenv("SECRET_KEY")
    token = jwt.encode(payload=payload, key=key)
    return token


@pytest.fixture(scope="session")
def max_offset():
    max_offset = os.getenv("MAX_OFFSET")
    return int(max_offset)


@pytest.fixture(scope="session")
def max_limit():
    max_limit = os.getenv("MAX_LIMIT")
    return int(max_limit)


@pytest.fixture(scope="session")
def default_offset():
    default_offset = os.getenv("DEFAULT_OFFSET")
    return int(default_offset)


@pytest.fixture(scope="session")
def default_limit():
    default_limit = os.getenv("DEFAULT_LIMIT")
    return int(default_limit)


@pytest.fixture(scope="session")
def default_sort_bids():
    default_sort_bids = os.getenv("DEFAULT_SORT_BIDS")
    return default_sort_bids


@pytest.fixture(scope="session")
def default_sort_questions():
    default_sort_questions = os.getenv("DEFAULT_SORT_QUESTIONS")
    return default_sort_questions
