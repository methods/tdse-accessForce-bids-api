import pytest, os
import requests


pytestmark = pytest.mark.usefixtures("integration_setup_and_teardown")


@pytest.mark.integration
def test_get_bids_with_api_key(test_client, api_key):
    headers = {
        "host": "localhost:8080",
        "Content-Type": "application/json",
        "X-API-Key": api_key,
    }

    response = test_client.get("/api/bids", headers=headers)

    env = os.environ.get("TEST_ENVIRONMENT")
    print("This", env)
    assert response.status_code == 200
    assert len(response.get_json()["items"]) == 2
