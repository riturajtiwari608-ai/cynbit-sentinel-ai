"""
CLI Demonstration Runner for Cynbit AI Sentinel
Usage: python scripts/run_demo.py
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.pipeline.sentinel_orchestrator import SentinelOrchestrator


def main():
    print("=" * 80)
    print("CYNBIT AI SENTINEL - AUTONOMOUS REPUTATION INTELLIGENCE PROTOTYPE")
    print("Candidate: Rituraj Tiwari | Role: AI/ML Engineer Intern")
    print("=" * 80)

    orchestrator = SentinelOrchestrator()

    sample_review = (
        "Severe food poisoning after eating the seafood platter yesterday. Three members "
        "of our family are currently hospitalized with acute gastroenteritis. We are filing "
        "a formal complaint with the Food Safety and Standards Authority (FSSAI) and our lawyer "
        "will contact your management."
    )

    print(f"\n[INCOMING REVIEW STREAM]")
    print(f"'{sample_review}'\n")

    result = orchestrator.process_review(
        text=sample_review,
        business_name="Urban Taste Bistro",
        branch_location="Mumbai Bandra",
        rating=1,
        customer_tier="Standard",
        customer_name="Sanjay Verma"
    )

    sent = result["sentiment_intelligence"]
    crisis = result["crisis_governance"]
    fin = result["financial_exposure"]
    resp = result["response_intelligence"]

    print("=" * 80)
    print("1. SENTIMENT & ASPECT BREAKDOWN (ABSA)")
    print(f"   Overall Sentiment : {sent['overall_sentiment']} (Polarity: {sent['polarity_score']})")
    print(f"   Model Confidence  : {int(sent['confidence'] * 100)}%")
    print("   Aspect Attributes:")
    for aspect, data in sent["aspect_breakdown"].items():
        print(f"     - {aspect:<25} : {data['sentiment']} ({data['score']})")

    print("\n2. CRISIS & REPUTATIONAL GOVERNANCE")
    print(f"   Severity Level    : {crisis['severity_level']} (Rank: {crisis['severity_rank']}/4)")
    print(f"   Human Sign-off Req: {crisis['requires_human_approval']}")
    print(f"   Response SLA Window: < {crisis['response_sla_hours']} Hours")
    print(f"   Action Protocol   : {crisis['recommended_action']}")
    print(f"   Detected Triggers : {crisis['matched_keywords']}")

    print("\n3. FINANCIAL EXPOSURE & CHURN RISK")
    print(f"   Customer Tier     : {fin['customer_tier']}")
    print(f"   Estimated CLV     : INR {fin['estimated_clv']:,}")
    print(f"   Revenue at Risk   : INR {fin['estimated_revenue_at_risk']:,}")
    print(f"   Churn Risk Tier   : {fin['churn_risk_tier']} ({int(fin['churn_probability'] * 100)}%)")

    print("\n4. GROUNDED AI RESPONSE SYNTHESIS")
    print(f"   Persona Applied   : {resp['persona_applied'].upper()}")
    print(f"   PII Redacted      : {resp['guardrail_checks']['pii_redacted']}")
    print(f"   Policy Compliant  : {resp['guardrail_checks']['policy_compliant']}")
    print("-" * 80)
    print(resp["generated_response"])
    print("=" * 80)


if __name__ == "__main__":
    main()
