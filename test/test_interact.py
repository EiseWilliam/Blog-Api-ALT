# from fastapi.testclient import TestClient
# from app.main import app

# client = TestClient(app)

# def test_like_article_success():
#     response = client.post(
#         "/articles/test-article+",
#         headers={"Authorization": "Bearer test_token"},
#         json={},
#     )
#     assert response.status_code == 202
#     assert response.json() == {"message": "liked article sucessfully"}

# def test_like_article_already_liked():
#     response = client.post(
#         "/articles/test-article+",
#         headers={"Authorization": "Bearer test_token"},
#         json={},
#     )
#     assert response.status_code == 400
#     assert response.json() == {"detail": "You have already liked this article"}