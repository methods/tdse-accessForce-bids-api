import pytest
from marshmallow import ValidationError
from api.schemas.question_schema import QuestionSchema
from helpers.helpers import is_valid_uuid, is_valid_isoformat


# Case 1: New instance of bid model class generates expected fields
def test_question_model():
    data = {
        "description": "This is a question",
        "question_url": "https://organisation.sharepoint.com/Docs/dummyfolder",
        "feedback": {
            "description": "Good feedback",
            "url": "https://organisation.sharepoint.com/Docs/dummyfolder",
        },
    }
    bid_id = "be15c306-c85b-4e67-a9f6-682553c065a1"
    data["bid_id"] = bid_id
    bid_document = QuestionSchema().load(data)
    to_post = QuestionSchema().dump(bid_document)

    question_id = to_post["_id"]
    # Test that UUID is generated and is valid UUID
    assert to_post["_id"] is not None
    assert is_valid_uuid(question_id) is True
    # Test UUID validator
    assert is_valid_uuid("99999") is False

    # Test that links object is generated and URLs are correct
    assert to_post["links"] is not None
    assert "self" in to_post["links"]
    assert to_post["links"]["self"] == f"/api/bids/{bid_id}/questions/{question_id}"
    assert "bid" in to_post["links"]
    assert to_post["links"]["bid"] == f"/api/bids/{bid_id}"

    # Test that status is set to in_progress
    assert to_post["status"] == "in_progress"

    # Test that last_updated field has been added and is valid
    assert to_post["last_updated"] is not None
    assert is_valid_isoformat(to_post["last_updated"]) is True
    # Test ISOformat validator
    assert is_valid_isoformat("07-06-2023") is False


# Case 2: Field validation - description
def test_validate_description():
    data = {
        "description": 42,
        "question_url": "https://organisation.sharepoint.com/Docs/dummyfolder",
        "feedback": {
            "description": "Good feedback",
            "url": "https://organisation.sharepoint.com/Docs/dummyfolder",
        },
    }
    bid_id = "be15c306-c85b-4e67-a9f6-682553c065a1"
    data["bid_id"] = bid_id
    with pytest.raises(ValidationError):
        QuestionSchema().load(data)


# Case 3: Field validation - question_url
def test_validate_description():
    data = {
        "description": "This is a question",
        "question_url": "Not a valid url",
        "feedback": {
            "description": "Good feedback",
            "url": "https://organisation.sharepoint.com/Docs/dummyfolder",
        },
    }
    bid_id = "be15c306-c85b-4e67-a9f6-682553c065a1"
    data["bid_id"] = bid_id
    with pytest.raises(ValidationError):
        QuestionSchema().load(data)


# Case 4: Field validation - feedback description
def test_validate_feedback_description():
    data = {
        "description": "This is a question",
        "question_url": "https://organisation.sharepoint.com/Docs/dummyfolder",
        "feedback": {
            "description": 42,
            "url": "https://organisation.sharepoint.com/Docs/dummyfolder",
        },
    }
    bid_id = "be15c306-c85b-4e67-a9f6-682553c065a1"
    data["bid_id"] = bid_id
    with pytest.raises(ValidationError):
        QuestionSchema().load(data)


# Case 5: Field validation - feedback url
def test_validate_feedback_url():
    data = {
        "description": "This is a question",
        "question_url": "https://organisation.sharepoint.com/Docs/dummyfolder",
        "feedback": {
            "description": "Good feedback",
            "url": "Not a valid url",
        },
    }
    bid_id = "be15c306-c85b-4e67-a9f6-682553c065a1"
    data["bid_id"] = bid_id
    with pytest.raises(ValidationError):
        QuestionSchema().load(data)
