from flask import Flask
from datetime import datetime
import pytest

from api.controllers.bid_controller import bid


@pytest.fixture   
def client():
    app = Flask(__name__)
    app.register_blueprint(bid, url_prefix='/api')
    with app.test_client() as client:
        yield client

# Case 1: Valid data
def test_post_is_valid(client):
    data = {
        "tender": "Sample Tender",
        "client": "Sample Client",
        "bid_date": "20-06-2023",
        "alias": "Sample Alias",
        "bid_folder_url": "https://example.com/bid",
        "feedback":{
            "feedback_description": "Sample feedback",
            "feedback_url": "https://example.com/feedback"
        }
    }
    response = client.post("api/bids", json=data)
    assert response.status_code == 201
    assert response.get_json() is not None
    assert response.get_json().get("id") is not None
    assert response.get_json().get("tender") == data.get("tender")
    assert response.get_json().get("client") == data.get("client")
    assert response.get_json().get("bid_date") == datetime.strptime(data.get("bid_date"), "%d-%m-%Y").isoformat()
    assert response.get_json().get("alias") == data.get("alias")
    assert response.get_json().get("bid_folder_url") == data.get("bid_folder_url")
    assert response.get_json().get("feedback") is not None
    assert response.get_json().get("feedback_description") == data.get("feedback_description")
    assert response.get_json().get("feedback_url") == data.get("feedback_url")
    
# Case 2: Missing mandatory fields
def test_field_missing(client):
    data = {
        "client": "Sample Client",
        "bid_date": "20-06-2023"
    }
    response = client.post("api/bids", json=data)
    assert response.status_code == 400
    assert response.get_json().get("error") == "Missing mandatory field: tender"

# Case 3: Invalid JSON
def test_post_is_invalid(client):
    response = client.post("api/bids", data="Invalid JSON")
    assert response.status_code == 400
    assert response.get_json().get("error") == "Invalid JSON"