import pytest
import requests


pytestmark = pytest.mark.usefixtures("integration_setup_and_teardown")


@pytest.mark.integration
def test_get_bids_with_api_key(api_key):
    headers = {"Content-Type": "application/json", "X-API-Key": api_key}

    response = requests.get("http://localhost:8080/api/bids", headers=headers)

    assert response.status_code == 200
    assert len(response.json()["items"]) == 2
