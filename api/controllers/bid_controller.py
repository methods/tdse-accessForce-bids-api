from flask import Blueprint, jsonify
from api.models.bid_models import get_bids, create_bid
from api.schemas.bid_request import BidRequestSchema
from helpers.helpers import save_in_memory

bid = Blueprint('bid', __name__)

@bid.route("/bids", methods=["GET"])
def get_all_bids():
    response = get_bids()
    return response

@bid.route("/bids", methods=["POST"])
def post_bid():
    try:
        bid_document = create_bid()
        # Serialize to a JSON-encoded string
        data = BidRequestSchema().dumps(bid_document)
        save_in_memory('./db.txt', data)
        return  data, 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
