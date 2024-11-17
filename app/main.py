from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from app.routes import users, pairs, tournament, stats, predictions
from app.database import registered_users, user_stats, tournament_bracket  # Import shared variables

# Initialize the FastAPI app
app = FastAPI(
    title="Llaut Mus Tournament",
    description="A web application to manage and visualize mus card game tournaments.",
    version="0.1.0",
)

# Allow CORS for frontend
origins = [
    "http://localhost:3000",  # Frontend during development
    "https://llaut-mus-frontend.fly.dev",  # Frontend in production
]

# Mount the static directory
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Jinja2Templates for HTML rendering
templates = Jinja2Templates(directory="app/templates")

# Include modularized routes
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(pairs.router, prefix="/pairs", tags=["Pairs"])
app.include_router(tournament.router, prefix="/tournament", tags=["Tournament"])
app.include_router(stats.router, prefix="/stats", tags=["Stats"])
app.include_router(predictions.router, prefix="/predictions", tags=["Predictions"])


# Homepage route
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    """
    Render the homepage with the tournament bracket.
    """
    # Prepare the bracket with indexes
    bracket_with_index = list(enumerate(tournament_bracket))

    return templates.TemplateResponse(
        "home.html", {"request": request, "bracket_with_index": bracket_with_index}
    )


# Users page route
@app.get("/users", response_class=HTMLResponse)
def get_users_page(request: Request):
    """
    Render the users management page.
    """
    return templates.TemplateResponse("users.html", {"request": request, "users": registered_users})


# Register user route
@app.post("/users/register", response_class=RedirectResponse)
def register_user(username: str = Form(...)):
    """
    Handle user registration from a form submission.
    """
    if username in registered_users:
        raise HTTPException(status_code=400, detail="Username already exists.")
    # Add user and initialize stats
    registered_users.append(username)
    user_stats[username] = {"games_played": 0, "games_won": 0, "games_lost": 0}
    return RedirectResponse("/users", status_code=303)


# Leaderboard route
@app.get("/leaderboard", response_class=HTMLResponse)
def get_leaderboard_page(request: Request):
    """
    Render the leaderboard page.
    """
    # Sort users by games won (descending)
    sorted_leaderboard = sorted(user_stats.items(), key=lambda x: x[1]["games_won"], reverse=True)
    return templates.TemplateResponse(
        "leaderboard.html", {"request": request, "leaderboard": sorted_leaderboard}
    )
