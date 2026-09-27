# 🚀 EndpointShield AI — FastAPI Service (`api/`)

This directory contains the production web service that serves static malware predictions over HTTP REST endpoints.

---

## 📁 Files Included
* **`main.py`**: Core FastAPI application establishing `/` and `/predict` endpoints.
* **`../src/predict.py`**: Model wrapper loading `data/processed/baseline_model.pkl`.
* **`../src/sanity_check.py`**: Input validator checking array dimensions ($1 \times 512$).

---

## 🛠️ API Routes & Logic

### 1. Health Check (`GET /`)
* **Purpose:** Confirms the service is live and reachable.
* **Response:** `{"status": "online", "model_version": "1.0.0"}`

### 2. Malware Inference (`POST /predict`)
* **Purpose:** Accepts a JSON vector of 512 static features and returns threat evaluation.
* **Business Rule:** Enforces Sneha's **0.20 cost-optimized threshold**.
  * If `malware_probability >= 0.20` $\rightarrow$ `"status": "MALWARE_BLOCKED"`
  * If `malware_probability < 0.20` $\rightarrow$ `"status": "BENIGN_ALLOWED"`

---

## 🧪 Automated Testing
To run unit tests against these endpoints:
```bash
pytest tests/test_api.py
