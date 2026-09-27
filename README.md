# 🛡️ EndpointShield AI — Enterprise Static Malware Classification Platform

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Production-green)](https://fastapi.tiangolo.com/)
[![Model](https://img.shields.io/badge/Model-LightGBM-orange)](https://lightgbm.readthedocs.io/)
[![Testing](https://img.shields.io/badge/Tests-Pytest%20Passed-brightgreen)](https://docs.pytest.org/)
[![Dashboard](https://img.shields.io/badge/BI-Power%20BI-yellow)](https://powerbi.microsoft.com/)

## Executive Summary
EndpointShield AI is an enterprise-grade solution designed to classify malicious versus benign binary files using static features extracted from Portable Executable (PE) headers, byte histograms, and sliding-window entropy values[cite: 1]. Developed for enterprise endpoint security environments, the system evaluates incoming threats without executing files in memory, eliminating execution risk while enforcing cost-optimized threat detection[cite: 1].

---

## Technical Objectives & Performance Metrics
* **Primary Metric — Asymmetric Risk Cost Reduction:** Minimizing False Negatives (missed malware) is paramount ($100,000 breach cost vs. $50 analyst review cost)[cite: 1].
* **Optimal Decision Cutoff (0.20 Threshold):** Down-shifted probability decision threshold from standard 0.50 to **0.20**, prioritizing Malware Recall (>85%) to prevent costly security breaches[cite: 1].
* **Secondary Metric — Discrimination (ROC-AUC: ~0.937):** Achieves strong class separation across static byte and entropy feature distributions[cite: 1].
* **Safety Protocol:** Strictly static feature analysis; zero dynamic execution of untrusted binary files[cite: 1].

---

## Dataset Provenance & Ingestion
* **Source & Schema:** 1,503 PE executable samples evaluated across **512 static features** (256 byte frequency counts + 256 sliding-window entropy values)[cite: 1].
* **Repository Compliance:** To respect GitHub file size limits (< 50MB), raw feature extractions and light samples are tracked in `data/raw/sample_project.csv` for full pipeline verification[cite: 1].

---

## Data Consultancy Team & Functional Roles

| Team Member | Functional Role | Owned Deliverables |
| :--- | :--- | :--- |
| **Mayur D. Kumar (Lead)** | Machine Learning Engineer (MLE) | FastAPI service (`api/main.py`), inference wrapper (`src/predict.py`), feature validation (`src/sanity_check.py`), automated unit testing (`tests/test_api.py`), pipeline notebook (`notebooks/FastAPI_Pipeline_Server.ipynb`). |
| **Noel Abraham** | Data Engineer (DE) | Feature extraction logic (`src/extract_features.py`), dataset preprocessing (`src/Dataset_preprocessing.py`), project sample (`data/raw/sample_project.csv`), dependency manifest (`requirements.txt`)[cite: 1]. |
| **Benny Bernard** | Data Analyst (DA) | Exploratory data analysis, byte entropy distribution plots, static feature importances (`notebooks/EDA.ipynb`)[cite: 1]. |
| **Sam Prajwal** | Data Scientist (DS) | LightGBM classifier training, ROC-AUC tuning, serialized model weights (`data/processed/baseline_model.pkl`, `notebooks/Baseline_Model.ipynb`)[cite: 1]. |
| **Sneha Kati** | Analytics Engineer (AE) | Asymmetric financial cost optimization ($100k FN vs $50 FP), 0.20 decision cutoff engine (`src/cost_analysis.py`, `notebooks/Cost_Threshold_Optimization.ipynb`, `report/cost_curve (1).png`)[cite: 1]. |
| **Sujith Yesudas** | BI Developer (BI) | Executive Threat Center dashboard (`dashboard/Final project report.pbix`, `dashboard/Final project report.pdf`)[cite: 1]. |

---

## 🧪 System Verification & Test Proof

The production FastAPI pipeline was verified directly within the Google Colab environment using `pytest`[cite: 1, 3].

```bash
!PYTHONPATH=. pytest tests/test_api.py
```
---
##Repo RoadMap
ML-Final-Lab-Group-04/
├── api/
│   ├── main.py                     # Production FastAPI application endpoints[cite: 1]
│   └── README.md                   # API deployment & route documentation[cite: 1]
├── data/
│   ├── raw/
│   │   └── sample_project.csv      # 1,503 PE executable feature sample dataset[cite: 1]
│   ├── processed/
│   │   └── baseline_model.pkl     # Serialized LightGBM model weights[cite: 1]
│   └── README.md                   # Feature schema & dataset dictionary[cite: 1]
├── dashboard/
│   ├── Final project report.pbix   # Power BI interactive Threat Center dashboard[cite: 1]
│   └── Final project report.pdf    # Executive dashboard PDF export[cite: 1]
├── notebooks/
│   ├── Baseline_Model.ipynb        # LightGBM training & ROC-AUC evaluation[cite: 1]
│   ├── Cost_Threshold_Optimization.ipynb # 0.20 threshold cost analysis[cite: 1]
│   ├── EDA.ipynb                   # Feature importance & entropy analysis[cite: 1]
│   └── FastAPI_Pipeline_Server.ipynb# API integration & testing notebook[cite: 1]
├── report/
│   └── cost_curve (1).png          # Asymmetric business cost trade-off plot[cite: 1]
├── reports/
│   └── figures/
│       └── api_test_proof.png      # Verified pytest execution output proof[cite: 1, 3]
├── src/
│   ├── extract_features.py         # Static PE byte & entropy feature extractor[cite: 1]
│   ├── Dataset_preprocessing.py    # Stratified data loading & split pipeline[cite: 1]
│   ├── predict.py                  # Model inference wrapper[cite: 1]
│   ├── cost_analysis.py            # Business risk evaluation module[cite: 1]
│   ├── sanity_check.py             # Feature dimension validator (512 features)[cite: 1]
│   └── README.md                   # Core module source documentation[cite: 1]
├── tests/
│   └── test_api.py                 # Automated pytest unit test suite[cite: 1, 2]
├── requirements.txt                # Locked environment dependencies[cite: 1]
└── README.md                       # Project overview landing page[cite: 1]

---
