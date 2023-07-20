from flask import jsonify
import uuid
from datetime import datetime
from api.schemas.bid_schema import BidSchema
from api.schemas.bid_request_schema import BidRequestSchema
from api.schemas.valid_bid_id_schema import valid_bid_id_schema


def showInternalServerError():
    return jsonify({"Error": "Could not connect to database"})


def showNotFoundError():
    return jsonify({"Error": "Resource not found"})


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
    bid_document = BidRequestSchema().load(request)
    # Serialize to a JSON object
    data = BidSchema().dump(bid_document)
    return data


def validate_bid_id_path(bid_id):
    valid_bid_id = valid_bid_id_schema().load({"bid_id": bid_id})
    data = valid_bid_id["bid_id"]
    return data


def validate_bid_update(user_request):
    data = BidSchema().load(user_request, partial=True)
    return data


def prepend_host_to_links(resource, hostname):
    host = f"http://{hostname}"
    for key in resource["links"]:
        resource["links"][key] = f'{host}{resource["links"][key]}'
    return resource
