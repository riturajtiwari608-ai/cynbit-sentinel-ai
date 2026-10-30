"""
Production-Ready FastAPI Microservice for Cynbit AI Sentinel
Provides RESTful APIs for real-time review intelligence, batch ingestion, and crisis triage.
"""

from typing import List, Optional, Dict, Any
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import pandas as pd

from src.pipeline.sentinel_orchestrator import SentinelOrchestrator

# Initialize FastAPI App
app = FastAPI(
    title="Cynbit Sentinel Intelligence API",
    description="Autonomous Aspect-Based Sentiment, Crisis Early-Warning, and Reputation Intelligence Engine.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Enable CORS for cross-domain dashboard integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Orchestrator instance
orchestrator = SentinelOrchestrator()


# Request/Response Schemas with Pydantic v2 compliant examples
class ReviewAnalysisRequest(BaseModel):
    text: str = Field(..., json_schema_extra={"example": "Worst experience ever. The AC stopped working at 2 AM and the manager was rude."})
    business_name: Optional[str] = Field("Cynbit Hospitality Suite", json_schema_extra={"example": "The Grand Regent Hotel"})
    branch_location: Optional[str] = Field("Jaipur Central", json_schema_extra={"example": "Jaipur Central"})
    rating: Optional[int] = Field(None, ge=1, le=5, json_schema_extra={"example": 1})
    customer_tier: Optional[str] = Field("Standard", json_schema_extra={"example": "VIP"})
    customer_name: Optional[str] = Field("Valued Guest", json_schema_extra={"example": "Rahul Sharma"})
    override_persona: Optional[str] = Field(None, json_schema_extra={"example": "crisis_defusal"})


class BatchReviewItem(BaseModel):
    review_id: Optional[str] = None
    text: str
    business_name: Optional[str] = "Partner Store"
    branch_location: Optional[str] = "Main"
    rating: Optional[int] = None
    customer_tier: Optional[str] = "Standard"


class BatchAnalysisRequest(BaseModel):
    reviews: List[BatchReviewItem]


class CrisisScanRequest(BaseModel):
    text: str


@app.get("/")
def root():
    return {
        "service": "Cynbit AI Sentinel",
        "status": "operational",
        "version": "1.0.0",
        "author": "Rituraj Tiwari",
        "documentation": "/docs"
    }


@app.get("/api/v1/health")
def health_check():
    return {
        "status": "healthy",
        "engine_absa": "ready",
        "engine_crisis_sentinel": "active",
        "engine_churn_estimator": "calibrated"
    }


@app.post("/api/v1/analyze")
def analyze_review(payload: ReviewAnalysisRequest):
    try:
        result = orchestrator.process_review(
            text=payload.text,
            business_name=payload.business_name,
            branch_location=payload.branch_location,
            rating=payload.rating,
            customer_tier=payload.customer_tier,
            customer_name=payload.customer_name,
            override_persona=payload.override_persona
        )
        return {"success": True, "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/batch-analyze")
def batch_analyze(payload: BatchAnalysisRequest):
    try:
        data = [item.model_dump() for item in payload.reviews]
        df = pd.DataFrame(data)
        result = orchestrator.batch_process(df)
        return {"success": True, "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/crisis-scan")
def crisis_scan(payload: CrisisScanRequest):
    """
    Sub-millisecond lightweight endpoint to screen for brand crisis terms.
    """
    try:
        triggers = orchestrator.crisis_detector.scan_for_triggers(payload.text)
        is_crisis = len(triggers) > 0
        return {
            "has_crisis_trigger": is_crisis,
            "matched_categories": list(triggers.keys()),
            "matched_keywords": triggers
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
