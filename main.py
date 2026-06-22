from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import engine, get_db, Base
from app.models import Player
from app.schemas import PlayerCreate, PlayerResponse
import uuid

# Creates the 'players' table if it doesn't exist
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Cricket Players API",
    description="Register and manage cricket players — powered by PostgreSQL",
    version="2.0.0"
)


# ── Health check ──────────────────────────────────────────────────────────────
@app.get("/health")
def health(db: Session = Depends(get_db)):
    player_count = db.query(Player).count()
    return {
        "status": "ok",
        "database": "connected",
        "total_players": player_count
    }


# ── 1. Register a player ──────────────────────────────────────────────────────
@app.post("/players/register", response_model=PlayerResponse, status_code=201)
def register_player(player: PlayerCreate, db: Session = Depends(get_db)):

    # Check jersey number not already taken
    existing = db.query(Player).filter(
        Player.jersey_number == player.jersey_number
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail=f"Jersey number {player.jersey_number} is already taken"
        )

    new_player = Player(
        id=str(uuid.uuid4()),
        **player.model_dump()
    )

    db.add(new_player)       # stage the insert
    db.commit()              # write to PostgreSQL
    db.refresh(new_player)   # get the saved data back (with created_at etc)

    return new_player


# ── 2. Get one player by ID ───────────────────────────────────────────────────
@app.get("/players/{player_id}", response_model=PlayerResponse)
def get_player(player_id: str, db: Session = Depends(get_db)):

    player = db.query(Player).filter(Player.id == player_id).first()

    if not player:
        raise HTTPException(
            status_code=404,
            detail=f"Player with id '{player_id}' not found"
        )

    return player


# ── 3. Get all players ────────────────────────────────────────────────────────
@app.get("/players", response_model=list[PlayerResponse])
def get_all_players(db: Session = Depends(get_db)):
    players = db.query(Player).all()
    return players