from unittest.mock import patch


# Case 1: Successful update
@patch("api.controllers.bid_controller.dbConnection")
def test_update_bid_by_id_success(mock_dbConnection, client):
    mock_db = mock_dbConnection.return_value
    mock_db["bids"].find_one_and_update.return_value = {
        "_id": "9f688442-b535-4683-ae1a-a64c1a3b8616",
        "tender": "Business Intelligence and Data Warehousing",
        "alias": "ONS",
        "bid_date": "2023-06-23",
        "bid_folder_url": "https://organisation.sharepoint.com/Docs/dummyfolder",
        "client": "Office for National Statistics",
        "was_successful": False,
    }

    bid_id = "9f688442-b535-4683-ae1a-a64c1a3b8616"
    update = {"tender": "UPDATED TENDER"}
    response = client.put(f"api/bids/{bid_id}", json=update)
    mock_dbConnection.assert_called_once()
    mock_db["bids"].find_one_and_update.assert_called_once()
    assert response.status_code == 200


# Case 2: Invalid user input
@patch("api.controllers.bid_controller.dbConnection")
def test_input_validation(mock_dbConnection, client):
    bid_id = "9f688442-b535-4683-ae1a-a64c1a3b8616"
    update = {"tender": 42}
    response = client.put(f"api/bids/{bid_id}", json=update)
    assert response.status_code == 400
    assert response.get_json()["Error"] == "{'tender': ['Not a valid string.']}"


# Case 3: Bid not found
@patch("api.controllers.bid_controller.dbConnection")
def test_bid_not_found(mock_dbConnection, client):
    mock_db = mock_dbConnection.return_value
    mock_db["bids"].find_one_and_update.return_value = None
    bid_id = "9f688442-b535-4683-ae1a-a64c1a3b8616"
    update = {"tender": "Updated tender"}
    response = client.put(f"api/bids/{bid_id}", json=update)
    assert response.status_code == 404
    assert response.get_json()["Error"] == "Resource not found"


# Case 4: Cannot update status
@patch("api.controllers.bid_controller.dbConnection")
def test_cannot_update_status(mock_dbConnection, client):
    bid_id = "9f688442-b535-4683-ae1a-a64c1a3b8616"
    update = {"status": "deleted"}
    response = client.put(f"api/bids/{bid_id}", json=update)
    assert response.status_code == 422
    assert response.get_json()["Error"] == "Cannot update status"


# Case 5: Failed to call database
@patch("api.controllers.bid_controller.dbConnection")
def test_update_by_id_find_error(mock_dbConnection, client):
    mock_db = mock_dbConnection.return_value
    mock_db["bids"].find_one_and_update.side_effect = Exception
    bid_id = "9f688442-b535-4683-ae1a-a64c1a3b8616"
    update = {"tender": "Updated tender"}
    response = client.put(f"api/bids/{bid_id}", json=update)
    assert response.status_code == 500
    assert response.get_json() == {"Error": "Could not connect to database"}
