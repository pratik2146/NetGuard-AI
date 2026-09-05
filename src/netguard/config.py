import os
from pathlib import Path
from typing import Dict, Any

# Project Root Directory
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Data Directories
DATA_DIR = BASE_DIR / "data"
FAULT_LOG_DIR = DATA_DIR / "fault_log"

# Model & Output Directories
MODEL_DIR = BASE_DIR / "models"
OUTPUT_DIR = BASE_DIR / "outputs"

# File Paths
MODEL_PATH = MODEL_DIR / "netguard_model.joblib"
FEATURE_PATH = MODEL_DIR / "feature_columns.json"
THRESHOLD_PATH = MODEL_DIR / "optimal_threshold.json"

COMBINED_DATA_PATH = OUTPUT_DIR / "combined_data.csv"
MODEL_COMPARISON_PATH = OUTPUT_DIR / "model_comparison.csv"
FEATURE_IMPORTANCE_PATH = OUTPUT_DIR / "feature_importance.csv"
TEST_PREDICTIONS_PATH = OUTPUT_DIR / "test_predictions.csv"
TRAINING_SUMMARY_PATH = OUTPUT_DIR / "training_summary.json"
FAULT_LOG_PATH = FAULT_LOG_DIR / "FAULT_LOG.csv"

# MongoDB Default Configuration
MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017/")
MONGODB_DB_NAME = os.getenv("MONGODB_DB_NAME", "netguard_ai")
MONGODB_COLLECTION_NAME = os.getenv("MONGODB_COLLECTION_NAME", "predictions")

# Default Parameters
DEFAULT_THRESHOLD = 0.50
RANDOM_STATE = 42
TEST_SIZE = 0.20

# Operational Risk Levels
RISK_LEVELS: Dict[str, Dict[str, Any]] = {
    "CRITICAL": {
        "min_prob": 0.80,
        "emoji": "🔴",
        "badge": "CRITICAL",
        "advice": "Immediate inspection recommended. Check connectivity, interface status, SNMP availability, packet errors and recent fault logs."
    },
    "HIGH": {
        "min_prob": 0.60,
        "emoji": "🟠",
        "badge": "HIGH",
        "advice": "Investigate abnormal latency, packet loss, interface errors and utilization. Schedule preventive maintenance if the condition persists."
    },
    "MEDIUM": {
        "min_prob": 0.30,
        "emoji": "🟡",
        "badge": "MEDIUM",
        "advice": "Increase monitoring frequency and review recent trends before the next maintenance window."
    },
    "LOW": {
        "min_prob": 0.00,
        "emoji": "🟢",
        "badge": "LOW",
        "advice": "Continue normal monitoring and scheduled preventive maintenance."
    }
}

# Features to exclude from ML training inputs
EXCLUDED_COLUMNS = {
    "class",
    "target",
    "timestamp",
    "timestamp_dt",
    "source_file",
    "Device_name",
    "router_name",
    "device_name"
}

# Priority features for quick form prediction UI
PREFERRED_FORM_FEATURES = [
    "ICMP loss",
    "ICMP response time",
    "SNMP agent availability",
    "path_up",
    "Operational status",
    "packets",
    "errors",
    "traffic",
    "temperature",
    "CPU",
    "memory"
]
