from unittest.mock import patch


# Case 1: Successful get
@patch("api.controllers.bid_controller.dbConnection")
def test_get_bids_success(mock_dbConnection, client):
    mock_db = mock_dbConnection.return_value
    mock_db["bids"].find.return_value = []

    response = client.get("/api/bids")
    mock_db["bids"].find.assert_called_once_with({"status": {"$ne": "deleted"}})
    assert response.status_code == 200
    assert response.get_json() == {"total_count": 0, "items": []}


# Case 2: Links prepended with hostname
@patch("api.controllers.bid_controller.dbConnection")
def test_links_with_host(mock_dbConnection, client):
    mock_db = mock_dbConnection.return_value
    mock_db["bids"].find.return_value = [
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

    response = client.get("/api/bids", headers={"host": "localhost:8080"})
    assert response.status_code == 200
    assert response.get_json() == {
        "total_count": 1,
        "items": [
            {
                "_id": "1ff45b42-b72a-464c-bde9-9bead14a07b9",
                "bid_date": "2023-06-23",
                "client": "Office for National Statistics",
                "links": {
                    "questions": "http://localhost:8080/bids/faaf8ef5-5db4-459d-8d24-bc39492e1301/questions",
                    "self": "http://localhost:8080/bids/faaf8ef5-5db4-459d-8d24-bc39492e1301",
                },
                "status": "in_progress",
                "tender": "Business Intelligence and Data Warehousing",
            }
        ],
    }


# Case 3: Connection error
@patch("api.controllers.bid_controller.dbConnection", side_effect=Exception)
def test_get_bids_connection_error(mock_dbConnection, client):
    response = client.get("/api/bids")
    assert response.status_code == 500
    assert response.get_json() == {"Error": "Could not connect to database"}
