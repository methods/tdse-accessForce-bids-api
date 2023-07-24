from flask import jsonify
import uuid
from datetime import datetime
from werkzeug.exceptions import UnprocessableEntity
from api.schemas.bid_schema import BidSchema
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
