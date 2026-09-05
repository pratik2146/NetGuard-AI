import pandas as pd
import streamlit as st
import plotly.express as px

from netguard.models.predictor import NetGuardPredictor
from netguard.ui.styles import render_hero, render_metric_card
from netguard.ui.theme import apply_chart_theme

def render_batch_view(predictor: NetGuardPredictor) -> None:
    """
    Render CSV Batch Prediction View.
    """
    render_hero(
        "📤 CSV Batch Prediction",
        "Upload new network monitoring datasets for automated bulk risk estimation.",
        "BATCH AI INFERENCE"
    )

    st.markdown(
        """
        <div class="info-card">
            Upload any CSV file containing network monitoring metrics. Missing features are automatically handled, 
            and extraneous columns are preserved in the final downloadable report.
        </div>
        """,
        unsafe_allow_html=True
    )

    uploaded_file = st.file_uploader("Upload Network Data CSV", type=["csv"])

    if uploaded_file:
        try:
            new_data = pd.read_csv(uploaded_file, low_memory=False)
            st.success(f"Successfully loaded dataset with {len(new_data):,} records.")

            features = predictor.features
            available = [f for f in features if f in new_data.columns]
            missing = [f for f in features if f not in new_data.columns]

            c1, c2, c3 = st.columns(3)
            with c1:
                render_metric_card("UPLOADED RECORDS", f"{len(new_data):,}")
            with c2:
                render_metric_card("FEATURES MATCHED", f"{len(available)}/{len(features)}")
            with c3:
                render_metric_card("MISSING FEATURES", f"{len(missing)}")

            if missing:
                st.warning(f"{len(missing)} expected model features are missing and will be treated as NaN.")
                with st.expander("View missing feature names"):
                    st.write(missing)

            st.markdown('<div class="section-title">Data Preview</div>', unsafe_allow_html=True)
            st.dataframe(new_data.head(15), use_container_width=True, hide_index=True)

            if st.button("🚀 RUN BATCH INFERENCE", use_container_width=True):
                with st.spinner("Analyzing network records..."):
                    probs, risk_infos = predictor.predict_dataframe(new_data)

                results = new_data.copy()
                results["fault_probability"] = probs
                results["fault_probability_percent"] = (probs * 100).round(2)
                results["risk_level"] = [info["risk_level"] for info in risk_infos]
                results["is_fault_predicted"] = (probs >= predictor.threshold).astype(int)

                st.session_state["batch_results"] = results
                st.success("Batch prediction completed successfully.")

            if "batch_results" in st.session_state:
                results = st.session_state["batch_results"]
                st.markdown('<div class="section-title">Batch Risk Summary</div>', unsafe_allow_html=True)

                risk_counts = results["risk_level"].value_counts().reindex(
                    ["CRITICAL", "HIGH", "MEDIUM", "LOW"], fill_value=0
                )

                a, b, c, d = st.columns(4)
                with a:
                    render_metric_card("🔴 CRITICAL", f"{risk_counts['CRITICAL']:,}")
                with b:
                    render_metric_card("🟠 HIGH", f"{risk_counts['HIGH']:,}")
                with c:
                    render_metric_card("🟡 MEDIUM", f"{risk_counts['MEDIUM']:,}")
                with d:
                    render_metric_card("🟢 LOW", f"{risk_counts['LOW']:,}")

                chart_df = risk_counts.reset_index()
                chart_df.columns = ["Risk Level", "Records"]

                fig_bar = px.bar(
                    chart_df,
                    x="Risk Level",
                    y="Records",
                    text="Records",
                    title="Predicted Risk Distribution",
                    color="Risk Level",
                    color_discrete_map={
                        "CRITICAL": "#EF4444",
                        "HIGH": "#F97316",
                        "MEDIUM": "#F59E0B",
                        "LOW": "#10B981"
                    }
                )
                apply_chart_theme(fig_bar)
                st.plotly_chart(fig_bar, use_container_width=True)

                st.markdown('<div class="section-title">Batch Prediction Results</div>', unsafe_allow_html=True)
                st.dataframe(results, use_container_width=True, hide_index=True)

                csv_bytes = results.to_csv(index=False).encode("utf-8")
                st.download_button(
                    "📥 DOWNLOAD BATCH PREDICTIONS (CSV)",
                    data=csv_bytes,
                    file_name="netguard_batch_predictions.csv",
                    mime="text/csv",
                    use_container_width=True
                )

        except Exception as exc:
            st.error("Failed to process uploaded CSV file.")
            st.exception(exc)
