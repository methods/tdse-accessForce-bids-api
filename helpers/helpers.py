"""
This module contains helper functions for the API.
"""
import jwt
import logging
import os
import uuid
from datetime import datetime
from dotenv import load_dotenv
from flask import g, jsonify, request
from functools import wraps
from jwt.exceptions import InvalidTokenError
from werkzeug.exceptions import UnprocessableEntity
from api.schemas.bid_schema import BidSchema
from api.schemas.id_schema import IdSchema
from api.schemas.question_schema import QuestionSchema

logger = logging.getLogger()


def showForbiddenError():
    return jsonify({"Error": "Forbidden"})


def showInternalServerError():
    return jsonify({"Error": "Could not connect to database"})


def showNotFoundError():
    return jsonify({"Error": "Resource not found"})


def showUnauthorizedError():
    return jsonify({"Error": "Unauthorized"})


def showUnprocessableEntityError(error):
    return jsonify({"Error": str(error.description)})


def showValidationError(error):
    return jsonify({"Error": str(error)})


def is_valid_uuid(string):
    try:
        uuid.UUID(str(string))
        return True
    except ValueError:
        return False


def is_valid_isoformat(string):
    try:
        datetime.fromisoformat(string)
        return True
    except ValueError:
        return False


def validate_and_create_bid_document(request):
    # Process input and create data model
    bid_document = BidSchema().load(request)
    # Serialize to a JSON object
    data = BidSchema().dump(bid_document)
    return data


def validate_id_path(id):
    valid_id = IdSchema().load({"id": id})
    data = valid_id["id"]
    return data


def validate_bid_update(request, resource):
    if "status" in request:
        raise UnprocessableEntity("Cannot update status")
    resource.update(request)
    bid = BidSchema().load(resource, partial=True)
    data = BidSchema().dump(bid)
    return data


def validate_status_update(request, resource):
    if request == {}:
        raise UnprocessableEntity("Request must not be empty")
    resource.update(request)
    bid = BidSchema().load(resource, partial=True)
    data = BidSchema().dump(bid)
    return data


def prepend_host_to_links(resource, hostname):
    host = f"http://{hostname}"
    for key in resource["links"]:
        resource["links"][key] = f'{host}{resource["links"][key]}'
    return resource


def require_api_key(fn):
    @wraps(fn)
    def validate_api_key(*args, **kwargs):
        try:
            load_dotenv()
            api_key = request.headers.get("X-API-Key")
            assert api_key == os.getenv("API_KEY"), "API Key is not valid"
        except AssertionError:
            logger.error(f"{g.request_id} failed", exc_info=True)
            return showUnauthorizedError(), 401
        return fn(*args, **kwargs)

    return validate_api_key


def require_jwt(fn):
    @wraps(fn)
    def validate_jwt(*args, **kwargs):
        try:
            validate_token(request=request)
        except (AssertionError, InvalidTokenError):
            logger.error(f"{g.request_id} failed", exc_info=True)
            return showUnauthorizedError(), 401
        return fn(*args, **kwargs)

    return validate_jwt


def require_admin_access(fn):
    @wraps(fn)
    def validate_admin(*args, **kwargs):
        try:
            decoded = validate_token(request=request)
            if decoded["admin"] is False:
                raise PermissionError("Forbidden")
        except PermissionError:
            logger.error(f"{g.request_id} failed", exc_info=True)
            return showForbiddenError(), 403
        except (AssertionError, InvalidTokenError):
            logger.error(f"{g.request_id} failed", exc_info=True)
            return showUnauthorizedError(), 401
        return fn(*args, **kwargs)

    return validate_admin


def validate_token(request):
    prefix = "Bearer "
    auth_header = request.headers.get("Authorization")
    assert auth_header is not None, "Not authorized"
    assert auth_header.startswith(prefix) is True, "Not authorized"
    token = auth_header[len(prefix) :]
    load_dotenv()
    key = os.getenv("SECRET_KEY")
    decoded = jwt.decode(token, key, algorithms="HS256")
    return decoded


def validate_and_create_question_document(request, bid_id):
    request["bid_id"] = bid_id
    # Process input and create data model
    question_document = QuestionSchema().load(request)
    # Serialize to a JSON object
    data = QuestionSchema().dump(question_document)
    return data


def validate_question_update(request, resource):
    if request == {}:
        raise UnprocessableEntity("Request must not be empty")
    resource.update(request)
    question_document = QuestionSchema().load(resource, partial=True)
    data = QuestionSchema().dump(question_document)
    return data


def validate_pagination(limit, offset):
    load_dotenv()

    def validate_param(value, default_value, max_value, param_name):
        maximum = int(os.getenv(max_value))
        if value:
            try:
                valid_value = int(value)
                assert maximum > valid_value >= 0
            except (ValueError, AssertionError):
                raise ValueError(
                    f"{param_name} value must be a number between 0 and {maximum}"
                )
        else:
            valid_value = int(os.getenv(default_value))
        return valid_value

    valid_limit = validate_param(limit, "DEFAULT_LIMIT", "MAX_LIMIT", "Limit")
    valid_offset = validate_param(offset, "DEFAULT_OFFSET", "MAX_OFFSET", "Offset")
    return valid_limit, valid_offset


def validate_sort(sort_value, resource):
    load_dotenv()
    if resource == "bids":
        field = os.getenv("DEFAULT_SORT_BIDS")
        valid_fields = [
            "client",
            "tender",
            "bid_date",
            "alias",
            "status",
            "last_updated",
            "was_successful",
        ]
    elif resource == "questions":
        field = os.getenv("DEFAULT_SORT_QUESTIONS")
        valid_fields = ["description", "score", "respondents", "status", "last_updated"]
    order = 1
    try:
        if sort_value:
            if sort_value[0] == "-":
                field = sort_value[1:]
                order = -1
            else:
                field = sort_value
        assert field in valid_fields
    except AssertionError:
        raise ValueError("Invalid sort criteria")
    return field, order
