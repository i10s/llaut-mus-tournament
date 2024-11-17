from fastapi.testclient import TestClient
from app.main import app
from app.database import users
from app.routes.stats import user_stats

client = TestClient(app)

def setup_function():
    # Clear users and user stats before each test
    users.clear()
    user_stats.clear()

def test_update_user_stats():
    # Add a user and initialize stats
    users.append("Player1")
    user_stats["Player1"] = {"games_played": 0, "games_won": 0, "games_lost": 0}
    
    # Update stats
    response = client.post("/stats/update-user-stats/", json={
        "username": "Player1",
        "games_played": 5,
        "games_won": 3,
        "games_lost": 2
    })
    
    # Verify response and updated stats
    assert response.status_code == 200
    assert user_stats["Player1"]["games_played"] == 5
    assert user_stats["Player1"]["games_won"] == 3
    assert user_stats["Player1"]["games_lost"] == 2
