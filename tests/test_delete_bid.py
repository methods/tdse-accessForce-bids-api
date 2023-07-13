from flask import Flask
import pytest
from api.controllers.bid_controller import bid
from pymongo.errors import ConnectionFailure
from unittest.mock import patch
from marshmallow import ValidationError

@pytest.fixture
def client():
    app = Flask(__name__)
    app.register_blueprint(bid, url_prefix='/api')
    with app.test_client() as client:
        yield client

# Case 1: Successful delete a bid by changing status to deleted
@patch('api.controllers.bid_controller.dbConnection')
def test_delete_bid_success(mock_dbConnection, client):
    mock_db = mock_dbConnection.return_value
    mock_db['bids'].update_one.return_value = {
        '_id': '1ff45b42-b72a-464c-bde9-9bead14a07b9',
        'status': 'deleted'
    }
    response = client.put('/api/bids/1ff45b42-b72a-464c-bde9-9bead14a07b9')
    assert response.status_code == 204
    assert response.get_json() is None

# Case 2: Failed to call database
@patch('api.controllers.bid_controller.dbConnection')
def test_delete_bid_find_error(mock_dbConnection, client):
    mock_db = mock_dbConnection.return_value
    mock_db['bids'].update_one.side_effect = ConnectionFailure
    response = client.put('/api/bids/1ff45b42-b72a-464c-bde9-9bead14a07b9')
    assert response.status_code == 500
    assert response.get_json() == {"Error": "Could not connect to database"}

# Case 3: Validation error
@patch('api.controllers.bid_controller.valid_bid_id_schema.load')
def test_get_bid_by_id_validation_error(mock_valid_bid_id_schema_load, client):
    mock_valid_bid_id_schema_load.side_effect = ValidationError('Invalid Bid ID')
    response = client.get('/api/bids/invalid_bid_id')
    mock_valid_bid_id_schema_load.assert_called_once_with({'bid_id': 'invalid_bid_id'})
    assert response.status_code == 400
    assert response.get_json() == {"Error": "Invalid Bid ID"}