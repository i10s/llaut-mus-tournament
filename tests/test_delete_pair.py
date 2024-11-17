from fastapi.testclient import TestClient
from app.main import app
from app.database import users, pairs  # Ensure correct imports for users and pairs

client = TestClient(app)

def setup_function():
    """
    Reset the users and pairs lists to ensure a clean state before each test.
    """
    users.clear()
    pairs.clear()

def test_delete_pair():
    """
    Test deleting a pair by its index.
    """
    # Add a specific pair manually
    pairs.append(("Player1", "Player2"))

    # Confirm the state before deletion
    assert len(pairs) == 1
    assert pairs[0] == ("Player1", "Player2")

    # Delete the pair
    response = client.delete("/pairs/0/")
    assert response.status_code == 200

    # Check the response message
    expected_message = {"message": "Pair ('Player1', 'Player2') deleted successfully."}
    assert response.json() == expected_message, f"Unexpected response: {response.json()}"

    # Confirm the pair has been removed
    assert len(pairs) == 0, f"Unexpected pairs list after deletion: {pairs}"
