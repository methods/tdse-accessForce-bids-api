from unittest.mock import patch
from pymongo.errors import ConnectionFailure

# Case 1: Successful post
@patch('api.controllers.bid_controller.dbConnection')
def test_post_is_successful(mock_dbConnection, client):
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
    mock_db = mock_dbConnection.return_value
    mock_db['bids'].insert_one.return_value = data

    response = client.post("api/bids", json=data)
    assert response.status_code == 201
    assert "_id" in response.get_json() and response.get_json()["_id"] is not None  
    assert "tender" in response.get_json() and response.get_json()["tender"] == "Business Intelligence and Data Warehousing"
    assert "client" in response.get_json() and response.get_json()["client"] == "Office for National Statistics"
    assert "last_updated" in response.get_json() and response.get_json()["last_updated"] is not None
    assert "bid_date" in response.get_json() and response.get_json()["bid_date"] == "2023-06-21"


# Case 2: Missing mandatory fields
def test_field_missing(client):
    data = {
        "client": "Sample Client",
        "bid_date": "20-06-2023"
    }
    
    response = client.post("api/bids", json=data)
    assert response.status_code == 400
    assert response.get_json() == {
        'Error': "{'tender': {'message': 'Missing mandatory field'}}"
    }


# Case 3: Connection error
@patch('api.controllers.bid_controller.dbConnection', side_effect=ConnectionFailure)
def test_get_bids_connection_error(mock_dbConnection, client):
     # Mock the behavior of dbConnection
    mock_db = mock_dbConnection.return_value
    mock_db['bids'].insert_one.side_effect = Exception
    response = client.get('/api/bids')
    assert response.status_code == 500
    assert response.get_json() == {"Error": "Could not connect to database"}


# Case 4: Neither success nor failed fields phase can be more than 2
@patch('api.controllers.bid_controller.dbConnection')
def test_phase_greater_than_2(mock_dbConnection, client):
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
    mock_db = mock_dbConnection.return_value
    mock_db['bids'].insert_one.side_effect = Exception

    response = client.post("api/bids", json=data)
    assert response.status_code == 400
    assert response.get_json() == {
        'Error': "{'failed': {'phase': ['Must be one of: 1, 2.']}}"
    }


# Case 5: Neither success nor failed fields can have the same phase
@patch('api.controllers.bid_controller.dbConnection')
def test_same_phase(mock_dbConnection, client):
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
    mock_db = mock_dbConnection.return_value
    mock_db['bids'].insert_one.side_effect = Exception

    response = client.post("api/bids", json=data)
    assert response.status_code == 400
    assert response.get_json() == {
        'Error': "{'success': [\"Phase value already exists in 'failed' section and cannot be repeated.\"]}"
    }


# Case 6: Success cannot have the same phase in the list
@patch('api.controllers.bid_controller.dbConnection')
def test_success_same_phase(mock_dbConnection, client):
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
    mock_db = mock_dbConnection.return_value
    mock_db['bids'].insert_one.side_effect = Exception

    response = client.post("api/bids", json=data)
    assert response.status_code == 400
    assert response.get_json() == {
        'Error': "{'success': [\"Phase value already exists in 'success' list and cannot be repeated.\"]}"
    }
