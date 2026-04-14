# PROJECT 11 — PREDICTION GATE V2 PROTOCOL
## Compression-Based Prediction (Pre-Registered)

**Date:** April 2026  
**Status:** DRAFT → LOCKED after predictions are saved  
**Gate:** prediction_gate_v2

---

## 0) Core Idea

Gate V1 failed because coarse map intuition did not beat a strong nearest-neighbor baseline.

Gate V2 tests a stronger claim:

> A compact boundary rule (inequalities) can predict regions beyond nearest-neighbor interpolation.

---

## 1) Space Definition (same as Project 10)

- H := residual_abs (heterogeneity magnitude)
- P := universal_power

Each point is (H, P).

---

## 2) Ground Truth (LOCKED)

Ground truth is EXACTLY the Project 10 phase-diagram region rule:

- `project_11/docs/PREDICTION_GATE_V1_GROUND_TRUTH_RULE.md`

No changes allowed.

---

## 3) Holdout Rule (Anti-leakage)

Holdout points must:
- not equal Project 10 grid values:
  - H ∉ {0.003, 0.009, 0.015}
  - P ∉ {0.30, 0.36, 0.42}
- avoid refinement bands used in Project 10:
  - H not in [0.0060, 0.0075]
  - P not in [0.320, 0.340]
- avoid exact refinement probe points:
  - H not equal {0.003, 0.0045, 0.006, 0.0075, 0.009}
  - P not equal {0.30, 0.32, 0.34, 0.36}

Holdout list is locked in:
- `project_11/results/prediction_gate_v2_holdout_points.json`

---

## 4) Prediction Method (Pre-Registered Compressed Rule)

We predict using a compact inequality approximation derived from the Project 10 scoring structure:

Let:
- D_min(H,P) = 0.80*H + 0.40*(0.30 - P)   (harder families: shared_failure=0.40)
- D_max(H,P) = 0.80*H + 0.41*(0.30 - P)   (easier families: shared_failure=0.41)
- gap_est(H,P) = 0.80*H + 0.405*(0.30 - P)  (average shared_failure=0.405)

Predict:
- family-aware region if:
  - D_min > 0.005 AND gap_est > 0.005
- universal region if:
  - D_max < -0.005 OR gap_est < -0.003
- else:
  - transition region

This is a **compressed boundary rule** (not nearest-neighbor).

Predictions are locked in:
- `project_11/results/prediction_gate_v2_predictions.json`

---

## 5) Baselines (Required)

- majority baseline (from Project 10 grid)
- nearest-neighbor baseline (Project 10 grid)

---

## 6) Pass Condition (LOCKED)

Gate V2 PASSES if:
- macro-F1 >= best_baseline_macroF1 + 0.15
- AND macro-F1 >= 0.80

Otherwise FAIL.

---

## 7) Prohibitions

- No edits to holdout list after predictions are saved
- No edits to predictions after lock
- No threshold tweaking
- No selective reporting

---
