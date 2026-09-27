import os
import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

# 1. Initialize FastAPI with docs_url=None (we will serve a customized dark-mode /docs route)
app = FastAPI(
    title="🛡️ EndpointShield AI — Threat Operations Center",
    description="""
    ### 🚀 Low-Latency Static PE Malware Detection Service
    
    EndpointShield AI evaluates **512-feature static PE binary vectors** and applies an **asymmetric 0.20 risk threshold** ($100,000 False Negative breach cost vs. $50 False Positive analyst review cost) to enforce real-time binary quarantine.
    
    * **Model Engine:** LightGBM Classifier (ROC-AUC: 0.94)[cite: 1]
    * **Target Malware Recall:** 85.35%
    * **Enforced Action Cutoff:** `0.20`[cite: 1]
    * **Inference Latency:** < 15 ms
    """,
    version="1.0.0",
    docs_url=None,  # Overridden below
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
    print("[✓] LightGBM Model successfully loaded into FastAPI service.")
except Exception as e:
    model = None
    print(f"[!] Warning: Model failed to load ({e}). Engine in fallback mode.")

class FeaturePayload(BaseModel):
    features: list  # Expects list of 512 numerical static PE features[cite: 1]

@app.get("/", include_in_schema=False)
def health_check():
    return {"status": "online", "system": "EndpointShield AI Engine"}

@app.post("/scan-binary", summary="🔍 Scan Static PE Binary Vector", description="Evaluates 512 static features and applies 0.20 threshold[cite: 1].")
def scan_binary(payload: FeaturePayload, threshold: float = 0.20):
    if len(payload.features) != 512:
        raise HTTPException(status_code=400, detail="Payload must contain exactly 512 static features.")

    if model is None:
        raise HTTPException(status_code=500, detail="Model artifact missing or uninitialized.")

    X_input = pd.DataFrame([payload.features])

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

# ==============================================================================
# ENHANCED DARK-MODE SWAGGER UI ROUTE
# ==============================================================================
@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui():
    return HTMLResponse("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>EndpointShield AI — Swagger Operations</title>
        <link rel="stylesheet" type="text/css" href="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui.css">
        <style>
            /* Dark Theme Styling for Swagger UI */
            body { background-color: #0d1117 !important; color: #c9d1d9 !important; margin: 0; }
            .swagger-ui { filter: invert(88%) hue-rotate(180deg); }
            .swagger-ui .topbar { display: none; } /* Hide default green topbar */
            .swagger-ui img { filter: invert(100%) hue-rotate(180deg); } /* Fix image inversion */
            .swagger-ui .info { margin: 30px 0; }
            .swagger-ui .scheme-container { background-color: #161b22 !important; box-shadow: none !important; }
        </style>
    </head>
    <body>
        <div id="swagger-ui"></div>
        <script src="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui-bundle.js"></script>
        <script>
            window.onload = () => {
                window.ui = SwaggerUIBundle({
                    url: '/openapi.json',
                    dom_id: '#swagger-ui',
                    docExpansion: 'full',        // Auto-expand endpoints on load
                    defaultModelsExpandDepth: -1 // Hide cluttered schema objects at bottom
                });
            };
        </script>
    </body>
    </html>
    """)
