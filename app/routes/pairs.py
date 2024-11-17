from fastapi import APIRouter, HTTPException, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from app.database import pairs, pair_stats, registered_users  # Import shared data
import random

# Initialize router and templates
router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/")
def list_pairs(request: Request):
    """
    Render a page listing all pairs with their stats.

    Args:
        request (Request): The request object for rendering the template.

    Returns:
        TemplateResponse: Rendered template with pair and stats information.
    """
    # Prepare data to handle None values in pairs
    processed_pairs = []
    for pair in pairs:
        pair_key = "-".join([p for p in pair if p is not None])
        stats = pair_stats.get(pair_key, {"games_played": 0, "games_won": 0, "games_lost": 0})
        processed_pairs.append({"pair": pair, "stats": stats})

    return templates.TemplateResponse(
        "pairs.html", {"request": request, "processed_pairs": processed_pairs}
    )

@router.post("/generate/")
def generate_pairs():
    """
    Generate random pairs from registered users.

    Returns:
        dict: Information about generated pairs and their stats.

    Raises:
        HTTPException: If there are not enough registered users to generate pairs.
    """
    if len(registered_users) < 2:
        raise HTTPException(status_code=400, detail="Not enough users to generate pairs.")

    # Shuffle the users and create pairs
    shuffled_users = registered_users[:]
    random.shuffle(shuffled_users)
    global pairs, pair_stats
    pairs.clear()
    pair_stats.clear()

    pairs = [
        (shuffled_users[i], shuffled_users[i + 1] if i + 1 < len(shuffled_users) else None)
        for i in range(0, len(shuffled_users), 2)
    ]

    # Initialize pair stats, handling None in pairs
    pair_stats.update({
        "-".join([p for p in pair if p is not None]): {
            "games_played": 0,
            "games_won": 0,
            "games_lost": 0
        }
        for pair in pairs
    })

    return {"pairs": pairs, "pair_stats": pair_stats}

@router.post("/add-match/{pair_name}/")
def add_match(pair_name: str, result: str = Form(...)):
    """
    Update the stats for a specific pair based on match results.

    Args:
        pair_name (str): The unique identifier for the pair.
        result (str): The result of the match, either "win" or "loss".

    Returns:
        RedirectResponse: Redirects to the pairs list page.

    Raises:
        HTTPException: If the pair is not found or the result is invalid.
    """
    if pair_name not in pair_stats:
        raise HTTPException(status_code=404, detail="Pair not found.")

    if result not in ["win", "loss"]:
        raise HTTPException(status_code=400, detail="Invalid result. Must be 'win' or 'loss'.")

    pair_stats[pair_name]["games_played"] += 1
    if result == "win":
        pair_stats[pair_name]["games_won"] += 1
    elif result == "loss":
        pair_stats[pair_name]["games_lost"] += 1

    return RedirectResponse("/pairs", status_code=303)
