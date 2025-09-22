# backend/app/models/base.py
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    """Shared base class for all models."""
    pass
