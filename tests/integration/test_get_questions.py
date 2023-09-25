import pytest


pytestmark = pytest.mark.usefixtures(
    "bids_db_setup_and_teardown", "questions_db_setup_and_teardown"
)


def test_get_questions(test_client, api_key):
    headers = {
        "host": "localhost:8080",
        "X-API-Key": api_key,
    }

    response = test_client.get(
        "/api/bids/be15c306-c85b-4e67-a9f6-682553c065a1/questions", headers=headers
    )

    assert response.status_code == 200
    assert len(response.get_json()["items"]) == 2
