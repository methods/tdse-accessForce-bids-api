"""
This file contains tests for the update_bid_by_id endpoint
"""
from unittest.mock import patch


# Case 1: Successful update
@patch("api.controllers.bid_controller.current_app.db")
def test_update_bid_by_id_success(mock_db, test_client, basic_jwt):
    mock_db["bids"].find_one.return_value = {
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
    response = test_client.put(
        f"api/bids/{bid_id}",
        json=update,
        headers={"Authorization": f"Bearer {basic_jwt}"},
    )
    mock_db["bids"].find_one.assert_called_once_with(
        {"_id": bid_id, "status": "in_progress"}
    )
    mock_db["bids"].replace_one.assert_called_once()
    assert response.status_code == 200
    assert response.get_json()["tender"] == "UPDATED TENDER"


# Case 2: Invalid user input
@patch("api.controllers.bid_controller.current_app.db")
def test_input_validation(mock_db, test_client, basic_jwt):
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
    update = {"tender": 42}
    response = test_client.put(
        f"api/bids/{bid_id}",
        json=update,
        headers={"Authorization": f"Bearer {basic_jwt}"},
    )
    assert response.status_code == 400
    assert response.get_json()["Error"] == "{'tender': ['Not a valid string.']}"


# Case 3: Bid not found
@patch("api.controllers.bid_controller.current_app.db")
def test_bid_not_found(mock_db, test_client, basic_jwt):
    mock_db["bids"].find_one.return_value = None
    bid_id = "9f688442-b535-4683-ae1a-a64c1a3b8616"
    update = {"tender": "Updated tender"}
    response = test_client.put(
        f"api/bids/{bid_id}",
        json=update,
        headers={"Authorization": f"Bearer {basic_jwt}"},
    )
    assert response.status_code == 404
    assert response.get_json()["Error"] == "Resource not found"


# Case 4: Cannot update status
@patch("api.controllers.bid_controller.current_app.db")
def test_cannot_update_status(mock_db, test_client, basic_jwt):
    bid_id = "9f688442-b535-4683-ae1a-a64c1a3b8616"
    update = {"status": "deleted"}
    response = test_client.put(
        f"api/bids/{bid_id}",
        json=update,
        headers={"Authorization": f"Bearer {basic_jwt}"},
    )
    assert response.status_code == 422
    assert response.get_json()["Error"] == "Cannot update status"


# Case 5: Failed to call database
@patch("api.controllers.bid_controller.current_app.db")
def test_update_by_id_find_error(mock_db, test_client, basic_jwt):
    mock_db["bids"].find_one.return_value = {
        "_id": "9f688442-b535-4683-ae1a-a64c1a3b8616",
        "tender": "Business Intelligence and Data Warehousing",
        "alias": "ONS",
        "bid_date": "2023-06-23",
        "bid_folder_url": "https://organisation.sharepoint.com/Docs/dummyfolder",
        "client": "Office for National Statistics",
        "was_successful": False,
    }
    mock_db["bids"].find_one.side_effect = Exception
    bid_id = "9f688442-b535-4683-ae1a-a64c1a3b8616"
    update = {"tender": "Updated tender"}
    response = test_client.put(
        f"api/bids/{bid_id}",
        json=update,
        headers={"Authorization": f"Bearer {basic_jwt}"},
    )
    assert response.status_code == 500
    assert response.get_json() == {"Error": "Could not connect to database"}


# Case 6: Update failed field
@patch("api.controllers.bid_controller.current_app.db")
def test_update_failed(mock_db, test_client, basic_jwt):
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
    update = {"failed": {"phase": 2, "has_score": True, "score": 20, "out_of": 36}}
    response = test_client.put(
        f"api/bids/{bid_id}",
        json=update,
        headers={"Authorization": f"Bearer {basic_jwt}"},
    )
    mock_db["bids"].find_one.assert_called_once_with(
        {"_id": bid_id, "status": "in_progress"}
    )
    mock_db["bids"].replace_one.assert_called_once()
    assert response.status_code == 200


# Case 7: Update success field
@patch("api.controllers.bid_controller.current_app.db")
def test_update_success(mock_db, test_client, basic_jwt):
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
    update = {
        "success": [
            {"phase": 1, "has_score": True, "score": 20, "out_of": 36},
            {"phase": 2, "has_score": True, "score": 20, "out_of": 36},
        ]
    }
    response = test_client.put(
        f"api/bids/{bid_id}",
        json=update,
        headers={"Authorization": f"Bearer {basic_jwt}"},
    )
    mock_db["bids"].find_one.assert_called_once_with(
        {"_id": bid_id, "status": "in_progress"}
    )
    mock_db["bids"].replace_one.assert_called_once()
    assert response.status_code == 200


# Case 8: Unauthorized - invalid token
@patch("api.controllers.bid_controller.current_app.db")
def test_update_bid_by_id_unauthorized(mock_db, test_client, basic_jwt):
    mock_db["bids"].find_one.return_value = {
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
    response = test_client.put(
        f"api/bids/{bid_id}",
        json=update,
        headers={"Authorization": "Bearer N0tV4l1djsonW3Bt0K3n"},
    )
    assert response.status_code == 401
    assert response.get_json() == {"Error": "Unauthorized"}
