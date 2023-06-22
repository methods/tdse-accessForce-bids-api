from flask import request, jsonify
from api.schemas.bid_schema import BidSchema, PhaseInfo

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
    bid_schema = BidSchema(
        tender=request.json['tender'],
        client=request.json['client'],
        alias=request.json.get('alias', ''),
        bid_date=request.json['bid_date'],
        bid_folder_url=request.json.get('bid_folder_url', ''),
        status='in-progress',
        
        failed=request.json.get('failed', {}),
        feedback=request.json.get('feedback', {})
    )
    success_phase =  PhaseInfo()
    bid_schema.success.append(success_phase(1, True, 2, 3))
    bid_schema.was_successful = bid_schema.failed == {} 
    # Convert the mock BidSchema object to a dictionary
    bid_json = bid_schema.toDbCollection()
    
    # Save data in memory
    f=open('./test.txt','a')
    f.write(str(bid_json))
    f.close

    return bid_json, 201