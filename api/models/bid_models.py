from flask import request, jsonify
from api.schemas.bid_schema import BidSchema, Status
from api.schemas.phase_schema import PhaseInfo

def get_bids():
    f = open('./db.txt','r')
    bids = f.read()
    f.close()
    return bids, 200
    

def create_bid():
    mandatory_fields = ['tender', 'client', 'bid_date']
    if not request.is_json:
        return jsonify({'error': 'Invalid JSON'}), 400
    
    for field in mandatory_fields:
        if field not in request.json:
            return jsonify({'error': f'Missing mandatory field: {field}'}), 400
        
    # BidSchema object   
    bid_schema = BidSchema(
        tender= request.json['tender'],
        client= request.json['client'],
        alias= request.json.get('alias', ''),
        bid_date= request.json['bid_date'],
        bid_folder_url= request.json.get('bid_folder_url', ''),
        feedback= request.json.get('feedback', '')
    )
    # Append phase information to the success list
    successPhases= [PhaseInfo(phase=3, has_score=True, score=50, out_of=100), PhaseInfo(phase=4, has_score=True, score=50, out_of=100)]
    for phase in successPhases:
        bid_schema.addSuccessPhase(phase)
            
    # Set failed phase info
    failedPhase = bid_schema.setFailedPhase(PhaseInfo(phase=3, has_score=True, score=50, out_of=100))
    
    # Convert the mock BidSchema object to a dictionary
    bid_json = bid_schema.toDbCollection()
    
    # Save data in memory
    f=open('./db.txt','a')
    f.write(str(bid_json))
    f.close

    return bid_json, 201