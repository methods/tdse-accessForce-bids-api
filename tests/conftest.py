"""
This file contains fixtures that are used by multiple tests.
"""

import os
import jwt
import pytest
import os
from app import app
from dotenv import load_dotenv


@pytest.fixture(scope="session")
def test_client():
    os.environ["TEST_ENVIRONMENT"] = "True"
    with app.test_client() as client:
        yield client
    os.environ.pop("TEST_ENVIRONMENT")


@pytest.fixture(scope="session")
def api_key():
    load_dotenv()
    api_key = os.getenv("API_KEY")
    return api_key


@pytest.fixture(scope="session")
def basic_jwt():
    payload = {"username": "User McTestface", "admin": False}
    load_dotenv()
    key = os.getenv("SECRET_KEY")
    token = jwt.encode(payload=payload, key=key)
    return token


@pytest.fixture(scope="session")
def admin_jwt():
    payload = {"username": "Admin McTestface", "admin": True}
    load_dotenv()
    key = os.getenv("SECRET_KEY")
    token = jwt.encode(payload=payload, key=key)
    return token
