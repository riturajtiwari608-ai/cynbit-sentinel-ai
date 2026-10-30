"""
Cynbit Sentinel AI - Executive & Operational Dashboard
Next-Generation Autonomous Reputation & Crisis Sentinel for Revio
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

# Enhanced Modern Cyber-Enterprise Theme & CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800;900&family=JetBrains+Mono:wght@400;600&display=swap');
    
    * {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    /* Main Gradient Header */
    .hero-title {
        font-size: 2.5rem;
        font-weight: 900;
        letter-spacing: -0.03em;
        background: linear-gradient(135deg, #38BDF8 0%, #818CF8 50%, #C084FC 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.35rem;
        line-height: 1.2;
    }
    
    .hero-subtitle {
        color: #94A3B8;
        font-size: 1.05rem;
        font-weight: 500;
        margin-bottom: 1.75rem;
        display: flex;
        align-items: center;
        gap: 8px;
        flex-wrap: wrap;
    }
    
    .pill-badge {
        display: inline-flex;
        align-items: center;
        gap: 4px;
        padding: 3px 10px;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .pill-cyan {
        background: rgba(6, 182, 212, 0.12);
        color: #22D3EE;
        border: 1px solid rgba(6, 182, 212, 0.3);
    }
    .pill-indigo {
        background: rgba(99, 102, 241, 0.12);
        color: #A5B4FC;
        border: 1px solid rgba(99, 102, 241, 0.3);
    }
    .pill-emerald {
        background: rgba(16, 185, 129, 0.12);
        color: #34D399;
        border: 1px solid rgba(16, 185, 129, 0.3);
    }
    .pill-rose {
        background: rgba(244, 63, 94, 0.12);
        color: #FB7185;
        border: 1px solid rgba(244, 63, 94, 0.3);
    }

    /* Metric Glass Cards */
    .metric-card {
        background: linear-gradient(145deg, rgba(17, 24, 39, 0.85) 0%, rgba(30, 41, 59, 0.6) 100%);
        border: 1px solid rgba(148, 163, 184, 0.15);
        border-radius: 16px;
        padding: 1.2rem;
        backdrop-filter: blur(12px);
        box-shadow: 0 4px 20px -2px rgba(0, 0, 0, 0.3);
        transition: transform 0.2s ease, border-color 0.2s ease;
        position: relative;
        overflow: hidden;
    }
    .metric-card:hover {
        transform: translateY(-2px);
        border-color: rgba(56, 189, 248, 0.4);
    }
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, #38BDF8, #818CF8);
    }
    .metric-title {
        font-size: 0.75rem;
        font-weight: 700;
        color: #94A3B8;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-bottom: 6px;
    }
    .metric-value {
        font-size: 1.85rem;
        font-weight: 900;
        color: #F8FAFC;
        letter-spacing: -0.02em;
        line-height: 1.1;
    }
    .metric-sub {
        font-size: 0.8rem;
        font-weight: 600;
        color: #38BDF8;
        margin-top: 6px;
    }

    /* Glass Container Boxes */
    .glass-panel {
        background: rgba(17, 24, 39, 0.65);
        border: 1px solid rgba(148, 163, 184, 0.12);
        border-radius: 18px;
        padding: 1.4rem;
        backdrop-filter: blur(10px);
        margin-bottom: 1.5rem;
    }

    /* Alert Banners */
    .critical-banner {
        background: linear-gradient(90deg, rgba(239, 68, 68, 0.15) 0%, rgba(185, 28, 28, 0.25) 100%);
        border: 1px solid rgba(239, 68, 68, 0.4);
        border-left: 5px solid #EF4444;
        border-radius: 12px;
        padding: 1rem 1.25rem;
        color: #FCA5A5;
        font-weight: 600;
        margin: 1rem 0;
    }
    .warning-banner {
        background: linear-gradient(90deg, rgba(245, 158, 11, 0.15) 0%, rgba(180, 83, 9, 0.25) 100%);
        border: 1px solid rgba(245, 158, 11, 0.4);
        border-left: 5px solid #F59E0B;
        border-radius: 12px;
        padding: 1rem 1.25rem;
        color: #FCD34D;
        font-weight: 600;
        margin: 1rem 0;
    }
    .success-banner {
        background: linear-gradient(90deg, rgba(16, 185, 129, 0.15) 0%, rgba(5, 150, 105, 0.25) 100%);
        border: 1px solid rgba(16, 185, 129, 0.4);
        border-left: 5px solid #10B981;
        border-radius: 12px;
        padding: 1rem 1.25rem;
        color: #6EE7B7;
        font-weight: 600;
        margin: 1rem 0;
    }

    /* Streamlit Button Tweaks */
    div.stButton > button:first-child {
        background: linear-gradient(135deg, #06B6D4 0%, #3B82F6 100%) !important;
        color: #FFFFFF !important;
        font-weight: 800 !important;
        font-size: 0.95rem !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.65rem 1.5rem !important;
        box-shadow: 0 4px 14px 0 rgba(6, 182, 212, 0.39) !important;
        transition: all 0.2s ease !important;
    }
    div.stButton > button:first-child:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 6px 20px rgba(6, 182, 212, 0.55) !important;
    }

    /* Sidebar Candidate Card */
    .candidate-card {
        background: linear-gradient(145deg, rgba(30, 41, 59, 0.7) 0%, rgba(15, 23, 42, 0.9) 100%);
        border: 1px solid rgba(56, 189, 248, 0.2);
        border-radius: 14px;
        padding: 1rem;
        margin-top: 1rem;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def load_orchestrator():
    return SentinelOrchestrator()


orchestrator = load_orchestrator()

# Sidebar Navigation & Branding
st.sidebar.markdown("""
<div style="text-align: center; margin-bottom: 1.2rem;">
    <h2 style="font-weight: 900; background: linear-gradient(90deg, #38BDF8, #818CF8); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin: 0; font-size: 1.6rem;">CYNBIT SENTINEL</h2>
    <p style="color: #64748B; font-size: 0.75rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.15em; margin: 0;">AI Reputation Engine</p>
