# Statistics and leaderboard module placeholder
from fastapi import APIRouter, HTTPException
from app.database import users, pairs  # Import shared state

# Initialize the router for stats and leaderboard
router = APIRouter()

# In-memory storage for stats
user_stats = {user: {"games_played": 0, "games_won": 0, "games_lost": 0} for user in users}
pair_stats = {"-".join(pair): {"games_played": 0, "games_won": 0, "games_lost": 0} for pair in pairs}

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
def update_user_stats(username: str, games_played: int, games_won: int, games_lost: int):
    """
    Update stats for a specific user.

    Args:
        username (str): The username of the player.
        games_played (int): The number of games played.
        games_won (int): The number of games won.
        games_lost (int): The number of games lost.

    Returns:
        dict: Confirmation message after updating stats.

    Raises:
        HTTPException: If the user is not found.
    """
    if username not in user_stats:
        raise HTTPException(status_code=404, detail="User not found")

    user_stats[username]["games_played"] += games_played
    user_stats[username]["games_won"] += games_won
    user_stats[username]["games_lost"] += games_lost
    return {"message": f"Stats updated for user '{username}'."}

@router.post("/update-pair-stats/")
def update_pair_stats(pair_name: str, games_played: int, games_won: int, games_lost: int):
    """
    Update stats for a specific pair.

    Args:
        pair_name (str): The pair name (e.g., "Player1-Player2").
        games_played (int): The number of games played.
        games_won (int): The number of games won.
        games_lost (int): The number of games lost.

    Returns:
        dict: Confirmation message after updating stats.

    Raises:
        HTTPException: If the pair is not found.
    """
    if pair_name not in pair_stats:
        raise HTTPException(status_code=404, detail="Pair not found")

    pair_stats[pair_name]["games_played"] += games_played
    pair_stats[pair_name]["games_won"] += games_won
    pair_stats[pair_name]["games_lost"] += games_lost
    return {"message": f"Stats updated for pair '{pair_name}'."}
