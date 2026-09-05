import os
import pandas as pd
import streamlit as st
import plotly.express as px

from netguard.config import MODEL_COMPARISON_PATH, FEATURE_IMPORTANCE_PATH
from netguard.ui.styles import render_hero, render_metric_card
from netguard.ui.theme import apply_chart_theme

def render_model_performance_view(feature_count: int, threshold: float) -> None:
    """
    Render Machine Learning Performance Evaluation View.
    """
    render_hero(
        "🧠 Model Performance Evaluation",
        "Benchmark models, evaluate metric tradeoffs, and inspect predictive features.",
        "MACHINE LEARNING EVALUATION"
    )

    if os.path.exists(MODEL_COMPARISON_PATH):
        st.markdown('<div class="section-title">Classifier Benchmark Comparison</div>', unsafe_allow_html=True)
        results = pd.read_csv(MODEL_COMPARISON_PATH)
        
        st.dataframe(
            results.style.format({col: "{:.4f}" for col in results.columns if col != "model"}),
            use_container_width=True,
            hide_index=True
        )

        selected_metric = st.selectbox(
            "Select Evaluation Metric to Compare",
            ["f1", "recall", "precision", "roc_auc", "accuracy"]
        )

        fig_comp = px.bar(
            results,
            x="model",
            y=selected_metric,
            range_y=[0, 1.05],
            text_auto=".4f",
            title=f"Benchmark Comparison — {selected_metric.upper()}",
            color="model",
            color_discrete_sequence=["#3B82F6", "#10B981"]
        )
        apply_chart_theme(fig_comp)
        st.plotly_chart(fig_comp, use_container_width=True)

    st.markdown('<div class="section-title">Selected Active Production Model</div>', unsafe_allow_html=True)

    a, b, c = st.columns(3)
    with a:
        render_metric_card("CLASSIFIER ARCHITECTURE", "Random Forest", "300 Trees (sqrt features)")
    with b:
        render_metric_card("FEATURE DIMENSIONS", f"{feature_count:,}", "Extracted network metrics")
    with c:
        render_metric_card("DECISION THRESHOLD", f"{threshold:.2f}", "Optimized via F1 Grid Search")

    if os.path.exists(FEATURE_IMPORTANCE_PATH):
        st.markdown('<div class="section-title">Top Predictive Indicators</div>', unsafe_allow_html=True)
        fi_df = pd.read_csv(FEATURE_IMPORTANCE_PATH).head(20).sort_values("importance")

        fig_fi = px.bar(
            fi_df,
            x="importance",
            y="feature",
            orientation="h",
            title="Random Forest Gini Feature Importance (Top 20)",
            color="importance",
            color_continuous_scale="Blues"
        )
        apply_chart_theme(fig_fi)
        st.plotly_chart(fig_fi, use_container_width=True)

    st.markdown(
        """
        <div class="info-card">
            <b>Evaluation Methodology Note:</b> In network fault prediction under class imbalance, metrics like Recall, 
            Precision, F1-Score, and PR-AUC take precedence over standard accuracy. The optimal threshold is selected 
            to maximize F1-score and prevent unmonitored silent outages.
        </div>
        """,
        unsafe_allow_html=True
    )
