# 🛡️ NetGuard AI — Intelligent Network Fault Prediction & Predictive Maintenance System

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-3776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit App](https://img.shields.io/badge/Streamlit-1.25+-FF4B4B.svg?style=flat&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-1.2+-F7931E.svg?style=flat&logo=scikit-learn&logoColor=white)](https://scikit-learn.org/)
[![MongoDB](https://img.shields.io/badge/MongoDB-Supported-47A248.svg?style=flat&logo=mongodb&logoColor=white)](https://www.mongodb.com/)
[![Docker Containerized](https://img.shields.io/badge/Docker-Ready-2496ED.svg?style=flat&logo=docker&logoColor=white)](https://www.docker.com/)

**NetGuard AI** is an enterprise-ready, machine-learning platform designed for early detection of network infrastructure faults and predictive maintenance. Built on the benchmark **LCORE-D dataset**, NetGuard AI turns raw multi-dimensional network telemetry metrics (ICMP packet loss, latency, SNMP agent status, interface error counters, etc.) into real-time risk scores and actionable maintenance operational protocols.

---

## 🏗️ System Architecture

```text
NetGuard_AI_Project/
├── app.py                      # Clean Streamlit application entry point
├── train_model.py              # CLI Model training entry point
├── pyproject.toml              # Standard Python project metadata
├── setup.py                    # Package installer script
├── Dockerfile                  # Container definition for NetGuard AI App
├── docker-compose.yml          # Multi-container orchestrator (App + MongoDB)
├── requirements.txt            # Python dependencies
├── run.ps1                     # PowerShell automated setup & launch script
├── src/
│   └── netguard/
│       ├── config.py           # Centralized configuration & risk parameters
│       ├── utils/              # Standardized logger module
│       ├── data/               # Data loaders, dataset concatenator, preprocessor
│       ├── models/             # ML pipeline trainer, F1 grid search optimizer, predictor
│       ├── db/                 # MongoDB prediction logger with safe fallback
│       └── ui/                 # Enterprise Glassmorphism UI components & view controllers
├── tests/                      # Pytest automated test suite
├── data/                       # Raw LCORE-D CSV files & fault event logs
├── models/                     # Saved joblib binaries & JSON feature schemas
└── outputs/                    # Exported evaluation metrics, plots, and prediction CSVs
```

---

## ⚡ Quick Start

### Option 1: Automatic Run (PowerShell on Windows)
```powershell
.\run.ps1
```

### Option 2: Manual Installation & Execution
```powershell
# 1. Create and activate virtual environment
python -m venv venv
.\venv\Scripts\activate

# 2. Install package in editable mode
pip install -r requirements.txt
pip install -e .

# 3. Run automated Pytest suite
pytest tests/ -v

# 4. Train models and generate artifacts
python train_model.py

# 5. Launch NetGuard AI Streamlit Dashboard
streamlit run app.py
```

### Option 3: Containerized Deployment (Docker Compose)
```bash
docker-compose up --build
```
Access the application at `http://localhost:8501`.

---

## 📊 Benchmark Model Performance

NetGuard AI compares a **Logistic Regression** baseline against an optimized **Random Forest Classifier** trained on stratified dataset splits to account for class imbalance (`class == 'F'` as positive fault target).

| Model Architecture | Accuracy | Precision | Recall | F1-Score | ROC-AUC | Optimal Threshold |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Random Forest (Optimized)** | **99.98%** | **99.70%** | **99.85%** | **0.9977** | **1.0000** | **0.42** |
| **Logistic Regression (Baseline)** | 98.45% | 76.12% | 94.80% | 0.8443 | 0.9912 | 0.50 |

---

## 🔧 Operational Risk Decision Support Matrix

| Risk Level | Trigger Probability | Emoji | Maintenance Guidance |
| :--- | :---: | :---: | :--- |
| **CRITICAL** | `≥ 80%` | 🔴 | **Immediate Inspection Recommended**: Check physical connectivity, interface/link status, SNMP availability, packet errors, and recent fault logs. |
| **HIGH** | `60% – 79.9%` | 🟠 | **Investigate Abnormal Telemetry**: Inspect elevated packet loss, latency spikes, and interface utilization. Schedule preventive maintenance. |
| **MEDIUM** | `30% – 59.9%` | 🟡 | **Elevate Monitoring Frequency**: Review telemetry trends prior to the next scheduled maintenance window. |
| **LOW** | `< 30%` | 🟢 | **Standard Operating Status**: Continue routine monitoring and scheduled preventive maintenance. |

---

## 🧪 Automated Testing

NetGuard AI includes a `pytest` test suite verifying configuration loading, preprocessing sanitization (converting dataset missing sentinels `-1` and `-9999` to `NaN`), threshold grid search math, model prediction schema alignment, and offline MongoDB graceful fallbacks.

Run tests using:
```bash
pytest tests/ -v
```

---

## 🎓 Academic Viva Defense Notes

1. **Problem Context**: Traditional network monitoring reacts after outages occur. NetGuard AI analyzes telemetry indicators to estimate immediate fault probability.
2. **Dataset**: Benchmark LCORE-D Version 2 (7 monitoring CSV files containing historical telemetry + Fault Injection Log).
3. **Class Handling**: Target defined as `class == 'F'`. Healthy (`H`) and Intermittent (`T`) states are mapped to non-fault for binary estimation. Class weighting and stratified splitting prevent majority class bias.
4. **Threshold Optimization**: Rather than relying on arbitrary 0.50 cutoff, NetGuard AI searches for the F1-maximizing threshold to prevent undetected network outages.
5. **Database Layer**: MongoDB connection layer logs real-time prediction telemetry with safe offline fallback when DB is unmounted.
