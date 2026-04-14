# PROJECT 11 — PHASE E1
## Adaptive NN via Boundary-Focused Sampling (Soft-Clamp labels)

**Date:** April 2026  
**Status:** DRAFT → LOCKED after reference generation (SHA256)  
**Test:** phase_e1_adaptive_nn

---

## 0) Purpose

Phase D showed a clean tradeoff:
- V3.1 provides interpretable global structure and strong boundary behavior.
- NN improves with resolution, but cost scales with grid points (e.g., 81×81 = 6561 points).

Phase E1 tests whether we can get NN-like performance with far fewer points by sampling:
- uniform points for coverage
- boundary-focused points using Rule V3 internal boundary score (NO ground-truth used for selection)

---

## 1) Data (Locked)

- System:
  - hard: `project_11/results/transfer_t4_system.json` (families + thresholds)
  - soft: `project_11/results/phase_d_soft_clamp/system_soft_clamp.json` (k)

- Holdout (evaluation set):
  - `project_11/results/phase_c3_sat_margin/holdout_points.json` (800 points, seed=223311)

Ground truth for evaluation:
- computed with softplus-based soft clamp (same as Phase D audit recompute)

---

## 2) Reference set generation (LOCKED)

Output folder:
- `project_11/results/phase_e1_adaptive_nn/`

Reference points file:
- `reference_points.json` (contains H,P,kind)

Generation parameters (LOCKED):
- seed = 551122
- pool_size = 50000 (for boundary candidates)
- n_uniform = 1000
- n_boundary = 1000
- total = 2000

Boundary selection:
- score points by V3 boundary score (smaller = closer to V3 thresholds)
- select the top n_boundary unique points not overlapping uniform set

Lock:
- generator prints SHA256 of reference_points.json

---

## 3) Predictors evaluated

- V3.1 (same as Phase D)
- NN-adaptive (reference set size = 2000)
- NN41 grid (1681) and NN81 grid (6561) for comparison

---

## 4) Outputs

- `reference_points.json` (generated + SHA256 printed)
- `report.md`
- `artifact.json`

---
