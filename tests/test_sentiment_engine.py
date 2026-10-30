"""
Unit tests for AspectSentimentEngine
"""

import pytest
from src.models.sentiment_engine import AspectSentimentEngine


@pytest.fixture
def engine():
    return AspectSentimentEngine()


def test_positive_sentiment_detection(engine):
    text = "Wonderful experience! The staff was extremely polite and the food was delicious."
    res = engine.analyze(text=text, rating=5)

    assert res["overall_sentiment"] == "Positive"
    assert res["polarity_score"] > 0.2
    assert "Staff & Management" in res["aspect_breakdown"]
    assert res["aspect_breakdown"]["Staff & Management"]["sentiment"] == "Positive"


def test_negative_sentiment_and_negation(engine):
    text = "The room was not clean and service was terribly slow."
    res = engine.analyze(text=text, rating=1)

    assert res["overall_sentiment"] == "Negative"
    assert res["polarity_score"] < -0.15
    assert "Facility & Infrastructure" in res["aspect_breakdown"]


def test_hinglish_polarity(engine):
    text = "Khana theek tha lekin service bahot slow thi."
    res = engine.analyze(text=text, rating=2)

    assert res["overall_sentiment"] == "Negative"
    assert "Service & Operations" in res["aspect_breakdown"]


def test_neutral_sentiment(engine):
    text = "The product arrived on Tuesday as scheduled."
    res = engine.analyze(text=text, rating=3)

    assert res["overall_sentiment"] in ["Neutral", "Positive"]
