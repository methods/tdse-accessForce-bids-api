"""
This file contains tests for the GET /bids/{bid_id}/questions endpoint.
"""

from unittest.mock import patch


# Case 1: Successful get
@patch("api.controllers.question_controller.current_app.db")
def test_get_questions_success(
    mock_db, test_client, api_key, default_limit, default_offset
):
    # Set up the sample data and expected result
    sample_bid_id = "66fb5dba-f129-413a-b12e-5a68b5a647d6"
    sample_data = [
        {
            "_id": "2b18f477-627f-4d48-a008-ca0d9cea3791",
            "description": "This is a question",
            "feedback": {
                "description": "Good feedback",
                "url": "https://organisation.sharepoint.com/Docs/dummyfolder",
            },
            "last_updated": "2023-08-01T23:11:59.336092",
            "links": {
                "bid": f"/api/bids/{sample_bid_id}",
                "self": f"/api/bids/{sample_bid_id}/questions/2b18f477-627f-4d48-a008-ca0d9cea3791",
            },
            "out_of": None,
            "question_url": "https://organisation.sharepoint.com/Docs/dummyfolder",
            "respondents": [],
            "response": None,
            "score": None,
            "status": "in_progress",
        },
    ]

    mock_db["questions"].find.return_value = sample_data

    mock_db["questions"].count_documents.return_value = len(sample_data)

    # Make a request to the endpoint to get the questions
    response = test_client.get(
        f"api/bids/{sample_bid_id}/questions",
        headers={"host": "localhost:8080", "X-API-Key": api_key},
    )

    # Assert the response status code and content
    assert response.status_code == 200
    response_data = response.get_json()
    assert response_data["total_count"] == len(sample_data)
    assert response_data["items"] == sample_data
    assert response_data["limit"] == default_limit
    assert response_data["offset"] == default_offset


# Case 2: Links prepended with hostname
@patch("api.controllers.question_controller.current_app.db")
def test_links_with_host(mock_db, test_client, api_key):
    # Set up the sample data and expected result
    sample_bid_id = "66fb5dba-f129-413a-b12e-5a68b5a647d6"
    sample_data = [
        {
            "_id": "2b18f477-627f-4d48-a008-ca0d9cea3791",
            "description": "This is a question",
            "feedback": {
                "description": "Good feedback",
                "url": "https://organisation.sharepoint.com/Docs/dummyfolder",
            },
            "last_updated": "2023-08-01T23:11:59.336092",
            "links": {
                "bid": f"/api/bids/{sample_bid_id}",
                "self": f"/api/bids/{sample_bid_id}/questions/2b18f477-627f-4d48-a008-ca0d9cea3791",
            },
            "out_of": None,
            "question_url": "https://organisation.sharepoint.com/Docs/dummyfolder",
            "respondents": [],
            "response": None,
            "score": None,
            "status": "in_progress",
        }
    ]

    # Mock the database find method to return the filtered sample data
    mock_db["questions"].find.return_value = sample_data

    mock_db["questions"].count_documents.return_value = len(sample_data)

    # Make a request to the endpoint to get the questions
    response = test_client.get(
        f"api/bids/{sample_bid_id}/questions",
        headers={"host": "localhost:8080", "X-API-Key": api_key},
    )

    # Assert the response status code and content
    response_data = response.get_json()
    assert (
        response_data["items"][0]["links"]["bid"]
        == f"http://localhost:8080/api/bids/{sample_bid_id}"
    )

    assert (
        response_data["items"][0]["links"]["self"]
        == f"http://localhost:8080/api/bids/{sample_bid_id}/questions/2b18f477-627f-4d48-a008-ca0d9cea3791"
    )


# Case 3: Connection error
@patch("api.controllers.question_controller.current_app.db")
def test_get_questions_connection_error(mock_db, test_client, api_key):
    # Set up the sample bid ID
    sample_bid_id = "66fb5dba-f129-413a-b12e-5a68b5a647d6"

    # Mock the database find method to raise a ConnectionError
    mock_db["questions"].find.side_effect = Exception

    # Make a request to the endpoint to get the questions
    response = test_client.get(
        f"api/bids/{sample_bid_id}/questions",
        headers={"host": "localhost:8080", "X-API-Key": api_key},
    )

    # Assert the response status code and content
    assert response.status_code == 500
    response_data = response.get_json()
    assert response_data == {"Error": "Could not connect to database"}


