# 🛡️ NetGuard AI
## Intelligent Network Fault Prediction & Predictive Maintenance System

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.25+-FF4B4B?style=flat&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-1.2+-F7931E?style=flat&logo=scikit-learn&logoColor=white)](https://scikit-learn.org/)
[![MongoDB](https://img.shields.io/badge/MongoDB-6.0-47A248?style=flat&logo=mongodb&logoColor=white)](https://www.mongodb.com/)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=flat&logo=docker&logoColor=white)](https://www.docker.com/)
[![Git-LFS](https://img.shields.io/badge/Git-LFS-Enabled-F64935?style=flat&logo=git&logoColor=white)](https://git-lfs.github.io/)

NetGuard AI is an intelligent machine-learning-based network fault prediction and predictive maintenance platform.

The system analyzes network telemetry data and predicts the probability of network faults. It converts machine-learning predictions into operational risk levels and provides an interactive dashboard for monitoring, analytics, device exploration, and predictive maintenance.

The application is built with Python, Scikit-Learn, Streamlit, MongoDB, Docker, Docker Compose, Git, Git LFS, and Pytest.

---

## 🚀 Key Features

### 🤖 Machine Learning

- Logistic Regression baseline model
- Optimized Random Forest classifier
- Network fault probability prediction
- F1-score-based threshold optimization
- Class imbalance handling
- Stratified train/test splitting
- Model evaluation and comparison
- Feature importance analysis

### 📊 Network Analytics

- Network health overview
- Fault vs healthy device analysis
- Network telemetry visualization
- Device-level exploration
- Batch prediction
- Model performance analysis
- Prediction history
- Risk classification

### 🛠️ Predictive Maintenance

NetGuard AI converts predicted fault probabilities into operational risk levels.

| Risk Level | Probability | Recommended Action |
|---|---:|---|
| 🔴 **CRITICAL** | ≥ 80% | Immediate inspection recommended |
| 🟠 **HIGH** | 60% – 79.9% | Investigate abnormal telemetry |
| 🟡 **MEDIUM** | 30% – 59.9% | Increase monitoring frequency |
| 🟢 **LOW** | < 30% | Continue standard monitoring |

### 🗄️ Database

- MongoDB prediction logging
- Persistent Docker volume
- Docker service-to-service networking
- Graceful fallback when MongoDB is unavailable

### 🐳 Deployment

- Dockerized Streamlit application
- Docker Compose orchestration
- MongoDB container
- MongoDB healthcheck
- Persistent database storage
- Docker Hub deployment
- Git LFS for large ML files

---

# 🏗️ System Architecture

```text
                    ┌─────────────────────────┐
                    │      Network Data       │
                    │   LCORE-D Telemetry     │
                    └────────────┬────────────┘
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │    Data Preprocessing   │
                    │                         │
                    │ • Data Cleaning         │
                    │ • Missing Values        │
                    │ • Feature Preparation   │
                    └────────────┬────────────┘
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │     ML Prediction       │
                    │                         │
                    │ Logistic Regression     │
                    │ Random Forest           │
                    └────────────┬────────────┘
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │   Fault Probability     │
                    │                         │
                    │   Risk Classification   │
                    └────────────┬────────────┘
                                 │
                    ┌────────────┴────────────┐
                    ▼                         ▼
        ┌──────────────────────┐    ┌─────────────────────┐
        │ Streamlit Dashboard  │    │ MongoDB Prediction  │
        │                      │    │ Logging             │
        │ • Analytics          │    │                     │
        │ • Predictions        │    │ • Predictions       │
        │ • Devices            │    │ • Timestamps        │
        │ • Maintenance        │    │ • Risk Information  │
        └──────────────────────┘    └─────────────────────┘
```

---

# 📁 Project Structure

```text
NetGuard-AI/
│
├── app.py
├── train_model.py
├── requirements.txt
├── pyproject.toml
├── setup.py
├── run.ps1
│
├── Dockerfile
├── docker-compose.yml
├── .dockerignore
├── .env.example
├── .gitignore
├── .gitattributes
│
├── data/
│   ├── LCORE-D R1.csv
│   ├── LCORE-D R2.csv
│   ├── LCORE-D R3.csv
│   ├── LCORE-D R4.csv
│   ├── LCORE-D R5.csv
│   ├── LCORE-D R6.csv
│   ├── LCORE-D R7.csv
│   └── fault_log/
│       └── FAULT_LOG.csv
│
├── models/
│   ├── netguard_model.joblib
│   ├── feature_columns.json
│   └── optimal_threshold.json
│
├── outputs/
│   ├── combined_data.csv
│   ├── model_comparison.csv
│   ├── feature_importance.csv
│   ├── test_predictions.csv
│   └── training_summary.json
│
├── src/
│   └── netguard/
│       ├── config.py
│       ├── data/
│       │   ├── loader.py
│       │   └── preprocessor.py
│       ├── models/
│       │   ├── trainer.py
│       │   ├── predictor.py
│       │   └── evaluator.py
│       ├── db/
│       │   └── mongo.py
│       ├── ui/
│       │   ├── styles.py
│       │   ├── theme.py
│       │   └── views/
│       └── utils/
│           └── logger.py
│
└── tests/
    ├── test_config.py
    ├── test_data_loader.py
    ├── test_db.py
    └── test_model.py
```

---

# 📊 Machine Learning Pipeline

```text
Raw Network Telemetry
        │
        ▼
Data Loading
        │
        ▼
Data Cleaning & Preprocessing
        │
        ▼
Feature Preparation
        │
        ▼
Train/Test Split
        │
        ▼
Model Training
   ┌────┴──────────────┐
   ▼                   ▼
Logistic Regression   Random Forest
   │                   │
   └────────┬──────────┘
            ▼
      Model Evaluation
            │
            ▼
    Threshold Optimization
            │
            ▼
    Fault Probability
            │
            ▼
      Risk Classification
```

---

# 📈 Model Performance

NetGuard AI evaluates a Logistic Regression baseline against an optimized Random Forest classifier.

| Model | Accuracy | Precision | Recall | F1-Score | ROC-AUC | Threshold |
|---|---:|---:|---:|---:|---:|---:|
| **Random Forest (Optimized)** | **99.98%** | **99.70%** | **99.85%** | **0.9977** | **1.0000** | **0.42** |
| Logistic Regression | 98.45% | 76.12% | 94.80% | 0.8443 | 0.9912 | 0.50 |

The Random Forest model achieved the strongest overall performance in the project's evaluation.

---

# 🎯 Fault Detection Strategy

The project uses network state information to determine whether a device should be considered faulty.

```text
F = Fault
H = Healthy
T = Intermittent
```

For binary fault prediction:

```text
Fault          → Positive Class
Healthy        → Non-Fault
Intermittent   → Non-Fault
```

The system uses class weighting and stratified splitting to improve model performance when dealing with imbalanced classes.

---

# ⚙️ Threshold Optimization

Instead of using a fixed probability threshold of `0.50`, NetGuard AI searches for a threshold that provides a better F1-score.

```text
Default Threshold
        │
        ▼
      0.50
        │
        ▼
Threshold Search
        │
        ▼
F1-Score Optimization
        │
        ▼
Optimal Threshold
      0.42
```

The optimized threshold helps balance:

- Precision
- Recall
- False positives
- False negatives

This is particularly useful in network fault detection where missing a real fault can be costly.

---

# 🧪 Testing

The project includes automated tests using Pytest.

Tests cover:

- Configuration
- Data loading
- Data preprocessing
- Model prediction
- Feature validation
- MongoDB functionality
- Prediction logic

Run:

```powershell
pytest tests/ -v
```

---

# 🐳 Docker Deployment

NetGuard AI uses Docker Compose to run both the Streamlit application and MongoDB.

```text
┌────────────────────────────────────┐
│          Docker Compose            │
│                                    │
│  ┌──────────────────────────────┐  │
│  │       NetGuard AI App        │  │
│  │       Streamlit :8501        │  │
│  └──────────────┬───────────────┘  │
│                 │                  │
│                 ▼                  │
│  ┌──────────────────────────────┐  │
│  │         MongoDB 6.0          │  │
│  │         Port :27017          │  │
│  └──────────────┬───────────────┘  │
│                 │                  │
│                 ▼                  │
│       Persistent Docker Volume     │
└────────────────────────────────────┘
```

---

# 🚀 Run the Project

## Requirements

Install:

- Git
- Docker Desktop

No Python installation is required when using Docker.

---

## 1. Clone the Repository

```powershell
git clone https://github.com/pratik2146/NetGuard-AI.git
cd NetGuard-AI
```

---

## 2. Start NetGuard AI

```powershell
docker compose up -d
```

Docker Compose will automatically:

1. Pull the NetGuard AI image from Docker Hub.
2. Pull MongoDB 6.0.
3. Create the Docker network.
4. Start MongoDB.
5. Check MongoDB health.
6. Start the Streamlit application.
7. Create the persistent MongoDB volume.

---

## 3. Open the Dashboard

Open your browser:

```text
http://localhost:8501
```

---

## 4. Check Containers

```powershell
docker compose ps
```

You should see:

```text
netguard_app
netguard_mongo
```

Both containers should be running and healthy.

---

# 🐳 Docker Hub

The official NetGuard AI Docker image is:

```text
pratikdesai2146/netguard-ai:v1.0
```

Pull the image manually:

```powershell
docker pull pratikdesai2146/netguard-ai:v1.0
```

The Docker Compose configuration automatically uses this image.

---

# 🗄️ MongoDB Persistence

MongoDB uses a persistent Docker volume:

```text
netguard_ai_project_mongo_data
```

This means MongoDB prediction data remains available even if the containers are restarted or recreated.

The application connects to MongoDB using:

```text
mongodb://mongo:27017/
```

The Docker service name `mongo` is used instead of `localhost` because the application and database run in separate containers.

---

# 🔐 Environment Variables

The example environment file is:

```text
.env.example
```

It contains:

```env
MONGODB_URI=mongodb://mongo:27017/
MONGODB_DB_NAME=netguard_ai
MONGODB_COLLECTION_NAME=predictions

STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=0.0.0.0
```

Never commit real passwords, API keys, or other secrets to GitHub.

---

# 💻 Local Development

If you want to run the project without Docker:

### Create virtual environment

```powershell
python -m venv venv
```

### Activate virtual environment

```powershell
.\venv\Scripts\activate
```

### Install dependencies

```powershell
pip install -r requirements.txt
pip install -e .
```

### Run tests

```powershell
pytest tests/ -v
```

### Train model

```powershell
python train_model.py
```

### Start Streamlit

```powershell
streamlit run app.py
```

---

# 📦 Git LFS

The project contains large machine-learning artifacts.

Git LFS is used for:

```text
models/netguard_model.joblib
outputs/combined_data.csv
```

Check tracked LFS files:

```powershell
git lfs ls-files
```

Expected files include:

```text
models/netguard_model.joblib
outputs/combined_data.csv
```

---

# 🧰 Technology Stack

| Category | Technology |
|---|---|
| Programming Language | Python |
| Machine Learning | Scikit-Learn |
| Data Processing | Pandas, NumPy |
| Visualization | Matplotlib |
| Web Application | Streamlit |
| Database | MongoDB |
| Containerization | Docker |
| Orchestration | Docker Compose |
| Version Control | Git |
| Large Files | Git LFS |
| Testing | Pytest |
| Container Registry | Docker Hub |

---

# 🎓 Viva Explanation

## What is NetGuard AI?

NetGuard AI is a machine-learning-based predictive maintenance system for network infrastructure.

It analyzes network telemetry and predicts whether a network device is likely to experience a fault.

---

## What problem does it solve?

Traditional network monitoring often detects problems after a failure or significant degradation has already occurred.

NetGuard AI attempts to identify abnormal network behavior earlier so that maintenance teams can investigate devices before major service disruption occurs.

---

## How does the system work?

```text
Network Data
     ↓
Preprocessing
     ↓
Feature Engineering
     ↓
Machine Learning Model
     ↓
Fault Probability
     ↓
Risk Classification
     ↓
Dashboard + MongoDB
```

---

## Why Random Forest?

Random Forest was selected because it achieved better evaluation performance than the Logistic Regression baseline in this project.

It can also model nonlinear relationships between different network telemetry features.

---

## Why threshold optimization?

A probability threshold of `0.50` is not always the best threshold for a classification problem.

NetGuard AI searches for a threshold that improves the F1-score and provides a better balance between precision and recall.

The optimized threshold used in the project is:

```text
0.42
```

---

# ⭐ Project Highlights

- 🤖 Machine-learning-based fault prediction
- 🌲 Optimized Random Forest classifier
- 📊 Interactive Streamlit dashboard
- 🎯 Probability threshold optimization
- 🛠️ Predictive maintenance recommendations
- 🗄️ MongoDB prediction logging
- 🐳 Dockerized deployment
- 🔗 Docker Compose multi-container architecture
- 💾 Persistent MongoDB storage
- 📦 Docker Hub image
- 🧪 Automated testing with Pytest
- 📁 Git LFS for large ML artifacts
- 📈 Model performance analytics

---

# 🔮 Future Improvements

Possible future enhancements:

- Real-time network telemetry ingestion
- Live network device monitoring
- Automated email/SMS alerts
- Time-series forecasting
- Model drift detection
- Automated model retraining
- CI/CD pipeline
- Cloud deployment
- Role-based authentication
- Advanced anomaly detection
- Network topology visualization
- Real-time alert notifications

---

# 👥 Team

**NetGuard AI**

Academic machine-learning and predictive network monitoring project.

---

# 📄 License

This project is intended for academic, educational, and portfolio purposes.
