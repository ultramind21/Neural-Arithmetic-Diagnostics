# PROJECT 11 — PHASE B2 (TRANSFER)
## Transfer Test T4 (Clamp + Extreme sf Stress) using Rule V3 (Pre-Registered)

**Date:** April 2026  
**Status:** DRAFT → LOCKED after predictions are saved  
**Test:** transfer_t4_rule_v3

---

## 0) Purpose

Transfer T2 failed under stress for Rule V2. Rule V3 fixed T3.

T4 is a NEW stress system designed to test:
- extreme shared_failure distribution effects (top-2 vs bottom-2)
- clamp/saturation sensitivity in ground truth (since base_global is high for some families)

Rule V3 predictions:
- use shared_failure distribution
- do NOT use base_global
- do NOT use clamp in prediction

Ground truth evaluation:
- uses base_global + clamp exactly (as always)

---

## 1) Rule V3 (LOCKED)

Given sf_i from the system, compute:

delta_i_est(H,P) = 0.80*H + (0.30 - P) * sf_i

Then:
- fam_wins_est = count(delta_i_est > 0.005)
- uni_wins_est = count(delta_i_est < -0.005)
- gap_est = mean(delta_i_est)

Predict:
- family-aware region if (fam_wins_est >= 3 AND gap_est > 0.005)
- universal region if (uni_wins_est >= 2 OR gap_est < -0.003)
- else transition region

Predictions must match Rule V3 exactly (rule-compliance enforced).

---

## 2) System + Holdout + Predictions (locked)

- System: `project_11/results/transfer_t4_system.json`
- Holdout: `project_11/results/transfer_t4_holdout_points.json`
- Predictions: `project_11/results/transfer_t4_predictions.json`

---

## 3) Ground Truth (for evaluation; uses clamp)

For each family:
- universal_score = clamp(base_global + P * shared_failure)
- family_aware_score = clamp(base_global + 0.30*shared_failure + 0.80*H)

Per-family winner:
- universal if uni > fam + 0.005
- family_aware if fam > uni + 0.005
- else near_tie

Region:
- family-aware region if (fam_wins >= 3 AND gap > 0.005)
- universal region if (uni_wins >= 2 OR gap < -0.003)
- else transition region

---

## 4) Baselines (required)

Baselines use a 3x3 grid (same coordinates as Project 10; labels from T4 ground truth):
- H in {0.003, 0.009, 0.015}
- P in {0.30, 0.36, 0.42}

Baselines:
- majority label from the T4 3x3 grid
- nearest-neighbor on the T4 3x3 grid

---

## 5) Pass Condition (LOCKED)

PASS if:
- macro-F1 >= best_baseline_macroF1 + 0.10
- AND macro-F1 >= 0.70

Otherwise FAIL.

---

## 6) Prohibitions

- No edits after lock
- No tuning after results
- No selective reporting

---
