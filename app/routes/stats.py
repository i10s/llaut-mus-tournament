from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.database import registered_users, pairs  # Import shared state

# Initialize the router for stats and leaderboard
router = APIRouter()

# In-memory storage for stats
user_stats = {user: {"games_played": 0, "games_won": 0, "games_lost": 0} for user in registered_users}
pair_stats = {"-".join(pair): {"games_played": 0, "games_won": 0, "games_lost": 0} for pair in pairs}

# Pydantic models for validation
class UpdateUserStatsRequest(BaseModel):
    username: str
    games_played: int
    games_won: int
    games_lost: int

class UpdatePairStatsRequest(BaseModel):
    pair_name: str
    games_played: int
    games_won: int
    games_lost: int

@router.get("/leaderboard/")
def get_leaderboard():
    """
    Retrieve the leaderboard for users and pairs based on performance.

    Returns:
        dict: Leaderboard data for users and pairs.
    """
    user_leaderboard = sorted(
        user_stats.items(),
        key=lambda x: x[1]["games_won"],
        reverse=True
    )
    pair_leaderboard = sorted(
        pair_stats.items(),
        key=lambda x: x[1]["games_won"],
        reverse=True
    )
    return {
        "user_leaderboard": user_leaderboard,
        "pair_leaderboard": pair_leaderboard,
    }

@router.post("/update-user-stats/")
def update_user_stats(request: UpdateUserStatsRequest):
    """
    Update stats for a specific user.

    Args:
        request (UpdateUserStatsRequest): A Pydantic model containing the stats update data.

    Returns:
        dict: Confirmation message after updating stats.

    Raises:
        HTTPException: If the user is not found.
    """
    if request.username not in user_stats:
        raise HTTPException(status_code=404, detail="User not found")

    stats = user_stats[request.username]
    stats["games_played"] += request.games_played
    stats["games_won"] += request.games_won
    stats["games_lost"] += request.games_lost
    return {"message": f"Stats updated for user '{request.username}'."}

@router.post("/update-pair-stats/")
def update_pair_stats(request: UpdatePairStatsRequest):
    """
    Update stats for a specific pair.

    Args:
        request (UpdatePairStatsRequest): A Pydantic model containing the stats update data.

    Returns:
        dict: Confirmation message after updating stats.

    Raises:
        HTTPException: If the pair is not found.
    """
    if request.pair_name not in pair_stats:
        raise HTTPException(status_code=404, detail="Pair not found")

    stats = pair_stats[request.pair_name]
    stats["games_played"] += request.games_played
    stats["games_won"] += request.games_won
    stats["games_lost"] += request.games_lost
    return {"message": f"Stats updated for pair '{request.pair_name}'."}
