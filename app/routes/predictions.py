# Prediction logic module placeholder
from fastapi import APIRouter, HTTPException
from app.database import pairs  # Import shared state
from app.routes.stats import pair_stats  # Import statistics data

# Initialize the router for predictions
router = APIRouter()

@router.get("/predict-winner/")
def predict_winner():
    """
    Predict the pair most likely to win the tournament based on stats.

    Returns:
        dict: The predicted winner and the reasoning.

    Raises:
        HTTPException: If no pairs are available or stats are insufficient.
    """
    if not pairs:
        raise HTTPException(status_code=404, detail="No pairs available for prediction")

    if not pair_stats:
        raise HTTPException(status_code=404, detail="No stats available for prediction")

    # Calculate win rates for each pair
    win_rates = {}
    for pair_name, stats in pair_stats.items():
        games_played = stats["games_played"]
        games_won = stats["games_won"]
        if games_played > 0:
            win_rates[pair_name] = games_won / games_played
        else:
            win_rates[pair_name] = 0

    # Find the pair with the highest win rate
    predicted_winner = max(win_rates, key=win_rates.get)
    win_rate = win_rates[predicted_winner]

    return {
        "predicted_winner": predicted_winner,
        "win_rate": f"{win_rate:.2%}",
        "reasoning": f"The pair '{predicted_winner}' has the highest win rate of {win_rate:.2%}."
    }
