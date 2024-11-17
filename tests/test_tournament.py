from fastapi.testclient import TestClient
from app.main import app
from app.database import pairs, tournament_bracket

client = TestClient(app)

def setup_function():
    # Clear pairs and tournament bracket before each test
    pairs.clear()
    tournament_bracket.clear()

def test_create_tournament_bracket():
    # Add pairs for the tournament
    pairs.extend([("Player1", "Player2"), ("Player3", "Player4")])
    
    # Create bracket
    response = client.post("/tournament/create-bracket/")
    assert response.status_code == 200
    assert len(response.json()["tournament_bracket"]) > 0

def test_list_tournament_bracket():
    # Add a round manually
    tournament_bracket.append([{"pair1": ("Player1", "Player2"), "pair2": ("Player3", "Player4"), "winner": None}])
    
    # List the bracket
    response = client.get("/tournament/bracket/")
    assert response.status_code == 200
    assert "tournament_bracket" in response.json()

def test_register_match_result():
    # Add a round manually
    tournament_bracket.append([{"pair1": ("Player1", "Player2"), "pair2": ("Player3", "Player4"), "winner": None}])
    
    # Register match result
    response = client.post("/tournament/register-match-result/", json={
        "round_index": 0,
        "match_index": 0,
        "winner": "Player1-Player2"
    })
    assert response.status_code == 200
    assert tournament_bracket[0][0]["winner"] == "Player1-Player2"
