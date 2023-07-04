from flask import Flask
from datetime import datetime
import pytest
import json
from unittest.mock import patch, MagicMock
from bson import ObjectId
from pymongo.errors import ConnectionFailure
from marshmallow import ValidationError
from flask import jsonify
from dbconfig.mongo_setup import dbConnection


from api.controllers.bid_controller import bid


@pytest.fixture   
def client():
    app = Flask(__name__)
    app.register_blueprint(bid, url_prefix='/api')
    with app.test_client() as client:
        yield client

def test_post_bid(client):
    # Mock the necessary objects and methods
    request_data = {
        "tender": "Business Intelligence and request_data Warehousing",
        "client": "Office for National Statistics",
        "bid_date": "21-06-2023",
        "alias": "ONS",
        "bid_folder_url": "https://organisation.sharepoint.com/Docs/dummyfolder",
        "feedback": {
            "description": "Feedback from client in detail",
            "url": "https://organisation.sharepoint.com/Docs/dummyfolder/feedback"
        },
        "success": [
            {
            "phase": 1,
            "has_score": True,
            "score": 28,
            "out_of": 36
            },
            {
            "phase": 2,
            "has_score": False
            }
        ],
        "failed": {
            "phase": 3,
            "has_score": True,
            "score": 20,
            "out_of": 36
            }
        }
    mock_db = MagicMock()
    mock_db_connection = MagicMock(return_value=mock_db)
    mock_bids = MagicMock()
    # mock_bids.insert_one.return_value = ObjectId("60e8b7a57cdef32e1cfe3a1b")

    # Patch the required methods and objects with the mocks
    with patch("dbconfig.mongo_setup.dbConnection", mock_db_connection), \
      patch("api.controllers.bid_controller.BidSchema.dump", return_value=request_data), \
        patch("api.controllers.bid_controller.BidSchema.load", return_value=request_data), \
          patch("api.controllers.bid_controller.BidSchema.validate", return_value=True), \
             patch("dbconfig.mongo_setup.dbConnection.db['bids']", mock_bids):
        # Make a POST request to the API endpoint
        response = client.post("api/bids", json=request_data)

    # Assert the response
    actual_response = json.loads(response.data)
    expected_response = {
        "_id": f"{actual_response['_id']}",
        "alias": "ONS",
        "bid_date": "2023-06-21",
        "bid_folder_url": "https://organisation.sharepoint.com/Docs/dummyfolder",
        "client": "Office for National Statistics",
        "failed": {
            "has_score": True,
            "out_of": 36,
            "phase": 3,
            "score": 20
        },
        "feedback": {
            "description": "Feedback from client in detail",
            "url": "https://organisation.sharepoint.com/Docs/dummyfolder/feedback"
        },
        "last_updated": f"{actual_response['last_updated']}",
        "links": {
            "questions": f"/bids/{actual_response['_id']}/questions",
            "self": f"/bids/{actual_response['_id']}"
        },
        "status": "in_progress",
        "success": [
            {
            "has_score": True,
            "out_of": 36,
            "phase": 1,
            "score": 28
            },
            {
            "has_score": False,
            "phase": 2
            }
        ],
        "tender": "Business Intelligence and Data Warehousing",
        "was_successful": False
    }

    # assert response.status_code == 201
    # assert actual_response == expected_response
    
    # # Assert that the necessary methods were called
    assert response.status_code == 201
    assert response.get_json() is not None
    assert response.get_json().get("_id") is not None
    assert response.get_json().get("tender") == request_data.get("tender")
    assert response.get_json().get("client") == request_data.get("client")
    assert response.get_json().get("bid_date") == datetime.strptime(request_data.get("bid_date"), "%d-%m-%Y").isoformat()
    assert response.get_json().get("alias") == request_data.get("alias")
    assert response.get_json().get("bid_folder_url") == request_data.get("bid_folder_url")
    assert response.get_json().get("feedback") is not None
    assert response.get_json().get("feedback_description") == request_data.get("feedback_description")
    assert response.get_json().get("feedback_url") == request_data.get("feedback_url")

    # # Assert that the necessary methods were called
    # mock_db_connection.assert_called_once()
    # mock_bids.insert_one.assert_called_once_with(request_data)

