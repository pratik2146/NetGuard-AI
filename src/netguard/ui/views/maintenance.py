import streamlit as st

from netguard.config import RISK_LEVELS
from netguard.ui.styles import render_hero

def render_maintenance_view() -> None:
    """
    Render Predictive Maintenance Operational Guidance View.
    """
    render_hero(
        "🔧 Predictive Maintenance Protocols",
        "Operational decision matrix translating AI risk probabilities into practical network protocols.",
        "DECISION SUPPORT MATRIX"
    )

    levels = [
        ("🔴 CRITICAL RISK", "Probability ≥ 80%", RISK_LEVELS["CRITICAL"]["advice"]),
        ("🟠 HIGH RISK", "Probability 60% – 79.9%", RISK_LEVELS["HIGH"]["advice"]),
        ("🟡 MEDIUM RISK", "Probability 30% – 59.9%", RISK_LEVELS["MEDIUM"]["advice"]),
        ("🟢 LOW RISK", "Probability < 30%", RISK_LEVELS["LOW"]["advice"]),
    ]

    for title, rng, advice in levels:
        st.markdown(
            f"""
            <div class="info-card">
                <h3 style="margin-top:0; margin-bottom: 8px; color: #F8FAFC;">{title}</h3>
                <div style="font-weight: 700; color: #60A5FA; margin-bottom: 12px;">Trigger Boundary: {rng}</div>
                <div>{advice}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.caption(
        "Operating threshold guidelines are designed to minimize unscheduled network downtime while optimizing "
        "field engineering resources. Calibration should be updated periodically based on cost-of-outage matrices."
    )
