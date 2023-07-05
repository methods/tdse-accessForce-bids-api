from flask import Blueprint, jsonify, request
from marshmallow import ValidationError
from api.schemas.bid_schema import BidSchema
from api.schemas.bid_request_schema import BidRequestSchema
from dbconfig.mongo_setup import dbConnection
from pymongo.errors import ConnectionFailure, PyMongoError
from helpers.helpers import showConnectionError, showNotFoundError


bid = Blueprint('bid', __name__)

@bid.route("/bids", methods=["GET"])
def get_bids():
    return "Under construction", 200

@bid.route("/bids/<bid_id>", methods=["GET"])
def get_bid_by_id(bid_id):
    try:
        db = dbConnection()
        data = db['bids'].find_one({"_id": bid_id})
        if data is None:
            return showNotFoundError()
        return data, 200
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


