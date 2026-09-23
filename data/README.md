# Data Pipeline & Artifacts Overview

This directory contains raw and processed data artifacts for the **EndpointShield AI** static malware detection pipeline.

---

## 1. File Structure

* **`data/raw/sample.csv`**: Raw dataset containing 1,503 samples extracted from the EMBER 2018 malware dataset.
* **`data/processed/baseline_model.pkl`**: Serialized LightGBM classifier artifact output by the Data Science pipeline.

---

## 2. Dataset Schema

The static feature extraction pipeline generates **512 continuous numerical features** per sample, along with a binary target label:

| Feature Range | Name | Description |
| :--- | :--- | :--- |
| `0` to `255` | `byte_hist_0` – `byte_hist_255` | Normalized 256-bin raw byte value frequency counts. |
| `256` to `511` | `entropy_0` – `entropy_255` | 256-bin sliding window Shannon byte entropy distribution. |
| `512` | `label` | Ground truth label: `1` (Malicious), `0` (Benign), `-1` (Unlabeled). |

---

## 3. Data Ingestion & Preprocessing Workflow

1. Raw Windows PE binaries (`.exe`/`.dll`) or byte streams are parsed using `src/extract_features.py`.
2. Feature vectors are processed through `src/preprocessing.py` to ensure alignment with the 512-feature schema.
3. Prepared tensors/arrays are passed to `src/predict.py` or the `api/main.py` FastAPI endpoint for live threat scoring.
4.
