import os
import pytest
from dotenv import load_dotenv
from flask import Flask
from api.controllers.bid_controller import bid


@pytest.fixture(scope="session")
def test_client():
    app = Flask(__name__)
    app.register_blueprint(bid, url_prefix="/api")
    with app.test_client() as client:
        yield client


@pytest.fixture(scope="session")
def api_key():
    load_dotenv()
    api_key = os.getenv("API_KEY")
    return api_key
