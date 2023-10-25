from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_edit_article_by_id():
    # Create a new article
    response = client.post(
        "/articles/",
        json={
            "title": "Test Article",
            "content": "This is a test article",
            "author_id": 1
        }
    )
    article_id = response.json()["id"]

    # Edit the article
    response = client.put(
        f"/articles/?article_id={article_id}",
        json={
            "title": "Updated Test Article",
            "content": "This is an updated test article"
        }
    )

    # Check that the article was updated successfully
    assert response.status_code == 200
    assert response.json()["id"] == article_id
    assert response.json()["message"] == "Article updated successfully"

    # Delete the article
    response = client.delete(f"/articles/?article_id={article_id}")
    assert response.status_code == 200
    assert response.json()["message"] == "Article deleted successfully"