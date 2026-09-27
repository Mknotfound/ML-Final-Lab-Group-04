import os
import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.openapi.docs import get_swagger_ui_html
from pydantic import BaseModel

# 1. Initialize FastAPI with docs_url=None so we can override it with custom Swagger UI
app = FastAPI(
    title="🛡️ EndpointShield AI — Threat Operations Center",
    description="""
    ### 🚀 Low-Latency Static PE Malware Detection Service
    
    EndpointShield AI evaluates **512-feature static PE binary vectors** and applies Sneha's **0.20 asymmetric risk threshold** ($100,000 False Negative breach cost vs. $50 False Positive analyst review cost) to enforce real-time binary quarantine.
    
    * **Model Engine:** LightGBM Classifier (ROC-AUC: 0.94)[cite: 1]
    * **Target Malware Recall:** 85.35%
    * **Enforced Action Cutoff:** `0.20`[cite: 1]
    * **Inference Latency:** < 15 ms
    """,
    version="1.0.0",
    docs_url=None,  # Disable default raw docs to serve our customized version
    redoc_url="/redoc"
)

# --- Model Loading Logic ---
MODEL_PATH = "baseline_model.pkl"

def load_model():
    model_url = "https://raw.githubusercontent.com/Mknotfound/ML-Final-Lab-Group-04/main/data/processed/baseline_model.pkl"
    if not os.path.exists(MODEL_PATH):
        print("[+] Fetching model artifact from GitHub...")
        os.system(f"wget -O {MODEL_PATH} {model_url}")
    return joblib.load(MODEL_PATH)

try:
    model = load_model()
    print("[✓] Model successfully loaded.")
except Exception as e:
    model = None

class FeaturePayload(BaseModel):
    features: list  # Expects list of 512 numerical features[cite: 1]

@app.get("/", include_in_schema=False)
def health_check():
    return {"status": "online", "system": "EndpointShield AI Engine"}

@app.post("/scan-binary", summary="🔍 Scan Static PE Binary", description="Evaluates 512 static features and applies 0.20 threshold[cite: 1].")
def scan_binary(payload: FeaturePayload, threshold: float = 0.20):
    if len(payload.features) != 512:
        raise HTTPException(status_code=400, detail="Payload must contain exactly 512 static features.")

    if model is None:
        raise HTTPException(status_code=500, detail="Model artifact missing.")

    X_input = pd.DataFrame([payload.features])

    if hasattr(model, "predict_proba"):
        prob = float(model.predict_proba(X_input)[0, 1])
    else:
        prob = float(model.prob(X_input)[0])

    is_malicious = prob >= threshold

    return {
        "threat_probability": round(prob, 4),
        "prediction_label": "MALICIOUS" if is_malicious else "BENIGN",
        "applied_threshold": threshold,
        "action_recommended": "QUARANTINE_FILE" if is_malicious else "ALLOW_EXECUTION"
    }

# ==============================================================================
# CUSTOM ENHANCED SWAGGER UI ROUTE
# ==============================================================================
@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title="EndpointShield AI — API Operations",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_favicon_url="https://fastapi.tiangolo.com/img/favicon.png",
        # Inject custom Dark Mode CSS & styled elements into raw Swagger
        swagger_js_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui-bundle.js",
        swagger_css_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui.css",
        swagger_ui_parameters={
            "defaultModelsExpandDepth": -1, # Hide unnecessary schema models at bottom
            "docExpansion": "full",         # Auto-expand endpoints
            "filter": True,                 # Add dynamic search filter bar
        }
    )
