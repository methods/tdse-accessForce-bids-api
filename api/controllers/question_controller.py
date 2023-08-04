from datetime import datetime
from flask import Blueprint, request
from marshmallow import ValidationError
from werkzeug.exceptions import UnprocessableEntity
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
    require_jwt,
    require_admin_access,
)

question = Blueprint("question", __name__)


@question.route("/bids/<bid_id>/questions", methods=["POST"])
@require_jwt
def post_question(bid_id):
    try:
        bid_id = validate_id_path(bid_id)
        # Check if the bid exists in the database
        bid = db["bids"].find_one({"_id": bid_id})
        if not bid:
            return showNotFoundError(), 404
        # Process input and create data model
        data = validate_and_create_question_document(request.get_json(), bid_id)
        # Insert document into database collection
        db["questions"].insert_one(data)
        return data, 201
    # Return 400 response if input validation fails
    except ValidationError as e:
        return showValidationError(e), 400
    # Return 500 response in case of connection failure
    except Exception:
        return showInternalServerError(), 500


@question.route("/bids/<bid_id>/questions", methods=["GET"])
@require_jwt
def get_questions(bid_id):
    try:
        bid_id = validate_id_path(bid_id)
        hostname = request.headers.get("host")
        data = list(
            db["questions"].find(
                {
                    "status": {"$ne": Status.DELETED.value},
                    "links.bid": f"/bids/{bid_id}",
                }
            )
        )
        if len(data) == 0:
            return showNotFoundError(), 404
        for question in data:
            prepend_host_to_links(question, hostname)
        return {"total_count": len(data), "items": data}, 200
    except ValidationError as e:
        return showValidationError(e), 400
    except Exception:
        return showInternalServerError(), 500


@question.route("/bids/<bid_id>/questions/<question_id>", methods=["GET"])
@require_jwt
def get_question(bid_id, question_id):
    try:
        bid_id = validate_id_path(bid_id)
        question_id = validate_id_path(question_id)
        hostname = request.headers.get("host")
        data = db["questions"].find_one(
            {
                "_id": question_id,
                "links.self": f"/bids/{bid_id}/questions/{question_id}",
                "status": {"$ne": Status.DELETED.value},
            }
        )
        if len(data) == 0:
            return showNotFoundError(), 404
        prepend_host_to_links(data, hostname)
        return data, 200
    except ValidationError as e:
        return showValidationError(e), 400
    except Exception as e:
        return showInternalServerError(), 500


@question.route("/bids/<bid_id>/questions/<question_id>", methods=["DELETE"])
@require_admin_access
def delete_question(bid_id, question_id):
    try:
        bid_id = validate_id_path(bid_id)
        question_id = validate_id_path(question_id)
        bid = db["bids"].find_one({"_id": bid_id})
        if bid is None:
            return showNotFoundError(), 404
        data = db["questions"].delete_one({"_id": question_id})
        return data.raw_result, 204
    except ValidationError as e:
        return showValidationError(e), 400
    except Exception:
        return showInternalServerError(), 500


@question.route("/bids/<bid_id>/questions/<question_id>", methods=["PUT"])
@require_jwt
def update_question(bid_id, question_id):
    try:
        bid_id = validate_id_path(bid_id)
        question_id = validate_id_path(question_id)
        data = db["questions"].find_one(
            {
                "_id": question_id,
                "links.self": f"/bids/{bid_id}/questions/{question_id}",
            }
        )
        # Return 404 response if not found / returns None
        if len(data) == 0:
            return showNotFoundError(), 404

        updated_question = validate_question_update(request.get_json(), data)
        db["questions"].replace_one({"_id": question_id}, updated_question)
        return updated_question, 200
    except ValidationError as e:
        return showValidationError(e), 400
    except UnprocessableEntity as e:
        return showUnprocessableEntityError(e), 422
    except Exception:
        return showInternalServerError(), 500
