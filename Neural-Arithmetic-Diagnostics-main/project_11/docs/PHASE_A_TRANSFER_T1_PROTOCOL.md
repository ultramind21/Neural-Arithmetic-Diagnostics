# PROJECT 11 — PHASE A1 (TRANSFER)
## Transfer Test T1 (Pre-Registered)

**Date:** April 2026  
**Status:** DRAFT → LOCKED after predictions are saved  
**Test:** transfer_t1

---

## 0) Purpose

Test whether the **V2 compressed inequality rule** (derived from Project 10 structure) transfers to a **modified system** where family shared_failure values are different.

This is a transfer test against "system-specific fitting".

---

## 1) What stays fixed

- H := residual_abs (heterogeneity magnitude)
- P := universal_power
- Same region labeling rule structure (wins + gap thresholds)
- Same clamp to [0,1]

Predictions are still generated from the **same V2 compressed rule** (no tuning).

---

## 2) What changes (Transfer System T1)

Families are changed (shared_failure distribution changes).

System is locked in:
- `project_11/results/transfer_t1_system.json`

---

## 3) Holdout points (locked)

Holdout list is locked in:
- `project_11/results/transfer_t1_holdout_points.json`

---

## 4) Predictions (locked)

Predictions are locked in:
- `project_11/results/transfer_t1_predictions.json`

Predictions must match the same V2 compressed rule (rule-compliance is enforced).

---

## 5) Ground Truth for T1 (locked rule)

Using T1 system parameters:

For each family:
- universal_score = clamp(base_global + P * shared_failure)
- family_aware_score = clamp(base_global + 0.30*shared_failure + 0.80*H)

Per-family winner threshold:
- universal if uni > fam + 0.005
- family_aware if fam > uni + 0.005
- else near_tie

Region label:
- family-aware region if (fam_wins >= 3 AND gap > 0.005)
- universal region if (uni_wins >= 2 OR gap < -0.003)
- else transition region

---

## 6) Baselines (required)

Baselines use a 3x3 grid (same coordinates as Project 10, but labels come from T1 ground truth):
- H in {0.003, 0.009, 0.015}
- P in {0.30, 0.36, 0.42}

Baselines:
- majority label from the T1 3x3 grid
- nearest-neighbor on the T1 3x3 grid

---

## 7) Pass Condition (LOCKED)

Transfer T1 PASSES if:
- macro-F1 >= best_baseline_macroF1 + 0.10
- AND macro-F1 >= 0.70

Otherwise FAIL.

---

## 8) Prohibitions

- No edits to holdout after predictions are saved
- No edits to predictions after lock
- No parameter tuning after results
- No selective reporting

---
