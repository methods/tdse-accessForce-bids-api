import pytest


pytestmark = pytest.mark.usefixtures("integration_setup_and_teardown")


def test_delete_bid(test_app, test_client, admin_jwt):
    headers = {"host": "localhost:8080", "Authorization": f"Bearer {admin_jwt}"}
    id = "be15c306-c85b-4e67-a9f6-682553c065a1"

    response = test_client.delete(f"/api/bids/{id}", headers=headers)

    assert response.status_code == 204
    assert test_app.db["bids"].count_documents({"status": {"$ne": "deleted"}}) == 1
