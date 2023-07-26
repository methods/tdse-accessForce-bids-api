from unittest.mock import patch


# Case 1: Successful post
@patch("api.controllers.bid_controller.db")
def test_post_is_successful(mock_db, test_client, api_key):
    data = {
        "tender": "Business Intelligence and Data Warehousing",
        "client": "Office for National Statistics",
        "bid_date": "2023-06-21",
        "alias": "ONS",
        "bid_folder_url": "https://organisation.sharepoint.com/Docs/dummyfolder",
        "feedback": {
            "description": "Feedback from client in detail",
            "url": "https://organisation.sharepoint.com/Docs/dummyfolder/feedback",
        },
        "success": [{"phase": 1, "has_score": True, "out_of": 36, "score": 30}],
        "failed": {"phase": 2, "has_score": True, "score": 20, "out_of": 36},
    }

    # Mock the behavior of db
    mock_db["bids"].insert_one.return_value = data

    response = test_client.post("api/bids", json=data, headers={"X-API-Key": api_key})
    assert response.status_code == 201
    assert "_id" in response.get_json() and response.get_json()["_id"] is not None
    assert (
        "tender" in response.get_json()
        and response.get_json()["tender"]
        == "Business Intelligence and Data Warehousing"
    )
    assert (
        "client" in response.get_json()
        and response.get_json()["client"] == "Office for National Statistics"
    )
    assert (
        "last_updated" in response.get_json()
        and response.get_json()["last_updated"] is not None
    )
    assert (
        "bid_date" in response.get_json()
        and response.get_json()["bid_date"] == "2023-06-21"
    )


# Case 2: Missing mandatory fields
@patch("api.controllers.bid_controller.db")
def test_field_missing(mock_db, test_client, api_key):
    data = {"client": "Sample Client", "bid_date": "2023-06-20"}

    response = test_client.post("api/bids", json=data, headers={"X-API-Key": api_key})
    assert response.status_code == 400
    assert response.get_json() == {
        "Error": "{'tender': {'message': 'Missing mandatory field'}}"
    }


# Case 3: Connection error
@patch("api.controllers.bid_controller.db")
def test_post_bid_connection_error(mock_db, test_client, api_key):
    data = {
        "tender": "Business Intelligence and Data Warehousing",
        "client": "Office for National Statistics",
        "bid_date": "2023-06-21",
        "alias": "ONS",
        "bid_folder_url": "https://organisation.sharepoint.com/Docs/dummyfolder",
        "feedback": {
            "description": "Feedback from client in detail",
            "url": "https://organisation.sharepoint.com/Docs/dummyfolder/feedback",
        },
        "success": [{"phase": 1, "has_score": True, "out_of": 36, "score": 30}],
        "failed": {"phase": 2, "has_score": True, "score": 20, "out_of": 36},
    }
    # Mock the behavior of db
    mock_db["bids"].insert_one.side_effect = Exception
    response = test_client.post("/api/bids", json=data, headers={"X-API-Key": api_key})

    assert response.status_code == 500
    assert response.get_json() == {"Error": "Could not connect to database"}


# Case 4: Unauthorized - invalid API key
@patch("api.controllers.bid_controller.db")
def test_post_bid_unauthorized(mock_db, test_client, api_key):
    data = {
        "tender": "Business Intelligence and Data Warehousing",
        "client": "Office for National Statistics",
        "bid_date": "2023-06-21",
        "alias": "ONS",
        "bid_folder_url": "https://organisation.sharepoint.com/Docs/dummyfolder",
        "feedback": {
            "description": "Feedback from client in detail",
            "url": "https://organisation.sharepoint.com/Docs/dummyfolder/feedback",
        },
        "success": [{"phase": 1, "has_score": True, "out_of": 36, "score": 30}],
        "failed": {"phase": 2, "has_score": True, "score": 20, "out_of": 36},
    }

    # Mock the behavior of db
    mock_db["bids"].insert_one.return_value = data
    response = test_client.post("api/bids", json=data, headers={"X-API-Key": "INVALID"})
    assert response.status_code == 401
    assert response.get_json() == {"Error": "Unauthorized"}
