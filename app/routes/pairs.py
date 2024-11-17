from fastapi import APIRouter, HTTPException
from app.database import users, pairs  # Import shared state
from app.models import Pair  # Import the Pair model
import random

# Initialize the router for pair management
router = APIRouter()

@router.post("/generate-random/")
def generate_random_pairs():
    """
    Generate random pairs from the list of users.

    Returns:
        dict: List of randomly generated pairs.

    Raises:
        HTTPException: If there are not enough users to generate pairs.
    """
    if len(users) < 2:
        raise HTTPException(status_code=400, detail="Not enough users to generate pairs")

    # Shuffle the users and create pairs
    random.shuffle(users)
    global pairs
    pairs.clear()  # Reset existing pairs
    pairs = [(users[i], users[i + 1]) for i in range(0, len(users) - 1, 2)]

    # Handle odd number of users
    if len(users) % 2 != 0:
        pairs.append((users[-1], None))  # Pair the last user with None

    return {"pairs": pairs}

@router.get("/")
def list_pairs():
    """
    Retrieve the list of all pairs.

    Returns:
        dict: List of pairs.
    """
    return {"pairs": pairs}

@router.put("/{pair_index}/")
def update_pair(pair_index: int, pair: Pair):
    """
    Update an existing pair.

    Args:
        pair_index (int): Index of the pair to update.
        pair (Pair): New pair information.

    Returns:
        dict: Confirmation message if the pair is updated successfully.

    Raises:
        HTTPException: If the pair index is invalid or users in the new pair are invalid.
    """
    if pair_index < 0 or pair_index >= len(pairs):
        raise HTTPException(status_code=404, detail="Pair index out of range")

    if pair.player1 not in users or (pair.player2 is not None and pair.player2 not in users):
        raise HTTPException(status_code=400, detail="Both players must be registered users")

    # Update the pair
    pairs[pair_index] = (pair.player1, pair.player2)
    return {"message": f"Pair {pair_index} updated to ({pair.player1}, {pair.player2})."}

@router.delete("/{index}/")
def delete_pair(index: int):
    """
    Delete a pair by its index.

    Args:
        index (int): The index of the pair to delete.

    Returns:
        dict: Confirmation message after deleting the pair.

    Raises:
        HTTPException: If the index is invalid.
    """
    try:
        pair = pairs.pop(index)  # Remove the pair at the specified index
    except IndexError:
        raise HTTPException(status_code=404, detail="Invalid pair index")

    return {"message": f"Pair {pair} deleted successfully."}
