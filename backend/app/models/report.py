# backend/app/models/report.py
from sqlalchemy import Integer, String, Enum, DateTime, ForeignKey, SmallInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from app.models.base import Base
from app.models.domain import Domain  # for typing
import enum

class AbuseType(enum.Enum):
    PHISHING = "PHISHING"
    MALWARE = "MALWARE"
    BOTNET_C2 = "BOTNET_C2"
    CSAM = "CSAM"
    SPAM = "SPAM"
    OTHER = "OTHER"

class RiskLevel(enum.Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"

class Report(Base):
    __tablename__ = "reports"

    report_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    domain_id: Mapped[int] = mapped_column(ForeignKey("domains.domain_id", ondelete="CASCADE"), index=True, nullable=False)

    reporter_source: Mapped[str] = mapped_column(String(100), nullable=False)
    abuse_type: Mapped[AbuseType] = mapped_column(Enum(AbuseType), nullable=False)

    reported_timestamp: Mapped["DateTime"] = mapped_column(DateTime(timezone=True), nullable=False)

    confidence_score: Mapped[int] = mapped_column(SmallInteger, nullable=False)  # 0-100

    risk_level: Mapped[RiskLevel] = mapped_column(Enum(RiskLevel), nullable=False)

    created_at: Mapped["DateTime"] = mapped_column(DateTime(timezone=True), server_default=func.now())

    # relationship
    domain: Mapped["Domain"] = relationship(back_populates="reports")
