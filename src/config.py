"""
System Configuration and Ontology Definitions for Cynbit AI Sentinel
"""

from typing import Dict, List

# Core Aspect Categories and Seed Keywords
ASPECT_TAXONOMY: Dict[str, List[str]] = {
    "Product & Quality": [
        "product", "quality", "food", "taste", "dish", "meal", "flavour", "bug",
        "feature", "performance", "speed", "code", "software", "material", "item"
    ],
    "Staff & Management": [
        "staff", "manager", "receptionist", "waiter", "cashier", "doctor", "nurse",
        "representative", "executive", "team", "behavior", "attitude", "polite", "arrogant", "rude"
    ],
    "Service & Operations": [
        "service", "wait", "waiting", "delay", "slow", "fast", "prompt", "quick",
        "delivery", "order", "process", "booking", "appointment", "checkin", "checkout"
    ],
    "Billing & Pricing": [
        "bill", "price", "expensive", "charge", "charged", "cost", "refund",
        "payment", "money", "fee", "transaction", "pricing", "value", "overpriced"
    ],
    "Facility & Infrastructure": [
        "room", "ac", "air conditioning", "clean", "dirty", "hygiene", "washroom",
        "bathroom", "ambience", "atmosphere", "parking", "outage", "downtime", "sync", "server", "crash"
    ]
}

# Critical Crisis Lexicons (Severity Trigger Words)
CRISIS_TRIGGERS: Dict[str, List[str]] = {
    "LEGAL_REGULATORY": [
        "lawyer", "attorney", "court", "police", "fssai", "consumer court", "sue",
        "legal notice", "fir", "litigation", "regulatory"
    ],
    "HEALTH_SAFETY": [
        "food poisoning", "hospitalized", "hospital", "acute", "injury", "bleeding",
        "infection", "negligence", "toxic", "vomiting", "expired"
    ],
    "FINANCIAL_FRAUD": [
        "fraud", "scam", "stolen", "theft", "double charged", "unauthorized",
        "cheat", "swindle", "extortion", "card cloned"
    ],
    "CRITICAL_OUTAGE": [
        "production outage", "downtime", "database down", "sla penalty", "data leak",
        "breach", "zero day", "dropped checkout", "catastrophic failure"
    ]
}

# Hinglish Polarity Markers for Indian Market Context
HINGLISH_LEXICON: Dict[str, float] = {
    "bahot accha": 0.8,
    "badhiya": 0.75,
    "shandar": 0.85,
    "theek tha": 0.05,
    "maza aa gaya": 0.9,
    "bahot slow": -0.7,
    "bekaar": -0.85,
    "kharab": -0.8,
    "bakwas": -0.9,
    "koi dhyan nahi": -0.65,
    "fraud hai": -0.95
}

# Severity Levels
SEVERITY_LEVELS = {
    "NORMAL": 1,
    "WATCHLIST": 2,
    "WARNING": 3,
    "CRITICAL": 4
}

# Persona System Prompts for Response Generation
RESPONSE_PERSONAS = {
    "empathetic": "A warm, deeply empathetic customer success manager who acknowledges distress, takes immediate accountability without defensive remarks, and offers an expedited resolution.",
    "vip_concierge": "An elite executive guest relations lead who prioritizes high-tier patrons, offering direct private communication channels and bespoke remediation.",
    "professional": "A polite, balanced, and fact-focused corporate representative seeking structured details to continuously improve services.",
    "crisis_defusal": "A senior legal and risk mitigation lead who acknowledges critical complaints with utmost gravity, offers immediate direct escalations, while adhering strictly to compliance.",
    "appreciative": "An enthusiastic and appreciative brand ambassador who thanks loyal promoters and invites them back with VIP warmth."
}
