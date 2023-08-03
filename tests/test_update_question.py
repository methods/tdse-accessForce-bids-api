from unittest.mock import patch


# Case 1: Successful question update
@patch("api.controllers.question_controller.db")
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
    assert response_data == sample_updated_question
