import pytest
from marshmallow import ValidationError
from api.schemas.update_bid_schema import UpdateBidSchema


# Case 1: Failed phase cannot be more than 2
def test_failed_phase_greater_than_2():
    data = {
        "failed": {"phase": 3, "has_score": True, "score": 20, "out_of": 36},
    }

    with pytest.raises(ValidationError, match="Must be one of: 1, 2."):
        UpdateBidSchema().load(data, partial=True)


# Case 2: Success phase cannot be more than 2
def test_success_phase_greater_than_2():
    data = {"success": [{"phase": 4, "has_score": True, "out_of": 36, "score": 30}]}

    with pytest.raises(ValidationError, match="Must be one of: 1, 2."):
        UpdateBidSchema().load(data, partial=True)


# # Case 2: Success cannot have the same phase in the list
# def test_phase_already_exists_in_success():
#     data = {
#         "tender": "Business Intelligence and Data Warehousing",
#         "client": "Office for National Statistics",
#         "bid_date": "21-06-2023",
#         "alias": "ONS",
#         "bid_folder_url": "https://organisation.sharepoint.com/Docs/dummyfolder",
#         "feedback": {
#             "description": "Feedback from client in detail",
#             "url": "https://organisation.sharepoint.com/Docs/dummyfolder/feedback",
#         },
#         "success": [
#             {"phase": 1, "has_score": True, "out_of": 36, "score": 30},
#             {"phase": 1, "has_score": True, "out_of": 50, "score": 60},
#         ],
#     }

#     with pytest.raises(
#         ValidationError,
#         match="Phase value already exists in 'success' list and cannot be repeated.",
#     ):
#         UpdateBidSchema().load(data, partial=True)


# # Case 3: Success cannot contain same phase value as failed
# def test_phase_already_in_failed():
#     data = {
#         "tender": "Business Intelligence and Data Warehousing",
#         "client": "Office for National Statistics",
#         "bid_date": "21-06-2023",
#         "alias": "ONS",
#         "bid_folder_url": "https://organisation.sharepoint.com/Docs/dummyfolder",
#         "feedback": {
#             "description": "Feedback from client in detail",
#             "url": "https://organisation.sharepoint.com/Docs/dummyfolder/feedback",
#         },
#         "failed": {"phase": 1, "has_score": True, "score": 20, "out_of": 36},
#         "success": [{"phase": 1, "has_score": True, "out_of": 36, "score": 30}],
#     }

#     with pytest.raises(
#         ValidationError,
#         match="Phase value already exists in 'failed' section and cannot be repeated.",
#     ):
#         UpdateBidSchema().load(data, partial=True)


# # Case 4: Failed cannot contain same phase value as success
# def test_phase_already_in_success():
#     data = {
#         "tender": "Business Intelligence and Data Warehousing",
#         "client": "Office for National Statistics",
#         "bid_date": "21-06-2023",
#         "alias": "ONS",
#         "bid_folder_url": "https://organisation.sharepoint.com/Docs/dummyfolder",
#         "feedback": {
#             "description": "Feedback from client in detail",
#             "url": "https://organisation.sharepoint.com/Docs/dummyfolder/feedback",
#         },
#         "success": [{"phase": 1, "has_score": True, "out_of": 36, "score": 30}],
#         "failed": {"phase": 1, "has_score": True, "score": 20, "out_of": 36},
#     }

#     with pytest.raises(ValidationError, match="Phase value already exists in 'success' list and cannot be repeated."):
#         UpdateBidSchema().load(data, partial=True)
