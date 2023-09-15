from unittest.mock import patch


# Case 1: Successful get
@patch("api.controllers.bid_controller.current_app.db")
def test_get_bids_success(mock_db, test_client, api_key, default_limit, default_offset):
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
    mock_db["bids"].count_documents.return_value = len(sample_data)

    response = test_client.get(
        "/api/bids",  # Provide correct query parameters
        headers={"host": "localhost:8080", "X-API-Key": api_key},
    )

    # # Assert the response status code and content
    assert response.status_code == 200
    response_data = response.get_json()
    assert response_data["total_count"] == len(sample_data)
    assert response_data["items"] == sample_data
    assert response_data["limit"] == default_limit
    assert response_data["offset"] == default_offset


# Case 2: Links prepended with hostname
@patch("api.controllers.bid_controller.current_app.db")
def test_links_with_host(mock_db, test_client, api_key):
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
    mock_db["bids"].count_documents.return_value = len(sample_data)

    response = test_client.get(
        "/api/bids", headers={"host": "localhost:8080", "X-API-Key": api_key}
    )
    assert response.status_code == 200
    response_data = response.get_json()
    assert response_data["total_count"] == len(sample_data)
    assert response_data["items"] == sample_data
    assert (
        response_data["items"][0]["links"]["bids"]
        == "http://localhost:8080/bids/faaf8ef5-5db4-459d-8d24-bc39492e1301/bids"
    )
    assert (
        response_data["items"][0]["links"]["self"]
        == "http://localhost:8080/bids/faaf8ef5-5db4-459d-8d24-bc39492e1301"
    )


# Case 3: Connection error
@patch("api.controllers.bid_controller.current_app.db")
def test_get_bids_connection_error(mock_db, test_client, api_key):
    mock_db["bids"].find.side_effect = Exception
    response = test_client.get(
        "/api/bids", headers={"host": "localhost:8080", "X-API-Key": api_key}
    )
    assert response.status_code == 500
    assert response.get_json() == {"Error": "Could not connect to database"}


# Case 4: Unauthorized / invalid api key
@patch("api.controllers.bid_controller.current_app.db")
def test_get_bids_unauthorized(mock_db, test_client):
    response = test_client.get(
        "/api/bids", headers={"host": "localhost:8080", "X-API-Key": "INVALID_API_KEY"}
    )
    assert response.status_code == 401
    assert response.get_json()["Error"] == "Unauthorized"


# Case 5: Invalid offset - greater than maximum
@patch("api.controllers.bid_controller.current_app.db")
def test_get_bids_max_offset(mock_db, test_client, api_key, max_offset):
    invalid_offset = int(max_offset) + 1
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

    mock_db["bids"].count_documents.return_value = len(sample_data)

    # Make a request to the endpoint to get the bids
    response = test_client.get(
        f"api/bids?offset={invalid_offset}",
        headers={"host": "localhost:8080", "X-API-Key": api_key},
    )

    assert response.status_code == 400
    assert (
        response.get_json()["Error"]
        == f"Offset value must be a number between 0 and {max_offset}"
    )


# Case 6: Invalid offset - not a number
@patch("api.controllers.bid_controller.current_app.db")
def test_get_bids_nan_offset(mock_db, test_client, api_key, max_offset):
    invalid_offset = "five"
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

    mock_db["bids"].count_documents.return_value = len(sample_data)

    # Make a request to the endpoint to get the bids
    response = test_client.get(
        f"api/bids?offset={invalid_offset}",
        headers={"host": "localhost:8080", "X-API-Key": api_key},
    )

    assert response.status_code == 400
    assert (
        response.get_json()["Error"]
        == f"Offset value must be a number between 0 and {max_offset}"
    )


# Case 7: Invalid offset - negative number
@patch("api.controllers.bid_controller.current_app.db")
def test_get_bids_negative_offset(mock_db, test_client, api_key, max_offset):
    invalid_offset = -1
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

    mock_db["bids"].count_documents.return_value = len(sample_data)

    # Make a request to the endpoint to get the bids
    response = test_client.get(
        f"api/bids?offset={invalid_offset}",
        headers={"host": "localhost:8080", "X-API-Key": api_key},
    )

    assert response.status_code == 400
    assert (
        response.get_json()["Error"]
        == f"Offset value must be a number between 0 and {max_offset}"
    )


# Case 8: Invalid limit - greater than maximum
@patch("api.controllers.bid_controller.current_app.db")
def test_get_bids_max_limit(mock_db, test_client, api_key, max_limit):
    invalid_limit = int(max_limit) + 1
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

    mock_db["bids"].count_documents.return_value = len(sample_data)

    # Make a request to the endpoint to get the bids
    response = test_client.get(
        f"api/bids?limit={invalid_limit}",
        headers={"host": "localhost:8080", "X-API-Key": api_key},
    )

    assert response.status_code == 400
    assert (
        response.get_json()["Error"]
        == f"Limit value must be a number between 0 and {max_limit}"
    )


# Case 9: Invalid limit - not a number
@patch("api.controllers.bid_controller.current_app.db")
def test_get_bids_nan_limit(mock_db, test_client, api_key, max_limit):
    invalid_limit = "five"
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

    mock_db["bids"].count_documents.return_value = len(sample_data)

    # Make a request to the endpoint to get the bids
    response = test_client.get(
        f"api/bids?limit={invalid_limit}",
        headers={"host": "localhost:8080", "X-API-Key": api_key},
    )

    assert response.status_code == 400
    assert (
        response.get_json()["Error"]
        == f"Limit value must be a number between 0 and {max_limit}"
    )


# Case 10: Invalid limit - negative number
@patch("api.controllers.bid_controller.current_app.db")
def test_get_bids_negative_limit(mock_db, test_client, api_key, max_limit):
    invalid_limit = -1
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

    mock_db["bids"].count_documents.return_value = len(sample_data)

    # Make a request to the endpoint to get the bids
    response = test_client.get(
        f"api/bids?limit={invalid_limit}",
        headers={"host": "localhost:8080", "X-API-Key": api_key},
    )

    assert response.status_code == 400
    assert (
        response.get_json()["Error"]
        == f"Limit value must be a number between 0 and {max_limit}"
    )
