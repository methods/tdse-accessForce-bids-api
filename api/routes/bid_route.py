
from flask import Blueprint, jsonify, request
from api.schemas.bid_schema import BidSchema

bid = Blueprint('bid', __name__)

@bid.route("/bids", methods=["GET"])
def get_test():
    if request.method == "GET":
        return 'test', 200
    
@bid.route("/bids", methods=["POST"])
def create_bid():
    mandatory_fields = ['id', 'tender', 'client', 'bid_date', 'status']
    if not request.is_json:
        return jsonify({'error': 'Invalid JSON'}), 400
    
    for field in mandatory_fields:
        if field not in request.json:
            return jsonify({'error': f'Missing mandatory field: {field}'}), 400
    
    # Create a mock BidSchema object with sample values
    bid_schema = BidSchema(
        id=request.json['id'],
        tender=request.json['tender'],
        client=request.json['client'],
        alias=request.json.get('alias', ''),
        bid_date=request.json['bid_date'],
        bid_folder_url=request.json.get('bid_folder_url', ''),
        status='in-progress',
        links={
            'self': f"/bids/{request.json['id']}",
            'questions': f"/bids/{request.json['id']}/questions"
        },
        was_successful=request.json.get('was_successful', ''),
        success=request.json.get('success', []),
        failed=request.json.get('failed', {}),
        feedback=request.json.get('feedback', {}),
        last_updated=''
    )
    
    # Convert the mock BidSchema object to a dictionary
    bid_json = bid_schema.toDbCollection()
    return bid_json, 201

@bid.errorhandler(404)
def notFound(error=None):
    message = {
        "message": "Resource not found",
        "status": 404
    }
    response = jsonify(message)
    response.status_code = 404
    return response
