"""
Customer Churn & Revenue-at-Risk Estimator
Quantifies business impact, retention urgency, and Customer Lifetime Value (CLV) exposure.
"""

from typing import Dict, Any


class ChurnRiskEstimator:
    """
    Translates raw sentiment scores and crisis indicators into financial exposure
    and churn likelihood metrics.
    """

    # Baseline average annual customer value benchmarks (in INR)
    TIER_BENCHMARKS = {
        "STANDARD": 15000,
        "VIP": 150000,
        "ENTERPRISE": 1200000
    }

    def estimate(
        self,
        polarity_score: float,
        rating: int,
        severity_level: str,
        customer_tier: str = "Standard"
    ) -> Dict[str, Any]:
        tier = customer_tier.upper() if customer_tier else "STANDARD"
        base_clv = self.TIER_BENCHMARKS.get(tier, 15000)

        # Baseline churn probability from rating
        if rating == 1:
            churn_base = 0.70
        elif rating == 2:
            churn_base = 0.45
        elif rating == 3:
            churn_base = 0.20
        elif rating == 4:
            churn_base = 0.05
        else:
            churn_base = 0.01

        # Adjust with polarity
        polarity_penalty = max(0.0, -polarity_score * 0.25)
        churn_prob = min(0.99, churn_base + polarity_penalty)

        # Multiplier from crisis severity
        severity_multipliers = {
            "NORMAL": 1.0,
            "WATCHLIST": 1.15,
            "WARNING": 1.35,
            "CRITICAL": 1.60
        }
        churn_prob = min(0.99, churn_prob * severity_multipliers.get(severity_level, 1.0))
        churn_prob = round(churn_prob, 2)

        # Financial exposure
        revenue_at_risk = int(base_clv * churn_prob)

        # Churn tier classification
        if churn_prob >= 0.75:
            risk_tier = "EXTREME"
        elif churn_prob >= 0.45:
            risk_tier = "HIGH"
        elif churn_prob >= 0.20:
            risk_tier = "MODERATE"
        else:
            risk_tier = "LOW"

        return {
            "churn_probability": churn_prob,
            "churn_risk_tier": risk_tier,
            "customer_tier": tier,
            "estimated_clv": base_clv,
            "estimated_revenue_at_risk": revenue_at_risk,
            "currency": "INR"
        }
