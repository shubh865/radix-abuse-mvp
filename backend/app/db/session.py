from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import SQLALCHEMY_DATABASE_URI

engine = create_engine(SQLALCHEMY_DATABASE_URI, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# backend/app/db/session.py
from contextlib import contextmanager
from sqlalchemy.orm import Session

# FastAPI-style dependency
def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()
