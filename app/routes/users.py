# User management module placeholder
from fastapi import APIRouter, HTTPException
from app.database import users  # Import the shared users list
from app.models import User  # Import the User model

# Initialize the router for user management
router = APIRouter()

@router.post("/register/")
def register_user(user: User):
    """
    Register a new user with a unique username.

    Args:
        user (User): A Pydantic model containing the username.

    Returns:
        dict: Confirmation message if the user is successfully registered.

    Raises:
        HTTPException: If the username already exists.
    """
    if user.username in users:
        raise HTTPException(status_code=400, detail="Username already exists")
    users.append(user.username)
    return {"message": f"User '{user.username}' registered successfully."}

@router.get("/")
def list_users():
    """
    Retrieve the list of all registered users.

    Returns:
        dict: List of usernames.
    """
    return {"users": users}

@router.put("/{username}/")
def update_user(username: str, new_username: str):
    """
    Update an existing user's username.

    Args:
        username (str): The current username of the user to be updated.
        new_username (str): The new username to replace the current one.

    Returns:
        dict: Confirmation message if the username is successfully updated.

    Raises:
        HTTPException: If the current username does not exist or the new username already exists.
    """
    if username not in users:
        raise HTTPException(status_code=404, detail="User not found")
    if new_username in users:
        raise HTTPException(status_code=400, detail="New username already exists")

    # Update the username
    users[users.index(username)] = new_username
    return {"message": f"User '{username}' updated to '{new_username}' successfully."}

@router.delete("/{username}/")
def delete_user(username: str):
    """
    Delete an existing user by username.

    Args:
        username (str): The username of the user to be deleted.

    Returns:
        dict: Confirmation message if the user is successfully deleted.

    Raises:
        HTTPException: If the username does not exist.
    """
    if username not in users:
        raise HTTPException(status_code=404, detail="User not found")

    # Remove the user
    users.remove(username)
    return {"message": f"User '{username}' deleted successfully."}
