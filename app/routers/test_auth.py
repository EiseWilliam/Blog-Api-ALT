from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_register_new_user():
    # Register a new user
    response = client.post(
        "/register",
        json={
            "email": "test@example.com",
            "username": "testuser",
            "password": "password",
            "confirm_password": "password"
        }
    )

    # Check that the user was registered successfully
    assert response.status_code == 201
    assert response.json()["status"] == "User registered successfully!"
    assert "access_token" in response.cookies
    assert "refresh_token" in response.cookies
    assert "logged_in" in response.cookies