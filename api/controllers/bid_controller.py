"""
This module implements the bid controller.
"""
from datetime import datetime, timedelta
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
    validate_sort,
    validate_pagination,
)

bid = Blueprint("bid", __name__)

# request_history = {}  # Store request history for throttling

# @bid.before_request
# def backend_throttling_middleware():
#     user_ip = request.remote_addr
#     current_time = datetime.now()

#     # Define the maximum requests per second (configurable)
#     max_requests_per_second = 2

#     # Check if user IP exists in the request history
#     if user_ip in request_history:
#         # Calculate the time elapsed since the last request
#         time_elapsed = current_time - request_history[user_ip]
#         if time_elapsed < timedelta(seconds=1 / max_requests_per_second):
#             # Throttle the request and return an error response with Retry-After header
#             retry_after = (1 / max_requests_per_second) - time_elapsed.total_seconds()
#             response = jsonify({"error": "Too many requests. Please try again later."})
#             return response, 429, {'Retry-After': int(retry_after)}

#     # Update the request history with the current time
#     request_history[user_ip] = current_time


@bid.route("/bids", methods=["GET"])
@require_api_key
def get_bids():
    try:
        hostname = request.headers.get("host")
        field, order = validate_sort(request.args.get("sort"), "bids")
        limit, offset = validate_pagination(
            request.args.get("limit"), request.args.get("offset")
        )

        # Prepare query filter and options
        query_filter = {}
        query_options = {"sort": [(field, order)], "skip": offset, "limit": limit}
        # Define allowed search fields
        allowed_filter_fields = [
            "was_successful",
            "tender",
            "status",
            "alias",
            "description",
            "client",
        ]
        # Apply search filters from query string
        for param, value in request.args.items():
            if param == "sort" or param == "limit" or param == "offset":
                continue

            if param in allowed_filter_fields:
                if ":" in value:
                    key, value = value.split(":")
                    if key == "partial":
                        query_filter[param] = {"$regex": value, "$options": "i"}
                    if key == "not":
                        query_filter[param] = {"$ne": value}
                else:
                    query_filter[param] = value
            else:
                raise ValueError(f"Invalid search field: {param}")

        # Fetch data and count documents
        data = list(db["bids"].find(query_filter, **query_options))
        total_count = db["bids"].count_documents({})

        for resource in data:
            prepend_host_to_links(resource, hostname)

        deleted_items_count = db["bids"].count_documents(
            {"status": Status.DELETED.value}
        )
        in_progress_items_count = db["bids"].count_documents(
            {"status": Status.IN_PROGRESS.value}
        )
        successful_items_count = db["bids"].count_documents(
            {"status": Status.COMPLETED.value}
        )

        return {
            "count": len(data),
            "total_count": total_count,
            "limit": limit,
            "offset": offset,
            "items": data,
            "deleted_items": deleted_items_count,
            "in_progress_items": in_progress_items_count,
            "successful_items": successful_items_count,
        }, 200
    except ValueError as error:
        return jsonify({"Error": str(error)}), 400
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
        if not data:
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
        if not current_bid:
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
        if not data:
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
