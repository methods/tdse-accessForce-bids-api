from unittest.mock import patch


# Case 1: Successful hard delete question
@patch("api.controllers.question_controller.db")
def test_delete_question_success(mock_db, test_client, admin_jwt):
    mock_db["bids"].find_one_return_value = {
        "_id": "1ff45b42-b72a-464c-bde9-9bead14a07b9",
        "alias": "ONS",
        "bid_date": "2023-06-23",
        "bid_folder_url": "https://organisation.sharepoint.com/Docs/dummyfolder",
        "client": "Office for National Statistics",
        "links": {
            "questions": "/bids/1ff45b42-b72a-464c-bde9-9bead14a07b9/questions",
            "self": "/bids/1ff45b42-b72a-464c-bde9-9bead14a07b9",
        },
        "status": "in_progress",
        "tender": "Business Intelligence and Data Warehousing",
        "was_successful": False,
    }
    response = test_client.delete(
        "/api/bids/1ff45b42-b72a-464c-bde9-9bead14a07b9/questions/6e7d3f8a-fab3-4ebf-8348-96d0808d325e",
        headers={"Authorization": f"Bearer {admin_jwt}"},
    )
    mock_db["bids"].find_one.assert_called_once_with(
        {"_id": "1ff45b42-b72a-464c-bde9-9bead14a07b9"}
    )
    mock_db["questions"].delete_one.assert_called_once_with(
        {"_id": "6e7d3f8a-fab3-4ebf-8348-96d0808d325e"}
    )
    assert response.status_code == 204


# Case 2: Failed to call database
@patch("api.controllers.question_controller.db")
def test_delete_question_connection_error(mock_db, test_client, admin_jwt):
    mock_db["questions"].delete_one.side_effect = Exception
    response = test_client.delete(
        "/api/bids/1ff45b42-b72a-464c-bde9-9bead14a07b9/questions/6e7d3f8a-fab3-4ebf-8348-96d0808d325e",
        headers={"Authorization": f"Bearer {admin_jwt}"},
    )
    assert response.status_code == 500
    assert response.get_json() == {"Error": "Could not connect to database"}


# Case 3: Validation error
@patch("api.controllers.question_controller.db")
def test_delete_question_validation_error(mock_db, test_client, admin_jwt):
    response = test_client.delete(
        "/api/bids/invalid-bid-id/questions/6e7d3f8a-fab3-4ebf-8348-96d0808d325e",
        headers={"Authorization": f"Bearer {admin_jwt}"},
    )
    assert response.status_code == 400
    assert response.get_json() == {"Error": "{'id': ['Invalid Id']}"}


# Case 4: Related bid not found
@patch("api.controllers.question_controller.db")
def test_delete_question_bid_not_found(mock_db, test_client, admin_jwt):
    mock_db["bids"].find_one.return_value = None
    response = test_client.delete(
        "/api/bids/1ff45b42-b72a-464c-bde9-9bead14a07b9/questions/6e7d3f8a-fab3-4ebf-8348-96d0808d325e",
        headers={"Authorization": f"Bearer {admin_jwt}"},
    )

    mock_db["bids"].find_one.assert_called_once_with(
        {"_id": "1ff45b42-b72a-464c-bde9-9bead14a07b9"}
    )
    assert response.status_code == 404
    mock_db["questions"].delete_one.assert_not_called()
    assert response.get_json() == {"Error": "Resource not found"}


# Case 5: Unauthorized - invalid token
@patch("api.controllers.question_controller.db")
def test_delete_question_unauthorized(mock_db, test_client):
    response = test_client.delete(
        "/api/bids/1ff45b42-b72a-464c-bde9-9bead14a07b9/questions/6e7d3f8a-fab3-4ebf-8348-96d0808d325e",
        headers={"Authorization": "Bearer N0tV4l1djsonW3Bt0K3n"},
    )
    assert response.status_code == 401
    assert response.get_json() == {"Error": "Unauthorized"}


# Case 6: Forbidden - not admin
@patch("api.controllers.question_controller.db")
def test_delete_question_forbidden(mock_db, test_client, basic_jwt):
    response = test_client.delete(
        "/api/bids/1ff45b42-b72a-464c-bde9-9bead14a07b9/questions/6e7d3f8a-fab3-4ebf-8348-96d0808d325e",
        headers={"Authorization": f"Bearer {basic_jwt}"},
    )
    assert response.status_code == 403
    assert response.get_json() == {"Error": "Forbidden"}


# # Case 7: Idempotence - question not found / already deleted
# @patch("api.controllers.question_controller.db")
# def test_delete_question_idempotence(mock_db, test_client, admin_jwt):
#     response = test_client.delete(
#         "/api/bids/1ff45b42-b72a-464c-bde9-9bead14a07b9/questions/6e7d3f8a-fab3-4ebf-8348-96d0808d325e",
#         headers={"Authorization": f"Bearer {admin_jwt}"},
#     )
#     assert response.status_code == 204
