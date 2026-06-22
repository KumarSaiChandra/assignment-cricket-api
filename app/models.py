

from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.sql import func
from app.database import Base


class Player(Base):
    __tablename__ = "players"   # name of the table in PostgreSQL

    id       = Column(String, primary_key=True, index=True)
    name     = Column(String, nullable=False)
    country  = Column(String, nullable=False)
    role     = Column(String, nullable=False)
    jersey_number  = Column(Integer, unique=True, nullable=False)
    matches_played = Column(Integer, default=0)
    runs_scored    = Column(Integer, default=0)
    created_at     = Column(DateTime(timezone=True), server_default=func.now())