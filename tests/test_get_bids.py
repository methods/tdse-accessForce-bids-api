from unittest.mock import patch
from pymongo.errors import ConnectionFailure

# Case 1: Successful get
@patch('api.controllers.bid_controller.dbConnection')
def test_get_bids(mock_dbConnection, client):
    mock_db = mock_dbConnection.return_value
    mock_db['bids'].find.return_value = []

    response = client.get('/api/bids')
    assert response.status_code == 200
    assert response.get_json() == {'total_count': 0, 'items': []}

# Case 2: Connection error
@patch('api.controllers.bid_controller.dbConnection', side_effect=ConnectionFailure)
def test_get_bids_connection_error(mock_dbConnection, client):
    response = client.get('/api/bids')
    assert response.status_code == 500
    assert response.get_json() == {"Error": "Could not connect to database"}

# Case 3: Failed to call db['bids'].find
@patch('api.controllers.bid_controller.dbConnection')
def test_get_bids_find_error(mock_dbConnection, client):
    mock_db = mock_dbConnection.return_value
    mock_db['bids'].find.side_effect = Exception

    response = client.get('/api/bids')
    assert response.status_code == 500
    assert response.get_json() == {"Error": "Could not retrieve bids"}