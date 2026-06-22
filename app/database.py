

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()  # reads your .env file

DATABASE_URL = os.getenv("DATABASE_URL")

# Engine = actual connection to PostgreSQL
engine = create_engine(DATABASE_URL)

# SessionLocal = a factory that creates DB sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base = parent class for all our database models
Base = declarative_base()


# Dependency — gives each API request its own DB session
# automatically closes it when request is done
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()