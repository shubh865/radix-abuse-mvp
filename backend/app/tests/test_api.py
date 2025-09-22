# backend/app/tests/test_api.py
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.db.session import get_db
from app.models import Base  # imports all models so metadata is complete

# --- Create a temporary SQLite engine for tests (file-based so relationships work) ---
TEST_DB_URL = "sqlite:///./test_api.db"
engine = create_engine(TEST_DB_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create all tables for the test database
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

# --- Dependency override: use test DB session instead of MySQL ---
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def test_post_report_high_risk_phishing():
    payload = {
        "domain_name": "verify-paypal-online.online",
        "reporter_source": "Netcraft",
        "abuse_type": "PHISHING",
        "timestamp": "2025-09-19T08:30:00Z",
        "confidence_score": 10  # still HIGH because abuse_type is PHISHING
    }
    r = client.post("/report", json=payload)
    assert r.status_code == 201, r.text
    data = r.json()
    assert data["domain_name"] == "verify-paypal-online.online"
    assert data["abuse_type"] == "PHISHING"
    assert data["risk_level"] == "HIGH"
    assert "report_id" in data

def test_update_status_and_detail_view():
    # First ensure domain exists via a report
    payload = {
        "domain_name": "support-chase-online.online",
        "reporter_source": "Netcraft",
        "abuse_type": "SPAM",
        "timestamp": "2025-09-19T08:35:00Z",
        "confidence_score": 55  # MEDIUM here
    }
    r = client.post("/report", json=payload)
    assert r.status_code == 201

    # Update status to REVIEWED with initials
    s = client.post(
        "/domains/support-chase-online.online/status",
        json={"new_status": "REVIEWED", "reviewer_initials": "SD", "notes": "Looks suspicious"}
    )
    assert s.status_code == 200, s.text
    sdata = s.json()
    assert sdata["new_status"] == "REVIEWED"
    assert sdata["reviewer_initials"] == "SD"

    # Fetch detail; ensure status_history has one item and current_status updated
    d = client.get("/report/support-chase-online.online")
    assert d.status_code == 200, d.text
    detail = d.json()
    assert detail["domain"]["current_status"] == "REVIEWED"
    assert isinstance(detail["status_history"], list)
    assert len(detail["status_history"]) == 1
    assert detail["status_history"][0]["new_status"] == "REVIEWED"
