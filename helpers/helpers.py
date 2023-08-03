import jwt
from jwt.exceptions import InvalidTokenError
import os
import uuid
from dotenv import load_dotenv
from datetime import datetime
from flask import jsonify, request
from functools import wraps
from werkzeug.exceptions import UnprocessableEntity
from api.schemas.bid_schema import BidSchema
from api.schemas.bid_id_schema import BidIdSchema
from api.schemas.question_schema import QuestionSchema


def showForbiddenError():
    return jsonify({"Error": "Forbidden"})


def showInternalServerError():
    return jsonify({"Error": "Could not connect to database"})


def showNotFoundError():
    return jsonify({"Error": "Resource not found"})


def showUnauthorizedError():
    return jsonify({"Error": "Unauthorized"})


def showUnprocessableEntityError(e):
    return jsonify({"Error": str(e.description)})


def showValidationError(e):
    return jsonify({"Error": str(e)})


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


def validate_bid_id_path(bid_id):
    valid_bid_id = BidIdSchema().load({"bid_id": bid_id})
    data = valid_bid_id["bid_id"]
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
    def wrapper(*args, **kwargs):
        try:
            load_dotenv()
            api_key = request.headers.get("X-API-Key")
            assert api_key == os.getenv("API_KEY")
        except AssertionError:
            return showUnauthorizedError(), 401
        return fn(*args, **kwargs)

    return wrapper


def require_jwt(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            validate_token(request=request)
        except (AssertionError, InvalidTokenError):
            return showUnauthorizedError(), 401
        return fn(*args, **kwargs)

    return wrapper


def require_admin_access(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            decoded = validate_token(request=request)
            if decoded["admin"] is False:
                return showForbiddenError(), 403
        except (AssertionError, InvalidTokenError):
            return showUnauthorizedError(), 401
        return fn(*args, **kwargs)

    return wrapper


def validate_token(request):
    PREFIX = "Bearer "
    auth_header = request.headers.get("Authorization")
    assert auth_header is not None
    assert auth_header.startswith(PREFIX) is True
    token = auth_header[len(PREFIX) :]
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


def validate_status_update_question(request, resource):
    if request == {}:
        raise UnprocessableEntity("Request must not be empty")
    resource.update(request)
    question_document = QuestionSchema().load(resource, partial=True)
    data = QuestionSchema().dump(question_document)
    return data
