"""
This module implements the bid controller.
"""
import logging
from datetime import datetime
from flask import Blueprint, current_app, g, jsonify, request
from marshmallow import ValidationError
from werkzeug.exceptions import NotFound, UnprocessableEntity
from api.models.status_enum import Status
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
logger = logging.getLogger()


@bid.route("/bids", methods=["GET"])
@require_api_key
def get_bids():
    try:
        db = current_app.db
        logger.info(f"Handling request {g.request_id}")
        hostname = request.headers.get("host")
        field, order = validate_sort(request.args.get("sort"), "bids")
        limit, offset = validate_pagination(
            request.args.get("limit"), request.args.get("offset")
        )

        # Prepare query filter and options
        query_filter = {"status": {"$ne": Status.DELETED.value}}
        query_options = {"sort": [(field, order)], "skip": offset, "limit": limit}

        # Fetch data and count documents
        data = list(db["bids"].find(query_filter, **query_options))
        total_count = db["bids"].count_documents(query_filter)

        for resource in data:
            prepend_host_to_links(resource, hostname)

        return {
            "count": len(data),
            "total_count": total_count,
            "limit": limit,
            "offset": offset,
            "items": data,
        }, 200
    except ValueError as error:
        logger.error(f"{g.request_id} failed", exc_info=True)
        return jsonify({"Error": str(error)}), 400
    except Exception:
        logger.error(f"{g.request_id} failed", exc_info=True)
        return showInternalServerError(), 500


@bid.route("/bids", methods=["POST"])
@require_jwt
def post_bid():
    try:
        db = current_app.db
        logger.info(f"Handling request {g.request_id}")
        # Process input and create data model
        data = validate_and_create_bid_document(request.get_json())
        # Insert document into database collection
        db["bids"].insert_one(data)
        return data, 201
    # Return 400 response if input validation fails
    except ValidationError as error:
        logger.error(f"{g.request_id} failed", exc_info=True)
        return showValidationError(error), 400
    # Return 500 response in case of connection failure
    except Exception:
        logger.error(f"{g.request_id} failed", exc_info=True)
        return showInternalServerError(), 500


@bid.route("/bids/<bid_id>", methods=["GET"])
@require_api_key
def get_bid_by_id(bid_id):
    try:
        db = current_app.db
        logger.info(f"Handling request {g.request_id}")
        bid_id = validate_id_path(bid_id)
        data = db["bids"].find_one(
            {"_id": bid_id, "status": {"$ne": Status.DELETED.value}}
        )
        if not data:
            raise NotFound("Resource not found")
        # Get hostname from request headers
        hostname = request.headers.get("host")
        # print(data, hostname)
        data = prepend_host_to_links(data, hostname)
        return data, 200
    # Return 404 response if not found / returns None
    except NotFound:
        logger.error(f"{g.request_id} failed", exc_info=True)
        return showNotFoundError(), 404
    # Return 400 if bid_id is invalid
    except ValidationError as error:
        logger.error(f"{g.request_id} failed", exc_info=True)
        return showValidationError(error), 400
    # Return 500 response in case of connection failure
    except Exception:
        logger.error(f"{g.request_id} failed", exc_info=True)
        return showInternalServerError(), 500


@bid.route("/bids/<bid_id>", methods=["PUT"])
@require_jwt
def update_bid_by_id(bid_id):
    try:
        db = current_app.db
        logger.info(f"Handling request {g.request_id}")
        bid_id = validate_id_path(bid_id)
        # Retrieve resource where id is equal to bid_id
        current_bid = db["bids"].find_one(
            {"_id": bid_id, "status": Status.IN_PROGRESS.value}
        )
        # Return 404 response if not found / returns None
        if not current_bid:
            raise NotFound("Resource not found")
        updated_bid = validate_bid_update(request.get_json(), current_bid)
        db["bids"].replace_one(
            {"_id": bid_id},
            updated_bid,
        )
        return updated_bid, 200
    except NotFound:
        logger.error(f"{g.request_id} failed", exc_info=True)
        return showNotFoundError(), 404
    # Return 400 response if input validation fails
    except ValidationError as error:
        logger.error(f"{g.request_id} failed", exc_info=True)
        return showValidationError(error), 400
    except UnprocessableEntity as error:
        logger.error(f"{g.request_id} failed", exc_info=True)
        return showUnprocessableEntityError(error), 422
    # Return 500 response in case of connection failure
    except Exception:
        logger.error(f"{g.request_id} failed", exc_info=True)
        return showInternalServerError(), 500


@bid.route("/bids/<bid_id>", methods=["DELETE"])
@require_admin_access
def change_status_to_deleted(bid_id):
    try:
        db = current_app.db
        logger.info(f"Handling request {g.request_id}")
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
            raise NotFound("Resource not found")
        return data, 204
    except NotFound:
        logger.error(f"{g.request_id} failed", exc_info=True)
        return showNotFoundError(), 404
    # Return 400 response if input validation fails
    except ValidationError as error:
        logger.error(f"{g.request_id} failed", exc_info=True)
        return showValidationError(error), 400
    # Return 500 response in case of connection failure
    except Exception:
        logger.error(f"{g.request_id} failed", exc_info=True)
        return showInternalServerError(), 500


@bid.route("/bids/<bid_id>/status", methods=["PUT"])
@require_admin_access
def update_bid_status(bid_id):
    try:
        db = current_app.db
        logger.info(f"Handling request {g.request_id}")
        bid_id = validate_id_path(bid_id)
        # Retrieve resource where id is equal to bid_id
        current_bid = db["bids"].find_one({"_id": bid_id})
        # Return 404 response if not found / returns None
        if current_bid is None:
            raise NotFound("Resource not found")
        updated_bid = validate_status_update(request.get_json(), current_bid)
        db["bids"].replace_one(
            {"_id": bid_id},
            updated_bid,
        )
        return updated_bid, 200
    except NotFound:
        logger.error(f"{g.request_id} failed", exc_info=True)
        return showNotFoundError(), 404
    # Return 400 response if input validation fails
    except ValidationError as error:
        logger.error(f"{g.request_id} failed", exc_info=True)
        return showValidationError(error), 400
    except UnprocessableEntity as error:
        logger.error(f"{g.request_id} failed", exc_info=True)
        return showUnprocessableEntityError(error), 422
    # Return 500 response in case of connection failure
    except Exception:
        logger.error(f"{g.request_id} failed", exc_info=True)
        return showInternalServerError(), 500
