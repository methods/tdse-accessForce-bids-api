"""
This file contains the tests for the GET /bids/{bidId}/questions/{questionId} endpoint
"""
from unittest.mock import patch


# Case 1: Successful get
@patch("api.controllers.question_controller.db")
def test_get_single_question_success(mock_db, test_client, api_key):
    # Set up the sample bid ID and question ID
    sample_bid_id = "66fb5dba-f129-413a-b12e-5a68b5a647d6"
    sample_question_id = "2b18f477-627f-4d48-a008-ca0d9cea3791"

    # Set up the sample data for a single question
    sample_data = {
        "_id": sample_question_id,
        "description": "This is a question",
        "feedback": {
            "description": "Good feedback",
            "url": "https://organisation.sharepoint.com/Docs/dummyfolder",
        },
        "last_updated": "2023-08-01T23:11:59.336092",
        "links": {
            "bid": f"/bids/{sample_bid_id}",
            "self": f"/bids/{sample_bid_id}/questions/{sample_question_id}",
        },
        "out_of": None,
        "question_url": "https://organisation.sharepoint.com/Docs/dummyfolder",
        "respondents": [],
        "response": None,
        "score": None,
        "status": "in_progress",
    }

    # Mock the database find_one method to return the sample question
    mock_db["questions"].find_one.return_value = sample_data

    # Make a request to the endpoint to get the single question
    response = test_client.get(
        f"api/bids/{sample_bid_id}/questions/{sample_question_id}",
        headers={"host": "localhost:8080", "X-API-Key": api_key},
    )

    # Assert the response status code and content
    assert response.status_code == 200
    response_data = response.get_json()
    assert response_data == sample_data


# Case 2: Links prepended with hostname
@patch("api.controllers.question_controller.db")
def test_single_question_links_with_host(mock_db, test_client, api_key):
    # Set up the sample bid ID and question ID
    sample_bid_id = "66fb5dba-f129-413a-b12e-5a68b5a647d6"
    sample_question_id = "2b18f477-627f-4d48-a008-ca0d9cea3791"

    # Set up the sample data for a single question
    sample_data = {
        "_id": sample_question_id,
        "description": "This is a question",
        "feedback": {
            "description": "Good feedback",
            "url": "https://organisation.sharepoint.com/Docs/dummyfolder",
        },
        "last_updated": "2023-08-01T23:11:59.336092",
        "links": {
            "bid": f"/bids/{sample_bid_id}",
            "self": f"/bids/{sample_bid_id}/questions/{sample_question_id}",
        },
        "out_of": None,
        "question_url": "https://organisation.sharepoint.com/Docs/dummyfolder",
        "respondents": [],
        "response": None,
        "score": None,
        "status": "in_progress",
    }

    # Mock the database find_one method to return the sample question
    mock_db["questions"].find_one.return_value = sample_data

    # Make a request to the endpoint to get the single question with hostname in the headers
    response = test_client.get(
        f"api/bids/{sample_bid_id}/questions/{sample_question_id}",
        headers={"host": "localhost:8080", "X-API-Key": api_key},
    )

    # Assert the response status code and content
    assert response.status_code == 200
    response_data = response.get_json()
    assert (
        response_data["links"]["bid"] == f"http://localhost:8080/bids/{sample_bid_id}"
    )
    assert (
        response_data["links"]["self"]
        == f"http://localhost:8080/bids/{sample_bid_id}/questions/{sample_question_id}"
    )


# Case 3: Connection error
@patch("api.controllers.question_controller.db")
def test_get_single_question_connection_error(mock_db, test_client, api_key):
    # Set up the sample bid ID and question ID
    sample_bid_id = "66fb5dba-f129-413a-b12e-5a68b5a647d6"
    sample_question_id = "2b18f477-627f-4d48-a008-ca0d9cea3791"

    # Mock the database find_one method to raise a ConnectionError
    mock_db["questions"].find_one.side_effect = Exception

    # Make a request to the endpoint to get the single question
    response = test_client.get(
        f"api/bids/{sample_bid_id}/questions/{sample_question_id}",
        headers={"host": "localhost:8080", "X-API-Key": api_key},
    )

    # Assert the response status code and content
    assert response.status_code == 500
    response_data = response.get_json()
    assert response_data == {"Error": "Could not connect to database"}


# Case 4: Unauthorized / invalid api key
@patch("api.controllers.question_controller.db")
def test_get_single_question_unauthorized(mock_db, test_client):
    # Set up the sample bid ID and question ID
    sample_bid_id = "66fb5dba-f129-413a-b12e-5a68b5a647d6"
    sample_question_id = "2b18f477-627f-4d48-a008-ca0d9cea3791"

    # Mock the database find_one method to return the question
    mock_db["questions"].find_one.return_value = {}

    # Make a request to the endpoint to get the single question without providing a JWT
    response = test_client.get(
        f"api/bids/{sample_bid_id}/questions/{sample_question_id}",
        headers={"host": "localhost:8080"},
    )

    # Assert the response status code and content
    assert response.status_code == 401
    response_data = response.get_json()
    assert response_data == {"Error": "Unauthorized"}

    # Make a request to the endpoint to get the single question with an invalid JWT
    response = test_client.get(
        f"api/bids/{sample_bid_id}/questions/{sample_question_id}",
        headers={"host": "localhost:8080", "Authorization": "Bearer INVALID_JWT"},
    )

    # Assert the response status code and content
    assert response.status_code == 401
    response_data = response.get_json()
    assert response_data == {"Error": "Unauthorized"}


# Case 5: No question found for the given ID
@patch("api.controllers.question_controller.db")
def test_no_question_found_by_id(mock_db, test_client, api_key):
    # Set up the sample question ID
    sample_bid_id = "66fb5dba-f129-413a-b12e-5a68b5a647d6"
    sample_question_id = "2b18f477-627f-4d48-a008-ca0d9cea3791"

    # Mock the database find_one method to return None (no question found)
    mock_db["questions"].find_one.return_value = []

    # Make a request to the endpoint to get the question by ID
    response = test_client.get(
        f"api/bids/{sample_bid_id}/questions/{sample_question_id}",
        headers={"host": "localhost:8080", "X-API-Key": api_key},
    )

    # Assert the response status code and content
    assert response.status_code == 404
    response_data = response.get_json()
    assert response_data == {"Error": "Resource not found"}


# Case 6: Validation error
@patch("api.controllers.question_controller.db")
def test_get_question_by_id_validation_error(mock_db, test_client, api_key):
    # Set up the sample question ID
    sample_bid_id = "Invalid bid Id"
    sample_question_id = "2b18f477-627f-4d48-a008-ca0d9cea3791"
    response = test_client.get(
        f"api/bids/{sample_bid_id}/questions/{sample_question_id}",
        headers={"host": "localhost:8080", "X-API-Key": api_key},
    )
    assert response.status_code == 400
    assert response.get_json() == {"Error": "{'id': ['Invalid Id']}"}
