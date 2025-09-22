# backend/app/schemas/status.py
from pydantic import BaseModel, Field
from typing import Literal

AllowedStatus = Literal["REVIEWED", "ESCALATED", "SUSPENDED"]

class StatusUpdateIn(BaseModel):
    new_status: AllowedStatus
    reviewer_initials: str = Field(min_length=1, max_length=8)
    notes: str | None = None

class StatusUpdateOut(BaseModel):
    domain_name: str
    new_status: AllowedStatus
    reviewer_initials: str
    notes: str | None = None
