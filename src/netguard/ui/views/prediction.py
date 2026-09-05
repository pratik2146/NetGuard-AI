import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px

from netguard.config import COMBINED_DATA_PATH
from netguard.models.predictor import NetGuardPredictor
from netguard.db.mongo import MongoPredictionLogger
from netguard.ui.styles import render_header, render_simple_card
from netguard.ui.theme import apply_chart_theme

@st.cache_data
def load_sample_dataset():
    if COMBINED_DATA_PATH.exists():
        return pd.read_csv(COMBINED_DATA_PATH, low_memory=False)
    return None

def render_prediction_view(predictor: NetGuardPredictor, mongo_logger: MongoPredictionLogger) -> None:
    """
    Render Fault Prediction View supporting Benchmark Presets and Custom Inputs.
    """
    render_header(
        "🔮 Network Fault Prediction",
        "Predict fault probability using 1-click LCORE-D benchmark records or custom parameter inputs."
    )

    tab1, tab2 = st.tabs(["⚡ Single Record Prediction", "📤 CSV Batch Prediction"])

    df_samples = load_sample_dataset()

    # TAB 1: Single Record Prediction
    with tab1:
        st.markdown('<div class="section-header">Select Preset Scenario or Manual Entry</div>', unsafe_allow_html=True)
        
        mode = st.radio(
            "Prediction Input Mode",
            ["🔴 Load LCORE-D Benchmark Fault Record", "🟢 Load LCORE-D Benchmark Healthy Record", "⚙️ Custom Telemetry Form"],
            horizontal=True
        )

        full_record_to_predict = {}

        if mode == "🔴 Load LCORE-D Benchmark Fault Record":
            st.info("Loaded real benchmark fault telemetry event (`class == 'F'`).")
            if df_samples is not None and "class" in df_samples.columns:
                fault_rows = df_samples[df_samples["class"] == "F"]
                if not fault_rows.empty:
                    sample_idx = st.selectbox("Select Fault Event Row", fault_rows.index[:10], format_func=lambda x: f"Fault Sample Record #{x}")
                    full_record_to_predict = fault_rows.loc[sample_idx].to_dict()

        elif mode == "🟢 Load LCORE-D Benchmark Healthy Record":
            st.info("Loaded real benchmark normal operating telemetry (`class == 'H'`).")
            if df_samples is not None and "class" in df_samples.columns:
                healthy_rows = df_samples[df_samples["class"] == "H"]
                if not healthy_rows.empty:
                    sample_idx = st.selectbox("Select Healthy Event Row", healthy_rows.index[:10], format_func=lambda x: f"Healthy Sample Record #{x}")
                    full_record_to_predict = healthy_rows.loc[sample_idx].to_dict()

        else:
            # Custom Form Mode
            st.markdown('<div class="section-header">Telemetry Parameter Form</div>', unsafe_allow_html=True)
            with st.form("custom_predict_form"):
                c1, c2 = st.columns(2)
                with c1:
                    icmp_loss = st.number_input("ICMP Loss % (0.0 to 100.0)", value=100.0, min_value=0.0, max_value=100.0, step=5.0)
                    icmp_time = st.number_input("ICMP Response Time (ms)", value=0.0, min_value=0.0, step=10.0)
                    icmp_ping = st.selectbox("ICMP Ping Status (1 = Pass, 0 = Fail)", [0.0, 1.0], index=0)
                    device_name = st.text_input("Device Name", value="Router_01")

                with c2:
                    uptime = st.number_input("Uptime in Seconds (Lower < 1000s indicates reboot/fault)", value=500.0, min_value=0.0, step=60.0)
                    p1_bits = st.number_input("Interface P1 Traffic Sent (Bits/sec)", value=1400000.0, min_value=0.0, step=10000.0)
                    snmp_avail = st.number_input("SNMP Agent Availability (0.0 to 1.0)", value=0.0, min_value=0.0, max_value=1.0, step=0.1)
                    path_up = st.selectbox("Path Up Status (1 = Up, 0 = Down)", [0.0, 1.0], index=0)

                submit_custom = st.form_submit_button("🚀 PREDICT FAULT RISK", use_container_width=True)

            if submit_custom:
                full_record_to_predict = {feat: np.nan for feat in predictor.features}
                full_record_to_predict["ICMP loss"] = icmp_loss
                full_record_to_predict["ICMP response time"] = icmp_time
                full_record_to_predict["ICMP ping"] = icmp_ping
                full_record_to_predict["Uptime (network)"] = uptime
                full_record_to_predict["Uptime2(network)"] = uptime
                full_record_to_predict["P1_Bits _sent"] = p1_bits
                full_record_to_predict["SNMP agent availability"] = snmp_avail
                full_record_to_predict["path_up"] = path_up
                full_record_to_predict["_device_name"] = device_name.strip()

        # Run Prediction if record is prepared
        if full_record_to_predict:
            dev_name = full_record_to_predict.get("_device_name", full_record_to_predict.get("Device_name", "Router_01"))
            res = predictor.predict_single(full_record_to_predict)
            
            st.session_state["last_single_prediction"] = {
                "result": res,
                "device_name": dev_name
            }

        # Render Results
        if "last_single_prediction" in st.session_state:
            pred_data = st.session_state["last_single_prediction"]
            res = pred_data["result"]
            dev_name = pred_data["device_name"]

            prob = res["fault_probability"]
            risk = res["risk_level"]
            emoji = res["emoji"]
            advice = res["advice"]

            st.markdown('<div class="section-header">Prediction Result</div>', unsafe_allow_html=True)

            k1, k2, k3 = st.columns(3)
            with k1:
                render_simple_card("FAULT PROBABILITY", f"{prob * 100:.1f}%")
            with k2:
                render_simple_card("RISK LEVEL", f"{emoji} {risk}")
            with k3:
                render_simple_card("DECISION THRESHOLD", f"{res['risk_threshold'] * 100:.1f}%", "Random Forest")

            if risk == "CRITICAL":
                st.error(f"🔴 **CRITICAL RISK** ({prob * 100:.1f}%) — {advice}")
            elif risk == "HIGH":
                st.warning(f"🟠 **HIGH RISK** ({prob * 100:.1f}%) — {advice}")
            elif risk == "MEDIUM":
                st.info(f"🟡 **MEDIUM RISK** ({prob * 100:.1f}%) — {advice}")
            else:
                st.success(f"🟢 **LOW RISK** ({prob * 100:.1f}%) — {advice}")

            if st.button("💾 Save Prediction Log to MongoDB"):
                success, msg = mongo_logger.log_prediction({
                    "device": str(dev_name),
                    "probability": prob,
                    "risk": risk,
                    "threshold": res["risk_threshold"],
                    "source": "manual"
                })
                if success:
                    st.success(msg)
                else:
                    st.info(msg)

    # TAB 2: CSV Batch Prediction
    with tab2:
        st.markdown('<div class="section-header">Upload CSV File</div>', unsafe_allow_html=True)
        uploaded_file = st.file_uploader("Choose a CSV file containing network telemetry", type=["csv"])

        if uploaded_file:
            try:
                batch_df = pd.read_csv(uploaded_file, low_memory=False)
                st.success(f"Loaded CSV with {len(batch_df):,} records.")
                st.dataframe(batch_df.head(10), use_container_width=True, hide_index=True)

                if st.button("⚡ Run Batch Prediction", use_container_width=True):
                    with st.spinner("Calculating fault probabilities..."):
                        probs, risk_infos = predictor.predict_dataframe(batch_df)

                    results = batch_df.copy()
                    results["fault_probability_%"] = (probs * 100).round(2)
                    results["risk_level"] = [info["risk_level"] for info in risk_infos]
                    results["is_fault_predicted"] = (probs >= predictor.threshold).astype(int)

                    st.session_state["simple_batch_results"] = results
                    st.success("Batch prediction completed.")

                if "simple_batch_results" in st.session_state:
                    res_df = st.session_state["simple_batch_results"]
                    st.markdown('<div class="section-header">Risk Breakdown</div>', unsafe_allow_html=True)

                    counts = res_df["risk_level"].value_counts().reindex(["CRITICAL", "HIGH", "MEDIUM", "LOW"], fill_value=0)
                    chart_df = counts.reset_index()
                    chart_df.columns = ["risk_level", "records"]

                    fig_bar = px.bar(
                        chart_df,
                        x="risk_level",
                        y="records",
                        text="records",
                        title="Predicted Risk Distribution",
                        color="risk_level",
                        color_discrete_map={"CRITICAL": "#EF4444", "HIGH": "#F97316", "MEDIUM": "#F59E0B", "LOW": "#10B981"}
                    )
                    apply_chart_theme(fig_bar)
                    st.plotly_chart(fig_bar, use_container_width=True)

                    st.dataframe(res_df.head(50), use_container_width=True, hide_index=True)
                    csv_bytes = res_df.to_csv(index=False).encode("utf-8")
                    st.download_button("📥 Download Predictions (CSV)", data=csv_bytes, file_name="netguard_predictions.csv", mime="text/csv")

            except Exception as exc:
                st.error("Failed to process CSV file.")
                st.exception(exc)
