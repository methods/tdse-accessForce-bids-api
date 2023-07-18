from flask import Blueprint, jsonify, request
from datetime import datetime
from marshmallow import ValidationError
from api.models.status_enum import Status
from dbconfig.mongo_setup import dbConnection
from pymongo.errors import ConnectionFailure
from api.schemas.bid_schema import BidSchema
from helpers.helpers import showConnectionError, showNotFoundError, validate_and_create_data, validate_bid_id_path

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
    try:
        bid_id = validate_bid_id_path(bid_id)
        db = dbConnection()
        data = db['bids'].find_one({"_id": bid_id , "status": {"$ne": Status.DELETED.value}})
        # Return 404 response if not found / returns None
        if data is None:
            return showNotFoundError()
        return data, 200
    # Return 500 response in case of connection failure
    except ConnectionFailure:
        return showConnectionError()
    # Return 400 if bid_id is invalid
    except ValidationError as e:
        return jsonify({"Error": str(e)}), 400

@bid.route("/bids/<bid_id>", methods=["PUT"])
def update_bid_by_id(bid_id):
    try:
        # Add id to request body from path param
        # This allows request to be validated against same schema
        user_request = request.get_json()
        user_request["last_updated"] = datetime.now()
        # Process input and create data model
        # data = validate_and_create_data(updated_bid)
        data = BidSchema().load(user_request, partial=True)
        # Find bid by id and replace with user request body
        db = dbConnection()
        db['bids'].update_one({"_id": bid_id}, {"$set": data})
        return data, 200
    except ValidationError as e:
        return jsonify({"Error": str(e)}), 400

@bid.route("/bids/<bid_id>", methods=["DELETE"])
def change_status_to_deleted(bid_id):
    try:
        bid_id = validate_bid_id_path(bid_id)
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
    try:
        db = dbConnection()
        # Process input and create data model
        data = validate_and_create_data(request.get_json())
        # Insert document into database collection
        db['bids'].insert_one(data)
        return data, 201
    # Return 400 response if input validation fails
    except ValidationError as e:
        return jsonify({"Error": str(e)}), 400
    # Return 500 response in case of connection failure
    except ConnectionFailure:
        return showConnectionError()