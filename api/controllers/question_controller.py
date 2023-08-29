"""
This module implements the Question Controller blueprint.
"""
import logging
from flask import Blueprint, g, request, jsonify
from marshmallow import ValidationError
from werkzeug.exceptions import NotFound, UnprocessableEntity
from api.models.status_enum import Status
from dbconfig.mongo_setup import db
from helpers.helpers import (
    showInternalServerError,
    showNotFoundError,
    showUnprocessableEntityError,
    showValidationError,
    validate_and_create_question_document,
    validate_id_path,
    validate_question_update,
    prepend_host_to_links,
    require_api_key,
    require_jwt,
    require_admin_access,
    validate_pagination,
    validate_sort,
)

question = Blueprint("question", __name__)
logger = logging.getLogger()


@question.route("/bids/<bid_id>/questions", methods=["POST"])
@require_jwt
def post_question(bid_id):
    try:
        logger.info(f"Handling request {g.request_id}")
        bid_id = validate_id_path(bid_id)
        # Check if the bid exists in the database
        bid = db["bids"].find_one({"_id": bid_id})
        if not bid:
            raise NotFound("Resource not found")
        # Process input and create data model
        data = validate_and_create_question_document(request.get_json(), bid_id)
        # Insert document into database collection
        db["questions"].insert_one(data)
        return data, 201
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


@question.route("/bids/<bid_id>/questions", methods=["GET"])
@require_api_key
def get_questions(bid_id):
    try:
        logger.info(f"Handling request {g.request_id}")
        bid_id = validate_id_path(bid_id)
        hostname = request.headers.get("host")
        field, order = validate_sort(request.args.get("sort"), "questions")
        limit, offset = validate_pagination(
            request.args.get("limit"), request.args.get("offset")
        )
        # Prepare query filter and options
        query_filter = {
            "status": {"$ne": Status.DELETED.value},
            "links.bid": f"/api/bids/{bid_id}",
        }
        query_options = {"sort": [(field, order)], "skip": offset, "limit": limit}

        # Fetch data and count documents
        data = list(db["questions"].find(query_filter, **query_options))
        total_count = db["questions"].count_documents(query_filter)

        if not data:
            raise NotFound("Resource not found")
        for question in data:
            prepend_host_to_links(question, hostname)
        return {
            "total_count": total_count,
            "count": len(data),
            "offset": offset,
            "limit": limit,
            "items": data,
        }, 200
    except NotFound:
        logger.error(f"{g.request_id} failed", exc_info=True)
        return showNotFoundError(), 404
    except ValidationError as error:
        logger.error(f"{g.request_id} failed", exc_info=True)
        return showValidationError(error), 400
    except ValueError as error:
        logger.error(f"{g.request_id} failed", exc_info=True)
        return jsonify({"Error": str(error)}), 400
    except Exception:
        logger.error(f"{g.request_id} failed", exc_info=True)
        return showInternalServerError(), 500


@question.route("/bids/<bid_id>/questions/<question_id>", methods=["GET"])
@require_api_key
def get_question(bid_id, question_id):
    try:
        logger.info(f"Handling request {g.request_id}")
        bid_id = validate_id_path(bid_id)
        question_id = validate_id_path(question_id)
        hostname = request.headers.get("host")
        data = db["questions"].find_one(
            {
                "_id": question_id,
                "links.self": f"/api/bids/{bid_id}/questions/{question_id}",
                "status": {"$ne": Status.DELETED.value},
            }
        )
        if not data:
            raise NotFound("Resource not found")
        prepend_host_to_links(data, hostname)
        return data, 200
    except NotFound:
        logger.error(f"{g.request_id} failed", exc_info=True)
        return showNotFoundError(), 404
    except ValidationError as error:
        logger.error(f"{g.request_id} failed", exc_info=True)
        return showValidationError(error), 400
    except Exception:
        logger.error(f"{g.request_id} failed", exc_info=True)
        return showInternalServerError(), 500


@question.route("/bids/<bid_id>/questions/<question_id>", methods=["DELETE"])
@require_admin_access
def delete_question(bid_id, question_id):
    try:
        logger.info(f"Handling request {g.request_id}")
        bid_id = validate_id_path(bid_id)
        question_id = validate_id_path(question_id)
        bid = db["bids"].find_one({"_id": bid_id})
        if not bid:
            raise NotFound("Resource not found")
        data = db["questions"].delete_one({"_id": question_id})
        return data.raw_result, 204
    except NotFound:
        logger.error(f"{g.request_id} failed", exc_info=True)
        return showNotFoundError(), 404
    except ValidationError as error:
        logger.error(f"{g.request_id} failed", exc_info=True)
        return showValidationError(error), 400
    except Exception:
        logger.error(f"{g.request_id} failed", exc_info=True)
        return showInternalServerError(), 500


@question.route("/bids/<bid_id>/questions/<question_id>", methods=["PUT"])
@require_jwt
def update_question(bid_id, question_id):
    try:
        logger.info(f"Handling request {g.request_id}")
        bid_id = validate_id_path(bid_id)
        question_id = validate_id_path(question_id)
        data = db["questions"].find_one(
            {
                "_id": question_id,
                "links.self": f"/api/bids/{bid_id}/questions/{question_id}",
            }
        )
        if not data:
            raise NotFound("Resource not found")
        updated_question = validate_question_update(request.get_json(), data)
        db["questions"].replace_one({"_id": question_id}, updated_question)
        return updated_question, 200
    except NotFound:
        logger.error(f"{g.request_id} failed", exc_info=True)
        return showNotFoundError(), 404
    except ValidationError as error:
        logger.error(f"{g.request_id} failed", exc_info=True)
        return showValidationError(error), 400
    except UnprocessableEntity as error:
        logger.error(f"{g.request_id} failed", exc_info=True)
        return showUnprocessableEntityError(error), 422
    except Exception:
        logger.error(f"{g.request_id} failed", exc_info=True)
        return showInternalServerError(), 500
