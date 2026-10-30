"""
Crisis Sentinel & Anomaly Early-Warning Detector
Monitors reputational hazards, regulatory risks, and severe service failure indicators.
"""

import re
from typing import Dict, List, Any
from src.config import CRISIS_TRIGGERS, SEVERITY_LEVELS


class CrisisSentinelDetector:
    """
    Evaluates incoming feedback for legal risks, food safety hazards,
    financial fraud allegations, and enterprise SLA disruptions.
    """

    def __init__(self):
        self.triggers = CRISIS_TRIGGERS

    def scan_for_triggers(self, text: str) -> Dict[str, List[str]]:
        """
        Identifies specific crisis keywords by category.
        """
        text_lower = text.lower()
        matched: Dict[str, List[str]] = {}

        for category, terms in self.triggers.items():
            hits = []
            for term in terms:
                pattern = rf"\b{re.escape(term)}\b"
                if re.search(pattern, text_lower):
                    hits.append(term)
            if hits:
                matched[category] = hits

        return matched

    def evaluate(
        self,
        text: str,
        polarity_score: float,
        rating: int = 3,
        customer_tier: str = "Standard"
    ) -> Dict[str, Any]:
        """
        Calculates severity level, SLA response window, and human escalation need.
        """
        matched_triggers = self.scan_for_triggers(text)
        is_high_tier = customer_tier.upper() in ["VIP", "ENTERPRISE"]

        # Base severity
        severity = "NORMAL"
        incident_tags: List[str] = []
        action_recommendation = "Standard automated response with satisfaction tracking."
        response_sla_hours = 24
        requires_human_approval = False

        total_trigger_count = sum(len(hits) for hits in matched_triggers.values())

        # Rule evaluation
        if "LEGAL_REGULATORY" in matched_triggers or "HEALTH_SAFETY" in matched_triggers:
            severity = "CRITICAL"
            requires_human_approval = True
            response_sla_hours = 1
            action_recommendation = (
                "EMERGENCY: Immediate GM & Legal Counsel escalation. Initiate phone contact within 60 mins."
            )
            for cat, words in matched_triggers.items():
                incident_tags.append(f"{cat}:{','.join(words)}")

        elif "FINANCIAL_FRAUD" in matched_triggers or "CRITICAL_OUTAGE" in matched_triggers:
            severity = "CRITICAL" if is_high_tier or polarity_score < -0.6 else "WARNING"
            requires_human_approval = True
            response_sla_hours = 2 if severity == "CRITICAL" else 4
            action_recommendation = (
                "URGENT: Route to Billing/DevOps on-call lead. Freeze automated response until investigation."
            )
            for cat, words in matched_triggers.items():
                incident_tags.append(f"{cat}:{','.join(words)}")

        elif total_trigger_count > 0 or (polarity_score < -0.5 and rating <= 2):
            if is_high_tier:
                severity = "WARNING"
                requires_human_approval = True
                response_sla_hours = 4
                action_recommendation = "High-tier churn warning. VIP Relationship Manager to intervene."
            else:
                severity = "WATCHLIST"
                requires_human_approval = False
                response_sla_hours = 12
                action_recommendation = "Priority queue: Automated response with prompt service discount."
            incident_tags.append("HIGH_DISSATISFACTION")

        elif polarity_score < -0.2:
            severity = "WATCHLIST"
            response_sla_hours = 18
            action_recommendation = "Routine dissatisfied feedback: Follow up on negative aspects."

        return {
            "severity_level": severity,
            "severity_rank": SEVERITY_LEVELS[severity],
            "requires_human_approval": requires_human_approval,
            "response_sla_hours": response_sla_hours,
            "matched_trigger_categories": list(matched_triggers.keys()),
            "matched_keywords": matched_triggers,
            "incident_tags": incident_tags,
            "recommended_action": action_recommendation
        }