# Case 4: Unauthorized / invalid api key
@patch("api.controllers.question_controller.current_app.db")
def test_get_questions_unauthorized(mock_db, test_client):
    # Set up the sample bid ID
    sample_bid_id = "66fb5dba-f129-413a-b12e-5a68b5a647d6"

    # Mock the database find method to return an empty list
    mock_db["questions"].find.return_value = []

    # Make a request to the endpoint to get the questions without providing a JWT
    response = test_client.get(
        f"api/bids/{sample_bid_id}/questions", headers={"host": "localhost:8080"}
    )

    # Assert the response status code and content
    assert response.status_code == 401
    response_data = response.get_json()
    assert response_data == {"Error": "Unauthorized"}

    # Make a request to the endpoint to get the questions with an invalid JWT
    response = test_client.get(
        f"api/bids/{sample_bid_id}/questions",
        headers={"host": "localhost:8080", "Authorization": "Bearer INVALID_JWT"},
    )

    # Assert the response status code and content
    assert response.status_code == 401
    response_data = response.get_json()
    assert response_data == {"Error": "Unauthorized"}


# Case 5: No questions found
@patch("api.controllers.question_controller.current_app.db")
def test_no_questions_found(mock_db, test_client, api_key):
    # Set up the sample bid ID
    sample_bid_id = "66fb5dba-f129-413a-b12e-5a68b5a647d6"

    # Mock the database find method to return an empty list
    mock_db["questions"].find.return_value = []

    # Make a request to the endpoint to get the questions
    response = test_client.get(
        f"api/bids/{sample_bid_id}/questions",
        headers={"host": "localhost:8080", "X-API-Key": api_key},
    )

    # Assert the response status code and content
    assert response.status_code == 404
    response_data = response.get_json()
    assert response_data == {"Error": "Resource not found"}


# Case 6: Validation error
@patch("api.controllers.question_controller.current_app.db")
def test_get_questions_bid_id_validation_error(mock_db, test_client, api_key):
    # Set up the sample question ID
    sample_bid_id = "Invalid bid Id"
    # Make a request to the endpoint to get the questions
    response = test_client.get(
        f"api/bids/{sample_bid_id}/questions",
        headers={"host": "localhost:8080", "X-API-Key": api_key},
    )
    assert response.status_code == 400
    assert response.get_json() == {"Error": "{'id': ['Invalid Id']}"}


# Case 7: Invalid offset - greater than maximum
@patch("api.controllers.question_controller.current_app.db")
def test_get_questions_max_offset(mock_db, test_client, api_key, max_offset):
    invalid_offset = int(max_offset) + 1
    sample_bid_id = "66fb5dba-f129-413a-b12e-5a68b5a647d6"
    sample_data = [
        {
            "_id": "2b18f477-627f-4d48-a008-ca0d9cea3791",
            "description": "This is a question",
            "feedback": {
                "description": "Good feedback",
                "url": "https://organisation.sharepoint.com/Docs/dummyfolder",
            },
            "last_updated": "2023-08-01T23:11:59.336092",
            "links": {
                "bid": f"/api/bids/{sample_bid_id}",
                "self": f"/api/bids/{sample_bid_id}/questions/2b18f477-627f-4d48-a008-ca0d9cea3791",
            },
            "out_of": None,
            "question_url": "https://organisation.sharepoint.com/Docs/dummyfolder",
            "respondents": [],
            "response": None,
            "score": None,
            "status": "in_progress",
        },
    ]

    mock_db["questions"].find.return_value = sample_data

    mock_db["questions"].count_documents.return_value = len(sample_data)

    # Make a request to the endpoint to get the questions
    response = test_client.get(
        f"api/bids/{sample_bid_id}/questions?offset={invalid_offset}",
        headers={"host": "localhost:8080", "X-API-Key": api_key},
    )

    assert response.status_code == 400
    assert (
        response.get_json()["Error"]
        == f"Offset value must be a number between 0 and {max_offset}"
    )


