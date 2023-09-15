import pytest


pytestmark = pytest.mark.usefixtures("integration_setup_and_teardown")


def test_delete_bid(test_app, test_client, basic_jwt):
    headers = {"host": "localhost:8080", "Authorization": f"Bearer {basic_jwt}"}

    id = "be15c306-c85b-4e67-a9f6-682553c065a1"

    data = {"tender": "THIS IS UPDATED"}

    response = test_client.put(f"/api/bids/{id}", json=data, headers=headers)

    bid = test_app.db["bids"].find_one({"_id": id})

    assert response.status_code == 200
    assert response.get_json()["tender"] == "THIS IS UPDATED"
    assert bid["tender"] == "THIS IS UPDATED"
