# PROJECT 11 — PHASE A2 (TRANSFER)
## Transfer Test T2 (Stress Transfer, Pre-Registered)

**Date:** April 2026  
**Status:** DRAFT → LOCKED after predictions are saved  
**Test:** transfer_t2

---

## 0) Purpose

Stress-test whether the **same V2 compressed inequality rule** transfers to a more extreme system:

- shared_failure values shift significantly
- some universal scores may clamp to 1.0 at higher P (saturation behavior)

Goal: test robustness beyond "nearby system" transfer.

---

## 1) What stays fixed

- The prediction rule stays EXACTLY the same V2 compressed rule (no tuning).
- Region labeling rule stays the same (wins + gap thresholds).
- clamp is still applied to [0,1].

---

## 2) What changes (Transfer System T2)

System parameters are locked in:
- `project_11/results/transfer_t2_system.json`

---

## 3) Holdout points (locked)

Holdout list is locked in:
- `project_11/results/transfer_t2_holdout_points.json`

---

## 4) Predictions (locked)

Predictions are locked in:
- `project_11/results/transfer_t2_predictions.json`

Predictions must match the same V2 compressed rule (rule-compliance is enforced).

---

## 5) Ground Truth for T2 (locked rule)

Using T2 system parameters:

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

Baselines use a 3x3 grid (same coordinates as Project 10, but labels come from T2 ground truth):
- H in {0.003, 0.009, 0.015}
- P in {0.30, 0.36, 0.42}

Baselines:
- majority label from the T2 3x3 grid
- nearest-neighbor on the T2 3x3 grid

---

## 7) Pass Condition (LOCKED)

Transfer T2 PASSES if:
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
