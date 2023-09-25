import pytest


pytestmark = pytest.mark.usefixtures(
    "bids_db_setup_and_teardown", "questions_db_setup_and_teardown"
)


def test_update_question(test_app, test_client, basic_jwt):
    headers = {
        "host": "localhost:8080",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {basic_jwt}",
    }

    id = "6e7d3f8a-fab3-4ebf-8348-96d0808d325e"

    data = {"description": "THIS IS UPDATED"}

    response = test_client.put(
        f"/api/bids/be15c306-c85b-4e67-a9f6-682553c065a1/questions/{id}",
        json=data,
        headers=headers,
    )

    question = test_app.db["questions"].find_one({"_id": id})

    assert response.status_code == 200
    assert response.get_json()["description"] == "THIS IS UPDATED"
    assert question["description"] == "THIS IS UPDATED"
