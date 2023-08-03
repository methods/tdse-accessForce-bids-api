from unittest.mock import patch


# Case 1: Successful get
@patch("api.controllers.question_controller.db")
def test_get_questions_success(mock_db, test_client, basic_jwt):
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
                "bid": f"/bids/{sample_bid_id}",
                "self": f"/bids/{sample_bid_id}/questions/2b18f477-627f-4d48-a008-ca0d9cea3791",
            },
            "out_of": None,
            "question_url": "https://organisation.sharepoint.com/Docs/dummyfolder",
            "respondents": [],
            "response": None,
            "score": None,
            "status": "in_progress",
        },
        {
            "_id": "bef5c1fb-46b4-4707-868a-c7719cfcc5ec",
            "description": "This is a question",
            "feedback": {
                "description": "Good feedback",
                "url": "https://organisation.sharepoint.com/Docs/dummyfolder",
            },
            "last_updated": "2023-08-02T09:35:58.295052",
            "links": {
                "bid": f"/bids/another-bid-id",
                "self": f"/bids/another-bid-id/questions/bef5c1fb-46b4-4707-868a-c7719cfcc5ec",
            },
            "out_of": None,
            "question_url": "https://organisation.sharepoint.com/Docs/dummyfolder",
            "respondents": [],
            "response": None,
            "score": None,
            "status": "in_progress",
        },
    ]

    # Filter the sample data to include only questions with the desired bid link
    filtered_sample_data = [
        question
        for question in sample_data
        if question["links"]["bid"] == f"/bids/{sample_bid_id}"
    ]

    # Mock the database find method to return the filtered sample data
    mock_db["questions"].find.return_value = filtered_sample_data

    # Make a request to the endpoint to get the questions
    response = test_client.get(
        f"api/bids/{sample_bid_id}/questions",
        headers={"host": "localhost:8080", "Authorization": f"Bearer {basic_jwt}"},
    )

    # Assert the response status code and content
    assert response.status_code == 200
    response_data = response.get_json()
    assert response_data["total_count"] == len(filtered_sample_data)
    assert response_data["items"] == filtered_sample_data


# Case 2: Links prepended with hostname
@patch("api.controllers.question_controller.db")
def test_links_with_host(mock_db, test_client, basic_jwt):
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
                "bid": f"/bids/{sample_bid_id}",
                "self": f"/bids/{sample_bid_id}/questions/2b18f477-627f-4d48-a008-ca0d9cea3791",
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

    # Make a request to the endpoint to get the questions
    response = test_client.get(
        f"api/bids/{sample_bid_id}/questions",
        headers={"host": "localhost:8080", "Authorization": f"Bearer {basic_jwt}"},
    )

    # Assert the response status code and content
    response_data = response.get_json()
    assert (
        response_data["items"][0]["links"]["bid"]
        == f"http://localhost:8080/bids/{sample_bid_id}"
    )

    assert (
        response_data["items"][0]["links"]["self"]
        == f"http://localhost:8080/bids/{sample_bid_id}/questions/2b18f477-627f-4d48-a008-ca0d9cea3791"
    )


# Case 3: Connection error
@patch("api.controllers.question_controller.db")
def test_get_questions_connection_error(mock_db, test_client, basic_jwt):
    # Set up the sample bid ID
    sample_bid_id = "66fb5dba-f129-413a-b12e-5a68b5a647d6"

    # Mock the database find method to raise a ConnectionError
    mock_db["questions"].find.side_effect = Exception

    # Make a request to the endpoint to get the questions
    response = test_client.get(
        f"api/bids/{sample_bid_id}/questions",
        headers={"host": "localhost:8080", "Authorization": f"Bearer {basic_jwt}"},
    )

    # Assert the response status code and content
    assert response.status_code == 500
    response_data = response.get_json()
    assert response_data == {"Error": "Could not connect to database"}


# Case 4: Unauthorized / invalid api key
@patch("api.controllers.question_controller.db")
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
@patch("api.controllers.question_controller.db")
def test_no_questions_found(mock_db, test_client, basic_jwt):
    # Set up the sample bid ID
    sample_bid_id = "66fb5dba-f129-413a-b12e-5a68b5a647d6"

    # Mock the database find method to return an empty list
    mock_db["questions"].find.return_value = []

    # Make a request to the endpoint to get the questions
    response = test_client.get(
        f"api/bids/{sample_bid_id}/questions",
        headers={"host": "localhost:8080", "Authorization": f"Bearer {basic_jwt}"},
    )

    # Assert the response status code and content
    assert response.status_code == 404
    response_data = response.get_json()
    assert response_data == {"Error": "Resource not found"}


# Case 6: Validation error
@patch("api.controllers.question_controller.db")
def test_get_question_by_id_validation_error(mock_db, test_client, basic_jwt):
    # Set up the sample question ID
    sample_bid_id = "Invalid bid Id"
    # Make a request to the endpoint to get the questions
    response = test_client.get(
        f"api/bids/{sample_bid_id}/questions",
        headers={"host": "localhost:8080", "Authorization": f"Bearer {basic_jwt}"},
    )
    assert response.status_code == 400
    assert response.get_json() == {"Error": "{'bid_id': ['Invalid bid Id']}"}
