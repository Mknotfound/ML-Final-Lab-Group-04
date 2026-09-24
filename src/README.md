# Analytics & Risk Optimization Engines

This directory contains utility modules for backend prediction support and financial risk trade-off analysis.

---

## `src/cost_analysis.py`

Evaluates model decision cutoffs by balancing asymmetric enterprise failure costs:

* **False Negative (Missed Malware):** $100,000 per security incident.
* **False Positive (Analyst Review):** $50 per clean binary flagged.

### Optimal Cutoff Selection
By shifting the threshold from the standard $0.50$ default down to **$0.20$**, the system maximizes **Malware Recall (~85%+)**, drastically reducing costly False Negatives while keeping analyst manual triage overhead manageable.
