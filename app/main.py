# Entry point for the FastAPI application
from fastapi import FastAPI
from app.routes import users, pairs, tournament, stats, predictions

# Initialize the FastAPI app
app = FastAPI(
    title="Llaut Mus Tournament",
    description="A web application to manage and visualize mus card game tournaments.",
    version="0.1.0",
)

# Include routes
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(pairs.router, prefix="/pairs", tags=["Pairs"])
app.include_router(tournament.router, prefix="/tournament", tags=["Tournament"])
app.include_router(stats.router, prefix="/stats", tags=["Stats"])
app.include_router(predictions.router, prefix="/predictions", tags=["Predictions"])

@app.get("/")
def root():
    return {"message": "Welcome to Llaut Mus Tournament API"}
