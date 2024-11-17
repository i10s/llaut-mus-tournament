# Entry point for the FastAPI application
from fastapi import FastAPI, Request, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from app.routes import users, pairs, tournament, stats, predictions

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

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Jinja2Templates for HTML rendering
templates = Jinja2Templates(directory="app/templates")

# Include routes
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(pairs.router, prefix="/pairs", tags=["Pairs"])
app.include_router(tournament.router, prefix="/tournament", tags=["Tournament"])
app.include_router(stats.router, prefix="/stats", tags=["Stats"])
app.include_router(predictions.router, prefix="/predictions", tags=["Predictions"])

# Example endpoints for template rendering
@app.get("/")
def root(request: Request):
    """
    Render the homepage using a template.
    """
    return templates.TemplateResponse("base.html", {"request": request})

@app.get("/users")
def get_users_page(request: Request):
    """
    Render the users management page.
    """
    return templates.TemplateResponse("users.html", {"request": request, "users": []})  # Replace with real data

@app.post("/users/register")
def register_user(username: str = Form(...)):
    """
    Handle user registration from a form submission.
    """
    # Replace this with your actual logic for adding users
    return RedirectResponse("/users", status_code=303)
