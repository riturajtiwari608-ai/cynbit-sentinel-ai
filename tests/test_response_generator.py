"""
Unit tests for GroundedResponseGenerator
"""

import pytest
from src.models.response_generator import GroundedResponseGenerator


@pytest.fixture
def generator():
    return GroundedResponseGenerator()


def test_pii_sanitization(generator):
    raw = "My phone is +91-9876543210 and email is john.doe@gmail.com and card 4111-2222-3333-4444."
    cleaned = generator.sanitize_pii(raw)

    assert "[CONFIDENTIAL_PHONE]" in cleaned
    assert "[CONFIDENTIAL_EMAIL]" in cleaned
    assert "[CONFIDENTIAL_CARD]" in cleaned
    assert "john.doe@gmail.com" not in cleaned


def test_crisis_persona_selection(generator):
    persona = generator.select_persona(severity_level="CRITICAL", customer_tier="Standard", polarity_score=-0.8)
    assert persona == "crisis_defusal"


def test_vip_persona_selection(generator):
    persona = generator.select_persona(severity_level="WARNING", customer_tier="VIP", polarity_score=-0.4)
    assert persona == "vip_concierge"


def test_grounded_response_synthesis(generator):
    aspects = {
        "Service & Operations": {"sentiment": "Negative", "score": -0.7, "confidence": 0.85, "snippets": ["slow service"]},
        "Product & Quality": {"sentiment": "Positive", "score": 0.6, "confidence": 0.8, "snippets": ["delicious food"]}
    }
    res = generator.synthesize(
        business_name="Grand Regent Hotel",
        customer_name="Rahul",
        severity_level="NORMAL",
        customer_tier="Standard",
        polarity_score=-0.4,
        aspect_breakdown=aspects
    )

    assert "Dear Rahul," in res["generated_response"]
    assert "Service & Operations" in res["addressed_negative_aspects"]
    assert res["guardrail_checks"]["pii_redacted"] is True
