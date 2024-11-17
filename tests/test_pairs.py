from fastapi.testclient import TestClient
from app.main import app
from app.database import users, pairs

client = TestClient(app)

def setup_function():
    # Clear users and pairs before each test
    pairs.clear()

def test_generate_random_pairs():
    # Add users for pairing
    client.post("/users/register/", json={"username": "Player1"})
    client.post("/users/register/", json={"username": "Player2"})
    client.post("/users/register/", json={"username": "Player3"})
    
    # Generate pairs
    response = client.post("/pairs/generate-random/")
    assert response.status_code == 200
    assert len(response.json()["pairs"]) > 0

def test_list_pairs():
    # Add a pair manually
    pairs.append(("Player1", "Player2"))
    
    # List pairs
    response = client.get("/pairs/")
    assert response.status_code == 200
    assert "pairs" in response.json()

def test_update_pair():
    # Add users and a pair
    users.extend(["Player1", "Player2", "Player3"])
    pairs.append(("Player1", "Player2"))
    
    # Update the pair
    response = client.put("/pairs/0/", json={"player1": "Player3", "player2": "Player2"})
    assert response.status_code == 200
    assert response.json()["message"] == "Pair 0 updated to (Player3, Player2)."

def test_delete_pair():
    """
    Test deleting a pair by its index.
    """
    # Add a specific pair manually
    pairs.append(("Player1", "Player2"))
    print(f"Pairs before deletion: {pairs}")

    # Delete the pair
    response = client.delete("/pairs/0/")
    print(f"Pairs after deletion: {pairs}")

    assert response.status_code == 200
    assert response.json() == {"message": "Pair ('Player1', 'Player2') deleted successfully."}

    # Confirm the pair has been removed
    assert len(pairs) == 0
