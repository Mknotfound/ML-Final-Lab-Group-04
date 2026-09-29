# 📊 EndpointShield — Analytical & Evaluation Report

This directory consolidates the analytical findings, business risk optimizations, visual assets, and verification proofs for the EndpointShield static malware classification platform.

---

## 📑 Executive Summary & Key Findings

### 1. Exploratory Data Analysis & Feature Selection (Benny — Data Analyst)
* **Dataset Scope:** Evaluated 1,503 Portable Executable (PE) binaries mapped across **512 static features** (256 byte frequency histograms + 256 sliding-window byte entropy values).
* **Primary Threat Indicator:** High sliding-window byte entropy values ($> 7.2$) serve as the single strongest signal for packed, encrypted, or obfuscated malware executables[cite: 1].
* **Feature Reduction:** Summary correlation rankings (`top_feature_correlations.csv`) and class separation metrics (`top_class_separation.csv`) confirm that byte entropy features provide superior discrimination compared to raw PE header flags.

---

## 💰 Business Risk & Cost Threshold Optimization (Sneha — Analytics Engineer)

Standard machine learning models default to a classification probability threshold of **0.50**[cite: 1]. However, in enterprise cybersecurity, decision costs are severely asymmetric:
* **False Negative (Missed Malware):** **$100,000** (Catastrophic breach, data exfiltration, ransomware recovery, and incident response)[cite: 1].
* **False Positive (Benign Flagged):** **$50** (Triage review by a Tier-1 SOC analyst)[cite: 1].

$$\text{Asymmetric Cost Ratio} = \frac{\$100,000 \text{ (FN)}}{\$50 \text{ (FP)}} = 2,000 : 1$$

### Optimal Cutoff Decision:
By evaluating the financial cost curve (`figures/cost_curve.png`), Sneha optimized the decision boundary down to **0.20**:
* **At 0.50 Threshold:** High False Negative rate resulted in unacceptable total enterprise risk exposure[cite: 1].
* **At 0.20 Threshold:** Boosted **Malware Recall to >85%**, drastically minimizing missed threats while maintaining an acceptable analyst triage queue[cite: 1].

---

## 🧪 System Deployment & API Verification (Mayur — MLE & Lead)

The serving engine (`api/main.py`) integrates Sam's LightGBM model weights (`data/processed/baseline_model.pkl`) with Sneha's 0.20 risk threshold[cite: 1].

### Automated Test Execution
```bash
!PYTHONPATH=. pytest tests/test_api.py
```
---
📊 Visual Assets & Figures Summary
1. API Verification Output (figures/api_test_proof.jpeg)Demonstrates automated pytest suite execution in Colab passing all route assertions (100% PASSED).
2. Optimal Cost Trade-off Curve (figures/cost_curve.png)Highlights total estimated enterprise cost vs. classification probability threshold, verifying $0.20$ as the minimum financial cost point[cite: 1, 5].
3. Class Distribution & Separation (figures/class_distribution.png, figures/class_separation.png)Visualizes target class ratios (Malware vs. Benign) and class separation performance across feature vectors.
4. Feature Skewness & Correlations (figures/feature_skewness.png, figures/top_feature_correlations.png)Maps feature distributions and highlights top static byte/entropy indicators correlated with malicious activity.

---
```
📁 Directory Asset Index
Asset Path   Description
figures/api_test_proof.jpeg->Pytest execution output proof demonstrating passing endpoint tests.
figures/cost_curve.png->Asymmetric risk cost curve showcasing the 0.20 optimal threshold cutoff.
figures/class_distribution.png->Target class ratio breakdown (Malware vs. Benign).
figures/class_separation.png->Feature separation plot across model decision scores.
figures/feature_skewness.png->Distribution plot highlighting entropy feature skewness.
figures/top_feature_correlations.png->Correlation heatmap of top static PE features.
feature_selection_summary.csv->Consolidated summary table of selected static features.
top_feature_correlations.csv->Ranked list of feature-to-target correlation scores.
top_class_separation.csv->Quantitative class separation metrics per feature.
