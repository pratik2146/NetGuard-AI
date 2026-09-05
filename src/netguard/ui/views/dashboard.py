import pandas as pd
import streamlit as st
import plotly.express as px

from netguard.data.loader import load_fault_log
from netguard.ui.styles import render_header, render_simple_card
from netguard.ui.theme import apply_chart_theme

def render_dashboard_view(df: pd.DataFrame, device_col: str) -> None:
    """
    Render Simplified Dashboard & Analytics View.
    """
    render_header(
        "🛡️ NetGuard AI Dashboard",
        "Network monitoring metrics, fault rates, and telemetry distribution analytics."
    )

    # Key Metrics
    total = len(df)
    faults = int((df["class"] == "F").sum()) if "class" in df.columns else 0
    healthy = int((df["class"] == "H").sum()) if "class" in df.columns else 0
    fault_rate = (faults / total * 100) if total > 0 else 0.0

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        render_simple_card("TOTAL RECORDS", f"{total:,}", "LCORE-D dataset")
    with c2:
        render_simple_card("FAULT RECORDS", f"{faults:,}", f"{fault_rate:.2f}% fault rate")
    with c3:
        render_simple_card("HEALTHY RECORDS", f"{healthy:,}", "Normal operation")
    with c4:
        render_simple_card("DEVICES MONITORED", f"{df[device_col].nunique() if device_col else 'N/A'}", "Active devices")

    st.markdown('<div class="section-header">Network Health & Activity</div>', unsafe_allow_html=True)
    col_left, col_right = st.columns(2)

    with col_left:
        counts = df["class"].fillna("Other").value_counts().reset_index()
        counts.columns = ["State", "Records"]
        fig_pie = px.pie(
            counts,
            names="State",
            values="Records",
            hole=0.5,
            title="Network State Distribution (H = Healthy, F = Fault, T = Transient)",
            color="State",
            color_discrete_map={"H": "#10B981", "F": "#EF4444", "T": "#F59E0B"}
        )
        apply_chart_theme(fig_pie)
        st.plotly_chart(fig_pie, use_container_width=True)

    with col_right:
        if "timestamp_dt" in df.columns:
            timeline = df.dropna(subset=["timestamp_dt"]).sort_values("timestamp_dt").copy()
            if len(timeline):
                timeline["fault"] = (timeline["class"] == "F").astype(int)
                resampled = timeline.set_index("timestamp_dt")["fault"].resample("6h").mean().reset_index()
                resampled["Fault Rate %"] = resampled["fault"] * 100

                fig_line = px.line(
                    resampled,
                    x="timestamp_dt",
                    y="Fault Rate %",
                    title="Observed Network Fault Rate Over Time",
                    color_discrete_sequence=["#EF4444"]
                )
                apply_chart_theme(fig_line)
                st.plotly_chart(fig_line, use_container_width=True)

    # Clean Telemetry Metric Distribution
    st.markdown('<div class="section-header">Telemetry Metrics Overview</div>', unsafe_allow_html=True)
    d1, d2 = st.columns(2)

    with d1:
        if "ICMP loss" in df.columns:
            clean_loss_df = df[df["ICMP loss"] >= 0].copy()
            fig_icmp = px.histogram(
                clean_loss_df,
                x="ICMP loss",
                color="class",
                nbins=30,
                title="ICMP Packet Loss Ratio Distribution",
                color_discrete_map={"H": "#10B981", "F": "#EF4444", "T": "#F59E0B"}
            )
            apply_chart_theme(fig_icmp)
            st.plotly_chart(fig_icmp, use_container_width=True)

    with d2:
        if "ICMP response time" in df.columns:
            clean_resp_df = df[df["ICMP response time"] >= 0].copy()
            fig_resp = px.box(
                clean_resp_df,
                x="class",
                y="ICMP response time",
                title="ICMP Response Time (ms) by Class State",
                color="class",
                color_discrete_map={"H": "#10B981", "F": "#EF4444", "T": "#F59E0B"}
            )
            apply_chart_theme(fig_resp)
            st.plotly_chart(fig_resp, use_container_width=True)

    # Historical Fault Log Table
    fault_log_df = load_fault_log()
    if fault_log_df is not None and not fault_log_df.empty:
        with st.expander("📋 View Benchmark Fault Log Events"):
            st.dataframe(fault_log_df, use_container_width=True, hide_index=True)
