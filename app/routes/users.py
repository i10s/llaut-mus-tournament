from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.database import registered_users  # Import the shared registered_users list
from app.models import User  # Import the User model

# Initialize the router for user management
router = APIRouter()

# Define the request model for updating a username
class UpdateUsernameRequest(BaseModel):
    new_username: str

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
    if user.username in registered_users:
        raise HTTPException(status_code=400, detail="Username already exists")
    registered_users.append(user.username)
    return {"message": f"User '{user.username}' registered successfully."}

@router.get("/")
def list_users():
    """
    Retrieve the list of all registered users.

    Returns:
        dict: List of usernames.
    """
    return {"users": registered_users}

@router.put("/{username}/")
def update_user(username: str, request: UpdateUsernameRequest):
    """
    Update an existing user's username.

    Args:
        username (str): The current username of the user to be updated.
        request (UpdateUsernameRequest): A Pydantic model containing the new username.

    Returns:
        dict: Confirmation message if the username is successfully updated.

    Raises:
        HTTPException: If the current username does not exist or the new username already exists.
    """
    if username not in registered_users:
        raise HTTPException(status_code=404, detail="User not found")
    if request.new_username in registered_users:
        raise HTTPException(status_code=400, detail="New username already exists")

    # Update the username
    registered_users[registered_users.index(username)] = request.new_username
    return {"message": f"User '{username}' updated to '{request.new_username}' successfully."}

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
    if username not in registered_users:
        raise HTTPException(status_code=404, detail="User not found")

    # Remove the user
    registered_users.remove(username)
    return {"message": f"User '{username}' deleted successfully."}
