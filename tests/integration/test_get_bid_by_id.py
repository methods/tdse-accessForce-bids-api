import pytest


pytestmark = pytest.mark.usefixtures("bids_db_setup_and_teardown")


def test_get_bid_by_id(test_client, api_key):
    headers = {
        "host": "localhost:8080",
        "X-API-Key": api_key,
    }
    id = "be15c306-c85b-4e67-a9f6-682553c065a1"

    response = test_client.get(f"/api/bids/{id}", headers=headers)

    assert response.status_code == 200
    assert response.get_json()["_id"] == id
