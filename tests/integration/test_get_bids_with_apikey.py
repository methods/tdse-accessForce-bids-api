# import pytest
import requests


# @pytest.mark.skip
def test_get_bids_with_api_key():
    auth_response = requests.get("http://localhost:5000/authorise/")

    api_key = auth_response.json()["API_KEY"]

    headers = {"Content-Type": "application/json", "X-API-Key": api_key}

    get_response = requests.get("http://localhost:8080/api/bids", headers=headers)

    assert auth_response.status_code == 200
    assert auth_response.json()["API_KEY"] is not None
    assert get_response.status_code == 200
    # 1 bid out of 10 has "status": "deleted"
    assert get_response.json()["total_count"] == 9
    assert get_response.json()["limit"] == 20
    assert get_response.json()["offset"] == 0
