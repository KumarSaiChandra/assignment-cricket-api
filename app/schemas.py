from pydantic import BaseModel
from typing import Optional


# What the user sends when registering
class PlayerCreate(BaseModel):
    name: str
    country: str
    role: str
    jersey_number: int
    matches_played: Optional[int] = 0
    runs_scored: Optional[int] = 0


# What we send back in responses
class PlayerResponse(BaseModel):
    id: str
    name: str
    country: str
    role: str
    jersey_number: int
    matches_played: int
    runs_scored: int

    class Config:
        from_attributes = True  # allows reading from SQLAlchemy model