from flask import Blueprint, jsonify, request
from marshmallow import ValidationError
from api.schemas.bid_schema import BidSchema
from api.schemas.bid_request_schema import BidRequestSchema
from dbconfig.mongo_setup import dbConnection
from pymongo.errors import ConnectionFailure
from helpers.helpers import showConnectionError, showNotFoundError


bid = Blueprint('bid', __name__)

@bid.route("/bids", methods=["GET"])
def get_bids():
    return "Under construction", 200

@bid.route("/bids/<bid_id>", methods=["GET"])
def get_bid_by_id(bid_id):
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
        bid_document = BidRequestSchema().load(request.json)
        # Serialize to a JSON object
        data = BidSchema().dump(bid_document)
        # Insert document into database collection
        bids = db['bids']
        bids.insert_one(data)
        return data, 201
    # Return 400 response if inout validation fails
    except ValidationError as e:
        return jsonify({"Error": str(e)}), 400
    # Return 500 response in case of connection failure
    except ConnectionFailure:
        return showConnectionError()


