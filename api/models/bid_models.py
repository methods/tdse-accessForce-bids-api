from flask import request, jsonify
from api.schemas.bid_schema import Bid, BidSchema
from api.schemas.phase_schema import Phase
from api.schemas.feedback_schema import Feedback
from helpers.helpers import save_in_memory

def get_bids():
    f = open('./db.txt','r')
    bids = f.read()
    f.close()
    return bids, 200
    

def create_bid():
    # mandatory_fields = ['tender', 'client', 'bid_date']
    # if not request.is_json:
    #     return 'Invalid JSON', 400
    
    # for field in mandatory_fields:
    #     if field not in request.json:
    #         return 'Missing mandatory field: %s' % field, 400
        
    # BidSchema object   
    bid_document = Bid(
        tender= request.json['tender'],
        client= request.json['client'],
        alias= request.json.get('alias', ''),
        bid_date= request.json['bid_date'],
        bid_folder_url= request.json.get('bid_folder_url', ''),
        feedback= request.json.get('feedback', '')
    )
    # Add successful phase info to success list
    successPhases= [Phase(phase=3, has_score=True, score=50, out_of=100), Phase(phase=4, has_score=True, score=50, out_of=100)]
    for phase in successPhases:
        bid_document.addSuccessPhase(phase)
            
    # Add failed phase info
    failedPhase = bid_document.setFailedPhase(Phase(phase=3, has_score=True, score=50, out_of=100))

    # Add feedback info
    feedback = Feedback(description="Description of feedback", url="https://organisation.sharepoint.com/Docs/dummyfolder/feedback")
    bid_document.addFeedback(feedback)
    
    # Serialize bid_document object
    schema = BidSchema()
    data = schema.dump(bid_document)

    # Save data in memory
    save_in_memory('./db.txt', data)

    return data, 201