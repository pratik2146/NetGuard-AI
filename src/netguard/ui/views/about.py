import os
import pandas as pd
import streamlit as st
import plotly.express as px

from netguard.config import MODEL_COMPARISON_PATH, FEATURE_IMPORTANCE_PATH
from netguard.ui.styles import render_header, render_simple_card
from netguard.ui.theme import apply_chart_theme

def render_about_view(feature_count: int, threshold: float) -> None:
    """
    Render Simplified Model Performance & Project Information View.
    """
    render_header(
        "🧠 Model Performance & Project Info",
        "Machine learning benchmark comparison, feature importance analysis, and project viva overview."
    )

    # 1. Model Summary KPIs
    c1, c2, c3 = st.columns(3)
    with c1:
        render_simple_card("PRIMARY MODEL", "Random Forest", "300 Trees")
    with c2:
        render_simple_card("FEATURES ANALYZED", f"{feature_count:,}", "Monitoring indicators")
    with c3:
        render_simple_card("DECISION THRESHOLD", f"{threshold:.2f}", "F1-Score optimized")

    # 2. Benchmark Comparison
    if os.path.exists(MODEL_COMPARISON_PATH):
        st.markdown('<div class="section-header">Model Benchmark Evaluation</div>', unsafe_allow_html=True)
        results_df = pd.read_csv(MODEL_COMPARISON_PATH)
        st.dataframe(results_df.style.format({c: "{:.4f}" for c in results_df.columns if c != "model"}), use_container_width=True, hide_index=True)

        fig_comp = px.bar(
            results_df,
            x="model",
            y="f1",
            text_auto=".4f",
            title="Model F1-Score Comparison (Random Forest vs Logistic Regression)",
            color="model",
            color_discrete_sequence=["#3B82F6", "#10B981"]
        )
        apply_chart_theme(fig_comp)
        st.plotly_chart(fig_comp, use_container_width=True)

    # 3. Feature Importance
    if os.path.exists(FEATURE_IMPORTANCE_PATH):
        st.markdown('<div class="section-header">Top 10 Predictive Telemetry Indicators</div>', unsafe_allow_html=True)
        fi_df = pd.read_csv(FEATURE_IMPORTANCE_PATH).head(10).sort_values("importance")

        fig_fi = px.bar(
            fi_df,
            x="importance",
            y="feature",
            orientation="h",
            title="Random Forest Feature Importance",
            color="importance",
            color_continuous_scale="Blues"
        )
        apply_chart_theme(fig_fi)
        st.plotly_chart(fig_fi, use_container_width=True)

    # 4. Viva Notes & Project Info
    st.markdown('<div class="section-header">Project Summary & Academic Viva Defense Notes</div>', unsafe_allow_html=True)
    viva_notes = [
        "**Problem Statement**: Proactively identify network fault states (`class == 'F'`) using historical telemetry.",
        "**Dataset**: LCORE-D Version 2 (7 monitoring CSV files + Fault Injection Log).",
        "**Target Handling**: Binary target where `class == 'F'` is positive fault state; `H` and `T` are non-fault.",
        "**Model Selected**: Random Forest Classifier with median missing value imputation.",
        "**Threshold Optimization**: Grid search maximizing F1-score to balance Precision and Recall.",
        "**Technology Stack**: Python, Pandas, Scikit-learn, Streamlit, Plotly, PyMongo, Docker."
    ]

    for note in viva_notes:
        st.write(f"✓ {note}")
