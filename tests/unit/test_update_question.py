"""
This file contains tests for the update_question endpoint.
"""
from unittest.mock import patch


# Case 1: Successful question update
@patch("api.controllers.question_controller.current_app.db")
def test_update_question_success(mock_db, test_client, basic_jwt):
    # Set up the sample bid ID and question ID
    sample_bid_id = "66fb5dba-f129-413a-b12e-5a68b5a647d6"
    sample_question_id = "2b18f477-627f-4d48-a008-ca0d9cea3791"
    sample_updated_question = {
        "_id": sample_question_id,
        "description": "Updated question description",
        "feedback": {
            "description": "Good feedback",
            "url": "https://organisation.sharepoint.com/Docs/dummyfolder",
        },
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

    # Mock the database find_one method to return the question data
    mock_db["questions"].find_one.return_value = sample_updated_question

    # Mock the database replace_one method to return the updated question
    mock_db["questions"].replace_one.return_value = sample_updated_question

    # Make a request to the endpoint to update the question
    response = test_client.put(
        f"api/bids/{sample_bid_id}/questions/{sample_question_id}",
        headers={"host": "localhost:8080", "Authorization": f"Bearer {basic_jwt}"},
        json=sample_updated_question,
        content_type="application/json",
    )

    # Assert the response status code and content
    assert response.status_code == 200

    response_data = response.get_json()
    assert response_data["last_updated"] is not None
    # Remove the 'last_updated' field from the response data before comparison
    response_data.pop("last_updated", None)
    assert response_data == sample_updated_question


# Case 2: Invalid user input
@patch("api.controllers.question_controller.current_app.db")
def test_update_question_invalid_input(mock_db, test_client, basic_jwt):
    # Set up the sample bid ID and question ID
    sample_bid_id = "66fb5dba-f129-413a-b12e-5a68b5a647d6"
    sample_question_id = "2b18f477-627f-4d48-a008-ca0d9cea3791"
    mock_db["questions"].find_one.return_value = {
        "_id": sample_question_id,
        "description": "Updated question description",
        "feedback": {
            "description": "Good feedback",
            "url": "https://organisation.sharepoint.com/Docs/dummyfolder",
        },
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
    update = {"description": 42}
    # Make a request to the endpoint to update the question with invalid data
    response = test_client.put(
        f"api/bids/{sample_bid_id}/questions/{sample_question_id}",
        headers={"host": "localhost:8080", "Authorization": f"Bearer {basic_jwt}"},
        json=update,
        content_type="application/json",
    )

    # Assert the response status code and content
    assert response.status_code == 400
    response_data = response.get_json()["Error"]
    assert response_data == "{'description': ['Not a valid string.']}"


# Case 3: Question not found
@patch("api.controllers.question_controller.current_app.db")
def test_question_not_found(mock_db, test_client, basic_jwt):
    # Set up the sample bid ID and question ID
    sample_bid_id = "66fb5dba-f129-413a-b12e-5a68b5a647d6"
    sample_question_id = "2b18f477-627f-4d48-a008-ca0d9cea3791"
    mock_db["questions"].find_one.return_value = {}

    # Make a request to the endpoint to update the question with invalid data
    response = test_client.put(
        f"api/bids/{sample_bid_id}/questions/{sample_question_id}",
        headers={"host": "localhost:8080", "Authorization": f"Bearer {basic_jwt}"},
        json={},
        content_type="application/json",
    )
    # Assert the response status code and content
    assert response.status_code == 404
    response_data = response.get_json()["Error"]
    assert response_data == "Resource not found"


# Case 4: Exception handling - Internal Server Error
@patch("api.controllers.question_controller.current_app.db")
def test_exception_internal_server_error(mock_db, test_client, basic_jwt):
    # Set up the sample bid ID and question ID
    sample_bid_id = "66fb5dba-f129-413a-b12e-5a68b5a647d6"
    sample_question_id = "2b18f477-627f-4d48-a008-ca0d9cea3791"
    # Mock the database find_one method to raise an Exception
    mock_db["questions"].find_one.side_effect = Exception("Test Exception")
    update = {"tender": "Updated tender"}
    response = test_client.put(
        f"api/bids/{sample_bid_id}/questions/{sample_question_id}",
        headers={"host": "localhost:8080", "Authorization": f"Bearer {basic_jwt}"},
        json=update,
        content_type="application/json",
    )
    assert response.status_code == 500
    assert response.get_json() == {"Error": "Could not connect to database"}


# Case 5: Empty request body
@patch("api.controllers.question_controller.current_app.db")
def test_update_question_invalid_empty_request_body(mock_db, test_client, basic_jwt):
    # Set up the sample bid ID and question ID
    sample_bid_id = "66fb5dba-f129-413a-b12e-5a68b5a647d6"
    sample_question_id = "2b18f477-627f-4d48-a008-ca0d9cea3791"
    mock_db["questions"].find_one.return_value = {
        "_id": sample_question_id,
        "description": "Updated question description",
        "feedback": {
            "description": "Good feedback",
            "url": "https://organisation.sharepoint.com/Docs/dummyfolder",
        },
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
    update = {}
    # Make a request to the endpoint to update the question with invalid data
    response = test_client.put(
        f"api/bids/{sample_bid_id}/questions/{sample_question_id}",
        headers={"host": "localhost:8080", "Authorization": f"Bearer {basic_jwt}"},
        json=update,
        content_type="application/json",
    )

    # Assert the response status code and content
    assert response.status_code == 422
    response_data = response.get_json()["Error"]
    assert response_data == "Request must not be empty"
