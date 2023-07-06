import pytest
from flask import Flask
from unittest.mock import patch, MagicMock
from pymongo.errors import ConnectionFailure

from api.controllers.bid_controller import bid


@pytest.fixture
def client():
    app = Flask(__name__)
    app.register_blueprint(bid, url_prefix='/api')
    with app.test_client() as client:
        yield client

# Case 1: Successful post
def test_post_is_successful(client):
    data = {
        "tender": "Business Intelligence and Data Warehousing",
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
                "out_of": 36,
                "score": 30
            }
        ],
        "failed": {
            "phase": 2,
            "has_score": True,
            "score": 20,
            "out_of": 36
        }
    }

    # Mock the behavior of dbConnection
    with patch('api.controllers.bid_controller.dbConnection') as mock_dbConnection:
        # Create a MagicMock object to simulate the behavior of the insert_one method
        mock_insert_one = MagicMock()
        # Set the return value of db['bids'].insert_one to the MagicMock object
        mock_dbConnection.return_value.__getitem__.return_value.insert_one = mock_insert_one

        response = client.post("api/bids", json=data)
        assert response.status_code == 201
        # Check that the insert_one method was called with the correct argument
        assert response.get_json() == mock_insert_one.call_args[0][0]

# Case 2: Missing mandatory fields
def test_field_missing(client):
    data = {
        "client": "Sample Client",
        "bid_date": "20-06-2023"
    }
    response = client.post("api/bids", json=data)
    # Check that the response status code is 400
    assert response.status_code == 400
    # Check that the response body contains the correct error message with the missing field (tender)
    assert response.get_json() == {
        'Error': "{'tender': {'message': 'Missing mandatory field'}}"}

# Case 3: Connection error
def test_get_bids_connection_error(client):
    # Mock the behavior of dbConnection to raise ConnectionFailure
    with patch('api.controllers.bid_controller.dbConnection', side_effect=ConnectionFailure):
        response = client.get('/api/bids')
        assert response.status_code == 500
        assert response.json == {"Error": "Could not connect to database"}

# Case 4: Neither success nor failed fields phase can be more than 2
def test_phase_greater_than_2(client):
    data = {
        "tender": "Business Intelligence and Data Warehousing",
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
                "out_of": 36,
                "score": 30
            }
        ],
        "failed": {
            "phase": 3,
            "has_score": True,
            "score": 20,
            "out_of": 36
        }
    }

    # Mock the behavior of dbConnection
    with patch('api.controllers.bid_controller.dbConnection') as mock_dbConnection:
        # Create a MagicMock object to simulate the behavior of the insert_one method
        mock_insert_one = MagicMock()
        # Set the return value of db['bids'].insert_one to the MagicMock object
        mock_dbConnection.return_value.__getitem__.return_value.insert_one = mock_insert_one

        response = client.post("api/bids", json=data)
        assert response.status_code == 400
        # Check that the insert_one method was called with the correct argument
        assert response.get_json() == {
            'Error': "{'failed': {'phase': ['Must be one of: 1, 2.']}}"}

# Case 5: Neither success nor failed fields can have the same phase
def test_same_phase(client):
    data = {
        "tender": "Business Intelligence and Data Warehousing",
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
                "out_of": 36,
                "score": 30
            }
        ],
        "failed": {
            "phase": 1,
            "has_score": True,
            "score": 20,
            "out_of": 36
        }
    }
    # Mock the behavior of dbConnection
    with patch('api.controllers.bid_controller.dbConnection') as mock_dbConnection:
        # Create a MagicMock object to simulate the behavior of the insert_one method
        mock_insert_one = MagicMock()
        # Set the return value of db['bids'].insert_one to the MagicMock object
        mock_dbConnection.return_value.__getitem__.return_value.insert_one = mock_insert_one

        response = client.post("api/bids", json=data)
        assert response.status_code == 400
        # Check that the insert_one method was called with the correct argument
        assert response.get_json() == {
            'Error': '{\'success\': ["Phase value already exists in \'failed\' section and cannot be repeated."]}'}

# Case 6: Success can not have the same phase in the list
def test_success_same_phase(client):
    data = {
        "tender": "Business Intelligence and Data Warehousing",
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
                "out_of": 36,
                "score": 30
            },
            {
                "phase": 1,
                "has_score": True,
                "out_of": 50,
                "score": 60
            }
        ],
    }

    # Mock the behavior of dbConnection
    with patch('api.controllers.bid_controller.dbConnection') as mock_dbConnection:
        # Create a MagicMock object to simulate the behavior of the insert_one method
        mock_insert_one = MagicMock()
        # Set the return value of db['bids'].insert_one to the MagicMock object
        mock_dbConnection.return_value.__getitem__.return_value.insert_one = mock_insert_one

        response = client.post("api/bids", json=data)
        assert response.status_code == 400
        # Check that the insert_one method was called with the correct argument
        assert response.get_json() == {
            'Error': '{\'success\': ["Phase value already exists in \'success\' list and cannot be repeated."]}'}