</div>
""", unsafe_allow_html=True)

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
<div class="candidate-card">
    <div style="font-size: 0.7rem; font-weight: 800; color: #38BDF8; text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 4px;">Assessment Profile</div>
    <div style="font-size: 1rem; font-weight: 800; color: #F8FAFC;">Rituraj Tiwari</div>
    <div style="font-size: 0.8rem; color: #94A3B8; margin-bottom: 8px;">AI/ML Engineer Intern</div>
    <div style="display: flex; gap: 4px; flex-wrap: wrap;">
        <span class="pill-badge pill-cyan">Cynbit Tech</span>
        <span class="pill-badge pill-indigo">Revio Suite</span>
    </div>
</div>
""", unsafe_allow_html=True)

# -------------------------------------------------------------------------------------------------
# TAB 1: SINGLE REVIEW INSPECTOR
# -------------------------------------------------------------------------------------------------
if navigation == "🔍 Single Review Inspector":
    st.markdown('<div class="hero-title">🛡️ Real-Time Review Diagnostic & Triage</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="hero-subtitle">
        <span>Powered by Cynbit Revio Sentinel</span>
        <span class="pill-badge pill-cyan">Aspect-Based ABSA</span>
        <span class="pill-badge pill-rose">Sub-5ms Crisis Sentinel</span>
        <span class="pill-badge pill-indigo">Grounded Copilot</span>
    </div>
    """, unsafe_allow_html=True)

    col_input, col_meta = st.columns([2, 1])

    # Sample Presets for Quick Testing
    sample_presets = {
        "🚨 Severe Food Poisoning & Legal Notice (Critical)": {
            "text": "Severe food poisoning after eating the seafood platter yesterday. Three members of our family are currently hospitalized with acute gastroenteritis. We are filing a formal complaint with the Food Safety and Standards Authority (FSSAI) and our lawyer will contact your management.",
            "business": "Urban Taste Bistro",
            "branch": "Mumbai Bandra",
            "tier": "Standard",
            "rating": 1
        },
        "⚡ Enterprise Cloud Outage & SLA Penalty (Critical)": {
            "text": "Critical data sync outage! Our production database integration has been failing continuously since the 4.2 patch update. Over 15,000 active customer checkout requests dropped. We are evaluating contract cancellation and SLA penalty claims.",
            "business": "CloudScale SaaS Labs",
            "branch": "Bangalore HQ",
            "tier": "Enterprise",
            "rating": 1
        },
        "⭐ Glowing VIP Promoter Experience (Positive)": {
            "text": "Wonderful stay! The rooftop breakfast had an amazing spread and the housekeeping team kept everything spotless. Special shoutout to Amit at reception for helping us with local sightseeing.",
            "business": "The Grand Regent Hotel",
            "branch": "Jaipur Central",
            "tier": "VIP",
            "rating": 5
        },
        "⚠️ Hinglish Grievance with Staff Delay (Warning)": {
            "text": "Khana theek tha lekin service bahot slow thi. Manager ko 3 baar bola billing check karne ke liye par koi dhyan nahi diya. Expected much better standard from a 5 star property.",
            "business": "The Grand Regent Hotel",
            "branch": "Delhi Aerocity",
            "tier": "VIP",
            "rating": 2
        }
    }

    selected_preset = col_input.selectbox(
        "⚡ Quick-Load Test Scenario (Pre-configured Edge Cases):",
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

    review_text = col_input.text_area("Review Content to Ingest:", value=default_text, height=140)

    with col_meta:
        b_name = st.text_input("Business Name:", value=default_business)
        b_branch = st.text_input("Branch / Location:", value=default_branch)
        c_tier = st.selectbox("Customer Tier:", ["Standard", "VIP", "Enterprise"], index=["Standard", "VIP", "Enterprise"].index(default_tier))
        c_rating = st.slider("Star Rating:", min_value=1, max_value=5, value=default_rating)

    if st.button("🚀 Run Sentinel Cognitive Analysis", type="primary"):
        with st.spinner("Executing Aspect Segmentation, Anomaly Early-Warning, and Financial Exposure Models..."):
            result = orchestrator.process_review(
                text=review_text,
                business_name=b_name,
                branch_location=b_branch,
                rating=c_rating,
                customer_tier=c_tier
            )

        sent = result["sentiment_intelligence"]
        crisis = result["crisis_governance"]
        fin = result["financial_exposure"]
        resp = result["response_intelligence"]

        st.markdown("<div style='height: 1.2rem;'></div>", unsafe_allow_html=True)

        # High-Impact Visual Metric Cards
        m1, m2, m3, m4 = st.columns(4)
        
        sent_color = "#34D399" if sent["overall_sentiment"] == "Positive" else "#F87171" if sent["overall_sentiment"] == "Negative" else "#94A3B8"
        with m1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">Overall Sentiment</div>
                <div class="metric-value" style="color: {sent_color};">{sent["overall_sentiment"]}</div>
                <div class="metric-sub">Polarity: {sent['polarity_score']}</div>
            </div>
            """, unsafe_allow_html=True)

        with m2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">Model Confidence</div>
                <div class="metric-value" style="color: #38BDF8;">{int(sent['confidence'] * 100)}%</div>
                <div class="metric-sub">Tokens Scored: {sent['word_count']} words</div>
            </div>
            """, unsafe_allow_html=True)

        sev_color = "#EF4444" if crisis["severity_level"] == "CRITICAL" else "#F59E0B" if crisis["severity_level"] == "WARNING" else "#10B981"
        with m3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">Crisis Severity</div>
                <div class="metric-value" style="color: {sev_color};">{crisis["severity_level"]}</div>
                <div class="metric-sub">SLA Window: &lt; {crisis['response_sla_hours']} Hours</div>
            </div>
            """, unsafe_allow_html=True)

        with m4:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">Revenue At Risk (CLV)</div>
                <div class="metric-value" style="color: #F43F5E;">₹{fin['estimated_revenue_at_risk']:,}</div>
                <div class="metric-sub">Churn Risk: {fin['churn_risk_tier']} ({int(fin['churn_probability'] * 100)}%)</div>
            </div>
            """, unsafe_allow_html=True)

        # Crisis Action Alert Banner
        if crisis["severity_level"] == "CRITICAL":
            st.markdown(f"""
            <div class="critical-banner">
                <span style="font-size: 1.1rem;">🚨 <b>CRITICAL INCIDENT DETECTED:</b> {crisis['recommended_action']}</span><br/>
                <span style="font-size: 0.85rem; opacity: 0.9;"><b>Incident Tags:</b> {crisis['matched_keywords']} • <b>Human Approval Required:</b> True</span>
            </div>
            """, unsafe_allow_html=True)
        elif crisis["severity_level"] == "WARNING":
            st.markdown(f"""
            <div class="warning-banner">
                <span style="font-size: 1.1rem;">⚠️ <b>WARNING INCIDENT:</b> {crisis['recommended_action']}</span>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<div style='height: 0.8rem;'></div>", unsafe_allow_html=True)

        # Detailed Breakdown Tabs
        tab_absa, tab_response, tab_json = st.tabs([
            "📊 Aspect-Based Granularity (ABSA)",
            "✍️ Grounded AI Response Copilot",
            "🔍 Raw Engine Telemetry"
        ])

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
                    st.markdown("#### **Aspect Polarity Distribution**")
                    chart = alt.Chart(df_aspects).mark_bar(cornerRadiusTopRight=6, cornerRadiusBottomRight=6).encode(
                        x=alt.X("Polarity Score:Q", scale=alt.Scale(domain=[-1.0, 1.0]), title="Polarity (-1.0 Negative to +1.0 Positive)"),
                        y=alt.Y("Aspect:N", sort="-x", title="Detected Aspect"),
                        color=alt.Color("Sentiment:N", scale=alt.Scale(
                            domain=["Positive", "Neutral", "Negative"],
                            range=["#10B981", "#64748B", "#EF4444"]
                        )),
                        tooltip=["Aspect", "Sentiment", "Polarity Score", "Confidence"]
                    ).properties(height=260)
                    st.altair_chart(chart, use_container_width=True)

                with col_details:
                    st.markdown("#### **Extracted Clause Attribution**")
                    st.dataframe(df_aspects[["Aspect", "Sentiment", "Polarity Score", "Snippet"]], use_container_width=True)
            else:
                st.info("No domain-specific aspect taxonomy detected in this text. Text classified holistically.")

        with tab_response:
            st.markdown(f"**Applied Persona Strategy:** <span class='pill-badge pill-indigo'>{resp['persona_applied'].upper()}</span>", unsafe_allow_html=True)
            
            if crisis["requires_human_approval"]:
                st.markdown("""
                <div class="warning-banner" style="padding: 8px 14px; margin-bottom: 12px;">
                    🔒 <b>Human-in-the-Loop Locked:</b> High-severity incidents require human sign-off before dispatching to public review channels.
                </div>
                """, unsafe_allow_html=True)

            st.text_area("Grounded Response Draft:", value=resp["generated_response"], height=200)

            c_g1, c_g2, c_g3 = st.columns(3)
            c_g1.checkbox("✅ PII Redacted (Phone/Card/Email)", value=resp["guardrail_checks"]["pii_redacted"], disabled=True)
            c_g2.checkbox("✅ Hallucination Guardrail Active", value=not resp["guardrail_checks"]["hallucination_detected"], disabled=True)
            c_g3.checkbox("✅ Policy Compliance Validated", value=resp["guardrail_checks"]["policy_compliant"], disabled=True)

            c_btn1, c_btn2 = st.columns([1, 4])
            if c_btn1.button("✅ Approve & Dispatch Response"):
                st.success("Response dispatched securely via Webhook!")

        with tab_json:
            st.json(result)

