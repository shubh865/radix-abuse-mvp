# backend/app/schemas/report.py
from pydantic import BaseModel, Field, field_validator
from typing import Literal
from datetime import datetime

# --- request schema (exact fields as spec) ---
class ReportCreate(BaseModel):
    domain_name: str = Field(..., examples=["verify-paypal-online.online"])
    reporter_source: str = Field(..., examples=["Netcraft"])
    abuse_type: Literal["PHISHING", "MALWARE", "BOTNET_C2", "CSAM", "SPAM", "OTHER"]
    timestamp: datetime  # store as reported_timestamp
    confidence_score: int = Field(..., ge=0, le=100)

    @field_validator("domain_name")
    @classmethod
    def normalize_domain(cls, v: str) -> str:
        v = v.strip().lower()
        # very simple sanity; we’ll trust frontend for heavy validation
        if "." not in v:
            raise ValueError("domain_name must contain a dot")
        return v

# --- minimal response for POST /report ---
class ReportOut(BaseModel):
    report_id: int
    domain_name: str
    abuse_type: str
    risk_level: Literal["LOW", "MEDIUM", "HIGH"]
    reported_timestamp: datetime

    class Config:
        from_attributes = True

# List item schema (same fields as ReportOut)
class ReportListItem(ReportOut):
    pass
