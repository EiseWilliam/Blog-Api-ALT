from fastapi.testclient import TestClient
from app.main import app
from app.routers import articles
from test.clear_test_db import clear_user


client = TestClient(app)

def test_setup_test_accounts():
    response = client.post(
        "auth/register",
        json={
            "email": "articletester@example.com",
            "username": "testuser0",
            "password": "password123",
            "confirm_password": "password123"
        }
    )
    assert response.status_code == 201
    response = client.post(
        "auth/register",
        json={
            "email": "articletester1@example.com",
            "username": "testuser1",
            "password": "password123",
            "confirm_password": "password123"
        }
    )
    assert response.status_code == 201
    
    
def test_article_id_operations_flow():
    # login
    response = client.post(
        "auth/login",
        data={"username": "articletester@example.com", "password": "password123"},
    )

    assert response.status_code == 200
    access_token = response.json()["access_token"]

    # Create a new article
    response = client.post(
        "/articles/",
        json={
            "title": "Test Article",
            "body": "This is a test article",
            "category": ["politics", "tech"],
        },
        headers={"Authorization": "bearer " + access_token},
    )
    assert response.status_code == 201
    article_id = response.json()["post"]["id"]

    # Edit the article
    response = client.patch(
        f"/articles/?article_id={article_id}",
        json={
            "title": "Updated Test Article",
            "body": "This is an updated test article",
            "category": ["politics", "sports"],
        },
        headers={"Authorization": "bearer " + access_token},
    )

    # Check that the article was updated successfully
    assert response.status_code == 200
    assert response.json()["article"]["id"] == article_id
    assert response.json()["status"] == "success"

    # Delete the article
    response = client.delete(
        f"/articles/?article_id={article_id}",
        headers={"Authorization": "bearer " + access_token},
    )
    assert response.status_code == 200
    assert response.json()["status"] == "success"


def test_view_articles():
    response = client.get("/articles/all")

    assert response.status_code == 200


def test_article_id_operations_flow_unauthorized():
    # Create a new article
    response = client.post(
        "/articles/",
        json={
            "title": "Test Article",
            "body": "This is a test article",
            "category": ["politics"],
        },
    )

    # Check that the request was unauthorized
    assert response.status_code == 401
    assert response.json()["message"] == "Not authenticated"

def test_article_path_operations():
    # login
    response = client.post(
        "auth/login",
        data={"username": "articletester@example.com", "password": "password123"},
    )

    assert response.status_code == 200
    access_token = response.json()["access_token"]

    # Create a new article
    response = client.post(
        "/articles/",
        json={
            "title": "Test Article",
            "body": "This is a test article",
            "category": ["politics", "tech"],
        },
        headers={"Authorization": "bearer " + access_token},
    )
    assert response.status_code == 201
    slug = response.json()["post"]["article_path"]
    
    response = client.patch(
        f"/articles/{slug}",
        json={
            "title": "Updated Test Article",
            "body": "This is an updated test article",
            "category": ["politics", "sports"],
        },
        headers={"Authorization": "bearer " + access_token},
    )

    # Check that the article was updated successfully
    assert response.status_code == 200
    assert response.json()["article"]["slug"] == slug
    assert response.json()["status"] == "success"

    # Delete the article
    response = client.delete(
        f"/articles/{slug}",
        headers={"Authorization": "bearer " + access_token},
    )
    assert response.status_code == 200
    assert response.json()["status"] == "success"
    
    
def test_insufficient_rights():
    response = client.post(
        "auth/login",
        data={"username": "articletester@example.com", "password": "password123"},
    )

    assert response.status_code == 200
    access_token = response.json()["access_token"]

    # Create a new article
    response = client.post(
        "/articles/",
        json={
            "title": "Test Article",
            "body": "This is a test article",
            "category": ["politics", "tech"],
        },
        headers={"Authorization": "bearer " + access_token},
    )
    assert response.status_code == 201
    slug = response.json()["post"]["article_path"]
    
    response = client.post(
        "auth/login",
        data={"username": "articletester1@example.com", "password": "password123"},
    )

    assert response.status_code == 200
    access_token = response.json()["access_token"]
    
    response = client.patch(
        f"/articles/{slug}",
        json={
            "title": "Updated Test Article",
            "body": "This is an updated test article",
            "category": ["politics", "sports"],
        },
        headers={"Authorization": "bearer " + access_token},
    )

    # Check that the article was updated successfully
    assert response.status_code == 401
    assert response.json()["status"] == "error"

    # Delete the article
    response = client.delete(
        f"/articles/{slug}",
        headers={"Authorization": "bearer " + access_token},
    )
    assert response.status_code == 401
    assert response.json()["status"] == "error"


def test_clear_users():
    cleared = clear_user()
    assert cleared == True