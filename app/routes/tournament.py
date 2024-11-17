from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.database import pairs, tournament_bracket  # Import shared state

# Initialize the router for tournament management
router = APIRouter()

class RegisterMatchResultRequest(BaseModel):
    round_index: int
    match_index: int
    winner: str

@router.post("/create-bracket/")
def create_tournament_bracket():
    """
    Generate the tournament bracket based on existing pairs.

    Returns:
        dict: The generated tournament bracket.

    Raises:
        HTTPException: If there are not enough pairs to create a tournament.
    """
    if len(pairs) < 2:
        raise HTTPException(
            status_code=400, detail="Not enough pairs to create a tournament bracket"
        )

    import random
    random.shuffle(pairs)  # Shuffle pairs to randomize matchups

    # Clear the global tournament bracket
    global tournament_bracket
    tournament_bracket.clear()

    # Create the initial round of matches
    current_round = [{"pair1": pairs[i], "pair2": pairs[i + 1], "winner": None}
                     for i in range(0, len(pairs) - 1, 2)]
    tournament_bracket.append(current_round)

    # Add placeholders for subsequent rounds
    while len(current_round) > 1:
        current_round = [{"pair1": None, "pair2": None, "winner": None}
                         for _ in range(len(current_round) // 2)]
        tournament_bracket.append(current_round)

    return {"tournament_bracket": tournament_bracket}

@router.get("/bracket/")
def get_tournament_bracket():
    """
    Retrieve the current state of the tournament bracket.

    Returns:
        dict: The current tournament bracket.
    """
    if not tournament_bracket:
        raise HTTPException(status_code=404, detail="Tournament bracket not created yet")
    return {"tournament_bracket": tournament_bracket}

@router.post("/register-match-result/")
def register_match_result(request: RegisterMatchResultRequest):
    """
    Register the result of a match in the tournament.

    Args:
        request (RegisterMatchResultRequest): A Pydantic model containing the match details.

    Returns:
        dict: Updated tournament bracket after registering the result.

    Raises:
        HTTPException: If the round or match index is invalid, or if the winner is invalid.
    """
    round_index = request.round_index
    match_index = request.match_index
    winner = request.winner

    try:
        match = tournament_bracket[round_index][match_index]
    except IndexError:
        raise HTTPException(status_code=404, detail="Invalid round or match index")

    if match["winner"] is not None:
        raise HTTPException(status_code=400, detail="Match already has a winner")

    valid_winners = ["-".join(match["pair1"]), "-".join(match["pair2"])]
    if winner not in valid_winners:
        raise HTTPException(status_code=400, detail=f"Winner must be one of the competing pairs: {valid_winners}")

    # Update the winner
    match["winner"] = winner

    # Advance the winner to the next round if applicable
    if round_index + 1 < len(tournament_bracket):
        next_match_index = match_index // 2
        next_match = tournament_bracket[round_index + 1][next_match_index]
        if next_match["pair1"] is None:
            next_match["pair1"] = winner.split("-")
        elif next_match["pair2"] is None:
            next_match["pair2"] = winner.split("-")

    return {"message": "Match result registered successfully", "tournament_bracket": tournament_bracket}
