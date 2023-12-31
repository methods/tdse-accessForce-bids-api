"""
This module contains tests for the bid schema.
"""
import pytest
from marshmallow import ValidationError
from api.schemas.bid_schema import BidSchema
from helpers.helpers import is_valid_uuid, is_valid_isoformat


# Case 1: New instance of bid model class generates expected fields
def test_bid_model():
    data = {
        "tender": "Business Intelligence and Data Warehousing",
        "client": "Office for National Statistics",
        "bid_date": "2023-06-21",
        "alias": "ONS",
        "bid_folder_url": "https://organisation.sharepoint.com/Docs/dummyfolder",
        "feedback": {
            "description": "Feedback from client in detail",
            "url": "https://organisation.sharepoint.com/Docs/dummyfolder/feedback",
        },
        "success": [{"phase": 1, "has_score": True, "out_of": 36, "score": 30}],
        "failed": {"phase": 2, "has_score": True, "score": 20, "out_of": 36},
    }
    bid_document = BidSchema().load(data)
    to_post = BidSchema().dump(bid_document)

    bid_id = to_post["_id"]
    # Test that UUID is generated and is valid UUID
    assert to_post["_id"] is not None
    assert is_valid_uuid(bid_id) is True
    # Test UUID validator
    assert is_valid_uuid("99999") is False

    # Test that links object is generated and URLs are correct
    assert to_post["links"] is not None
    assert "self" in to_post["links"]
    assert to_post["links"]["self"] == f"/api/bids/{bid_id}"
    assert "questions" in to_post["links"]
    assert to_post["links"]["questions"] == f"/api/bids/{bid_id}/questions"

    # Test that status is set to in_progress
    assert to_post["status"] == "in_progress"

    # Test that last_updated field has been added and is valid
    assert to_post["last_updated"] is not None
    assert is_valid_isoformat(to_post["last_updated"]) is True
    # Test ISOformat validator
    assert is_valid_isoformat("07-06-2023") is False


# Case 2: Field validation - tender
def test_validate_tender():
    data = {
        "tender": 42,
        "client": "Office for National Statistics",
        "bid_date": "2023-06-21",
    }
    with pytest.raises(ValidationError):
        BidSchema().load(data)


# Case 3: Field validation - client
def test_validate_client():
    data = {
        "tender": "Business Intelligence and Data Warehousing",
        "client": 42,
        "bid_date": "2023-06-21",
    }
    with pytest.raises(ValidationError):
        BidSchema().load(data)


# Case 4: Field validation - bid_date
def test_validate_bid_date():
    data = {
        "tender": "Business Intelligence and Data Warehousing",
        "client": "Office for National Statistics",
        "bid_date": "20-12-2023",
    }
    with pytest.raises(ValidationError):
        BidSchema().load(data)


# Case 5: Field validation - bid_folder_url
def test_validate_bid_folder_url():
    data = {
        "tender": "Business Intelligence and Data Warehousing",
        "client": "Office for National Statistics",
        "bid_date": "2023-06-21",
        "bid_folder_url": "Not a valid URL",
    }

    with pytest.raises(ValidationError):
        BidSchema().load(data)


# Case 6: Field validation - feedback
def test_validate_feedback():
    data = {
        "tender": "Business Intelligence and Data Warehousing",
        "client": "Office for National Statistics",
        "bid_date": "2023-06-21",
        "alias": "ONS",
        "bid_folder_url": "https://organisation.sharepoint.com/Docs/dummyfolder",
        "feedback": {"description": 42, "url": "Invalid URL"},
    }

    with pytest.raises(ValidationError):
        BidSchema().load(data)


# Case 7: Failed phase cannot be more than 2
def test_failed_phase_greater_than_2():
    data = {
        "failed": {"phase": 3, "has_score": True, "score": 20, "out_of": 36},
    }

    with pytest.raises(ValidationError, match="Must be one of: 1, 2."):
        BidSchema().load(data, partial=True)


# Case 8: Success phase cannot be more than 2
def test_success_phase_greater_than_2():
    data = {"success": [{"phase": 4, "has_score": True, "out_of": 36, "score": 30}]}

    with pytest.raises(ValidationError, match="Must be one of: 1, 2."):
        BidSchema().load(data, partial=True)


# Case 9: Success cannot have the same phase in the list
def test_phase_already_exists_in_success():
    data = {
        "tender": "Business Intelligence and Data Warehousing",
        "client": "Office for National Statistics",
        "bid_date": "2023-06-21",
        "alias": "ONS",
        "bid_folder_url": "https://organisation.sharepoint.com/Docs/dummyfolder",
        "feedback": {
            "description": "Feedback from client in detail",
            "url": "https://organisation.sharepoint.com/Docs/dummyfolder/feedback",
        },
        "success": [
            {"phase": 1, "has_score": True, "out_of": 36, "score": 30},
            {"phase": 1, "has_score": True, "out_of": 50, "score": 60},
        ],
    }

    with pytest.raises(
        ValidationError,
        match="Phase values must be unique",
    ):
        BidSchema().load(data, partial=True)


# Case 10: Success cannot contain same phase value as failed
def test_same_phase():
    data = {
        "tender": "Business Intelligence and Data Warehousing",
        "client": "Office for National Statistics",
        "bid_date": "2023-06-21",
        "alias": "ONS",
        "bid_folder_url": "https://organisation.sharepoint.com/Docs/dummyfolder",
        "feedback": {
            "description": "Feedback from client in detail",
            "url": "https://organisation.sharepoint.com/Docs/dummyfolder/feedback",
        },
        "failed": {"phase": 1, "has_score": True, "score": 20, "out_of": 36},
        "success": [{"phase": 1, "has_score": True, "out_of": 36, "score": 30}],
    }

    with pytest.raises(
        ValidationError,
        match="Phase values must be unique",
    ):
        BidSchema().load(data, partial=True)
