# EndpointShield — Enterprise Malware Classification Platform

## Executive Summary
EndpointShield is an enterprise-grade AI solution designed to classify malicious versus benign binary files using purely static features extracted from Portable Executable (PE) headers, byte histograms, and import metadata[cite: 1]. Developed for enterprise security environments, the system evaluates incoming threats without executing files in memory, minimizing runtime risk while maximizing detection recall[cite: 1].

---

## Technical Objectives & Performance Metrics
* **Primary Metric — Malware Recall (Target: ≥ 98%):** Minimizing False Negatives (missed malware) is paramount, as an undetected malicious binary represents a catastrophic enterprise security breach[cite: 1].
* **Secondary Metric — ROC-AUC:** Evaluates overall model discrimination across varying classification thresholds[cite: 1].
* **Safety Protocol:** Strictly static feature analysis; zero dynamic execution of untrusted binary files[cite: 1].

---

## Dataset Provenance & Ingestion
* **Dataset:** EMBER (Elastic Malware Benchmark for Empowering Researchers)[cite: 1]
* **Feature Dimension:** 2,351 static extraction features per sample[cite: 1]
* **Repository Compliance:** To respect GitHub file size limits (< 50MB), raw feature extractions are downloaded locally via automated scripts, while a 500-row representative vector matrix is stored in `data/raw/sample.csv` for data schema verification[cite: 1].

---

## Data Consultancy Team & Functional Roles

| Team Member | Functional Role | Owned Deliverables |
| :--- | :--- | :--- |
| **Mayur D. Kumar** | Team Lead & ML Engineer (MLE)[cite: 1] | Repository architecture, `requirements.txt`, deployment pipeline (`src/predict.py`), latency validation[cite: 1]. |
| **Noel Abraham** | Data Engineer (DE)[cite: 1] | Data ingestion script, missing value/outlier processing (`src/preprocessing.py`), `data/raw/sample.csv`[cite: 1]. |
| **Benny Bernard** | Data Analyst (DA)[cite: 1] | Exploratory data analysis, byte entropy distribution plots, correlation heatmaps (`notebooks/EDA.ipynb`)[cite: 1]. |
| **Sam Prajwal** | Data Scientist (DS)[cite: 1] | Baseline vs. LightGBM/XGBoost models, cross-validation tuning, serialized model artifact (`notebooks/Baseline_Model.ipynb`)[cite: 1]. |
| **Sneha Kati** | Analytics Engineer (AE)[cite: 1] | Decision threshold trade-off tuning, confusion cost-matrix modeling (False Positive vs. False Negative cost analysis)[cite: 1]. |
| **Sujith Yesudas** | BI Developer (BI)[cite: 1] | Interactive executive dashboard (`dashboard/`), threat tester UI, operational security KPI cards[cite: 1]. |

---

## Project Directory Structure

```text
ML-Final-Lab-Group-04/
├── data/
│   ├── raw/                 # Contains sample.csv & ingestion script[cite: 1]
│   └── processed/           # Scaled & clean feature matrices[cite: 1]
├── notebooks/               # EDA and ML modeling notebooks (.ipynb)[cite: 1]
├── src/                     # Modular python scripts (.py) for pipelines[cite: 1]
├── dashboard/               # Power BI (.pbix) or Streamlit app interface[cite: 1]
├── report/                  # Project documentation & evaluation report[cite: 1]
├── presentation/            # 7-Slide client pitch deck[cite: 1]
├── .gitignore               # Excludes large binaries & data dumps[cite: 1]
├── requirements.txt         # Project dependency manifest[cite: 1]
└── README.md                # Project documentation landing page[cite: 1]
