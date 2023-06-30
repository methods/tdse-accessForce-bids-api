from flask import request
from api.schemas.bid_request import BidRequestSchema

def get_bids():
    f = open('./db.txt','r')
    bids = f.read()
    f.close()
    return bids, 200

def create_bid():
    # De-serialize request body and validate against Marshmallow schema
    bid = BidRequestSchema().load(request.json)
    return bid