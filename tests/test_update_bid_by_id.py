import ast
from unittest.mock import patch

# Case 1: Successful update
@patch('api.controllers.bid_controller.dbConnection')
def test_update_bid_by_id_success(mock_dbConnection, client):
    mock_db = mock_dbConnection.return_value
    mock_db['bids'].find_one_and_replace.return_value = {
        "_id": "9f688442-b535-4683-ae1a-a64c1a3b8616",
        "tender": "Business Intelligence and Data Warehousing",
        "alias": "ONS",
        "bid_date": "2023-06-23",
        "bid_folder_url": "https://organisation.sharepoint.com/Docs/dummyfolder",
        "client": "Office for National Statistics",
        "was_successful": False
    }

    bid_id = '9f688442-b535-4683-ae1a-a64c1a3b8616'
    updated_bid = {
        "tender": "UPDATED TENDER",
        "alias": "ONS",
        "bid_date": "21-06-2023",
        "bid_folder_url": "https://organisation.sharepoint.com/Docs/dummyfolder",
        "client": "Office for National Statistics",
        "was_successful": False
    }
    response = client.put(f"api/bids/{bid_id}", json=updated_bid)

    assert response.status_code == 200
    assert response.get_json()["tender"] == "UPDATED TENDER"
    assert "last_updated" in response.get_json() and response.get_json()["last_updated"] is not None
    assert response.get_json()["links"] is not None
    assert "self" in response.get_json()["links"]
    assert response.get_json()["links"]["self"] == f"/bids/{bid_id}"
    assert 'questions' in response.get_json()["links"]
    assert response.get_json()["links"]["questions"] == f"/bids/{bid_id}/questions"

# Case 2: Invalid user input
@patch('api.controllers.bid_controller.dbConnection')
def test_input_validation(mock_dbConnection, client):
    mock_db = mock_dbConnection.return_value
    mock_db['bids'].find_one_and_replace.return_value = {
        "_id": "9f688442-b535-4683-ae1a-a64c1a3b8616",
        "tender": "Business Intelligence and Data Warehousing",
        "alias": "ONS",
        "bid_date": "2023-06-23",
        "bid_folder_url": "https://organisation.sharepoint.com/Docs/dummyfolder",
        "client": "Office for National Statistics",
        "was_successful": False
    }

    bid_id = '9f688442-b535-4683-ae1a-a64c1a3b8616'
    updated_bid = {
        "tender": 42,
        "alias": "ONS",
        "bid_date": "2023-12-25",
        "bid_folder_url": "Not a valid URL",
        "client": 7,
        "was_successful": "String"
    }
    response = client.put(f"api/bids/{bid_id}", json=updated_bid)
    error_message = ast.literal_eval(response.get_json()["Error"])
    expected_errors = {
            'bid_folder_url': ['Not a valid URL.'],
            'client': ['Not a valid string.'],
            'tender': ['Not a valid string.'],
            'was_successful': ['Not a valid boolean.'],
            'bid_date': ['Not a valid date.']
        }

    assert response.status_code == 400
    assert expected_errors.items() <= error_message.items()