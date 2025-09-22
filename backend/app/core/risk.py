# backend/app/core/risk.py
from typing import Literal

RiskLevel = Literal["LOW", "MEDIUM", "HIGH"]

SUSPICIOUS_KEYWORDS = ("paypal", "secure", "login", "chase")

def compute_risk(domain_name: str, abuse_type: str, confidence_score: int) -> RiskLevel:
    # rule 1: confidence > 80 => HIGH
    if confidence_score > 80:
        return "HIGH"
    # rule 2: abuse type is phishing or malware => HIGH
    if abuse_type in ("PHISHING", "MALWARE"):
        return "HIGH"
    # rule 3: suspicious keywords in domain => HIGH
    dn = domain_name.lower()
    if any(k in dn for k in SUSPICIOUS_KEYWORDS):
        return "HIGH"
    # fallback: simple medium/low split
    return "MEDIUM" if confidence_score >= 50 else "LOW"
