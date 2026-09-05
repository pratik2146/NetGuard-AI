import os
import sys
import streamlit as st

# Add src directory to Python Path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "src")))

from netguard.config import MODEL_PATH, FEATURE_PATH, COMBINED_DATA_PATH
from netguard.models.predictor import NetGuardPredictor
from netguard.db.mongo import MongoPredictionLogger
from netguard.ui.styles import inject_custom_css
from netguard.ui.views import (
    render_dashboard_view,
    render_prediction_view,
    render_device_explorer_view,
    render_about_view,
)

# Page Configuration
st.set_page_config(
    page_title="NetGuard AI",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inject Clean Custom CSS
inject_custom_css()

# Ensure model artifacts exist
missing_files = [path for path in [MODEL_PATH, FEATURE_PATH, COMBINED_DATA_PATH] if not path.exists()]
if missing_files:
    st.error("Required model artifacts or combined datasets are missing:")
    for path in missing_files:
        st.write(f"• `{path.name}`")
    st.info("Please run `python train_model.py` to generate trained model artifacts.")
    st.stop()

# Cache Resources
@st.cache_resource
def get_predictor() -> NetGuardPredictor:
    return NetGuardPredictor()

@st.cache_data
def get_dashboard_data():
    import pandas as pd
    df = pd.read_csv(COMBINED_DATA_PATH, low_memory=False)
    if "timestamp_dt" in df.columns:
        df["timestamp_dt"] = pd.to_datetime(df["timestamp_dt"], errors="coerce")
    return df

predictor = get_predictor()
df = get_dashboard_data()
mongo_logger = MongoPredictionLogger()

device_col = next((c for c in ["Device_name", "router_name", "device_name"] if c in df.columns), None)

# Simplified Sidebar Navigation (4 Clean Pages)
with st.sidebar:
    st.markdown("# 🛡️ NetGuard AI\n**Intelligent Network Monitoring**")
    st.markdown("---")
    navigation = [
        "🏠 Dashboard & Analytics",
        "🔮 Fault Prediction",
        "🖥️ Device Explorer",
        "🧠 Model Performance & Info"
    ]
    page = st.radio("NAVIGATION", navigation)
    st.markdown("---")
    st.markdown(
        f"**Model**: Random Forest\n\n"
        f"**Features**: {len(predictor.features)}\n\n"
        f"**Threshold**: {predictor.threshold:.2f}"
    )
    st.markdown("---")
    st.caption("NetGuard AI Mini-Project v1.0")

# Dispatch Views
if page == "🏠 Dashboard & Analytics":
    render_dashboard_view(df, device_col)
elif page == "🔮 Fault Prediction":
    render_prediction_view(predictor, mongo_logger)
elif page == "🖥️ Device Explorer":
    render_device_explorer_view(df, device_col, predictor)
elif page == "🧠 Model Performance & Info":
    render_about_view(len(predictor.features), predictor.threshold)

# Simple Footer
st.markdown(
    """
    <div class="simple-footer">
        🛡️ NetGuard AI — Intelligent Network Fault Prediction System
    </div>
    """,
    unsafe_allow_html=True
)