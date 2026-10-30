"""
Unit tests for CrisisSentinelDetector
"""

import pytest
from src.models.crisis_detector import CrisisSentinelDetector


@pytest.fixture
def detector():
    return CrisisSentinelDetector()


def test_critical_legal_and_health_crisis(detector):
    text = "Severe food poisoning after eating the seafood platter. We are filing a police complaint and contacting our lawyer."
    res = detector.evaluate(text=text, polarity_score=-0.8, rating=1, customer_tier="Standard")

    assert res["severity_level"] == "CRITICAL"
    assert res["requires_human_approval"] is True
    assert res["response_sla_hours"] <= 2
    assert "LEGAL_REGULATORY" in res["matched_trigger_categories"]
    assert "HEALTH_SAFETY" in res["matched_trigger_categories"]


def test_enterprise_outage_crisis(detector):
    text = "Critical production outage! Dropped 15000 checkouts, seeking SLA penalty."
    res = detector.evaluate(text=text, polarity_score=-0.9, rating=1, customer_tier="Enterprise")

    assert res["severity_level"] == "CRITICAL"
    assert res["requires_human_approval"] is True


def test_normal_review_no_crisis(detector):
    text = "Great service and loved the atmosphere. Will visit again!"
    res = detector.evaluate(text=text, polarity_score=0.8, rating=5, customer_tier="Standard")

    assert res["severity_level"] == "NORMAL"
    assert res["requires_human_approval"] is False
