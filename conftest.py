"""
This file contains fixtures that are used by multiple tests.
"""

import json
import jwt
import logging
import os
import pytest
from app import create_app
from dotenv import load_dotenv

load_dotenv()

with open("./tests/integration/data.json") as data:
    test_data = json.load(data)


@pytest.fixture
def integration_setup_and_teardown(test_app):
    db = test_app.db
    collection = db["bids"]
    collection.insert_many(test_data)
    yield
    collection.delete_many({})
    # print("AFTER")


@pytest.fixture(scope="session")
def test_app():
    os.environ["CONFIG_TYPE"] = "config.TestingConfig"
    app = create_app()
    with app.app_context():
        yield app


@pytest.fixture(scope="session")
def test_client(test_app):
    with test_app.app_context():
        return test_app.test_client()


@pytest.fixture(autouse=True)
def pause_logging():
    logging.disable(logging.CRITICAL)
    print("----------Logging disabled----------")
    yield
    logging.disable(logging.NOTSET)
    print("----------Logging re-enabled----------")


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