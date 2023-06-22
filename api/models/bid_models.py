from flask import request, jsonify
from uuid import uuid4
from api.schemas.bid_schema import BidSchema

def get_test():
    return 'test', 200

def create_bid():
    mandatory_fields = ['tender', 'client', 'bid_date', 'status']
    if not request.is_json:
        return jsonify({'error': 'Invalid JSON'}), 400
    
    for field in mandatory_fields:
        if field not in request.json:
            return jsonify({'error': f'Missing mandatory field: {field}'}), 400
        
    # BidSchema object
    id_obj = uuid4()   
    bid_schema = BidSchema(
        id=id_obj,
        tender=request.json['tender'],
        client=request.json['client'],
        alias=request.json.get('alias', ''),
        bid_date=request.json['bid_date'],
        bid_folder_url=request.json.get('bid_folder_url', ''),
        status='in-progress',
        links={
            'self': f"/bids/{id_obj}",
            'questions': f"/bids/{id_obj}/questions"
        },
        was_successful=request.json.get('was_successful', ''),
        success=request.json.get('success', []),
        failed=request.json.get('failed', {}),
        feedback=request.json.get('feedback', {}),
        last_updated=''
    )
    # Convert the mock BidSchema object to a dictionary
    bid_json = bid_schema.toDbCollection()
    
    # Save data in memory
    f=open('test.txt','a')
    f.write(str(bid_json))
    f.close

    return bid_json, 201