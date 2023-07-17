from flask import Blueprint, jsonify, request
from marshmallow import ValidationError
from api.schemas.bid_schema import BidSchema
from api.schemas.bid_request_schema import BidRequestSchema
from api.schemas.valid_bid_id_schema import valid_bid_id_schema
from api.models.status_enum import Status
from dbconfig.mongo_setup import dbConnection
from pymongo.errors import ConnectionFailure
from helpers.helpers import showConnectionError, showNotFoundError



bid = Blueprint('bid', __name__)

@bid.route("/bids", methods=["GET"])
def get_bids():
    # Get all bids from database collection
    try:
        db = dbConnection()
        data = list(db['bids'].find({"status": {"$ne": Status.DELETED.value}}))
        return {'total_count': len(data), 'items': data}, 200  
    except ConnectionFailure:
        return showConnectionError()
    except Exception:
        return jsonify({"Error": "Could not retrieve bids"}), 500
    
@bid.route("/bids/<bid_id>", methods=["GET"])
def get_bid_by_id(bid_id):
    # Validates query param
    try:
        valid_bid_id = valid_bid_id_schema().load({"bid_id": bid_id})
        bid_id = valid_bid_id["bid_id"]
    except ValidationError as e:
        return jsonify({"Error": str(e)}), 400

    # Get bid by id from database collection
    try:
        db = dbConnection()
        data = db['bids'].find_one({"_id": bid_id , "status": {"$ne": Status.DELETED.value}})
        # Return 404 response if not found / returns None
        if data is None:
            return showNotFoundError()
        return data, 200
    # Return 500 response in case of connection failure
    except ConnectionFailure:
        return showConnectionError()

@bid.route("/bids/<bid_id>", methods=["PUT"])
def change_status_to_deleted(bid_id):
     # Validates query param
    try:
        valid_bid_id = valid_bid_id_schema().load({"bid_id": bid_id})
        bid_id = valid_bid_id["bid_id"]
    except ValidationError as e:
        return jsonify({"Error": str(e)}), 400
    
    try:
        db = dbConnection()
        data = db['bids'].find_one({"_id": bid_id , "status": {"$ne": Status.DELETED.value}})
        if data is None:
            return showNotFoundError()
        else:
            db['bids'].update_one({"_id": bid_id}, {"$set": {"status": Status.DELETED.value}})
        return data, 204
    except ConnectionFailure:
        return showConnectionError()
    except ValidationError as e:
        return jsonify({"Error": str(e)}), 400
    
    

@bid.route("/bids", methods=["POST"])
def post_bid():
    # Create bid document and inserts it into collection
    try:
        db = dbConnection()
        # Process input and create data model
        bid_document = BidRequestSchema().load(request.get_json())
        # Serialize to a JSON object
        data = BidSchema().dump(bid_document)
        # Insert document into database collection
        db['bids'].insert_one(data)
        return data, 201
    # Return 400 response if input validation fails
    except ValidationError as e:
        return jsonify({"Error": str(e)}), 400
    # Return 500 response in case of connection failure
    except ConnectionFailure:
        return showConnectionError()