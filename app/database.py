"""
This module contains the database configuration and dependencies.
"""

import os
from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv

load_dotenv()

DB_URL = os.getenv("DATABASE_URL")

engine = create_engine(DB_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
Base.metadata.create_all(bind=engine)

def get_db() -> Generator[Session, None, None]:
    """
    FastAPI dependency to get a database session.
    Yields a database session.
    Closes the database session after the context is exited.
    """

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
