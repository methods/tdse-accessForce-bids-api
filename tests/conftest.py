import pytest
from flask import Flask
from api.controllers.bid_controller import bid


@pytest.fixture
def test_client():
    app = Flask(__name__)
    app.register_blueprint(bid, url_prefix="/api")
    with app.test_client() as client:
        yield client
