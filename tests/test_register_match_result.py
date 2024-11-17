from fastapi.testclient import TestClient
from app.main import app
from app.database import tournament_bracket

client = TestClient(app)

def setup_function():
    # Clear tournament bracket before each test
    tournament_bracket.clear()

def test_register_match_result():
    # Add a round manually to the tournament bracket
    tournament_bracket.append([{
        "pair1": ("Player1", "Player2"),
        "pair2": ("Player3", "Player4"),
        "winner": None
    }])
    
    # Register match result
    response = client.post("/tournament/register-match-result/", json={
        "round_index": 0,
        "match_index": 0,
        "winner": "Player1-Player2"
    })
    
    # Verify response and updated bracket
    assert response.status_code == 200
    assert tournament_bracket[0][0]["winner"] == "Player1-Player2"
