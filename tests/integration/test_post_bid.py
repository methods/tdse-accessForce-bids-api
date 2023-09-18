import pytest


pytestmark = pytest.mark.usefixtures("integration_setup_and_teardown")


def test_post_bid(test_app, test_client, basic_jwt):
    headers = {
        "host": "localhost:8080",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {basic_jwt}",
    }

    data = {
        "bid_date": "2023-07-10",
        "client": "XYZ Innovations",
        "tender": "Advanced Analytics Platform",
    }

    response = test_client.post(f"/api/bids", json=data, headers=headers)

    assert response.status_code == 201
    assert test_app.db["bids"].count_documents({}) == 3
