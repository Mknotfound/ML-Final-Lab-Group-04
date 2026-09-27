## 🛠️ REST API Endpoints & Live Demonstration

### 1. Health Check Endpoint
* **HTTP Method:** `GET`
* **Path:** `/`
* **Description:** Verifies server uptime, system status, and model engine initialization.
* **Curl Command:**
  ```bash
  curl -X 'GET' '[https://unsettled-cough-labored.ngrok-free.dev/](https://unsettled-cough-labored.ngrok-free.dev/)' -H 'accept: application/json'
  ```
---
##Binary Scanning & Threat Inference
HTTP Method: POST

Path: /scan-binary (or /predict)

Description: Accepts a 512-feature static PE binary vector, runs inference through LightGBM, and enforces Sneha's 0.20 asymmetric decision threshold.

Input Constraint: Must contain an array of exactly 512 numerical feature values. Any other length returns an HTTP 400 Bad Request validation error.
---
```bash
 curl -X 'POST' \
  '[https://unsettled-cough-labored.ngrok-free.dev/scan-binary](https://unsettled-cough-labored.ngrok-free.dev/scan-binary)' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "features": [0.95, 0.98, 0.92, ... 512 values ...]
}'
```
---
🧪 Live Inference Test Outputs
A. Malware Detected Payload (High Entropy Sample)
When a high-risk vector extracted from data/raw/sample_project.csv is submitted:

Response Status: 200 OK

Response Body:

```JSON
{
  "threat_probability": 0.892,
  "prediction_label": "MALICIOUS",
  "applied_threshold": 0.2,
  "action_recommended": "QUARANTINE_FILE"
}
Explanation: Because threat_probability (0.892) >= applied_threshold (0.20), the API automatically triggers a QUARANTINE_FILE recommended action to prevent potential breach costs.
```
---
B. Clean Binary Payload (Benign Sample)
When a benign executable vector is evaluated:

Response Status: 200 OK

Response Body:

```JSON
{
  "threat_probability": 0.113,
  "prediction_label": "BENIGN",
  "applied_threshold": 0.2,
  "action_recommended": "ALLOW_EXECUTION"
}
Explanation: Because threat_probability (0.113) < applied_threshold (0.20), the engine permits execution on host devices.
```
---
C. Input Validation Error (Payload Size Mismatch)
If an incorrect array length (e.g., 4 features instead of 512) is submitted:

Response Status: 400 Bad Request

Response Body:

```JSON
{
  "detail": "Payload must contain exactly 512 static features."
}
```
---
---

### Why this works best for `api/README.md`:
1. It details the **HTTP Methods (`GET` / `POST`)**, **routes**, and **Curl commands** so developers can copy-paste and test commands from their local terminal.
2. It documents all three expected HTTP response codes (`200 OK` for Malware, `200 OK` for Benign, and `400 Bad Request` for validation failure) side-by-side with clear explanation notes.
