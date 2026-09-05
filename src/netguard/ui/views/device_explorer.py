import pandas as pd
import streamlit as st
import plotly.express as px

from netguard.models.predictor import NetGuardPredictor
from netguard.ui.styles import render_header, render_simple_card
from netguard.ui.theme import apply_chart_theme

def render_device_explorer_view(df: pd.DataFrame, device_col: str, predictor: NetGuardPredictor) -> None:
    """
    Render Simplified Device Explorer View.
    """
    render_header(
        "🖥️ Device Explorer",
        "Select a network router/switch to view its historical telemetry and AI risk trend."
    )

    if not device_col:
        st.warning("No device name column found in dataset.")
        st.stop()

    devices = sorted(df[device_col].dropna().astype(str).unique())
    selected_device = st.selectbox("Select Target Network Device", devices)

    device_df = df[df[device_col].astype(str) == selected_device].copy()

    # Predict risk for selected device
    probs, risk_infos = predictor.predict_dataframe(device_df)
    device_df["fault_risk"] = probs
    device_df["risk_level"] = [info["risk_level"] for info in risk_infos]

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        render_simple_card("TOTAL RECORDS", f"{len(device_df):,}")
    with c2:
        render_simple_card("OBSERVED FAULTS", f"{int((device_df['class'] == 'F').sum()):,}")
    with c3:
        render_simple_card("MAX AI RISK", f"{device_df['fault_risk'].max() * 100:.1f}%")
    with c4:
        render_simple_card("AVERAGE AI RISK", f"{device_df['fault_risk'].mean() * 100:.1f}%")

    st.markdown(f'<div class="section-header">Risk Trajectory — {selected_device}</div>', unsafe_allow_html=True)
    trend = device_df.dropna(subset=["timestamp_dt"]).sort_values("timestamp_dt")

    if not trend.empty:
        fig_line = px.line(
            trend,
            x="timestamp_dt",
            y="fault_risk",
            title=f"AI Risk Score History ({selected_device})",
            color_discrete_sequence=["#6366F1"]
        )
        fig_line.update_yaxes(tickformat=".0%", title="Fault Probability")
        apply_chart_theme(fig_line)
        st.plotly_chart(fig_line, use_container_width=True)

    st.markdown('<div class="section-header">Recent Telemetry Records</div>', unsafe_allow_html=True)
    st.dataframe(device_df[["timestamp_dt", "class", "fault_risk", "risk_level"]].tail(50), use_container_width=True, hide_index=True)
