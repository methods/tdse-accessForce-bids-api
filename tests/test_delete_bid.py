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
        