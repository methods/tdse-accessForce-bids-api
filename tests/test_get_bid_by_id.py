from unittest.mock import patch


# Case 1: Successful get_bid_by_id
@patch("api.controllers.bid_controller.db")
def test_get_bid_by_id_success(mock_db, test_client, api_key):
    mock_db["bids"].find_one.return_value = {
        "_id": "1ff45b42-b72a-464c-bde9-9bead14a07b9",
        "alias": "ONS",
        "bid_date": "2023-06-23",
        "bid_folder_url": "https://organisation.sharepoint.com/Docs/dummyfolder",
        "client": "Office for National Statistics",
        "links": {
            "questions": "/bids/faaf8ef5-5db4-459d-8d24-bc39492e1301/questions",
            "self": "/bids/faaf8ef5-5db4-459d-8d24-bc39492e1301",
        },
        "status": "in_progress",
        "tender": "Business Intelligence and Data Warehousing",
        "was_successful": False,
    }

    response = test_client.get(
        "/api/bids/1ff45b42-b72a-464c-bde9-9bead14a07b9",
        headers={"host": "localhost:8080", "X-API-Key": api_key},
    )

    mock_db["bids"].find_one.assert_called_once_with(
        {"_id": "1ff45b42-b72a-464c-bde9-9bead14a07b9", "status": {"$ne": "deleted"}}
    )
    assert response.status_code == 200
    assert response.get_json() == {
        "_id": "1ff45b42-b72a-464c-bde9-9bead14a07b9",
        "alias": "ONS",
        "bid_date": "2023-06-23",
        "bid_folder_url": "https://organisation.sharepoint.com/Docs/dummyfolder",
        "client": "Office for National Statistics",
        "links": {
            "questions": "http://localhost:8080/bids/faaf8ef5-5db4-459d-8d24-bc39492e1301/questions",
            "self": "http://localhost:8080/bids/faaf8ef5-5db4-459d-8d24-bc39492e1301",
        },
        "status": "in_progress",
        "tender": "Business Intelligence and Data Warehousing",
        "was_successful": False,
    }


# Case 2: Connection error
@patch("api.controllers.bid_controller.db", side_effect=Exception)
def test_get_bid_by_id_connection_error(mock_db, test_client, api_key):
    mock_db["bids"].find_one.side_effect = Exception
    response = test_client.get(
        "/api/bids/1ff45b42-b72a-464c-bde9-9bead14a07b9",
        headers={"host": "localhost:8080", "X-API-Key": api_key},
    )
    assert response.status_code == 500
    assert response.get_json() == {"Error": "Could not connect to database"}


# Case 3: Bid not found
@patch("api.controllers.bid_controller.db")
def test_get_bid_by_id_not_found(mock_db, test_client, api_key):
    mock_db["bids"].find_one.return_value = None

    response = test_client.get(
        "/api/bids/1ff45b42-b72a-464c-bde9-9bead14a07b9",
        headers={"host": "localhost:8080", "X-API-Key": api_key},
    )

    mock_db["bids"].find_one.assert_called_once_with(
        {"_id": "1ff45b42-b72a-464c-bde9-9bead14a07b9", "status": {"$ne": "deleted"}}
    )
    assert response.status_code == 404
    assert response.get_json() == {"Error": "Resource not found"}


# Case 4: Validation error
@patch("api.controllers.bid_controller.db")
def test_get_bid_by_id_validation_error(mock_db, test_client, api_key):
    response = test_client.get(
        "/api/bids/invalid_bid_id",
        headers={"host": "localhost:8080", "X-API-Key": api_key},
    )
    assert response.status_code == 400
    assert response.get_json() == {"Error": "{'id': ['Invalid Id']}"}