# Case 8: Invalid offset - not a number
@patch("api.controllers.question_controller.current_app.db")
def test_get_questions_nan_offset(mock_db, test_client, api_key, max_offset):
    invalid_offset = "five"
    sample_bid_id = "66fb5dba-f129-413a-b12e-5a68b5a647d6"
    sample_data = [
        {
            "_id": "2b18f477-627f-4d48-a008-ca0d9cea3791",
            "description": "This is a question",
            "feedback": {
                "description": "Good feedback",
                "url": "https://organisation.sharepoint.com/Docs/dummyfolder",
            },
            "last_updated": "2023-08-01T23:11:59.336092",
            "links": {
                "bid": f"/api/bids/{sample_bid_id}",
                "self": f"/api/bids/{sample_bid_id}/questions/2b18f477-627f-4d48-a008-ca0d9cea3791",
            },
            "out_of": None,
            "question_url": "https://organisation.sharepoint.com/Docs/dummyfolder",
            "respondents": [],
            "response": None,
            "score": None,
            "status": "in_progress",
        },
    ]

    mock_db["questions"].find.return_value = sample_data

    mock_db["questions"].count_documents.return_value = len(sample_data)

    # Make a request to the endpoint to get the questions
    response = test_client.get(
        f"api/bids/{sample_bid_id}/questions?offset={invalid_offset}",
        headers={"host": "localhost:8080", "X-API-Key": api_key},
    )

    assert response.status_code == 400
    assert (
        response.get_json()["Error"]
        == f"Offset value must be a number between 0 and {max_offset}"
    )


# Case 9: Invalid offset - negative number
@patch("api.controllers.question_controller.current_app.db")
def test_get_questions_negative_offset(mock_db, test_client, api_key, max_offset):
    invalid_offset = -1
    sample_bid_id = "66fb5dba-f129-413a-b12e-5a68b5a647d6"
    sample_data = [
        {
            "_id": "2b18f477-627f-4d48-a008-ca0d9cea3791",
            "description": "This is a question",
            "feedback": {
                "description": "Good feedback",
                "url": "https://organisation.sharepoint.com/Docs/dummyfolder",
            },
            "last_updated": "2023-08-01T23:11:59.336092",
            "links": {
                "bid": f"/api/bids/{sample_bid_id}",
                "self": f"/api/bids/{sample_bid_id}/questions/2b18f477-627f-4d48-a008-ca0d9cea3791",
            },
            "out_of": None,
            "question_url": "https://organisation.sharepoint.com/Docs/dummyfolder",
            "respondents": [],
            "response": None,
            "score": None,
            "status": "in_progress",
        },
    ]

    mock_db["questions"].find.return_value = sample_data

    mock_db["questions"].count_documents.return_value = len(sample_data)

    # Make a request to the endpoint to get the questions
    response = test_client.get(
        f"api/bids/{sample_bid_id}/questions?offset={invalid_offset}",
        headers={"host": "localhost:8080", "X-API-Key": api_key},
    )

    assert response.status_code == 400
    assert (
        response.get_json()["Error"]
        == f"Offset value must be a number between 0 and {max_offset}"
    )


