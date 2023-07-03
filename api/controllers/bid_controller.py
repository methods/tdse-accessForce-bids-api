from flask import Blueprint, jsonify, request
from marshmallow import ValidationError
from api.schemas.bid_schema import BidSchema
from api.schemas.bid_request_schema import BidRequestSchema
from helpers.helpers import save_in_memory

bid = Blueprint('bid', __name__)

@bid.route("/bids", methods=["POST"])
def post_bid():
    # Create bid document and return error if input validation fails
    try:
        bid_document = BidRequestSchema().load(request.json)
    except ValidationError as e:
        return jsonify({"Error": str(e)}), 400
    
    # Serialize to a JSON-encoded string
    data = BidSchema().dump(bid_document)
    save_in_memory('./db.txt', data)
    return data, 201