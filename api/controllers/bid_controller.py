"""
This module implements the bid controller.
"""
from datetime import datetime
from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from werkzeug.exceptions import UnprocessableEntity
from api.models.status_enum import Status
from dbconfig.mongo_setup import db
from helpers.helpers import (
    showInternalServerError,
    showNotFoundError,
    showUnprocessableEntityError,
    showValidationError,
    validate_and_create_bid_document,
    validate_id_path,
    validate_bid_update,
    validate_status_update,
    prepend_host_to_links,
    require_api_key,
    require_jwt,
    require_admin_access,
)

bid = Blueprint("bid", __name__)


@bid.route("/bids", methods=["GET"])
@require_api_key
def get_bids():
    try:
        # Validate and process the limit parameter
        limit = int(request.args.get("limit", 5))
        if limit < 1:
            return jsonify({"error": "Limit must be a positive number"}), 400

        offset = int(request.args.get("offset", 0))
        if offset < 0 or offset >= 1000:
            return jsonify({"error": "Offset must be between 0 and 999"}), 400

        sort = request.args.get("sort", "last_updated")
        order = int(request.args.get("order", 1))  # Default to ascending (1)

        # Prepare query filter and options
        query_filter = {"status": {"$ne": Status.DELETED.value}}
        query_options = {"sort": [(sort, order)], "skip": offset, "limit": limit}

        # Fetch data and count documents
        data = list(db["bids"].find(query_filter, **query_options))
        total_count = db["bids"].count_documents(query_filter)

        explain_result = (
            db["bids"]
            .find({"status": {"$ne": Status.DELETED.value}})
            .sort("alias", order)
            .explain()
        )
        print(explain_result["queryPlanner"]["winningPlan"])
        # Return the response
        if not data:
            return showNotFoundError(), 404

        hostname = request.headers.get("host")
        for resource in data:
            prepend_host_to_links(resource, hostname)

        return {
            "count": len(data),
            "total_count": total_count,
            "limit": limit,
            "offset": offset,
            "data": data,
        }, 200
    except ValueError:  # Handle non-integer values
        return jsonify({"error": "Page and limit must be valid integer values"}), 400
    except Exception:
        return showInternalServerError(), 500


@bid.route("/bids", methods=["POST"])
@require_jwt
def post_bid():
    try:
        # Process input and create data model
        data = validate_and_create_bid_document(request.get_json())
        # Insert document into database collection
        db["bids"].insert_one(data)
        return data, 201
    # Return 400 response if input validation fails
    except ValidationError as error:
        return showValidationError(error), 400
    # Return 500 response in case of connection failure
    except Exception:
        return showInternalServerError(), 500


@bid.route("/bids/<bid_id>", methods=["GET"])
@require_api_key
def get_bid_by_id(bid_id):
    try:
        bid_id = validate_id_path(bid_id)
        data = db["bids"].find_one(
            {"_id": bid_id, "status": {"$ne": Status.DELETED.value}}
        )
        # Return 404 response if not found / returns None
        if data is None:
            return showNotFoundError(), 404
        # Get hostname from request headers
        hostname = request.headers.get("host")
        # print(data, hostname)
        data = prepend_host_to_links(data, hostname)
        return data, 200
    # Return 400 if bid_id is invalid
    except ValidationError as error:
        return showValidationError(error), 400
    # Return 500 response in case of connection failure
    except Exception:
        return showInternalServerError(), 500


@bid.route("/bids/<bid_id>", methods=["PUT"])
@require_jwt
def update_bid_by_id(bid_id):
    try:
        bid_id = validate_id_path(bid_id)
        # Retrieve resource where id is equal to bid_id
        current_bid = db["bids"].find_one(
            {"_id": bid_id, "status": Status.IN_PROGRESS.value}
        )
        # Return 404 response if not found / returns None
        if current_bid is None:
            return showNotFoundError(), 404
        updated_bid = validate_bid_update(request.get_json(), current_bid)
        db["bids"].replace_one(
            {"_id": bid_id},
            updated_bid,
        )
        return updated_bid, 200
    # Return 400 response if input validation fails
    except ValidationError as error:
        return showValidationError(error), 400
    except UnprocessableEntity as error:
        return showUnprocessableEntityError(error), 422
    # Return 500 response in case of connection failure
    except Exception:
        return showInternalServerError(), 500


@bid.route("/bids/<bid_id>", methods=["DELETE"])
@require_admin_access
def change_status_to_deleted(bid_id):
    try:
        bid_id = validate_id_path(bid_id)
        data = db["bids"].find_one_and_update(
            {"_id": bid_id, "status": {"$ne": Status.DELETED.value}},
            {
                "$set": {
                    "status": Status.DELETED.value,
                    "last_updated": datetime.now().isoformat(),
                }
            },
        )
        if data is None:
            return showNotFoundError(), 404
        return data, 204
    # Return 400 response if input validation fails
    except ValidationError as error:
        return showValidationError(error), 400
    # Return 500 response in case of connection failure
    except Exception:
        return showInternalServerError(), 500


@bid.route("/bids/<bid_id>/status", methods=["PUT"])
@require_admin_access
def update_bid_status(bid_id):
    try:
        bid_id = validate_id_path(bid_id)
        # Retrieve resource where id is equal to bid_id
        current_bid = db["bids"].find_one({"_id": bid_id})
        # Return 404 response if not found / returns None
        if current_bid is None:
            return showNotFoundError(), 404
        updated_bid = validate_status_update(request.get_json(), current_bid)
        db["bids"].replace_one(
            {"_id": bid_id},
            updated_bid,
        )
        return updated_bid, 200
    # Return 400 response if input validation fails
    except ValidationError as error:
        return showValidationError(error), 400
    except UnprocessableEntity as error:
        return showUnprocessableEntityError(error), 422
    # Return 500 response in case of connection failure
    except Exception:
        return showInternalServerError(), 500
