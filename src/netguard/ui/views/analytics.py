import pandas as pd
import streamlit as st
import plotly.express as px

from netguard.data.loader import load_fault_log
from netguard.data.preprocessor import prepare_features
from netguard.ui.styles import render_hero
from netguard.ui.theme import apply_chart_theme

def render_analytics_view(df: pd.DataFrame, feature_columns: list) -> None:
    """
    Render Advanced Network Analytics and Fault Log Correlation View.
    """
    render_hero(
        "📊 Network Analytics",
        "Explore telemetry metric distributions, core correlations, and fault event logs.",
        "NETWORK DATA ANALYTICS"
    )

    left, right = st.columns(2)

    with left:
        if "ICMP loss" in df.columns:
            fig_hist = px.histogram(
                df,
                x="ICMP loss",
                color="class",
                nbins=40,
                title="ICMP Packet Loss Distribution",
                color_discrete_map={"H": "#10B981", "F": "#EF4444", "T": "#F59E0B"}
            )
            apply_chart_theme(fig_hist)
            st.plotly_chart(fig_hist, use_container_width=True)

    with right:
        if "ICMP response time" in df.columns:
            fig_box = px.box(
                df,
                x="class",
                y="ICMP response time",
                title="ICMP Latency / Response Time by Class State",
                color="class",
                color_discrete_map={"H": "#10B981", "F": "#EF4444", "T": "#F59E0B"}
            )
            apply_chart_theme(fig_box)
            st.plotly_chart(fig_box, use_container_width=True)

    numeric_data = prepare_features(df, feature_columns)
    corr_features = [
        c for c in ["ICMP loss", "ICMP response time", "SNMP agent availability", "path_up"]
        if c in numeric_data.columns
    ]

    if len(corr_features) >= 2:
        st.markdown('<div class="section-title">Telemetry Correlation Heatmap</div>', unsafe_allow_html=True)
        corr_matrix = numeric_data[corr_features].corr()
        fig_heat = px.imshow(
            corr_matrix,
            text_auto=".2f",
            title="Core Metric Correlation Matrix",
            color_continuous_scale="Viridis"
        )
        apply_chart_theme(fig_heat)
        st.plotly_chart(fig_heat, use_container_width=True)

    # Fault Log Analytics Section
    fault_log_df = load_fault_log()
    if fault_log_df is not None and not fault_log_df.empty:
        st.markdown('<div class="section-title">Historical Network Fault Event Log Analysis</div>', unsafe_allow_html=True)
        
        c1, c2 = st.columns(2)
        with c1:
            if "Fault Type" in fault_log_df.columns:
                type_counts = fault_log_df["Fault Type"].value_counts().reset_index()
                type_counts.columns = ["Fault Type", "Incidents"]
                fig_type = px.bar(
                    type_counts,
                    x="Incidents",
                    y="Fault Type",
                    orientation="h",
                    title="Fault Incident Types",
                    color="Incidents",
                    color_continuous_scale="Reds"
                )
                apply_chart_theme(fig_type)
                st.plotly_chart(fig_type, use_container_width=True)

        with c2:
            domain_col = [c for c in fault_log_df.columns if "Domain" in c]
            if domain_col:
                domain_counts = fault_log_df[domain_col[0]].value_counts().reset_index()
                domain_counts.columns = ["Fault Domain", "Incidents"]
                fig_domain = px.pie(
                    domain_counts,
                    names="Fault Domain",
                    values="Incidents",
                    hole=0.4,
                    title="Fault Breakdown by Infrastructure Domain"
                )
                apply_chart_theme(fig_domain)
                st.plotly_chart(fig_domain, use_container_width=True)

        with st.expander("View Full Fault Log Table"):
            st.dataframe(fault_log_df, use_container_width=True, hide_index=True)
