from fastapi import APIRouter, HTTPException, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

# Initialize router and templates
router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

# In-memory storage for the tournament bracket
tournament_bracket = []

@router.post("/generate/")
def generate_tournament():
    """
    Generate the initial tournament bracket from pairs.
    """
    from app.routes.pairs import pairs  # Import the pairs list

    if len(pairs) < 2:
        raise HTTPException(status_code=400, detail="Not enough pairs for a tournament.")

    global tournament_bracket
    tournament_bracket = []

    # Create the first round
    current_round = [{"pair1": pairs[i], "pair2": pairs[i + 1], "winner": None}
                     for i in range(0, len(pairs) - 1, 2)]
    tournament_bracket.append(current_round)

    # Handle subsequent rounds
    while len(current_round) > 1:
        current_round = [{"pair1": None, "pair2": None, "winner": None}
                         for _ in range(len(current_round) // 2)]
        tournament_bracket.append(current_round)

    return RedirectResponse("/", status_code=303)

@router.post("/register-winner/")
def register_winner(round_index: int = Form(...), match_index: int = Form(...), winner: str = Form(...)):
    """
    Register the winner of a match and advance them to the next round.
    """
    try:
        match = tournament_bracket[round_index][match_index]
    except IndexError:
        raise HTTPException(status_code=404, detail="Invalid round or match index.")

    if match["winner"] is not None:
        raise HTTPException(status_code=400, detail="Winner already registered for this match.")

    if winner not in ["-".join(match["pair1"]), "-".join(match["pair2"])]:
        raise HTTPException(status_code=400, detail="Winner must be one of the competing pairs.")

    # Register the winner
    match["winner"] = winner

    # Advance the winner to the next round
    if round_index + 1 < len(tournament_bracket):
        next_match_index = match_index // 2
        next_match = tournament_bracket[round_index + 1][next_match_index]
        if next_match["pair1"] is None:
            next_match["pair1"] = winner.split("-")
        elif next_match["pair2"] is None:
            next_match["pair2"] = winner.split("-")

    return RedirectResponse("/", status_code=303)

@router.get("/bracket/")
def get_bracket():
    """
    Retrieve the current tournament bracket.
    """
    return {"tournament_bracket": tournament_bracket}
