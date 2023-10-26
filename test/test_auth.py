from fastapi.testclient import TestClient


from ..app.main import app
from .clear_test_db import clear_user

client = TestClient(app)


def test_register_new_user():
    # Register a new user
    response = client.post(
        "auth/register",
        json={
            "email": "test@example.com",
            "username": "testuser",
            "password": "password123",
            "confirm_password": "password123"
        }
    )

    # Check that the user was registered successfully
    assert response.status_code == 201
    assert response.json()["status"] == "success"
    assert response.json()["message"] == "User registered successfully!"
    assert "access_token" in response.cookies
    assert "refresh_token" in response.cookies
    assert "logged_in" in response.cookies
    
def test_wrong_confirm_password():
    response = client.post(
        "auth/register",
        json={
            "email": "test1@example.com",
            "username": "testuser",
            "password": "password123",
            "confirm_password": "Notpassword123"
        }
    )
    assert response.status_code == 400
    assert response.json()["message"] == "Passwords do not match"
    
    
def test_register_existing_user():
    # Register a new user
    response = client.post(
        "auth/register",
        json={
            "email": "test1@example.com",
            "username": "testuser",
            "password": "password123",
            "confirm_password": "password123"
        }
    )
    # register again
    response = client.post(
        "auth/register",
        json={
            "email": "test1@example.com",
            "username": "testuser",
            "password": "password123",
            "confirm_password": "password123"
        }
    )
    
    assert response.status_code == 409
    assert response.json()["message"] == "User already registered"
    
def test_wrong_password():
    # Login the user with wrong password
    response = client.post(
        "auth/login",
        data={
            "username": "test@example.com",
            "password": "wrongpassword"
        }
    )

    # Check that the user was not logged in
    assert response.status_code == 401
    assert response.json()["status"] == "error"
    assert response.json()["message"] == "Incorrect password"
  

def test_nonuser_login():
    # Login the user with wrong password
    response = client.post(
        "auth/login",
        data={
            "username": "nonuser@example.com",
            "password": "password123"
        })
    
    assert response.status_code == 404
    assert response.json()["status"] == "error"
    assert response.json()["message"] == "User not registered"
    
    

def test_login_user():
    # Login the user
    response = client.post(
        "auth/login",
        data={
            "username": "test@example.com",
            "password": "password123"
        }
    )

    # Check that the user was logged in successfully
    assert response.status_code == 200
    assert response.json()["status"] == "success"
    
    assert "access_token" in response.cookies
    assert "refresh_token" in response.cookies
    assert "logged_in" in response.cookies
  

def test_logout_user():
    # Logout the user
        # Login the user
    response = client.post(
        "auth/login",
        data={
            "username": "test@example.com",
            "password": "password123"
        }
    )
    access_token = response.json()["access_token"]

    response = client.post(
        "auth/logout",
        headers={
            "Authorization": "bearer " + access_token
        }
    )

    # Check that the user was logged out successfully
    assert response.status_code == 200
    assert response.json()["status"] == "success"
    assert "access_token" not in response.cookies
    assert "refresh_token" not in response.cookies
    assert "logged_in" not in response.cookies
   
   
def test_clear_db():
    cleared = clear_user()
    assert cleared == True 
    
