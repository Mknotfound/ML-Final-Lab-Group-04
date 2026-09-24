"""
src/cost_analysis.py
Cost-Threshold Optimization Engine for EndpointShield AI
"""

import numpy as np
import pandas as pd
from sklearn.metrics import confusion_matrix

COST_FN = 100000  # Missed Malware Cost ($)
COST_FP = 50      # Analyst Review Cost ($)
OPTIMAL_THRESHOLD = 0.20

def compute_business_cost(y_true, y_probs, threshold=OPTIMAL_THRESHOLD):
    preds = (y_probs >= threshold).astype(int)
    cm = confusion_matrix(y_true, preds, labels=[0, 1])
    tn, fp, fn, tp = cm.ravel()
    total_cost = (fn * COST_FN) + (fp * COST_FP)
    return {
        "optimal_threshold": threshold,
        "total_cost_usd": total_cost,
        "false_negatives": int(fn),
        "false_positives": int(fp)
    }

if __name__ == "__main__":
    print(f"[✓] Cost analysis module initialized with default optimal cutoff: {OPTIMAL_THRESHOLD}")
