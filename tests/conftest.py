import jwt
import pytest
import os
from dotenv import load_dotenv
from flask import Flask
from api.controllers.bid_controller import bid
from api.controllers.question_controller import question


@pytest.fixture(scope="session")
def test_client():
    app = Flask(__name__)
    app.register_blueprint(bid, url_prefix="/api")
    app.register_blueprint(question, url_prefix="/api")
    with app.test_client() as client:
        yield client


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