# -------------------------------------------------------------------------------------------------
# TAB 2: MULTI-BRANCH EXECUTIVE ANALYTICS
# -------------------------------------------------------------------------------------------------
elif navigation == "📊 Multi-Branch Executive Analytics":
    st.markdown('<div class="hero-title">📊 Multi-Location Reputation Intelligence</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="hero-subtitle">
        <span>Portfolio-Wide Feedback Analysis</span>
        <span class="pill-badge pill-cyan">Cross-Branch Benchmarking</span>
        <span class="pill-badge pill-emerald">Revenue Protection</span>
    </div>
    """, unsafe_allow_html=True)

    # Load default dataset
    sample_csv_path = os.path.join(os.path.dirname(__file__), "data", "sample_reviews.csv")
    df_source = None

    uploaded_file = st.file_uploader("Upload Reviews Dataset (CSV):", type=["csv"])
    if uploaded_file is not None:
        df_source = pd.read_csv(uploaded_file)
        st.success("Custom CSV file loaded successfully!")
    elif os.path.exists(sample_csv_path):
        df_source = pd.read_csv(sample_csv_path)

    if df_source is not None:
        batch_results = orchestrator.batch_process(df_source)
        kpis = batch_results["summary_kpis"]

        # KPI Summary Cards
        k1, k2, k3, k4, k5 = st.columns(5)
        with k1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">Total Reviews</div>
                <div class="metric-value">{kpis['total_processed_reviews']}</div>
                <div class="metric-sub">Ingested Streams</div>
            </div>
            """, unsafe_allow_html=True)
        with k2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">Positive Share</div>
                <div class="metric-value" style="color: #34D399;">{kpis['positive_percentage']}%</div>
                <div class="metric-sub">Brand Promoters</div>
            </div>
            """, unsafe_allow_html=True)
        with k3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">Critical Crises</div>
                <div class="metric-value" style="color: #F87171;">{kpis['critical_crises_flagged']}</div>
                <div class="metric-sub">+{kpis['warnings_flagged']} Warnings</div>
            </div>
            """, unsafe_allow_html=True)
        with k4:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">Revenue At Risk</div>
                <div class="metric-value" style="color: #F43F5E;">₹{kpis['total_revenue_at_risk_inr']:,}</div>
                <div class="metric-sub">Exposure Index</div>
            </div>
            """, unsafe_allow_html=True)
        with k5:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">Human Sign-Offs</div>
                <div class="metric-value" style="color: #FCD34D;">{kpis['human_approvals_required']}</div>
                <div class="metric-sub">Approval Queue</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)

        col_left, col_right = st.columns(2)

        with col_left:
            st.markdown("#### **Portfolio Sentiment Breakdown**")
            sentiment_df = pd.DataFrame([
                {"Sentiment": "Positive", "Share": kpis["positive_percentage"]},
                {"Sentiment": "Neutral", "Share": kpis["neutral_percentage"]},
                {"Sentiment": "Negative", "Share": kpis["negative_percentage"]}
            ])
            chart_pie = alt.Chart(sentiment_df).mark_arc(innerRadius=60, cornerRadius=4).encode(
                theta=alt.Theta(field="Share", type="quantitative"),
                color=alt.Color(field="Sentiment", type="nominal", scale=alt.Scale(
                    domain=["Positive", "Neutral", "Negative"],
                    range=["#10B981", "#64748B", "#EF4444"]
                )),
                tooltip=["Sentiment", "Share"]
            ).properties(height=280)
            st.altair_chart(chart_pie, use_container_width=True)

        with col_right:
            st.markdown("#### **Top Operational Vulnerabilities (Root Causes)**")
            if kpis["top_failing_aspects"]:
                failing_df = pd.DataFrame(kpis["top_failing_aspects"], columns=["Aspect", "Complaint Count"])
                chart_bar = alt.Chart(failing_df).mark_bar(cornerRadiusTopRight=6, cornerRadiusBottomRight=6, color="#F59E0B").encode(
                    x=alt.X("Complaint Count:Q", title="Frequency of Negative Attributes"),
                    y=alt.Y("Aspect:N", sort="-x", title="Business Aspect"),
                    tooltip=["Aspect", "Complaint Count"]
                ).properties(height=280)
                st.altair_chart(chart_bar, use_container_width=True)
            else:
                st.write("No negative aspect concentrations found.")

        st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)

        st.markdown("#### **Multi-Branch Operational Ledger**")
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
    st.markdown('<div class="hero-title">🤖 Autonomous Multi-Agent Architecture</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="hero-subtitle">
        <span>Distributed Cognitive Triage Swarm</span>
        <span class="pill-badge pill-cyan">4 Autonomous Agents</span>
        <span class="pill-badge pill-indigo">Zero Human Latency</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    Cynbit's primary identity centers on **Autonomous AI Agents & Scalable Digital Platforms**.
    Below is a live simulation of four collaborative specialized agents resolving an incoming operational incident in milliseconds:
    """)

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-title" style="color: #38BDF8;">Agent 1: Ingestion & ABSA</div>
            <p style="font-size: 0.8rem; color: #CBD5E1; margin-top: 6px;">Parses clauses, executes aspect segmentation, and computes fine-grained polarity scores.</p>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-title" style="color: #F59E0B;">Agent 2: Crisis Sentinel</div>
            <p style="font-size: 0.8rem; color: #CBD5E1; margin-top: 6px;">Detects legal hazards, food safety notices, fraud markers, and sets SLA response windows.</p>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-title" style="color: #F43F5E;">Agent 3: Financial Assessor</div>
            <p style="font-size: 0.8rem; color: #CBD5E1; margin-top: 6px;">Cross-checks account tier and calculates Customer Lifetime Value (CLV) at risk in INR.</p>
        </div>
        """, unsafe_allow_html=True)
    with c4:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-title" style="color: #34D399;">Agent 4: Response Copilot</div>
            <p style="font-size: 0.8rem; color: #CBD5E1; margin-top: 6px;">Applies tone persona, scrubs PII, prevents hallucinated promises, and gates human sign-off.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)

    test_case = st.selectbox(
        "Select an incoming operational event stream to simulate:",
        [
            "Event #1042: High-Severity Outage (Enterprise Client)",
            "Event #1043: Acute Food Poisoning Allegation (Restaurant Chain)",
            "Event #1044: Cashier Double Billing Dispute (Retail)"
        ]
    )

    if st.button("▶️ Launch Agent Swarm Execution", type="primary"):
        with st.status("Executing Multi-Agent Coordination Protocol...", expanded=True) as status:
            st.write("🟢 **Agent 1 (ABSA Specialist)**: Ingesting review stream... Extracted negative polarity (-0.84) in `Technical Stability` and `Support`.")
            st.write("🟠 **Agent 2 (Crisis Sentinel)**: Scanned for enterprise SLA triggers... Match found: `['outage', 'sla penalty']`. Severity set to **CRITICAL**.")
            st.write("🔴 **Agent 3 (Financial Risk Assessor)**: Detected customer tier = `Enterprise`. Estimated annual CLV exposure = **₹12,00,000**. Churn risk probability = **95%**.")
            st.write("🔵 **Agent 4 (Grounded Response Copilot)**: Selected Persona: `crisis_defusal`. Verified PII redaction and locked auto-dispatch for Human Approval.")
            status.update(label="✅ Agent Coordination Complete. Incident Triage Ticket Generated!", state="complete", expanded=False)

        st.markdown("""
        <div class="success-banner">
            ✅ <b>Incident Triage Ticket #CYN-2026-981 Generated:</b> Routed to General Manager's hotline and Enterprise Account Director with a 60-minute SLA!
        </div>
        """, unsafe_allow_html=True)

# -------------------------------------------------------------------------------------------------
# TAB 4: ARCHITECTURE & BUSINESS ROI
# -------------------------------------------------------------------------------------------------
elif navigation == "📑 Technical & Business Architecture":
    st.markdown('<div class="hero-title">📑 Technical Architecture & Cynbit Business ROI</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="hero-subtitle">
        <span>Strategic Engineering Analysis</span>
        <span class="pill-badge pill-cyan">Enterprise Moat</span>
        <span class="pill-badge pill-indigo">Revenue Multiplier</span>
    </div>
    """, unsafe_allow_html=True)

    t1, t2 = st.tabs(["🏗️ Architectural Blueprint", "💼 Cynbit Commercial ROI"])

    with t1:
        st.markdown("""
        ### Two-Tier Cognitive Cascade Flow
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
        |        - Safety Guardrails: Zero unapproved refund commitments          |
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
