from flask import jsonify
import uuid
from datetime import datetime
from werkzeug.exceptions import UnprocessableEntity
from api.schemas.update_bid_schema import UpdateBidSchema
from api.schemas.post_bid_schema import PostBidSchema
from api.schemas.bid_id_schema import BidIdSchema


def showInternalServerError():
    return jsonify({"Error": "Could not connect to database"})


def showNotFoundError():
    return jsonify({"Error": "Resource not found"})


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
    except:
        return False


def validate_and_create_bid_document(request):
    # Process input and create data model
    bid_document = PostBidSchema().load(request)
    # Serialize to a JSON object
    data = PostBidSchema().dump(bid_document)
    return data


def validate_bid_id_path(bid_id):
    valid_bid_id = BidIdSchema().load({"bid_id": bid_id})
    data = valid_bid_id["bid_id"]
    return data


def validate_bid_update(user_request):
    if "status" in user_request:
        raise UnprocessableEntity("Cannot update status")
    data = UpdateBidSchema().load(user_request, partial=True)
    if "failed" in data:
        data["failed"]["phase"] = data["failed"]["phase"].value
    if "success" in data:
        for obj in data["success"]:
            obj["phase"] = obj["phase"].value
    return data


def validate_status_update(user_request):
    if user_request == {}:
        raise UnprocessableEntity("Request must not be empty")
    data = UpdateBidSchema().load(user_request, partial=True)
    if data:
        data["status"] = data["status"].value
    return data


def prepend_host_to_links(resource, hostname):
    host = f"http://{hostname}"
    for key in resource["links"]:
        resource["links"][key] = f'{host}{resource["links"][key]}'
    return resource
