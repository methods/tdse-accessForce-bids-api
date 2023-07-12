from flask import Flask
import pytest
from api.controllers.bid_controller import bid
from pymongo.errors import ConnectionFailure
from unittest.mock import patch, MagicMock
from marshmallow import ValidationError




@pytest.fixture
def client():
    app = Flask(__name__)
    app.register_blueprint(bid, url_prefix='/api')
    with app.test_client() as client:
        yield client
        
# Case 1: Successful delete a bid by changing status to deleted
def test_delete_bid_success(client):
   with patch('api.controllers.bid_controller.dbConnection') as mock_dbConnection:
       mock_db = MagicMock()
       mock_dbConnection.return_value = mock_db
       mock_db['bids'].update_one = MagicMock()
       mock_db['bids'].update_one.return_value = {'_id': '1ff45b42-b72a-464c-bde9-9bead14a07b9', 'status': 'deleted'}
       response = client.put('/api/bids/1ff45b42-b72a-464c-bde9-9bead14a07b9')
       assert response.status_code == 204
       assert response.get_json() == None


# Case 2: Failed to call database
def test_delete_bid_find_error(client):
    with patch('api.controllers.bid_controller.dbConnection') as mock_dbConnection:
        mock_db = MagicMock()
        mock_dbConnection.return_value = mock_db
        mock_db['bids'].update_one = MagicMock(side_effect=ConnectionFailure)
        response = client.put('/api/bids/1ff45b42-b72a-464c-bde9-9bead14a07b9')
        assert response.status_code == 500
        assert response.get_json() == {"Error": "Could not connect to database"}


# Case 3: Validation error
def test_delete_bid_by_id_validation_error(client):
    # Create a MagicMock object for mocking the valid_bid_id_schema object
    mock_valid_bid_id_schema = MagicMock()

    # Set up the side effect of valid_bid_id_schema.load to raise a ValidationError
    mock_valid_bid_id_schema().load.side_effect = ValidationError('Invalid Bid ID')

    # Patch the necessary functions and objects with the MagicMock object
    with patch('api.controllers.bid_controller.valid_bid_id_schema', mock_valid_bid_id_schema):
        # Call the endpoint with the desired URL
        response = client.get('/api/bids/invalid_bid_id')

    # Assertions
    mock_valid_bid_id_schema().load.assert_called_once_with({'bid_id': 'invalid_bid_id'})
    assert response.status_code == 400
    assert response.get_json() == {"Error": "Invalid Bid ID"}