from fastapi.testclient import TestClient
from app.main import app
from app.database import pairs
from app.routes.stats import pair_stats

client = TestClient(app)

def setup_function():
    # Clear pairs and stats before each test
    pairs.clear()
    pair_stats.clear()

def test_predict_winner():
    # Add pairs and stats
    pairs.append(("Player1", "Player2"))
    pair_stats["Player1-Player2"] = {"games_played": 5, "games_won": 4, "games_lost": 1}
    
    # Predict winner
    response = client.get("/predictions/predict-winner/")
    assert response.status_code == 200
    assert response.json()["predicted_winner"] == "Player1-Player2"
    assert "win_rate" in response.json()
