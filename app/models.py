# Pydantic models for request and response validation
from pydantic import BaseModel
from typing import Optional, List

class User(BaseModel):
    username: str

class Pair(BaseModel):
    player1: str
    player2: str

class MatchResult(BaseModel):
    pair1: str
    pair2: str
    winner: str

class PredictionResponse(BaseModel):
    prediction: str
