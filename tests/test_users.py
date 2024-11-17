# Tests for user management module
from fastapi.testclient import TestClient
from app.main import app
from app.database import users  # Import users list from the database

client = TestClient(app)

def setup_function():
    """
    Clear the users list before each test to ensure a clean slate.
    """
    users.clear()

def test_register_user():
    """
    Test registering a new user and handling duplicate usernames.
    """
    # Register a new user
    response = client.post("/users/register/", json={"username": "Player1"})
    assert response.status_code == 200
    assert response.json() == {"message": "User 'Player1' registered successfully."}

    # Attempt to register the same username
    response = client.post("/users/register/", json={"username": "Player1"})
    assert response.status_code == 400
    assert response.json() == {"detail": "Username already exists"}

def test_list_users():
    """
    Test retrieving the list of registered users.
    """
    # Add a user
    client.post("/users/register/", json={"username": "Player1"})
    
    # Retrieve the list of users
    response = client.get("/users/")
    assert response.status_code == 200
    assert "users" in response.json()
    assert response.json()["users"] == ["Player1"]

def test_update_user():
    """
    Test updating a user's username.
    """
    # Register a user
    client.post("/users/register/", json={"username": "Player2"})
    
    # Update the username
    response = client.put("/users/Player2/", json={"new_username": "PlayerUpdated"})
    assert response.status_code == 200
    assert response.json() == {"message": "User 'Player2' updated to 'PlayerUpdated' successfully."}

    # Verify the update
    response = client.get("/users/")
    assert "PlayerUpdated" in response.json()["users"]

def test_delete_user():
    """
    Test deleting a user.
    """
    # Register a user
    client.post("/users/register/", json={"username": "Player3"})
    
    # Delete the user
    response = client.delete("/users/Player3/")
    assert response.status_code == 200
    assert response.json() == {"message": "User 'Player3' deleted successfully."}

    # Verify the user is deleted
    response = client.get("/users/")
    assert "Player3" not in response.json()["users"]
