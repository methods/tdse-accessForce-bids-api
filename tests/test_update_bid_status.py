from unittest.mock import patch


# Case 1: Successful update
@patch("api.controllers.bid_controller.db")
def test_update_bid_status_success(mock_db, test_client):
    mock_db["bids"].find_one.return_value = {
        "_id": "4141fac8-8879-4169-a46d-2effb1f515f6",
        "alias": "ONS",
        "bid_date": "2023-06-23",
        "bid_folder_url": "https://organisation.sharepoint.com/Docs/dummyfolder",
        "client": "Office for National Statistics",
        "failed": None,
        "feedback": None,
        "last_updated": "2023-07-24T11:38:20.388019",
        "links": {
            "questions": "http://localhost:8080/bids/4141fac8-8879-4169-a46d-2effb1f515f6/questions",
            "self": "http://localhost:8080/bids/4141fac8-8879-4169-a46d-2effb1f515f6",
        },
        "status": "in_progress",
        "success": [],
        "tender": "Business Intelligence and Data Warehousing",
        "was_successful": False,
    }

    bid_id = "4141fac8-8879-4169-a46d-2effb1f515f6"
    update = {"status": "completed"}
    response = test_client.put(f"api/bids/{bid_id}/status", json=update)
    mock_db["bids"].find_one.assert_called_once_with({"_id": bid_id})
    # mock_db["bids"].replace_one.assert_called_once()
    assert response.status_code == 200


# Case 2: Invalid status
@patch("api.controllers.bid_controller.db")
def test_invalid_status(mock_db, test_client):
    mock_db["bids"].find_one.return_value = {
        "_id": "4141fac8-8879-4169-a46d-2effb1f515f6",
        "alias": "ONS",
        "bid_date": "2023-06-23",
        "bid_folder_url": "https://organisation.sharepoint.com/Docs/dummyfolder",
        "client": "Office for National Statistics",
        "failed": None,
        "feedback": None,
        "last_updated": "2023-07-24T11:38:20.388019",
        "links": {
            "questions": "http://localhost:8080/bids/4141fac8-8879-4169-a46d-2effb1f515f6/questions",
            "self": "http://localhost:8080/bids/4141fac8-8879-4169-a46d-2effb1f515f6",
        },
        "status": "in_progress",
        "success": [],
        "tender": "Business Intelligence and Data Warehousing",
        "was_successful": False,
    }
    bid_id = "9f688442-b535-4683-ae1a-a64c1a3b8616"
    update = {"status": "invalid"}
    response = test_client.put(f"api/bids/{bid_id}/status", json=update)
    assert response.status_code == 400
    assert (
        response.get_json()["Error"]
        == "{'status': ['Must be one of: deleted, in_progress, completed.']}"
    )


# Case 3: Empty request body
@patch("api.controllers.bid_controller.db")
def test_empty_request(mock_db, test_client):
    bid_id = "9f688442-b535-4683-ae1a-a64c1a3b8616"
    update = {}
    response = test_client.put(f"api/bids/{bid_id}/status", json=update)
    assert response.status_code == 422
    assert response.get_json()["Error"] == "Request must not be empty"


# Case 4: Bid not found
@patch("api.controllers.bid_controller.db")
def test_bid_not_found(mock_db, test_client):
    mock_db["bids"].find_one.return_value = None
    bid_id = "9f688442-b535-4683-ae1a-a64c1a3b8616"
    update = {"status": "completed"}
    response = test_client.put(f"api/bids/{bid_id}/status", json=update)
    assert response.status_code == 404
    assert response.get_json()["Error"] == "Resource not found"


# Case 5: Failed to call database
@patch("api.controllers.bid_controller.db")
def test_update_status_find_error(mock_db, test_client):
    mock_db["bids"].find_one.side_effect = Exception
    bid_id = "9f688442-b535-4683-ae1a-a64c1a3b8616"
    update = {"status": "completed"}
    response = test_client.put(f"api/bids/{bid_id}/status", json=update)
    assert response.status_code == 500
    assert response.get_json() == {"Error": "Could not connect to database"}
