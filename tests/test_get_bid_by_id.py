from flask import Flask
import pytest
from api.controllers.bid_controller import bid
from pymongo.errors import ConnectionFailure
from unittest.mock import patch, MagicMock
from marshmallow import ValidationError
from api.schemas.valid_bid_id_schema import valid_bid_id_schema


@pytest.fixture
def client():
    app = Flask(__name__)
    app.register_blueprint(bid, url_prefix='/api')
    with app.test_client() as client:
        yield client

# Case 1: Successful get_bid_by_id
def test_get_bid_by_id_success(client):
    # Create MagicMock objects for mocking the necessary functions and objects
    mock_db = MagicMock()  # Mock the database object
    mock_dbConnection = MagicMock(return_value=mock_db)  # Mock the dbConnection function
    mock_valid_bid_id_schema = MagicMock()  # Mock the valid_bid_id_schema object

    # Set up the return value of valid_bid_id_schema.load
    mock_valid_bid_id_schema().load.return_value = {'bid_id': '1ff45b42-b72a-464c-bde9-9bead14a07b9'}

    # Create a MagicMock object for the find_one method and assign it to the appropriate attribute
    mock_find_one = MagicMock(return_value={'_id': '1ff45b42-b72a-464c-bde9-9bead14a07b9', 'tender': 'Business Intelligence and Data Warehousing'})
    mock_dbConnection.return_value.__getitem__.return_value.find_one = mock_find_one

    # Patch the necessary functions and objects with the MagicMock objects
    with patch('api.controllers.bid_controller.dbConnection', mock_dbConnection), \
         patch('api.controllers.bid_controller.valid_bid_id_schema', mock_valid_bid_id_schema):
      
        # Call the endpoint with the desired URL
        response = client.get('/api/bids/1ff45b42-b72a-464c-bde9-9bead14a07b9')

    # Assertions
    mock_valid_bid_id_schema().load.assert_called_once_with({'bid_id': '1ff45b42-b72a-464c-bde9-9bead14a07b9'})
    mock_dbConnection.assert_called_once()
    mock_db['bids'].find_one.assert_called_once_with({'_id': '1ff45b42-b72a-464c-bde9-9bead14a07b9'})
    assert response.status_code == 200
    assert response.json == {'_id': '1ff45b42-b72a-464c-bde9-9bead14a07b9', 'tender': 'Business Intelligence and Data Warehousing'}

# Case 2: Connection error
def test_get_bids_connection_error(client):
    mock_valid_bid_id_schema = MagicMock()  # Mock the valid_bid_id_schema object

    # Set up the return value of valid_bid_id_schema.load
    mock_valid_bid_id_schema.load.return_value = {'bid_id': '1ff45b42-b72a-464c-bde9-9bead14a07b9'}

    # Mock the behavior of dbConnection to raise ConnectionFailure
    with patch('api.controllers.bid_controller.dbConnection', side_effect=ConnectionFailure), \
      patch('api.controllers.bid_controller.valid_bid_id_schema', mock_valid_bid_id_schema):
        response = client.get('/api/bids/1ff45b42-b72a-464c-bde9-9bead14a07b9')
        assert response.status_code == 500
        assert response.json == {"Error": "Could not connect to database"}


# Case 3: Bid not found
def test_get_bid_by_id_not_found(client):
    # Create MagicMock objects for mocking the necessary functions and objects
    mock_db = MagicMock()  # Mock the database object
    mock_dbConnection = MagicMock(return_value=mock_db)  # Mock the dbConnection function
    mock_valid_bid_id_schema = MagicMock()  # Mock the valid_bid_id_schema object

    # Set up the return value of valid_bid_id_schema.load
    mock_valid_bid_id_schema().load.return_value = {'bid_id': '1ff45b42-b72a-464c-bde9-9bead14a07b9'}

    # Create a MagicMock object for the find_one method and assign it to the appropriate attribute
    mock_find_one = MagicMock(return_value=None)  # Simulate not finding the bid
    mock_dbConnection.return_value.__getitem__.return_value.find_one = mock_find_one

    # Patch the necessary functions and objects with the MagicMock objects
    with patch('api.controllers.bid_controller.dbConnection', mock_dbConnection), \
         patch('api.controllers.bid_controller.valid_bid_id_schema', mock_valid_bid_id_schema):
      
        # Call the endpoint with the desired URL
        response = client.get('/api/bids/1ff45b42-b72a-464c-bde9-9bead14a07b9')

    # Assertions
    mock_valid_bid_id_schema().load.assert_called_once_with({'bid_id': '1ff45b42-b72a-464c-bde9-9bead14a07b9'})
    mock_dbConnection.assert_called_once()
    mock_db['bids'].find_one.assert_called_once_with({'_id': '1ff45b42-b72a-464c-bde9-9bead14a07b9'})
    assert response.status_code == 404
    assert response.json == {"Error": "Not found"}

# Case 4: Validation error
def test_get_bid_by_id_validation_error(client):
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
    assert response.json == {"Error": "Invalid Bid ID"}