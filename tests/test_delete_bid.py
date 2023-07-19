from pymongo.errors import ConnectionFailure
from unittest.mock import patch
from marshmallow import ValidationError

# Case 1: Successful delete a bid by changing status to deleted
@patch('api.controllers.bid_controller.dbConnection')
def test_delete_bid_success(mock_dbConnection, client):
    mock_db = mock_dbConnection.return_value
    mock_db['bids'].find_one_and_update.return_value = {
        "_id": "1ff45b42-b72a-464c-bde9-9bead14a07b9",
        "status": "deleted"
    }
    response = client.delete('/api/bids/1ff45b42-b72a-464c-bde9-9bead14a07b9')
    assert response.status_code == 204
    assert response.content_length is None

# Case 2: Failed to call database
@patch('api.controllers.bid_controller.dbConnection')
def test_delete_bid_find_error(mock_dbConnection, client):
    mock_db = mock_dbConnection.return_value
    mock_db['bids'].find_one_and_update.side_effect = ConnectionFailure
    response = client.delete('/api/bids/1ff45b42-b72a-464c-bde9-9bead14a07b9')
    assert response.status_code == 500
    assert response.get_json() == {"Error": "Could not connect to database"}

# Case 3: Validation error
@patch('api.controllers.bid_controller.dbConnection')
def test_get_bid_by_id_validation_error(mock_dbConnection, client):
    mock_dbConnection.side_effect = ValidationError
    response = client.delete('/api/bids/invalid_bid_id')
    assert response.status_code == 400
    assert response.get_json() == {"Error": "{'bid_id': ['Invalid bid Id']}"}