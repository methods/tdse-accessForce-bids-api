from flask import Blueprint, jsonify, request
from marshmallow import ValidationError
from api.schemas.bid_schema import BidSchema
from api.schemas.bid_request_schema import BidRequestSchema
from dbconfig.mongo_setup import dbConnection
from pymongo.errors import ConnectionFailure
from helpers.helpers import showConnectionError


bid = Blueprint('bid', __name__)

@bid.route("/bids", methods=["GET"])
def get_bids():
    # Get all bids from database collection
    try:
        db = dbConnection()
        bids = list(db['bids'].find({}))
        return {'total_count': len(bids), 'items': bids}, 200  
    except ConnectionFailure:
        return showConnectionError()
    
@bid.route("/bids", methods=["POST"])
def post_bid():
    # Create bid document and return error if input validation fails
    try:
        db = dbConnection()
        bid_document = BidRequestSchema().load(request.json)
        # Serialize to a JSON-encoded string
        data = BidSchema().dump(bid_document)
        # Insert document into database collection
        bids = db['bids']
        bids.insert_one(data)
        return data, 201
    except ValidationError as e:
        return jsonify({"Error": str(e)}), 400
    except ConnectionFailure:
        return showConnectionError()