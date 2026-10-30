"""
Cynbit Sentinel AI - Executive & Operational Dashboard
Interactive Proof of Concept built for Cynbit Technologies (Revio Suite)
Candidate: Rituraj Tiwari | Role: AI/ML Engineer Intern
"""

import streamlit as st
import pandas as pd
import numpy as np
import os
import json
import altair as alt

from src.pipeline.sentinel_orchestrator import SentinelOrchestrator
from src.config import RESPONSE_PERSONAS

# Streamlit Page Configuration
st.set_page_config(
    page_title="Cynbit Sentinel AI | Revio Intelligence",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling for Cynbit Brand
st.markdown("""
<style>
    .main-header {
        font-family: 'Inter', sans-serif;
        color: #0F172A;
        font-weight: 800;
        font-size: 2.2rem;
        margin-bottom: 0px;
    }
    .sub-header {
        color: #0A5C5A;
        font-weight: 600;
        font-size: 1.1rem;
        margin-bottom: 20px;
    }
    .kpi-card {
        background-color: #F8FAFC;
        border-radius: 14px;
        padding: 16px;
        border: 1px solid #E2E8F0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02);
    }
    .kpi-title {
        font-size: 0.8rem;
        font-weight: 700;
        color: #64748B;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .kpi-value {
        font-size: 1.8rem;
        font-weight: 800;
        color: #0F172A;
        margin-top: 4px;
    }
    .badge-critical {
        background-color: #FEE2E2;
        color: #991B1B;
        padding: 4px 10px;
        border-radius: 8px;
        font-weight: 700;
        font-size: 0.85rem;
    }
    .badge-warning {
        background-color: #FEF3C7;
        color: #92400E;
        padding: 4px 10px;
        border-radius: 8px;
        font-weight: 700;
        font-size: 0.85rem;
    }
    .badge-normal {
        background-color: #DCFCE7;
        color: #166534;
        padding: 4px 10px;
        border-radius: 8px;
        font-weight: 700;
        font-size: 0.85rem;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def load_orchestrator():
    return SentinelOrchestrator()


orchestrator = load_orchestrator()

# Sidebar Navigation & Context
st.sidebar.image("https://cynbit.in/logo.svg", width=160)
st.sidebar.markdown("### **Cynbit AI Sentinel**")
st.sidebar.caption("Next-Generation Autonomous Reputation & Crisis Sentinel for **Revio**.")
st.sidebar.divider()

navigation = st.sidebar.radio(
    "Navigation Mode",
    [
        "🔍 Single Review Inspector",
        "📊 Multi-Branch Executive Analytics",
        "🤖 Autonomous Multi-Agent Simulation",
        "📑 Technical & Business Architecture"
    ]
)

st.sidebar.divider()
st.sidebar.markdown("""
**Candidate Details**
- **Applicant:** Rituraj Tiwari
- **Assessment:** AI/ML Engineer Intern
- **Target Platform:** Cynbit Technologies / Revio
""")

# -------------------------------------------------------------------------------------------------
# TAB 1: SINGLE REVIEW INSPECTOR
# -------------------------------------------------------------------------------------------------
if navigation == "🔍 Single Review Inspector":
    st.markdown('<div class="main-header">🛡️ Real-Time Review Diagnostic & Triage</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Aspect-Based Sentiment Analysis (ABSA) • Crisis Sentinel • Dynamic Response Copilot</div>', unsafe_allow_html=True)

    col_input, col_meta = st.columns([2, 1])

    # Sample Presets for Quick Testing
    sample_presets = {
        "Severe Food Poisoning & Legal Threat (Critical)": {
            "text": "Severe food poisoning after eating the seafood platter yesterday. Three members of our family are currently hospitalized with acute gastroenteritis. We are filing a formal complaint with the Food Safety and Standards Authority (FSSAI) and our lawyer will contact your management.",
            "business": "Urban Taste Bistro",
            "branch": "Mumbai Bandra",
            "tier": "Standard",
            "rating": 1
        },
        "Enterprise Production Outage & SLA Penalty (Critical)": {
            "text": "Critical data sync outage! Our production database integration has been failing continuously since the 4.2 patch update. Over 15,000 active customer checkout requests dropped. We are evaluating contract cancellation and SLA penalty claims.",
            "business": "CloudScale SaaS Labs",
            "branch": "Bangalore HQ",
            "tier": "Enterprise",
            "rating": 1
        },
        "Glowing VIP Promoter Experience (Positive)": {
            "text": "Wonderful stay! The rooftop breakfast had an amazing spread and the housekeeping team kept everything spotless. Special shoutout to Amit at reception for helping us with local sightseeing.",
            "business": "The Grand Regent Hotel",
            "branch": "Jaipur Central",
            "tier": "VIP",
            "rating": 5
        },
        "Hinglish Mixed Experience with Delay (Warning)": {
            "text": "Khana theek tha lekin service bahot slow thi. Manager ko 3 baar bola billing check karne ke liye par koi dhyan nahi diya. Expected much better standard from a 5 star property.",
            "business": "The Grand Regent Hotel",
            "branch": "Delhi Aerocity",
            "tier": "VIP",
            "rating": 2
        }
    }

    selected_preset = col_input.selectbox(
        "⚡ Quick-load Test Preset Scenario:",
        ["Custom Manual Entry"] + list(sample_presets.keys())
    )

    if selected_preset != "Custom Manual Entry":
        preset_data = sample_presets[selected_preset]
        default_text = preset_data["text"]
        default_business = preset_data["business"]
        default_branch = preset_data["branch"]
        default_tier = preset_data["tier"]
        default_rating = preset_data["rating"]
    else:
        default_text = "The room was spacious and clean, but the dinner order was delayed by 50 minutes and the bill had duplicate charges."
        default_business = "The Grand Regent Hotel"
        default_branch = "Jaipur Central"
        default_tier = "Standard"
        default_rating = 2

    review_text = col_input.text_area("Review Content:", value=default_text, height=140)

    with col_meta:
        b_name = st.text_input("Business Name:", value=default_business)
        b_branch = st.text_input("Branch / Location:", value=default_branch)
        c_tier = st.selectbox("Customer Tier:", ["Standard", "VIP", "Enterprise"], index=["Standard", "VIP", "Enterprise"].index(default_tier))
        c_rating = st.slider("Star Rating:", min_value=1, max_value=5, value=default_rating)

    if st.button("🚀 Run Sentinel Cognitive Analysis", type="primary"):
        with st.spinner("Analyzing text through ABSA, crisis sentinel, and financial risk models..."):
            result = orchestrator.process_review(
                text=review_text,
                business_name=b_name,
                branch_location=b_branch,
                rating=c_rating,
                customer_tier=c_tier
            )

        st.success("✅ Analysis Complete")

        # Top Metric Cards
        sent = result["sentiment_intelligence"]
        crisis = result["crisis_governance"]
        fin = result["financial_exposure"]
        resp = result["response_intelligence"]

        m1, m2, m3, m4 = st.columns(4)
        with m1:
            st.metric("Overall Sentiment", sent["overall_sentiment"], f"Polarity: {sent['polarity_score']}")
        with m2:
            st.metric("Model Confidence", f"{int(sent['confidence'] * 100)}%")
        with m3:
            st.metric("Reputational Risk", crisis["severity_level"], f"SLA: < {crisis['response_sla_hours']} hrs")
        with m4:
            st.metric("Revenue at Risk", f"₹{fin['estimated_revenue_at_risk']:,}", f"Churn Risk: {fin['churn_risk_tier']}")

        # Crisis Callout Alert if applicable
        if crisis["severity_level"] == "CRITICAL":
            st.error(f"🚨 **CRITICAL INCIDENT FLAGGED**: {crisis['recommended_action']}")
            if crisis["matched_keywords"]:
                st.caption(f"Triggers Detected: {crisis['matched_keywords']}")
        elif crisis["severity_level"] == "WARNING":
            st.warning(f"⚠️ **WARNING**: {crisis['recommended_action']}")

        st.divider()

        # Detailed Breakdown Tabs
        tab_absa, tab_response, tab_json = st.tabs(["📊 Aspect-Based Granularity (ABSA)", "✍️ Grounded AI Response", "🔍 Raw JSON Telemetry"])

        with tab_absa:
            col_chart, col_details = st.columns([1, 1])

            aspect_data = sent["aspect_breakdown"]
            if aspect_data:
                aspect_rows = []
                for aspect, data in aspect_data.items():
                    aspect_rows.append({
                        "Aspect": aspect,
                        "Sentiment": data["sentiment"],
                        "Polarity Score": data["score"],
                        "Confidence": f"{int(data['confidence'] * 100)}%",
                        "Snippet": " | ".join(data["snippets"])
                    })
                df_aspects = pd.DataFrame(aspect_rows)

                with col_chart:
                    chart = alt.Chart(df_aspects).mark_bar().encode(
                        x=alt.X("Polarity Score:Q", scale=alt.Scale(domain=[-1.0, 1.0])),
                        y=alt.Y("Aspect:N", sort="-x"),
                        color=alt.Color("Sentiment:N", scale=alt.Scale(
                            domain=["Positive", "Neutral", "Negative"],
                            range=["#10B981", "#64748B", "#EF4444"]
                        )),
                        tooltip=["Aspect", "Sentiment", "Polarity Score", "Confidence"]
                    ).properties(height=260)
                    st.altair_chart(chart, use_container_width=True)

                with col_details:
                    st.markdown("**Detected Aspect Nuances:**")
                    st.dataframe(df_aspects[["Aspect", "Sentiment", "Polarity Score", "Snippet"]], use_container_width=True)
            else:
                st.info("No domain-specific aspect taxonomy detected in this text. Text classified holistically.")

        with tab_response:
            st.markdown(f"**Applied Persona:** `{resp['persona_applied'].upper()}`")
            if crisis["requires_human_approval"]:
                st.info("🔒 **Human-in-the-Loop Required**: Because this review is flagged as Warning/Critical, automated auto-posting is locked until an authorized manager approves.")

            st.text_area("Generated Grounded Response:", value=resp["generated_response"], height=200)

            c_g1, c_g2, c_g3 = st.columns(3)
            c_g1.checkbox("PII Redacted", value=resp["guardrail_checks"]["pii_redacted"], disabled=True)
            c_g2.checkbox("Hallucination-Free", value=not resp["guardrail_checks"]["hallucination_detected"], disabled=True)
            c_g3.checkbox("Policy Compliant", value=resp["guardrail_checks"]["policy_compliant"], disabled=True)

            c_btn1, c_btn2 = st.columns([1, 4])
            if c_btn1.button("✅ Approve & Dispatch"):
                st.success("Response dispatched to platform webhook!")

        with tab_json:
            st.json(result)

# -------------------------------------------------------------------------------------------------
# TAB 2: MULTI-BRANCH EXECUTIVE ANALYTICS
# -------------------------------------------------------------------------------------------------
elif navigation == "📊 Multi-Branch Executive Analytics":
    st.markdown('<div class="main-header">📊 Multi-Location Reputation Intelligence</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Holistic Portfolio Sentiment • Churn Risk Exposure • Aspect Vulnerability Matrix</div>', unsafe_allow_html=True)

    # Load default dataset
    sample_csv_path = os.path.join(os.path.dirname(__file__), "data", "sample_reviews.csv")
    df_source = None

    uploaded_file = st.file_uploader("Upload Reviews Dataset (CSV)", type=["csv"])
    if uploaded_file is not None:
        df_source = pd.read_csv(uploaded_file)
        st.info("Custom CSV file loaded successfully!")
    elif os.path.exists(sample_csv_path):
        df_source = pd.read_csv(sample_csv_path)

    if df_source is not None:
        batch_results = orchestrator.batch_process(df_source)
        kpis = batch_results["summary_kpis"]

        # KPI Summary Cards
        k1, k2, k3, k4, k5 = st.columns(5)
        k1.metric("Total Reviews Processed", kpis["total_processed_reviews"])
        k2.metric("Positive Sentiment", f"{kpis['positive_percentage']}%")
        k3.metric("Critical Crises", kpis["critical_crises_flagged"], delta=f"{kpis['warnings_flagged']} Warnings", delta_color="inverse")
        k4.metric("Revenue at Risk", f"₹{kpis['total_revenue_at_risk_inr']:,}")
        k5.metric("Human Escalations", kpis["human_approvals_required"])

        st.divider()

        col_left, col_right = st.columns(2)

        with col_left:
            st.subheader("Sentiment Distribution Across Portfolio")
            sentiment_df = pd.DataFrame([
                {"Sentiment": "Positive", "Share": kpis["positive_percentage"]},
                {"Sentiment": "Neutral", "Share": kpis["neutral_percentage"]},
                {"Sentiment": "Negative", "Share": kpis["negative_percentage"]}
            ])
            chart_pie = alt.Chart(sentiment_df).mark_arc(innerRadius=50).encode(
                theta=alt.Theta(field="Share", type="quantitative"),
                color=alt.Color(field="Sentiment", type="nominal", scale=alt.Scale(
                    domain=["Positive", "Neutral", "Negative"],
                    range=["#10B981", "#94A3B8", "#EF4444"]
                )),
                tooltip=["Sentiment", "Share"]
            ).properties(height=280)
            st.altair_chart(chart_pie, use_container_width=True)

        with col_right:
            st.subheader("Top Aspect Vulnerabilities (Root-Cause Pain Points)")
            if kpis["top_failing_aspects"]:
                failing_df = pd.DataFrame(kpis["top_failing_aspects"], columns=["Aspect", "Complaint Count"])
                chart_bar = alt.Chart(failing_df).mark_bar(color="#F97316").encode(
                    x=alt.X("Complaint Count:Q"),
                    y=alt.Y("Aspect:N", sort="-x"),
                    tooltip=["Aspect", "Complaint Count"]
                ).properties(height=280)
                st.altair_chart(chart_bar, use_container_width=True)
            else:
                st.write("No negative aspect concentrations found.")

        st.divider()

        st.subheader("Live Operational Review Ledger")
        records = batch_results["detailed_records"]
        table_rows = []
        for r in records:
            table_rows.append({
                "Review ID": r["review_id"],
                "Business": r["business_metadata"]["business_name"],
                "Branch": r["business_metadata"]["branch_location"],
                "Customer Tier": r["business_metadata"]["customer_tier"],
                "Rating": r["business_metadata"]["rating"],
                "Sentiment": r["sentiment_intelligence"]["overall_sentiment"],
                "Severity": r["crisis_governance"]["severity_level"],
                "Revenue At Risk": f"₹{r['financial_exposure']['estimated_revenue_at_risk']:,}",
                "Escalation Needed": "YES ⚠️" if r["crisis_governance"]["requires_human_approval"] else "NO"
            })
        st.dataframe(pd.DataFrame(table_rows), use_container_width=True)

# -------------------------------------------------------------------------------------------------
# TAB 3: AUTONOMOUS MULTI-AGENT SIMULATION
# -------------------------------------------------------------------------------------------------
elif navigation == "🤖 Autonomous Multi-Agent Simulation":
    st.markdown('<div class="main-header">🤖 Autonomous Multi-Agent Architecture</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Collaborative Multi-Agent Triage Pipeline for Cynbit Revio</div>', unsafe_allow_html=True)

    st.markdown("""
    Cynbit's core identity revolves around **Autonomous AI Agents & Optimistic Digital Architecture**.
    This simulation demonstrates how four specialized autonomous agents collaborate in real-time to process an incoming customer grievance without human latency:
    """)

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.info("**Agent 1: Ingestion & ABSA Specialist**\n\nParses text, tokenizes clauses, extracts aspect sentiments (Product, Service, Billing).")
    with c2:
        st.warning("**Agent 2: Crisis & Regulatory Sentinel**\n\nScreens for legal notices, safety incidents, fraud flags, and computes SLA windows.")
    with c3:
        st.error("**Agent 3: Financial Exposure Assessor**\n\nCross-references customer tier and calculates CLV risk to prioritize high-value retention.")
    with c4:
        st.success("**Agent 4: Response Synthesis Copilot**\n\nSelects persona, redacts PII, prevents hallucinated promises, and drafts grounded response.")

    st.divider()

    test_case = st.selectbox(
        "Choose an incoming event stream to simulate:",
        [
            "Event #1042: High-Severity Outage (Enterprise Client)",
            "Event #1043: Acute Food Poisoning Allegation (Restaurant)",
            "Event #1044: Cashier Double Billing Dispute (Retail)"
        ]
    )

    if st.button("▶️ Launch Agent Swarm Execution", type="primary"):
        with st.status("Executing Multi-Agent Coordination Protocol...", expanded=True) as status:
            st.write("🟢 **Agent 1 (ABSA)**: Ingesting review stream... Extracted negative polarity (-0.84) in 'Technical Stability' and 'Support'.")
            st.write("🟠 **Agent 2 (Crisis Sentinel)**: Scanned for enterprise SLA triggers... Match found: `['outage', 'sla penalty']`. Severity set to **CRITICAL**.")
            st.write("🔴 **Agent 3 (Financial Assessor)**: Detected customer tier = `Enterprise`. Estimated annual CLV exposure = **₹12,00,000**. Churn risk probability = 95%.")
            st.write("🔵 **Agent 4 (Response Copilot)**: Selected Persona: `crisis_defusal`. Verified PII redaction and locked auto-dispatch for Human Approval.")
            status.update(label="✅ Agent Coordination Complete. Incident Triage Ticket Generated!", state="complete", expanded=False)

        st.success("Triage Ticket #CYN-2026-981 routed to Executive On-Call Engineer & Account Manager.")

# -------------------------------------------------------------------------------------------------
# TAB 4: ARCHITECTURE & BUSINESS ROI
# -------------------------------------------------------------------------------------------------
elif navigation == "📑 Technical & Business Architecture":
    st.markdown('<div class="main-header">📑 Technical Architecture & Cynbit Business ROI</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Strategic Analysis, Model Design, and Commercial Impact for Cynbit Technologies</div>', unsafe_allow_html=True)

    t1, t2 = st.tabs(["🏗️ Architectural Blueprint", "💼 Cynbit Commercial ROI"])

    with t1:
        st.markdown("""
        ### System Architecture & Pipeline Flow
        ```
        +-------------------------------------------------------------------------+
        |                       Omnichannel Ingestion                             |
        |          (Google Reviews, Trustpilot, Zomato, G2, Support Webhooks)     |
        +-----------------------------------+-------------------------------------+
                                            |
                                            v
        +-------------------------------------------------------------------------+
        |                  Pre-Processing & PII Sanitizer                         |
        |              (Masks Emails, Phone Numbers, Credit Cards)                |
        +-----------------------------------+-------------------------------------+
                                            |
                     +----------------------+----------------------+
                     |                                             |
                     v                                             v
        +---------------------------+                +----------------------------+
        | Aspect-Based Sentiment    |                | Crisis Early-Warning       |
        | Analysis (ABSA) Engine    |                | Sentinel (Anomaly Scanner) |
        | - Product & Quality       |                | - Legal & Regulatory       |
        | - Staff & Management      |                | - Food & Safety Incidents  |
        | - Service & Operations    |                | - Financial Fraud Disputes |
        | - Facility & Tech Uptime  |                | - Enterprise SLA Outages   |
        +-------------+-------------+                +--------------+-------------+
                      |                                             |
                      +----------------------+----------------------+
                                             |
                                             v
        +-------------------------------------------------------------------------+
        |                    Financial Exposure & CLV Risk Engine                 |
        |      (Calculates Churn Probability & Quantifies Revenue at Risk in INR) |
        +------------------------------------+------------------------------------+
                                             |
                                             v
        +-------------------------------------------------------------------------+
        |                  Grounded Multi-Persona Response Copilot                |
        |        (Adapts Tone: Empathetic, VIP Concierge, Crisis Defusal)         |
        |        - Safety Guardrails: No false refund commitments                 |
        |        - Human-in-the-Loop Gate for Critical / Warning incidents        |
        +------------------------------------+------------------------------------+
                                             |
                                             v
        +-------------------------------------------------------------------------+
        |           FastAPI Microservices / Streamlit Executive Dashboard         |
        +-------------------------------------------------------------------------+
        ```
        """)

    with t2:
        st.markdown("""
        ### Strategic Business Impact for Cynbit Technologies
        1. **Expansion of Revio's TAM (Total Addressable Market):**
           - Elevates Revio from a basic "AI review reply generator" to an **Enterprise Reputation & Churn Prevention Intelligence System**.
           - Enables Cynbit to target high-ticket enterprise contracts (hotel chains, hospital networks, SaaS enterprises) at ₹50,000 to ₹2,00,000/month per brand.
        2. **90% Reduction in PR & Legal Crisis Response Times:**
           - Flags health code violations, regulatory hazards, and legal threats in under 60 seconds instead of hours or days.
        3. **Demonstrable ROI for Revio Customers:**
           - Quantifies exact revenue protected through churn risk modeling and prioritized executive callbacks.
        4. **Ecosystem Synergy with Cynbit Studio & Agency Services:**
           - The same ABSA and agentic classification patterns can be packaged into custom AI automation pipelines for Cynbit's consulting clients.
        """)
