from flask import Blueprint, request
from datetime import datetime
from marshmallow import ValidationError
from api.models.status_enum import Status
from dbconfig.mongo_setup import dbConnection
from helpers.helpers import showInternalServerError, showNotFoundError, showValidationError, validate_and_create_bid_document, validate_bid_id_path, validate_bid_update

bid = Blueprint('bid', __name__)

@bid.route("/bids", methods=["GET"])
def get_bids():
    # Get all bids from database collection
    try:
        db = dbConnection()
        data = list(db['bids'].find({"status": {"$ne": Status.DELETED.value}}))
        return {'total_count': len(data), 'items': data}, 200  
    except Exception:
        return showInternalServerError(), 500
    
@bid.route("/bids", methods=["POST"])
def post_bid():
    try:
        db = dbConnection()
        # Process input and create data model
        data = validate_and_create_bid_document(request.get_json())
        # Insert document into database collection
        db['bids'].insert_one(data)
        return data, 201
    # Return 400 response if input validation fails
    except ValidationError as e:
        return showValidationError(e), 400
    # Return 500 response in case of connection failure
    except Exception:
        return showInternalServerError(), 500
    
@bid.route("/bids/<bid_id>", methods=["GET"])
def get_bid_by_id(bid_id):
    try:
        bid_id = validate_bid_id_path(bid_id)
        db = dbConnection()
        data = db['bids'].find_one({"_id": bid_id , "status": {"$ne": Status.DELETED.value}})
        # Return 404 response if not found / returns None
        if data is None:
            return showNotFoundError(), 404
        return data, 200
    # Return 400 if bid_id is invalid
    except ValidationError as e:
        return showValidationError(e), 400
    # Return 500 response in case of connection failure
    except Exception:
        return showInternalServerError(), 500

@bid.route("/bids/<bid_id>", methods=["PUT"])
def update_bid_by_id(bid_id):
    try:
        bid_id = validate_bid_id_path(bid_id)
        user_request = validate_bid_update(request.get_json())
        # Updates document where id is equal to bid_id
        db = dbConnection()
        data = db['bids'].find_one_and_update({"_id": bid_id}, {"$set": user_request}, return_document=True)
        # Return 404 response if not found / returns None
        if data is None:
            return showNotFoundError(), 404
        return data, 200
    # Return 400 response if input validation fails
    except ValidationError as e:
        return showValidationError(e), 400
    # Return 500 response in case of connection failure
    except Exception:
        return showInternalServerError(), 500

@bid.route("/bids/<bid_id>", methods=["DELETE"])
def change_status_to_deleted(bid_id):
    try:
        bid_id = validate_bid_id_path(bid_id)
        db = dbConnection()
        data = db['bids'].find_one_and_update({"_id": bid_id, "status": {"$ne": Status.DELETED.value}}, {"$set": {"status": Status.DELETED.value, "last_updated": datetime.now().isoformat()}})
        if data is None:
            return showNotFoundError(), 404
        return data, 204
    # Return 400 response if input validation fails
    except ValidationError as e:
        return showValidationError(e), 400
    # Return 500 response in case of connection failure
    except Exception:
        return showInternalServerError(), 500
