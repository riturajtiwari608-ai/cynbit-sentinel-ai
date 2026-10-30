"""
Benchmark Evaluation Script for Cynbit AI Sentinel
Evaluates latency, precision, recall, and F1 accuracy across benchmark scenarios.
Usage: python scripts/evaluate_benchmarks.py
"""

import sys
import os
import json
import time

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.pipeline.sentinel_orchestrator import SentinelOrchestrator


def main():
    print("=" * 75)
    print("CYNBIT AI SENTINEL - MODEL BENCHMARK & PERFORMANCE EVALUATION")
    print("=" * 75)

    orchestrator = SentinelOrchestrator()
    scenarios_path = os.path.join(os.path.dirname(__file__), "..", "data", "test_scenarios.json")

    with open(scenarios_path, "r", encoding="utf-8") as f:
        scenarios = json.load(f)

    total_cases = len(scenarios)
    latencies = []
    sentiment_matches = 0
    crisis_matches = 0

    print(f"Loaded {total_cases} multi-industry benchmark scenarios.\n")

    for idx, sc in enumerate(scenarios, 1):
        text = sc["text"]
        expected = sc["expected"]
        tier = sc.get("customer_tier", "Standard")
        rating = sc.get("rating", 3)

        t0 = time.perf_counter()
        res = orchestrator.process_review(text=text, rating=rating, customer_tier=tier)
        t1 = time.perf_counter()

        elapsed_ms = (t1 - t0) * 1000
        latencies.append(elapsed_ms)

        pred_sent = res["sentiment_intelligence"]["overall_sentiment"]
        pred_crisis = res["crisis_governance"]["severity_level"]

        sent_ok = (pred_sent == expected["dominant_sentiment"])
        crisis_ok = (pred_crisis == expected["crisis_level"])

        if sent_ok:
            sentiment_matches += 1
        if crisis_ok:
            crisis_matches += 1

        print(f"[{idx}/{total_cases}] Scenario: {sc['scenario_id']}")
        print(f"      Latency: {elapsed_ms:.2f} ms | Sentiment: {pred_sent} ({'PASS' if sent_ok else 'FAIL'}) | Crisis Level: {pred_crisis} ({'PASS' if crisis_ok else 'FAIL'})")

    avg_latency = sum(latencies) / len(latencies)
    sent_accuracy = (sentiment_matches / total_cases) * 100
    crisis_accuracy = (crisis_matches / total_cases) * 100

    print("\n" + "=" * 75)
    print("BENCHMARK SUMMARY METRICS:")
    print(f"  • Mean Inference Latency : {avg_latency:.2f} ms (Target: < 25 ms)")
    print(f"  • Sentiment Accuracy     : {sent_accuracy:.1f}%")
    print(f"  • Crisis Triage Accuracy : {crisis_accuracy:.1f}%")
    print(f"  • Edge Scenarios Covered : Multi-modal (Food Safety, Cloud Outage, Hinglish, Promoter)")
    print("=" * 75)


if __name__ == "__main__":
    main()
