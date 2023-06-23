from flask import request, jsonify
from api.schemas.bid_schema import BidSchema, Status

def get_test():
    return 'test', 200

def create_bid():
    mandatory_fields = ['tender', 'client', 'bid_date']
    if not request.is_json:
        return jsonify({'error': 'Invalid JSON'}), 400
    
    for field in mandatory_fields:
        if field not in request.json:
            return jsonify({'error': f'Missing mandatory field: {field}'}), 400
        
    # BidSchema object   
    bid_schema = BidSchema(
        tender=request.json['tender'],
        client=request.json['client'],
        alias=request.json.get('alias', ''),
        bid_date=request.json['bid_date'],
        bid_folder_url=request.json.get('bid_folder_url', ''),
        feedback_description=request.json.get('feedback_description', ''),
        feedback_url=request.json.get('feedback_url', '')
    )
    # Append phase information to the success list
    bid_schema.addSuccessPhase(phase=2, has_score=True, score=80, out_of=100)
    # Set failed phase info
    # bid_schema.setFailedPhase(phase=3, has_score=True, score=50, out_of=100)
    # Change status
    # bid_schema.setStatus('deleted')
    # Convert the mock BidSchema object to a dictionary
    bid_json = bid_schema.toDbCollection()
    
    # Save data in memory
    f=open('./db.txt','a')
    f.write(str(bid_json))
    f.close

    return bid_json, 201