"""
This file contains tests for the phase schema.
"""
from unittest.mock import patch


# Case 1: score is mandatory when has_score is set to True
@patch("api.controllers.bid_controller.current_app.db")
def test_score_is_mandatory(mock_db, test_client, basic_jwt):
    data = {
        "tender": "Business Intelligence and Data Warehousing",
        "client": "Office for National Statistics",
        "bid_date": "2023-06-21",
        "success": [{"phase": 1, "has_score": True, "out_of": 36}],
    }

    response = test_client.post(
        "api/bids", json=data, headers={"Authorization": f"Bearer {basic_jwt}"}
    )
    assert response.status_code == 400
    assert (
        response.get_json()["Error"]
        == "{'success': {0: {'_schema': ['Score is mandatory when has_score is set to true.']}}}"
    )


# Case 2: out_of is mandatory when has_score is set to True
@patch("api.controllers.bid_controller.current_app.db")
def test_out_of_is_mandatory(mock_db, test_client, basic_jwt):
    data = {
        "tender": "Business Intelligence and Data Warehousing",
        "client": "Office for National Statistics",
        "bid_date": "2023-06-21",
        "failed": {"phase": 2, "has_score": True, "score": 20},
    }

    response = test_client.post(
        "api/bids", json=data, headers={"Authorization": f"Bearer {basic_jwt}"}
    )
    assert response.status_code == 400
    assert (
        response.get_json()["Error"]
        == "{'failed': {'_schema': ['Out_of is mandatory when has_score is set to true.']}}"
    )
