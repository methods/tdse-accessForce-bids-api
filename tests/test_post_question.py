"""
This file contains the tests for the POST /bids/<bid_id>/questions endpoint
"""
from unittest.mock import patch


# Case 1: Successful post
@patch("api.controllers.question_controller.db")
def test_post_is_successful(mock_db, test_client, basic_jwt):
    data = {
        "description": "This is a question",
        "question_url": "https://organisation.sharepoint.com/Docs/dummyfolder",
        "feedback": {
            "description": "Good feedback",
            "url": "https://organisation.sharepoint.com/Docs/dummyfolder",
        },
    }

    # Mock the behavior of db
    mock_db["questions"].insert_one.return_value = data

    response = test_client.post(
        "api/bids/be15c306-c85b-4e67-a9f6-682553c065a1/questions",
        json=data,
        headers={"Authorization": f"Bearer {basic_jwt}"},
    )
    assert response.status_code == 201
    assert "_id" in response.get_json() and response.get_json()["_id"] is not None
    assert (
        "description" in response.get_json()
        and response.get_json()["description"] == "This is a question"
    )
    assert (
        "question_url" in response.get_json()
        and response.get_json()["question_url"]
        == "https://organisation.sharepoint.com/Docs/dummyfolder"
    )
    assert (
        "last_updated" in response.get_json()
        and response.get_json()["last_updated"] is not None
    )
    assert "feedback" in response.get_json() and response.get_json()["feedback"] == {
        "description": "Good feedback",
        "url": "https://organisation.sharepoint.com/Docs/dummyfolder",
    }


# Case 2: Missing mandatory fields
@patch("api.controllers.question_controller.db")
def test_post_question_field_missing(mock_db, test_client, basic_jwt):
    data = {
        "question_url": "https://organisation.sharepoint.com/Docs/dummyfolder",
        "feedback": {
            "description": "Good feedback",
            "url": "https://organisation.sharepoint.com/Docs/dummyfolder",
        },
    }

    response = test_client.post(
        "api/bids/be15c306-c85b-4e67-a9f6-682553c065a1/questions",
        json=data,
        headers={"Authorization": f"Bearer {basic_jwt}"},
    )
    assert response.status_code == 400
    assert response.get_json() == {
        "Error": "{'description': {'message': 'Missing mandatory field'}}"
    }


# Case 3: Connection error
@patch("api.controllers.question_controller.db")
def test_post_question_connection_error(mock_db, test_client, basic_jwt):
    data = {
        "description": "This is a question",
        "question_url": "https://organisation.sharepoint.com/Docs/dummyfolder",
        "feedback": {
            "description": "Good feedback",
            "url": "https://organisation.sharepoint.com/Docs/dummyfolder",
        },
    }
    # Mock the behavior of db
    mock_db["questions"].insert_one.side_effect = Exception
    response = test_client.post(
        "/api/bids/be15c306-c85b-4e67-a9f6-682553c065a1/questions",
        json=data,
        headers={"Authorization": f"Bearer {basic_jwt}"},
    )

    assert response.status_code == 500
    assert response.get_json() == {"Error": "Could not connect to database"}


# Case 4: Unauthorized - invalid token
@patch("api.controllers.question_controller.db")
def test_post_question_unauthorized(mock_db, test_client):
    data = {
        "description": "This is a question",
        "question_url": "https://organisation.sharepoint.com/Docs/dummyfolder",
        "feedback": {
            "description": "Good feedback",
            "url": "https://organisation.sharepoint.com/Docs/dummyfolder",
        },
    }

    # Mock the behavior of db
    mock_db["questions"].insert_one.return_value = data
    response = test_client.post(
        "/api/bids/be15c306-c85b-4e67-a9f6-682553c065a1/questions",
        json=data,
        headers={"Authorization": "Bearer N0tV4l1djsonW3Bt0K3n"},
    )
    assert response.status_code == 401
    assert response.get_json() == {"Error": "Unauthorized"}


# Case 5: Related bid not found
@patch("api.controllers.question_controller.db")
def test_post_question_bid_not_found(mock_db, test_client, basic_jwt):
    data = {
        "description": "This is a question",
        "question_url": "https://organisation.sharepoint.com/Docs/dummyfolder",
        "feedback": {
            "description": "Good feedback",
            "url": "https://organisation.sharepoint.com/Docs/dummyfolder",
        },
    }
    # Mock the behavior of db
    mock_db["bids"].find_one.return_value = None
    response = test_client.post(
        "/api/bids/be15c306-c85b-4e67-a9f6-682553c065a1/questions",
        json=data,
        headers={"Authorization": f"Bearer {basic_jwt}"},
    )

    mock_db["bids"].find_one.assert_called_once()
    assert response.status_code == 404
    assert response.get_json() == {"Error": "Resource not found"}
