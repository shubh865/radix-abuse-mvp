# backend/app/api/report_router.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from datetime import datetime

from app.db.session import get_db
from app.schemas.report import ReportCreate, ReportOut
from app.core.risk import compute_risk
from app.models.domain import Domain, DomainStatus
from app.models.report import Report, AbuseType, RiskLevel
from app.models.domain_status_history import DomainStatusHistory


router = APIRouter()

@router.post("/report", response_model=ReportOut, status_code=201)
def create_report(payload: ReportCreate, db: Session = Depends(get_db)):
    # upsert domain
    domain = db.scalar(select(Domain).where(Domain.domain_name == payload.domain_name))
    if domain is None:
        domain = Domain(
            domain_name=payload.domain_name,
            current_status=DomainStatus.UNDER_REVIEW,  # optional: mark as under review on first report
        )
        db.add(domain)
        db.flush()  # get domain_id

    # compute risk from rules
    risk = compute_risk(
        domain_name=payload.domain_name,
        abuse_type=payload.abuse_type,
        confidence_score=payload.confidence_score,
    )

    # insert report
    report = Report(
        domain_id=domain.domain_id,
        reporter_source=payload.reporter_source,
        abuse_type=AbuseType[payload.abuse_type],
        reported_timestamp=payload.timestamp,
        confidence_score=payload.confidence_score,
        risk_level=RiskLevel[risk],
    )
    db.add(report)

    # optional: keep domain’s current_risk_level in sync with max (simple bump-up)
    # if risk is HIGH, we could later store it on Domain; minimal spec doesn’t require it.

    db.commit()
    db.refresh(report)

    # build response
    return ReportOut(
        report_id=report.report_id,
        domain_name=domain.domain_name,
        abuse_type=report.abuse_type.value,
        risk_level=report.risk_level.value,
        reported_timestamp=report.reported_timestamp,
    )

from typing import List
from sqlalchemy import select, desc
from app.schemas.report import ReportListItem

@router.get("/reports", response_model=List[ReportListItem])
def list_reports(db: Session = Depends(get_db)):
    # newest first
    stmt = (
        select(Report, Domain.domain_name)
        .join(Domain, Domain.domain_id == Report.domain_id)
        .order_by(desc(Report.reported_timestamp))
    )
    rows = db.execute(stmt).all()

    # rows are tuples (Report, domain_name) due to the select
    items: list[ReportListItem] = []
    for report, domain_name in rows:
        items.append(
            ReportListItem(
                report_id=report.report_id,
                domain_name=domain_name,
                abuse_type=report.abuse_type.value,
                risk_level=report.risk_level.value,
                reported_timestamp=report.reported_timestamp,
            )
        )
    return items

from fastapi import Path
from app.schemas.domain import DomainDetailOut, DomainOut, StatusHistoryOut
from app.schemas.report import ReportOut

@router.get("/report/{domain_name}", response_model=DomainDetailOut)
def get_domain_detail(
    domain_name: str = Path(..., description="Domain name, e.g., verify-paypal-online.online"),
    db: Session = Depends(get_db),
):
    # find the domain
    domain = db.scalar(select(Domain).where(Domain.domain_name == domain_name.lower()))
    if not domain:
        raise HTTPException(status_code=404, detail="Domain not found")

    # fetch reports (newest first)
    rep_rows = db.execute(
        select(Report)
        .where(Report.domain_id == domain.domain_id)
        .order_by(desc(Report.reported_timestamp))
    ).scalars().all()

    # fetch status history (newest first)
    sh_rows = db.execute(
        select(DomainStatusHistory)
        .where(DomainStatusHistory.domain_id == domain.domain_id)
        .order_by(desc(DomainStatusHistory.created_at))
    ).scalars().all()

    # build response
    return DomainDetailOut(
        domain=DomainOut(
            domain_id=domain.domain_id,
            domain_name=domain.domain_name,
            current_status=domain.current_status.value,
        ),
        reports=[
            ReportOut(
                report_id=r.report_id,
                domain_name=domain.domain_name,
                abuse_type=r.abuse_type.value,
                risk_level=r.risk_level.value,
                reported_timestamp=r.reported_timestamp,
            ).model_dump()
            for r in rep_rows
        ],
        status_history=[
            StatusHistoryOut(
                status_id=s.status_id,
                new_status=s.new_status.value,
                reviewer_initials=s.reviewer_initials,
                notes=s.notes,
                created_at=s.created_at,
            )
            for s in sh_rows
        ],
    )

from app.schemas.status import StatusUpdateIn, StatusUpdateOut
from app.models.domain import DomainStatus
from app.models.domain_status_history import DomainStatusHistory

@router.post("/domains/{domain_name}/status", response_model=StatusUpdateOut)
def update_domain_status(
    domain_name: str,
    payload: StatusUpdateIn,
    db: Session = Depends(get_db),
):
    # find the domain
    domain = db.scalar(select(Domain).where(Domain.domain_name == domain_name.lower()))
    if not domain:
        raise HTTPException(status_code=404, detail="Domain not found")

    # convert pydantic literal to our enum
    enum_status = DomainStatus[payload.new_status]

    # write history row
    history = DomainStatusHistory(
        domain_id=domain.domain_id,
        new_status=enum_status,
        reviewer_initials=payload.reviewer_initials,
        notes=payload.notes,
    )
    db.add(history)

    # update the domain’s current status (for quick dashboard display)
    domain.current_status = enum_status

    db.commit()

    return StatusUpdateOut(
        domain_name=domain.domain_name,
        new_status=payload.new_status,
        reviewer_initials=payload.reviewer_initials,
        notes=payload.notes,
    )
