from unittest.mock import patch


# Case 1: Successful delete a bid by changing status to deleted
@patch("api.controllers.bid_controller.db")
def test_delete_bid_success(mock_db, client):
    mock_db["bids"].find_one_and_update.return_value = {
        "_id": "1ff45b42-b72a-464c-bde9-9bead14a07b9",
        "status": "deleted",
    }
    response = client.delete("/api/bids/1ff45b42-b72a-464c-bde9-9bead14a07b9")
    assert response.status_code == 204
    assert response.content_length is None


# Case 2: Failed to call database
@patch("api.controllers.bid_controller.db")
def test_delete_bid_connection_error(mock_db, client):
    mock_db["bids"].find_one_and_update.side_effect = Exception
    response = client.delete("/api/bids/1ff45b42-b72a-464c-bde9-9bead14a07b9")
    assert response.status_code == 500
    assert response.get_json() == {"Error": "Could not connect to database"}


# Case 3: Validation error
@patch("api.controllers.bid_controller.db")
def test_delete_bid_validation_error(mock_db, client):
    response = client.delete("/api/bids/invalid_bid_id")
    assert response.status_code == 400
    assert response.get_json() == {"Error": "{'bid_id': ['Invalid bid Id']}"}


# Case 4: Bid not found
@patch("api.controllers.bid_controller.db")
def test_delete_bid_not_found(mock_db, client):
    mock_db["bids"].find_one_and_update.return_value = None

    response = client.delete("/api/bids/1ff45b42-b72a-464c-bde9-9bead14a07b9")

    mock_db["bids"].find_one_and_update.assert_called_once()
    assert response.status_code == 404
    assert response.get_json() == {"Error": "Resource not found"}
