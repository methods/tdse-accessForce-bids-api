from flask import Flask
import pytest
from api.controllers.bid_controller import bid
from pymongo.errors import ConnectionFailure
from unittest.mock import patch, MagicMock


@pytest.fixture
def client():
    app = Flask(__name__)
    app.register_blueprint(bid, url_prefix='/api')
    with app.test_client() as client:
        yield client

# Case 1: Successful get
def test_get_bids(client):
    # Mock the behavior of dbConnection and find methods
    with patch('api.controllers.bid_controller.dbConnection') as mock_dbConnection:
        # Create a MagicMock object to simulate the behavior of the find method
        mock_find = MagicMock(return_value=[])
        # Set the return value of db['bids'].find to the MagicMock object
        mock_dbConnection.return_value.__getitem__.return_value.find = mock_find

        response = client.get('/api/bids')
        assert response.status_code == 200
        assert response.json == {'total_count': 0, 'items': []}

# Case 2: Connection error
def test_get_bids_connection_error(client):
    # Mock the behavior of dbConnection to raise ConnectionFailure
    with patch('api.controllers.bid_controller.dbConnection', side_effect=ConnectionFailure):
        response = client.get('/api/bids')
        assert response.status_code == 500
        assert response.json == {"Error": "Could not connect to database"}
        
        
# Case 3: Failed to call db['bids'].find
def test_get_bids_find_error(client):
    # Mock the behavior of dbConnection and find methods
    with patch('api.controllers.bid_controller.dbConnection') as mock_dbConnection:
        # Create a MagicMock object to simulate the behavior of the find method
        mock_find = MagicMock(side_effect=Exception)
        # Set the return value of db['bids'].find to the MagicMock object
        mock_dbConnection.return_value.__getitem__.return_value.find = mock_find

        response = client.get('/api/bids')
        assert response.status_code == 500
        assert response.json == {"Error": "Could not retrieve bids"}