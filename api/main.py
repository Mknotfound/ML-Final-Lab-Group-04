import os
import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

# Initialize FastAPI with docs_url=None so we render our custom Swagger UI
app = FastAPI(
    title="🛡️ EndpointShield AI — Threat Operations Center",
    description="""
    ### Low-Latency Static PE Malware Detection Engine
    
    Evaluates **512-feature static PE binary vectors** against Sneha's **0.20 decision cutoff** ($100,000 breach cost vs $50 analyst review cost).
    
    * **Model Engine:** LightGBM Classifier (ROC-AUC: 0.94)
    * **Target Recall:** 85.35%
    * **Enforced Cutoff:** `0.20`
    * **Inference Latency:** < 15 ms
    """,
    version="1.0.0",
    docs_url=None,
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
    features: list  # Expects list of 512 numerical features

@app.get("/", include_in_schema=False)
def health_check():
    return {"status": "online", "system": "EndpointShield AI Engine"}

@app.post("/scan-binary", summary="🔍 Scan Static PE Binary", description="Evaluates 512 static features and applies 0.20 threshold.")
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
# NATIVE DARK THEME SWAGGER UI
# ==============================================================================
@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui():
    return HTMLResponse("""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>EndpointShield AI — Swagger API Docs</title>
        <link rel="stylesheet" type="text/css" href="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui.css">
        <!-- Official Swagger UI Darkness Theme -->
        <link rel="stylesheet" type="text/css" href="https://cdn.jsdelivr.net/npm/swagger-ui-themes@3.0.0/themes/3.x/theme-darkness.css">
        <style>
            body { background-color: #1b1b1b !important; }
            .swagger-ui .topbar { display: none !important; } /* Hide green topbar */
            .swagger-ui .info { margin: 20px 0 !important; }
            .swagger-ui .info .title { color: #58a6ff !important; }
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
                    docExpansion: 'full',         // Auto expand endpoints
                    defaultModelsExpandDepth: -1  // Hide messy schema boxes at bottom
                });
            };
        </script>
    </body>
    </html>
    """)
