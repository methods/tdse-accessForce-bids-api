from unittest.mock import patch


# Import the necessary modules
from unittest.mock import patch


# Case 1: Successful get
@patch("api.controllers.bid_controller.db")
def test_get_bids_success(mock_db, test_client, api_key):
    # Mock the find method of the db object
    sample_data = [
        {
            "_id": "1ff45b42-b72a-464c-bde9-9bead14a07b9",
            "bid_date": "2023-06-23",
            "client": "Office for National Statistics",
            "links": {
                "bids": "/bids/faaf8ef5-5db4-459d-8d24-bc39492e1301/bids",
                "self": "/bids/faaf8ef5-5db4-459d-8d24-bc39492e1301",
            },
            "status": "in_progress",
            "tender": "Business Intelligence and Data Warehousing",
        }
    ]
    mock_db["bids"].find.return_value = sample_data
    # mock_db["bids"].find.return_value.skip.return_value.limit.return_value = sample_data
    mock_db["bids"].count_documents.return_value = len(sample_data)

    response = test_client.get(
        "/api/bids",  # Provide correct query parameters
        headers={"host": "localhost:8080", "X-API-Key": api_key},
    )

    # # Assert the response status code and content
    assert response.status_code == 200
    response_data = response.get_json()
    assert response_data["total_count"] == len(sample_data)
    assert response_data["data"] == sample_data
    assert response_data["limit"] == 5
    assert response_data["offset"] == 0


# Case 2: Links prepended with hostname
@patch("api.controllers.bid_controller.db")
def test_links_with_host(mock_db, test_client, api_key):
    sample_data = [
        {
            "_id": "1ff45b42-b72a-464c-bde9-9bead14a07b9",
            "bid_date": "2023-06-23",
            "client": "Office for National Statistics",
            "links": {
                "questions": "/bids/faaf8ef5-5db4-459d-8d24-bc39492e1301/questions",
                "self": "/bids/faaf8ef5-5db4-459d-8d24-bc39492e1301",
            },
            "status": "in_progress",
            "tender": "Business Intelligence and Data Warehousing",
        }
    ]

    mock_db["bids"].find.return_value = sample_data
    mock_db["bids"].count_documents.return_value = len(sample_data)

    response = test_client.get(
        "/api/bids", headers={"host": "localhost:8080", "X-API-Key": api_key}
    )
    assert response.status_code == 200
    response_data = response.get_json()
    assert response_data["total_count"] == len(sample_data)
    assert response_data["data"] == sample_data
    assert response_data["limit"] == 5
    assert response_data["offset"] == 0
    assert (
        response_data["data"][0]["links"]["questions"]
        == "http://localhost:8080/bids/faaf8ef5-5db4-459d-8d24-bc39492e1301/questions"
    )
    assert (
        response_data["data"][0]["links"]["self"]
        == "http://localhost:8080/bids/faaf8ef5-5db4-459d-8d24-bc39492e1301"
    )


# Case 3: Connection error
@patch("api.controllers.bid_controller.db")
def test_get_bids_connection_error(mock_db, test_client, api_key):
    mock_db["bids"].find.side_effect = Exception
    response = test_client.get(
        "/api/bids", headers={"host": "localhost:8080", "X-API-Key": api_key}
    )
    assert response.status_code == 500
    assert response.get_json() == {"Error": "Could not connect to database"}


# Case 4: Unauthorized / invalid api key
@patch("api.controllers.bid_controller.db")
def test_get_bids_unauthorized(mock_db, test_client):
    response = test_client.get(
        "/api/bids", headers={"host": "localhost:8080", "X-API-Key": "INVALID_API_KEY"}
    )
    assert response.status_code == 401
    assert response.get_json()["Error"] == "Unauthorized"