def test_post_bid_validation_error(client):
    # Mock the necessary objects and methods
    request_data = {
  "tender": 42,
  "bid_folder_url": "https://organisation.sharepoint.com/Docs/dummyfolder",
  "last_updated": "2023-06-27T14:05:17.623827",
  "failed": {
    "phase": 2,
    "score": 22,
    "has_score": True,
    "out_of": 36
  },
  "feedback": {
    "url": "https://organisation.sharepoint.com/Docs/dummyfolder/feedback",
    "description": "Feedback from client in detail"
  },
  "success": [
    {
      "phase": 2,
      "score": 22,
      "has_score": True,
      "out_of": 36
    }
  ],
  "alias": "ONS",
  "client": "Office for National Statistics",
  "links": {
    "questions": "https://localhost:8080/api//bids/96d69775-29af-46b1-aaf4-bfbdb1543412/questions",
    "self": "https://localhost:8080/api/bids/471fea1f-705c-4851-9a5b-df7bc2651428"
  },
  "_id": "UUID('471fea1f-705c-4851-9a5b-df7bc2651428')",
  "bid_date": "2023-06-21T00:00:00",
  "status": "in_progress",
  "was_successful": True
}

    # Patch the required methods and objects with the mocks
    with patch("api.controllers.bid_controller.BidRequestSchema.load", side_effect=ValidationError("Invalid data")):
        # Make a POST request to the API endpoint
        response = client.post("api/bids", json=request_data)

    # Assert the response
    assert response.status_code == 400
    assert json.loads(response.data) == {"Error": "Invalid data"}

def test_post_bid_connection_failure(client):
    # Mock the necessary objects and methods
    request_data = {
  "tender": "Business Intelligence and Data Warehousing",
  "bid_folder_url": "https://organisation.sharepoint.com/Docs/dummyfolder",
  "last_updated": "2023-06-27T14:05:17.623827",
  "failed": {
    "phase": 2,
    "score": 22,
    "has_score": True,
    "out_of": 36
  },
  "feedback": {
    "url": "https://organisation.sharepoint.com/Docs/dummyfolder/feedback",
    "description": "Feedback from client in detail"
  },
  "success": [
    {
      "phase": 2,
      "score": 22,
      "has_score": True,
      "out_of": 36
    }
  ],
  "alias": "ONS",
  "client": "Office for National Statistics",
  "links": {
    "questions": "https://localhost:8080/api//bids/96d69775-29af-46b1-aaf4-bfbdb1543412/questions",
    "self": "https://localhost:8080/api/bids/471fea1f-705c-4851-9a5b-df7bc2651428"
  },
  "_id": "UUID('471fea1f-705c-4851-9a5b-df7bc2651428')",
  "bid_date": "2023-06-21T00:00:00",
  "status": "in_progress",
  "was_successful": True
}
    mock_db_connection = MagicMock(side_effect=ConnectionFailure)

    # Patch the required methods and objects with the mocks
    with patch("api.controllers.bid_controller.dbConnection", mock_db_connection), \
            patch("api.controllers.bid_controller.BidSchema.dump", return_value=request_data):
        # Make a POST request to the API endpoint
        response = client.post("api/bids", json=request_data)

    # Assert the response
    assert response.status_code == 500
    assert json.loads(response.data) == {"Error": "Could not connect to database"}

# Note: The above tests assume you have a Flask test client available as `client`.


# # Case 1: Valid data
# def test_post_is_valid(client):
#     data = {
#         "tender": "Sample Tender",
#         "client": "Sample Client",
#         "bid_date": "20-06-2023",
#         "alias": "Sample Alias",
#         "bid_folder_url": "https://example.com/bid",
#         "feedback":{
#             "feedback_description": "Sample feedback",
#             "feedback_url": "https://example.com/feedback"
#         }
#     }

    
# # Case 2: Missing mandatory fields
# def test_field_missing(client):
#     data = {
#         "client": "Sample Client",
#         "bid_date": "20-06-2023"
#     }
#     response = client.post("api/bids", json=data)
#     assert response.status_code == 400
#     assert response.get_json().get("error") == "Missing mandatory field: tender"

# # Case 3: Invalid JSON
# def test_post_is_invalid(client):
#     response = client.post("api/bids", data="Invalid JSON")
#     assert response.status_code == 400
#     assert response.get_json().get("error") == "Invalid JSON"

if __name__ == "__main__":
    pytest.main()