# Case 10: Invalid limit - greater than maximum
@patch("api.controllers.question_controller.current_app.db")
def test_get_questions_max_limit(mock_db, test_client, api_key, max_limit):
    invalid_limit = int(max_limit) + 1
    sample_bid_id = "66fb5dba-f129-413a-b12e-5a68b5a647d6"
    sample_data = [
        {
            "_id": "2b18f477-627f-4d48-a008-ca0d9cea3791",
            "description": "This is a question",
            "feedback": {
                "description": "Good feedback",
                "url": "https://organisation.sharepoint.com/Docs/dummyfolder",
            },
            "last_updated": "2023-08-01T23:11:59.336092",
            "links": {
                "bid": f"/api/bids/{sample_bid_id}",
                "self": f"/api/bids/{sample_bid_id}/questions/2b18f477-627f-4d48-a008-ca0d9cea3791",
            },
            "out_of": None,
            "question_url": "https://organisation.sharepoint.com/Docs/dummyfolder",
            "respondents": [],
            "response": None,
            "score": None,
            "status": "in_progress",
        },
    ]

    mock_db["questions"].find.return_value = sample_data

    mock_db["questions"].count_documents.return_value = len(sample_data)

    # Make a request to the endpoint to get the questions
    response = test_client.get(
        f"api/bids/{sample_bid_id}/questions?limit={invalid_limit}",
        headers={"host": "localhost:8080", "X-API-Key": api_key},
    )

    assert response.status_code == 400
    assert (
        response.get_json()["Error"]
        == f"Limit value must be a number between 0 and {max_limit}"
    )


# Case 11: Invalid limit - not a number
@patch("api.controllers.question_controller.current_app.db")
def test_get_questions_nan_limit(mock_db, test_client, api_key, max_limit):
    invalid_limit = "ten"
    sample_bid_id = "66fb5dba-f129-413a-b12e-5a68b5a647d6"
    sample_data = [
        {
            "_id": "2b18f477-627f-4d48-a008-ca0d9cea3791",
            "description": "This is a question",
            "feedback": {
                "description": "Good feedback",
                "url": "https://organisation.sharepoint.com/Docs/dummyfolder",
            },
            "last_updated": "2023-08-01T23:11:59.336092",
            "links": {
                "bid": f"/api/bids/{sample_bid_id}",
                "self": f"/api/bids/{sample_bid_id}/questions/2b18f477-627f-4d48-a008-ca0d9cea3791",
            },
            "out_of": None,
            "question_url": "https://organisation.sharepoint.com/Docs/dummyfolder",
            "respondents": [],
            "response": None,
            "score": None,
            "status": "in_progress",
        },
    ]

    mock_db["questions"].find.return_value = sample_data

    mock_db["questions"].count_documents.return_value = len(sample_data)

    # Make a request to the endpoint to get the questions
    response = test_client.get(
        f"api/bids/{sample_bid_id}/questions?limit={invalid_limit}",
        headers={"host": "localhost:8080", "X-API-Key": api_key},
    )

    assert response.status_code == 400
    assert (
        response.get_json()["Error"]
        == f"Limit value must be a number between 0 and {max_limit}"
    )


# Case 12: Invalid limit - negative number
@patch("api.controllers.question_controller.current_app.db")
def test_get_questions_negative_limit(mock_db, test_client, api_key, max_limit):
    invalid_limit = -1
    sample_bid_id = "66fb5dba-f129-413a-b12e-5a68b5a647d6"
    sample_data = [
        {
            "_id": "2b18f477-627f-4d48-a008-ca0d9cea3791",
            "description": "This is a question",
            "feedback": {
                "description": "Good feedback",
                "url": "https://organisation.sharepoint.com/Docs/dummyfolder",
            },
            "last_updated": "2023-08-01T23:11:59.336092",
            "links": {
                "bid": f"/api/bids/{sample_bid_id}",
                "self": f"/api/bids/{sample_bid_id}/questions/2b18f477-627f-4d48-a008-ca0d9cea3791",
            },
            "out_of": None,
            "question_url": "https://organisation.sharepoint.com/Docs/dummyfolder",
            "respondents": [],
            "response": None,
            "score": None,
            "status": "in_progress",
        },
    ]

    mock_db["questions"].find.return_value = sample_data

    mock_db["questions"].count_documents.return_value = len(sample_data)

    # Make a request to the endpoint to get the questions
    response = test_client.get(
        f"api/bids/{sample_bid_id}/questions?limit={invalid_limit}",
        headers={"host": "localhost:8080", "X-API-Key": api_key},
    )

    assert response.status_code == 400
    assert (
        response.get_json()["Error"]
        == f"Limit value must be a number between 0 and {max_limit}"
    )
