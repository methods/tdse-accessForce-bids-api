from unittest.mock import patch
from pymongo.errors import ConnectionFailure
from marshmallow import ValidationError

# Case 1: Successful get_bid_by_id
@patch('api.controllers.bid_controller.dbConnection')
def test_get_bid_by_id_success(mock_dbConnection, client):
    mock_db = mock_dbConnection.return_value
    mock_db['bids'].find_one.return_value = {
        '_id': '1ff45b42-b72a-464c-bde9-9bead14a07b9',
        'tender': 'Business Intelligence and Data Warehousing'
    }

    response = client.get('/api/bids/1ff45b42-b72a-464c-bde9-9bead14a07b9')

    mock_dbConnection.assert_called_once()
    mock_db['bids'].find_one.assert_called_once_with({'_id': '1ff45b42-b72a-464c-bde9-9bead14a07b9', 'status': {'$ne': 'deleted'}})
    assert response.status_code == 200
    assert response.get_json() == {
        '_id': '1ff45b42-b72a-464c-bde9-9bead14a07b9',
        'tender': 'Business Intelligence and Data Warehousing'
    }

# Case 2: Connection error
@patch('api.controllers.bid_controller.dbConnection', side_effect=ConnectionFailure)
def test_get_bids_connection_error(mock_dbConnection, client):
    response = client.get('/api/bids/1ff45b42-b72a-464c-bde9-9bead14a07b9')
    assert response.status_code == 500
    assert response.get_json() == {"Error": "Could not connect to database"}

# Case 3: Bid not found
@patch('api.controllers.bid_controller.dbConnection')
def test_get_bid_by_id_not_found(mock_dbConnection, client):
    mock_db = mock_dbConnection.return_value
    mock_db['bids'].find_one.return_value = None

    response = client.get('/api/bids/1ff45b42-b72a-464c-bde9-9bead14a07b9')

    mock_dbConnection.assert_called_once()
    mock_db['bids'].find_one.assert_called_once_with({'_id': '1ff45b42-b72a-464c-bde9-9bead14a07b9', 'status': {'$ne': 'deleted'}})
    assert response.status_code == 404
    assert response.get_json() == {"Error": "Not found"}

# Case 4: Validation error
@patch('api.controllers.bid_controller.dbConnection')
def test_get_bid_by_id_validation_error(mock_dbConnection, client):
    mock_dbConnection.side_effect = ValidationError
    response = client.get('/api/bids/invalid_bid_id')
    assert response.status_code == 400
    assert response.get_json() == {'Error': "{'bid_id': ['Shorter than minimum length 36.']}"}
