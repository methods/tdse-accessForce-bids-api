import pytest


pytestmark = pytest.mark.usefixtures("integration_setup_and_teardown")


def test_update_bid_status(test_app, test_client, admin_jwt):
    headers = {"host": "localhost:8080", "Authorization": f"Bearer {admin_jwt}"}

    id = "be15c306-c85b-4e67-a9f6-682553c065a1"

    data = {"status": "completed"}

    response = test_client.put(f"/api/bids/{id}/status", json=data, headers=headers)

    bid = test_app.db["bids"].find_one({"_id": id})

    assert response.status_code == 200
    assert response.get_json()["status"] == "completed"
    assert bid["status"] == "completed"
