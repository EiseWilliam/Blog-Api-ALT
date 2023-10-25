from fastapi.testclient import TestClient
from app.main import app



client = TestClient(app)

def test_edit_article_by_id():
    # Create a new article
    response = client.post(
        "/articles/",
        json={
            "title": "Test Article",
            "body": "This is a test article",
            "category": ["politics"]
        }
    )
    article_id = response.json()["id"]


    # Edit the article
    response = client.patch(
        f"/articles/?article_id={article_id}",
        json={
            "title": "Updated Test Article",
            "body": "This is an updated test article",
            "category": ["politics", "sports"]
        }
    )

    # Check that the article was updated successfully
    assert response.status_code == 200
    assert response.json()["article"]["id"] == article_id
    assert response.json()["message"] == "Article updated successfully"

    # Delete the article
    response = client.delete(f"/articles/?article_id={article_id}")
    assert response.status_code == 200
    assert response.json()["message"] == "Article deleted successfully"