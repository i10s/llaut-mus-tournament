from fastapi.testclient import TestClient
from app.main import app
from app.database import users, pairs
from app.routes.stats import user_stats, pair_stats

client = TestClient(app)

def setup_function():
    # Clear stats and users before each test
    users.clear()
    pairs.clear()
    user_stats.clear()
    pair_stats.clear()

def test_leaderboard():
    # Add users and update stats
    users.extend(["Player1", "Player2"])
    user_stats["Player1"] = {"games_played": 5, "games_won": 3, "games_lost": 2}
    user_stats["Player2"] = {"games_played": 5, "games_won": 2, "games_lost": 3}
    
    # Get leaderboard
    response = client.get("/stats/leaderboard/")
    assert response.status_code == 200
    assert "user_leaderboard" in response.json()
    assert len(response.json()["user_leaderboard"]) == 2

def test_update_user_stats():
    # Add a user
    users.append("Player1")
    user_stats["Player1"] = {"games_played": 0, "games_won": 0, "games_lost": 0}
    
    # Update stats
    response = client.post("/stats/update-user-stats/", json={
        "username": "Player1",
        "games_played": 5,
        "games_won": 3,
        "games_lost": 2
    })
    assert response.status_code == 200
    assert user_stats["Player1"]["games_played"] == 5
    assert user_stats["Player1"]["games_won"] == 3
    assert user_stats["Player1"]["games_lost"] == 2

def test_update_pair_stats():
    # Add a pair
    pairs.append(("Player1", "Player2"))
    pair_stats["Player1-Player2"] = {"games_played": 0, "games_won": 0, "games_lost": 0}
    
    # Update stats
    response = client.post("/stats/update-pair-stats/", json={
        "pair_name": "Player1-Player2",
        "games_played": 3,
        "games_won": 2,
        "games_lost": 1
    })
    assert response.status_code == 200
    assert pair_stats["Player1-Player2"]["games_played"] == 3
    assert pair_stats["Player1-Player2"]["games_won"] == 2
    assert pair_stats["Player1-Player2"]["games_lost"] == 1
