from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_show_profile():
    # Create a new user
    response = client.post(
        "/users/",
        json={
            "username": "testuser",
            "password": "testpassword",
            "email": "testuser@example.com"
        }
    )
    user_id = response.json()["id"]

    # Retrieve the user's profile
    response = client.get(
        "/users/",
        headers={"Authorization": f"Bearer {response.json()['access_token']}"}
    )

    # Check that the profile was retrieved successfully
    assert response.status_code == 200
    assert response.json()["user"]["id"] == user_id
    assert response.json()["message"] == "User profile retrieved successfully"

    # Delete the user
    response = client.delete(f"/users/{user_id}")
    assert response.status_code == 200
    assert response.json()["message"] == "User deleted successfully"


def test_show_profile_unauthorized():
    # Try to retrieve the user's profile without authorization
    response = client.get("/users/")

    # Check that the request was unauthorized
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"


def test_show_profile_invalid_token():
    # Try to retrieve the user's profile with an invalid token
    response = client.get(
        "/users/",
        headers={"Authorization": "Bearer invalid_token"}
    )

    # Check that the request was unauthorized
    assert response.status_code == 401
    assert response.json()["detail"] == "Could not validate credentials"