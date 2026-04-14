# PROJECT 11 — PREDICTION GATE V1 VERDICT

**Date:** April 2026  
**Status:** CLOSED — FAIL (Predictive)  
**Gate:** prediction_gate_v1

---

## 1) What this gate tested

Whether Project 10's phase-structure can be used for **pre-run prediction** on unseen (H, P) points.

- H := residual_abs (Project 10 heterogeneity magnitude)
- P := universal_power (Project 10 universal rescue power)

Ground truth labeling rule is locked in:
- `project_11/docs/PREDICTION_GATE_V1_GROUND_TRUTH_RULE.md`

Holdout points are locked in:
- `project_11/results/prediction_gate_v1_holdout_points.json`

Predictions are locked in:
- `project_11/results/prediction_gate_v1_predictions.json`

---

## 2) Result (authoritative numbers)

From the evaluation run:
- points: 16
- model accuracy: 0.8125
- model macro-F1: 0.7460
- best baseline macro-F1: 0.7460
- PASS: False

Evaluation artifacts:
- `project_11/results/prediction_gate_v1_report.md`
- `project_11/results/prediction_gate_v1_artifact.json`

---

## 3) Pass condition (locked in protocol)

PASS requires:
- macro-F1 >= best_baseline + 0.15
- AND macro-F1 >= 0.60

Observed:
- 0.7460 >= 0.7460 + 0.15  → FALSE
- 0.7460 >= 0.60           → TRUE

Verdict:
✅ protocol integrity ok  
❌ predictive performance threshold not met  
→ **FAIL**

---

## 4) Meaning (no hype)

This FAIL means:
- The V1 prediction method did not outperform a strong baseline on the chosen holdout set.
- Therefore Project 11 must not proceed to full "predictive regime theory" work under V1.

This is useful: it localizes the weakness (prediction quality / theory compression), not the metrics.

---

## 5) Next action (non-negotiable)

- Freeze V1 artifacts (no edits).
- Run a structured post-mortem:
  - list exactly which points were wrong
  - identify which theory assumption failed (especially near transition vs family-aware separation)
- Only then open **Prediction Gate V2** with:
  - revised prediction rule (theory revision)
  - new holdout set (outside V1)
  - locked protocol and predictions again

---
