# backend/app/models/domain.py
from sqlalchemy import Integer, String, Enum, DateTime, func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base
import enum

class DomainStatus(enum.Enum):
    OPEN = "OPEN"
    UNDER_REVIEW = "UNDER_REVIEW"
    REVIEWED = "REVIEWED"
    ESCALATED = "ESCALATED"
    SUSPENDED = "SUSPENDED"
    CLOSED = "CLOSED"

class Domain(Base):
    __tablename__ = "domains"

    domain_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    domain_name: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    current_status: Mapped[DomainStatus] = mapped_column(Enum(DomainStatus), default=DomainStatus.OPEN, nullable=False)

    created_at: Mapped["DateTime"] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped["DateTime"] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # relationships
    reports: Mapped[list["Report"]] = relationship(back_populates="domain", cascade="all, delete-orphan")
    status_history: Mapped[list["DomainStatusHistory"]] = relationship(back_populates="domain", cascade="all, delete-orphan")
