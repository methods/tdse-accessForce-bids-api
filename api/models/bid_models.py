from flask import request
from api.schemas.bid_schema import BidModel
from api.schemas.bid_request import BidRequestSchema
from api.schemas.phase_schema import PhaseModel
from api.schemas.feedback_schema import FeedbackModel

def get_bids():
    f = open('./db.txt','r')
    bids = f.read()
    f.close()
    return bids, 200

def create_bid():
    bid= BidRequestSchema().load(request.json)
    return bid