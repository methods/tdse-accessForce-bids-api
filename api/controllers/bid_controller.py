from flask import Blueprint, jsonify, request
from marshmallow import ValidationError
from api.schemas.bid_schema import BidSchema
from api.schemas.bid_request_schema import BidRequestSchema
from api.schemas.valid_bid_id_schema import valid_bid_id_schema
from dbconfig.mongo_setup import dbConnection
from pymongo.errors import ConnectionFailure
from helpers.helpers import showConnectionError, showNotFoundError


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
    except Exception:
        return jsonify({"Error": "Could not retrieve bids"}), 500
    
@bid.route("/bids/<bid_id>", methods=["GET"])
def get_bid_by_id(bid_id):
    print("bid_id", bid_id)
    # Validates query param
    try:
        valid_bid_id = valid_bid_id_schema().load({"bid_id": bid_id})
        bid_id = valid_bid_id["bid_id"]
    except ValidationError as e:
        return jsonify({"Error": str(e)}), 400
    # Returns bid document where _id is equal to bid_id argument
    try:
        db = dbConnection()
        data = db['bids'].find_one({"_id": bid_id})
        # Return 404 response if not found / returns None
        if data is None:
            return showNotFoundError()
        return data, 200
    # Return 500 response in case of connection failure
    except ConnectionFailure:
        return showConnectionError()

@bid.route("/bids", methods=["POST"])
def post_bid():
    # Create bid document and inserts it into collection
    try:
        db = dbConnection()
        # Deserialize and validate request against schema
        # Process input and create data model
        bid_document = BidRequestSchema().load(request.json)
        # Serialize to a JSON object
        data = BidSchema().dump(bid_document)
        # Insert document into database collection
        bids = db['bids']
        bids.insert_one(data)
        return data, 201
    # Return 400 response if input validation fails
    except ValidationError as e:
        return jsonify({"Error": str(e)}), 400
    # Return 500 response in case of connection failure
    except ConnectionFailure:
        return showConnectionError()