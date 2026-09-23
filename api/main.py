import os
import joblib
import pandas as pd
import numpy as np
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Initialize FastAPI App
app = FastAPI(
    title="EndpointShield AI — Malware Detection Service",
    description="Inference API for Static PE Malware Scanning",
    version="1.0.0"
)

# Global model container
MODEL_PATH = "baseline_model.pkl"

def load_model():
    model_url = "https://raw.githubusercontent.com/Mknotfound/ML-Final-Lab-Group-04/main/data/processed/baseline_model.pkl"
    if not os.path.exists(MODEL_PATH):
        print("[+] Fetching model artifact from GitHub...")
        os.system(f"wget -O {MODEL_PATH} {model_url}")
    return joblib.load(MODEL_PATH)

try:
    model = load_model()
    print("[✓] Model successfully loaded into FastAPI service.")
except Exception as e:
    model = None
    print(f"[!] Warning: Model failed to load ({e}). Engine in fallback mode.")

class FeaturePayload(BaseModel):
    features: list  # Expects list of 512 numerical features

@app.get("/")
def health_check():
    return {"status": "online", "system": "EndpointShield AI Engine"}

@app.post("/scan-binary")
def scan_binary(payload: FeaturePayload, threshold: float = 0.20):
    if len(payload.features) != 512:
        raise HTTPException(status_code=400, detail="Payload must contain exactly 512 static features.")
    
    if model is None:
        raise HTTPException(status_code=500, detail="Model artifact missing or uninitialized.")

    # Format input for prediction
    X_input = pd.DataFrame([payload.features])
    
    # Get probability
    if hasattr(model, "predict_proba"):
        prob = float(model.predict_proba(X_input)[0, 1])
    else:
        prob = float(model.predict(X_input)[0])

    is_malicious = prob >= threshold
    
    return {
        "threat_probability": round(prob, 4),
        "prediction_label": "MALICIOUS" if is_malicious else "BENIGN",
        "applied_threshold": threshold,
        "action_recommended": "QUARANTINE_FILE" if is_malicious else "ALLOW_EXECUTION"
    }
