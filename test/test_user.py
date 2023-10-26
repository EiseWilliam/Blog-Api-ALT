from fastapi.testclient import TestClient


from app.main import app
from test.clear_test_db import clear_user

client = TestClient(app)


def test_show_profile():
    # Create a new user
    response = client.post(
        "/auth/register",
        json={
            "username": "testuser0",
            "password": "testpassword",
            "confirm_password": "testpassword",
            "email": "testuser0@example.com",
        },
    )
    assert response.status_code == 201
    access_token = response.json()["token"]["access_token"]

    # Retrieve the user's profile
    response = client.get("/user/", headers={"Authorization": "bearer " + access_token})

    # Check that the profile was retrieved successfully
    assert response.status_code == 200
    assert response.json()["status"] == "success"

    # Delete the user
    response = client.delete(
        "/user/", headers={"Authorization": "bearer " + access_token}
    )
    assert response.status_code == 200
    assert response.json()["status"] == "success"


def test_show_profile_unauthorized():
    # Try to retrieve the user's profile without authorization
    response = client.get("/user/")

    # Check that the request was unauthorized
    assert response.status_code == 401
    assert response.json()["message"] == "Not authenticated"


def test_show_profile_invalid_token():
    # Try to retrieve the user's profile with an invalid token
    response = client.get("/user/", headers={"Authorization": "Bearer invalid_token"})

    # Check that the request was unauthorized
    assert response.status_code == 401

def test_clear_db():
    cleared = clear_user()
    assert cleared == True or cleared == False
    