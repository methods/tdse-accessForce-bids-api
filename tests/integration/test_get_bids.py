import pytest


pytestmark = pytest.mark.usefixtures("integration_setup_and_teardown")


def test_get_bids(test_client, api_key):
    headers = {
        "host": "localhost:8080",
        "Content-Type": "application/json",
        "X-API-Key": api_key,
    }

    response = test_client.get("/api/bids", headers=headers)

    assert response.status_code == 200
    assert len(response.get_json()["items"]) == 2
