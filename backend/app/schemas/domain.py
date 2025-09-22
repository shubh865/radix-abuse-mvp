# backend/app/schemas/domain.py
from pydantic import BaseModel
from typing import List, Literal
from datetime import datetime

class StatusHistoryOut(BaseModel):
    status_id: int
    new_status: Literal["REVIEWED", "ESCALATED", "SUSPENDED"]
    reviewer_initials: str
    notes: str | None = None
    created_at: datetime

    class Config:
        from_attributes = True

class DomainOut(BaseModel):
    domain_id: int
    domain_name: str
    current_status: Literal["OPEN","UNDER_REVIEW","REVIEWED","ESCALATED","SUSPENDED","CLOSED"]

    class Config:
        from_attributes = True

class DomainDetailOut(BaseModel):
    domain: DomainOut
    reports: List[dict]         # we’ll build dicts using existing Report fields
    status_history: List[StatusHistoryOut]
