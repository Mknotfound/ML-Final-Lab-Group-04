import os
import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

app = FastAPI(
    title="🛡️ EndpointShield AI — Executive Threat Engine",
    description="Low-Latency Static PE Malware Detection Service",
    version="1.0.0"
)

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
    features: list  # Expects list of 512 numerical static PE features

@app.get("/")
def health_check():
    return {"status": "online", "system": "EndpointShield AI Engine"}

@app.post("/scan-binary")
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

@app.get("/ui", response_class=HTMLResponse)
def get_dashboard_ui():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>EndpointShield AI — Operations Center</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
        <style>
            body { background-color: #0d1117; color: #c9d1d9; font-family: system-ui, sans-serif; }
            .card-dark { background-color: #161b22; border: 1px solid #30363d; border-radius: 12px; }
            .badge-threshold { background-color: #21262d; border: 1px solid #30363d; color: #8b949e; }
            .status-box { display: none; }
            .progress { background-color: #21262d; height: 12px; }
        </style>
    </head>
    <body class="py-5">
        <div class="container" style="max-width: 850px;">
            <div class="card-dark p-4 text-center shadow-lg mb-4">
                <h1 class="text-white fw-bold"><i class="fa-solid fa-shield-halved text-success me-2"></i>EndpointShield AI</h1>
                <p class="text-secondary">Asymmetric Static PE Malware Classification Engine</p>
            </div>

            <div class="card-dark p-4 shadow-lg text-center mb-4">
                <h4 class="text-white mb-3">Live Binary Scan Simulation</h4>
                <div class="d-flex justify-content-center gap-3">
                    <button class="btn btn-danger btn-lg fw-bold" onclick="runInference('malware')">
                        <i class="fa-solid fa-bug me-2"></i>Scan Malware Binary
                    </button>
                    <button class="btn btn-success btn-lg fw-bold" onclick="runInference('benign')">
                        <i class="fa-solid fa-circle-check me-2"></i>Scan Benign Binary
                    </button>
                </div>
            </div>

            <div id="resultCard" class="card-dark p-4 shadow-lg status-box">
                <div id="statusBanner" class="p-3 text-center rounded-3 fw-bold fs-4 mb-4"></div>
                <div class="mb-4">
                    <div class="d-flex justify-content-between small mb-1">
                        <span>Threat Probability Score</span>
                        <strong id="probPercentage" class="text-white">0%</strong>
                    </div>
                    <div class="progress">
                        <div id="probBar" class="progress-bar" role="progressbar" style="width: 0%;"></div>
                    </div>
                </div>
                <div class="row g-3 text-center">
                    <div class="col-md-4">
                        <div class="p-3 rounded-3" style="background-color: #21262d;">
                            <div class="text-secondary small">Prediction Label</div>
                            <strong id="lblVal" class="fs-5 text-white">-</strong>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="p-3 rounded-3" style="background-color: #21262d;">
                            <div class="text-secondary small">Applied Threshold</div>
                            <strong id="threshVal" class="fs-5 text-warning">0.20</strong>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="p-3 rounded-3" style="background-color: #21262d;">
                            <div class="text-secondary small">Mitigation Action</div>
                            <strong id="actVal" class="fs-5 text-white">-</strong>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <script>
            async function runInference(type) {
                let vector = (type === 'malware') ? Array(512).fill(0.95) : Array(512).fill(0.05);

                const response = await fetch('/scan-binary', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ features: vector })
                });

                const data = await response.json();
                document.getElementById('resultCard').style.display = 'block';

                const score = data.threat_probability;
                const pct = (score * 100).toFixed(1) + '%';
                document.getElementById('probPercentage').innerText = pct;
                
                const bar = document.getElementById('probBar');
                bar.style.width = pct;

                const banner = document.getElementById('statusBanner');
                const lbl = document.getElementById('lblVal');
                const act = document.getElementById('actVal');

                if (data.prediction_label === 'MALICIOUS' || data.prediction_label === 'MALWARE') {
                    banner.className = 'p-3 text-center rounded-3 fw-bold fs-4 mb-4 bg-danger text-white';
                    banner.innerHTML = '<i class="fa-solid fa-triangle-exclamation me-2"></i> THREAT DETECTED — ' + data.action_recommended;
                    bar.className = 'progress-bar bg-danger';
                    lbl.innerText = data.prediction_label;
                    lbl.className = 'fs-5 text-danger';
                    act.innerText = data.action_recommended;
                    act.className = 'fs-5 text-danger';
                } else {
                    banner.className = 'p-3 text-center rounded-3 fw-bold fs-4 mb-4 bg-success text-white';
                    banner.innerHTML = '<i class="fa-solid fa-shield-check me-2"></i> SAFE BINARY — ' + data.action_recommended;
                    bar.className = 'progress-bar bg-success';
                    lbl.innerText = data.prediction_label;
                    lbl.className = 'fs-5 text-success';
                    act.innerText = data.action_recommended;
                    act.className = 'fs-5 text-success';
                }
            }
        </script>
    </body>
    </html>
    """
