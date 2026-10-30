"""
Sentinel Orchestrator Pipeline
Unified intelligence workflow connecting Aspect Sentiment, Crisis Early-Warning,
Financial Exposure, and Grounded Response Generation.
"""

from typing import Dict, List, Any, Optional
import pandas as pd
from src.models import (
    AspectSentimentEngine,
    CrisisSentinelDetector,
    ChurnRiskEstimator,
    GroundedResponseGenerator
)


class SentinelOrchestrator:
    """
    Central workflow engine executing the complete AI review lifecycle.
    """

    def __init__(self):
        self.sentiment_engine = AspectSentimentEngine()
        self.crisis_detector = CrisisSentinelDetector()
        self.churn_estimator = ChurnRiskEstimator()
        self.response_generator = GroundedResponseGenerator()

    def process_review(
        self,
        text: str,
        business_name: str = "Enterprise Partner",
        branch_location: str = "Main Branch",
        rating: Optional[int] = None,
        customer_tier: str = "Standard",
        customer_name: str = "Guest",
        override_persona: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Executes end-to-end cognitive review intelligence on a single review.
        """
        # Step 1: ABSA Sentiment Analysis
        sentiment_res = self.sentiment_engine.analyze(text=text, rating=rating)
        polarity = sentiment_res["polarity_score"]

        # Step 2: Crisis and Reputational Anomaly Detection
        effective_rating = rating if rating is not None else (1 if polarity < -0.3 else 5 if polarity > 0.3 else 3)
        crisis_res = self.crisis_detector.evaluate(
            text=text,
            polarity_score=polarity,
            rating=effective_rating,
            customer_tier=customer_tier
        )

        # Step 3: Churn and Financial Risk Exposure
        churn_res = self.churn_estimator.estimate(
            polarity_score=polarity,
            rating=effective_rating,
            severity_level=crisis_res["severity_level"],
            customer_tier=customer_tier
        )

        # Step 4: Grounded Response Generation
        response_res = self.response_generator.synthesize(
            business_name=business_name,
            customer_name=customer_name,
            severity_level=crisis_res["severity_level"],
            customer_tier=customer_tier,
            polarity_score=polarity,
            aspect_breakdown=sentiment_res["aspect_breakdown"],
            override_persona=override_persona
        )

        # Synthesis
        return {
            "business_metadata": {
                "business_name": business_name,
                "branch_location": branch_location,
                "customer_tier": customer_tier,
                "rating": rating
            },
            "sentiment_intelligence": sentiment_res,
            "crisis_governance": crisis_res,
            "financial_exposure": churn_res,
            "response_intelligence": response_res
        }

    def batch_process(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Processes a dataframe of reviews and aggregates executive KPIs.
        Expected columns: text, and optionally business_name, branch_location, rating, customer_tier.
        """
        results: List[Dict[str, Any]] = []

        for _, row in df.iterrows():
            text = str(row.get("text", ""))
            business_name = str(row.get("business_name", "Enterprise Branch"))
            branch = str(row.get("branch_location", "Headquarters"))
            raw_rating = row.get("rating", None)
            try:
                rating = int(raw_rating) if pd.notna(raw_rating) else None
            except (ValueError, TypeError):
                rating = None
            customer_tier = str(row.get("customer_tier", "Standard"))

            res = self.process_review(
                text=text,
                business_name=business_name,
                branch_location=branch,
                rating=rating,
                customer_tier=customer_tier
            )
            res["review_id"] = str(row.get("review_id", f"REV-{len(results)+1:03d}"))
            results.append(res)

        # Aggregate Executive Analytics
        total_reviews = len(results)
        if total_reviews == 0:
            return {"total_reviews": 0, "results": []}

        sentiments = [r["sentiment_intelligence"]["overall_sentiment"] for r in results]
        severities = [r["crisis_governance"]["severity_level"] for r in results]
        total_revenue_risk = sum(r["financial_exposure"]["estimated_revenue_at_risk"] for r in results)
        critical_count = sum(1 for s in severities if s == "CRITICAL")
        warning_count = sum(1 for s in severities if s == "WARNING")
        human_approval_required = sum(1 for r in results if r["crisis_governance"]["requires_human_approval"])

        # Aggregate aspect complaints
        aspect_complaint_counts: Dict[str, int] = {}
        for r in results:
            for aspect, data in r["sentiment_intelligence"]["aspect_breakdown"].items():
                if data["sentiment"] == "Negative":
                    aspect_complaint_counts[aspect] = aspect_complaint_counts.get(aspect, 0) + 1

        return {
            "summary_kpis": {
                "total_processed_reviews": total_reviews,
                "positive_percentage": round((sentiments.count("Positive") / total_reviews) * 100, 1),
                "neutral_percentage": round((sentiments.count("Neutral") / total_reviews) * 100, 1),
                "negative_percentage": round((sentiments.count("Negative") / total_reviews) * 100, 1),
                "total_revenue_at_risk_inr": total_revenue_risk,
                "critical_crises_flagged": critical_count,
                "warnings_flagged": warning_count,
                "human_approvals_required": human_approval_required,
                "top_failing_aspects": sorted(aspect_complaint_counts.items(), key=lambda x: x[1], reverse=True)
            },
            "detailed_records": results
        }
