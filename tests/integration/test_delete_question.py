import pytest


pytestmark = pytest.mark.usefixtures(
    "bids_db_setup_and_teardown", "questions_db_setup_and_teardown"
)


def test_delete_question(test_app, test_client, admin_jwt):
    headers = {
        "host": "localhost:8080",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {admin_jwt}",
    }
    id = "6e7d3f8a-fab3-4ebf-8348-96d0808d325e"

    response = test_client.delete(
        f"/api/bids/be15c306-c85b-4e67-a9f6-682553c065a1/questions/{id}",
        headers=headers,
    )

    assert response.status_code == 204
    assert test_app.db["questions"].count_documents({"status": {"$ne": "deleted"}}) == 1
