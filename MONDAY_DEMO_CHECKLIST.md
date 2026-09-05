# 🛡️ NetGuard AI - Demonstration & Viva Verification Checklist

## 1. Quick Environment Setup
```powershell
# Option A: Automatic Launch
.\run.ps1

# Option B: Manual Launch
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
pip install -e .
```

## 2. Automated Test Suite Verification
Run Pytest to demonstrate clean software engineering principles:
```powershell
pytest tests/ -v
```

## 3. Model Training & Pipeline Execution
Run model training pipeline:
```powershell
python train_model.py
```

Expected generated artifacts:
- `models/netguard_model.joblib`
- `models/feature_columns.json`
- `models/optimal_threshold.json`
- `outputs/model_comparison.csv`
- `outputs/test_predictions.csv`
- `outputs/combined_data.csv`
- `outputs/feature_importance.csv`
- `outputs/confusion_matrix.png`
- `outputs/roc_curve.png`
- `outputs/precision_recall_curve.png`
- `outputs/training_summary.json`

## 4. Launch Enterprise Platform
```powershell
streamlit run app.py
```

## 5. Live Demonstration Flow
1. **🏠 Dashboard**: Show total monitoring records, H/T/F distribution, and temporal fault rate area chart.
2. **🔮 New Data Prediction**: Input sample ICMP/SNMP telemetry and show real-time risk score, risk level badge, and maintenance advice card.
3. **📤 CSV Batch Prediction**: Upload a new network CSV file, show automatic missing feature handling, batch predictions, and export results CSV.
4. **🖥️ Device Explorer**: Select a router/switch device and show per-device risk trajectory timeline.
5. **📊 Network Analytics**: Show ICMP loss/latency distribution, feature correlation heatmap, and historical Fault Log event analysis.
6. **🧠 Model Performance**: Review Logistic Regression vs Random Forest benchmark metrics, optimal threshold F1 search, and top feature importance graph.
7. **🔧 Predictive Maintenance**: Present operational decision support matrix and risk protocols.
8. **ℹ️ About Project**: Explain end-to-end architecture pipeline, tech stack, and viva defense points.

## 6. Viva Defense Highlights
- **Problem**: Reactive network monitoring detects failures too late.
- **Dataset**: LCORE-D benchmark telemetry data + fault logs.
- **Handling Imbalance**: Stratified splitting, class weight balancing, and F1 threshold optimization.
- **Architecture**: Modular Python package (`src/netguard/`), Pytest suite, MongoDB logging, Docker containerization.
