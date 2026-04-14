# PROJECT 11 — PHASE B (SCALE-UP)
## T4-Large (500 points, boundary-focused) using Rule V3

**Date:** April 2026  
**Status:** DRAFT → LOCKED after generation  
**Test:** transfer_t4_large_rule_v3

---

## 0) Purpose

T4 (20 points) passed, but sample size is small.

T4-Large tests statistical robustness:
- 500 holdout points
- 250 uniform
- 250 boundary-focused (based on Rule V3 internal boundary proximity, NOT ground truth)

Predictions remain strictly Rule V3.

---

## 1) System

Uses the locked T4 system:
- `project_11/results/transfer_t4_system.json`

---

## 2) Holdout + Predictions generation (locked)

Generated with a fixed seed and saved to:
- `project_11/results/transfer_t4_large_holdout_points.json`
- `project_11/results/transfer_t4_large_predictions.json`

Generator script:
- `project_11/experiments/transfer_t4_large_generate.py`

Generator must print SHA256 hashes of both files.

---

## 3) Rule compliance

Predictions must match Rule V3 exactly:
- `project_11/experiments/transfer_t4_large_rule_check.py`

---

## 4) Evaluation + Baselines (stronger)

Evaluation script:
- `project_11/experiments/transfer_t4_large_evaluate.py`

Baselines:
- Majority baseline from a denser 11×11 grid.
- Nearest-neighbor baseline on the same 11×11 grid.

(We also record the old 3×3 NN baseline for reference.)

---

## 5) Pass Condition (LOCKED)

PASS if:
- macro-F1 >= best_baseline_macroF1 + 0.10
- AND macro-F1 >= 0.80

Otherwise FAIL.

---
