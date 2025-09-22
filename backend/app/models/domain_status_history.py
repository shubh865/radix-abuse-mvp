# backend/app/models/domain_status_history.py
from sqlalchemy import Integer, String, Enum, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from app.models.base import Base
from app.models.domain import Domain, DomainStatus

class DomainStatusHistory(Base):
    __tablename__ = "domain_status_history"

    status_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    domain_id: Mapped[int] = mapped_column(ForeignKey("domains.domain_id", ondelete="CASCADE"), index=True, nullable=False)

    new_status: Mapped[DomainStatus] = mapped_column(Enum(DomainStatus), nullable=False)
    reviewer_initials: Mapped[str] = mapped_column(String(8), nullable=False)
    notes: Mapped[str | None] = mapped_column(String(500), nullable=True)

    created_at: Mapped["DateTime"] = mapped_column(DateTime(timezone=True), server_default=func.now())

    # relationship
    domain: Mapped["Domain"] = relationship(back_populates="status_history")
