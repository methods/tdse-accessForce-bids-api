
from flask import Blueprint
from api.models.bid_models import get_test, create_bid

bid = Blueprint('bid', __name__)

@bid.route("/bids", methods=["GET"])
def get_tested():
    response = get_test()
    return response

@bid.route("/bids", methods=["POST"])
def post_bid():
    response = create_bid()
    return response

