"""
Integration tests for FastAPI endpoints
"""

import pytest
import httpx
from src.api.server import app, root, health_check, analyze_review, crisis_scan, ReviewAnalysisRequest, CrisisScanRequest


def test_root_endpoint():
    data = root()
    assert data["status"] == "operational"
    assert data["service"] == "Cynbit AI Sentinel"


def test_health_endpoint():
    data = health_check()
    assert data["status"] == "healthy"
    assert data["engine_absa"] == "ready"


def test_analyze_endpoint():
    payload = ReviewAnalysisRequest(
        text="The food was delicious and the rooftop ambiance was wonderful.",
        business_name="Test Bistro",
        branch_location="Jaipur",
        rating=5,
        customer_tier="VIP"
    )
    res = analyze_review(payload)
    assert res["success"] is True
    assert res["data"]["sentiment_intelligence"]["overall_sentiment"] == "Positive"


def test_crisis_scan_endpoint():
    payload = CrisisScanRequest(text="We are reporting this to the police and filing with consumer court for fraud.")
    res = crisis_scan(payload)
    assert res["has_crisis_trigger"] is True
    assert "LEGAL_REGULATORY" in res["matched_categories"]
