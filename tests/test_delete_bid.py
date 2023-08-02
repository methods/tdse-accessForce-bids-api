from unittest.mock import patch


# Case 1: Successful delete a bid by changing status to deleted
@patch("api.controllers.bid_controller.db")
def test_delete_bid_success(mock_db, test_client, admin_jwt):
    mock_db["bids"].find_one_and_update.return_value = {
        "_id": "1ff45b42-b72a-464c-bde9-9bead14a07b9",
        "status": "deleted",
    }
    response = test_client.delete(
        "/api/bids/1ff45b42-b72a-464c-bde9-9bead14a07b9",
        headers={"Authorization": f"Bearer {admin_jwt}"},
    )
    assert response.status_code == 204
    assert response.content_length is None


# Case 2: Failed to call database
@patch("api.controllers.bid_controller.db")
def test_delete_bid_connection_error(mock_db, test_client, admin_jwt):
    mock_db["bids"].find_one_and_update.side_effect = Exception
    response = test_client.delete(
        "/api/bids/1ff45b42-b72a-464c-bde9-9bead14a07b9",
        headers={"Authorization": f"Bearer {admin_jwt}"},
    )
    assert response.status_code == 500
    assert response.get_json() == {"Error": "Could not connect to database"}


# Case 3: Validation error
@patch("api.controllers.bid_controller.db")
def test_delete_bid_validation_error(mock_db, test_client, admin_jwt):
    response = test_client.delete(
        "/api/bids/invalid_bid_id", headers={"Authorization": f"Bearer {admin_jwt}"}
    )
    assert response.status_code == 400
    assert response.get_json() == {"Error": "{'id': ['Invalid Id']}"}


# Case 4: Bid not found
@patch("api.controllers.bid_controller.db")
def test_delete_bid_not_found(mock_db, test_client, admin_jwt):
    mock_db["bids"].find_one_and_update.return_value = None

    response = test_client.delete(
        "/api/bids/1ff45b42-b72a-464c-bde9-9bead14a07b9",
        headers={"Authorization": f"Bearer {admin_jwt}"},
    )

    mock_db["bids"].find_one_and_update.assert_called_once()
    assert response.status_code == 404
    assert response.get_json() == {"Error": "Resource not found"}


# Case 5: Unauthorized - invalid token
@patch("api.controllers.bid_controller.db")
def test_delete_bid_unauthorized(mock_db, test_client):
    mock_db["bids"].find_one_and_update.return_value = {
        "_id": "1ff45b42-b72a-464c-bde9-9bead14a07b9",
        "status": "deleted",
    }
    response = test_client.delete(
        "/api/bids/1ff45b42-b72a-464c-bde9-9bead14a07b9",
        headers={"Authorization": "Bearer N0tV4l1djsonW3Bt0K3n"},
    )
    assert response.status_code == 401
    assert response.get_json() == {"Error": "Unauthorized"}


# Case 6: Forbidden - not admin
@patch("api.controllers.bid_controller.db")
def test_delete_bid_forbidden(mock_db, test_client, basic_jwt):
    mock_db["bids"].find_one_and_update.return_value = {
        "_id": "1ff45b42-b72a-464c-bde9-9bead14a07b9",
        "status": "deleted",
    }
    response = test_client.delete(
        "/api/bids/1ff45b42-b72a-464c-bde9-9bead14a07b9",
        headers={"Authorization": f"Bearer {basic_jwt}"},
    )
    assert response.status_code == 403
    assert response.get_json() == {"Error": "Forbidden"}
