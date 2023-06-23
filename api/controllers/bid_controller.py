
from flask import Blueprint
from flasgger import swag_from
from api.models.bid_models import get_test, create_bid

bid = Blueprint('bid', __name__)

@bid.route("/bids", methods=["GET"])
def get_tested():
    response = get_test()
    return response

@bid.route("/bids", methods=["POST"])
@swag_from('../../swagger_config.yaml')
def post_bid():
    response = create_bid()
    return response

