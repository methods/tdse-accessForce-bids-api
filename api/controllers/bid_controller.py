
from flask import Blueprint
from api.models.bid_models import get_bids, create_bid

bid = Blueprint('bid', __name__)

@bid.route("/bids", methods=["GET"])
def get_all_bids():
    response = get_bids()
    return response

@bid.route("/bids", methods=["POST"])
def post_bid():
    response = create_bid()
    return response

