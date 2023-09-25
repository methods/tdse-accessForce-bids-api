import pytest


pytestmark = pytest.mark.usefixtures(
    "bids_db_setup_and_teardown", "questions_db_setup_and_teardown"
)


def test_post_question(test_app, test_client, basic_jwt):
    headers = {
        "host": "localhost:8080",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {basic_jwt}",
    }

    data = {
        "description": "This is a question",
        "question_url": "https://organisation.sharepoint.com/Docs/dummyfolder",
        "feedback": {
            "description": "This is a description",
            "url": "https://organisation.sharepoint.com/Docs/dummyfolder",
        },
    }

    response = test_client.post(
        f"/api/bids/be15c306-c85b-4e67-a9f6-682553c065a1/questions",
        json=data,
        headers=headers,
    )

    assert response.status_code == 201
    assert test_app.db["questions"].count_documents({}) == 3
    assert response.get_json()["_id"] is not None
    assert response.get_json()["last_updated"] is not None
    assert response.get_json()["links"] is not None
