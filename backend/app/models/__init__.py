# backend/app/models/__init__.py
from app.models.base import Base
from app.models.domain import Domain, DomainStatus
from app.models.report import Report, AbuseType, RiskLevel
from app.models.domain_status_history import DomainStatusHistory
