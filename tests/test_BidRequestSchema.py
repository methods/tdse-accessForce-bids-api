import pytest
# from flask import jsonify, request
from api.schemas.bid_schema import BidSchema
from api.schemas.bid_request_schema import BidRequestSchema

def test_bid_model():
    data = {
        "tender": "Business Intelligence and Data Warehousing",
        "client": "Office for National Statistics",
        "bid_date": "21-06-2023",
        "alias": "ONS",
        "bid_folder_url": "https://organisation.sharepoint.com/Docs/dummyfolder",
        "feedback": {
            "description": "Feedback from client in detail",
            "url": "https://organisation.sharepoint.com/Docs/dummyfolder/feedback"
        },
        "success": [
            {
                "phase": 1,
                "has_score": True,
                "out_of": 36,
                "score": 30
            }
        ],
        "failed": {
            "phase": 2,
            "has_score": True,
            "score": 20,
            "out_of": 36
        }
    }
    bid_document = BidRequestSchema().load(data)
    to_post = BidSchema().dump(bid_document)

    # Test that UUID is generated and is valid UUID
    assert to_post["_id"] is not None
    
    # Test that status is set to in_progress
    assert to_post["status"] == "in_progress"

    # Test that links object is generated and URLs are correct
    id = to_post["_id"]
    assert to_post["links"] is not None
    assert "self" in to_post["links"]
    assert to_post["links"]["self"] == f"/bids/{id}"
    assert 'questions' in to_post["links"]
    assert to_post["links"]["questions"] == f"/bids/{id}/questions"

    # Test that last_updated field has been added and is valid
    assert to_post["last_updated"] is not None