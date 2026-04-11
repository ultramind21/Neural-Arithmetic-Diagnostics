# PROJECT 11 — PHASE E3
## Mixed Ratio Sweep + kNN Smoothing (Soft labels)

**Date:** April 2026  
**Status:** DRAFT → LOCKED on execution  
**Test:** phase_e3_ratio_knn

---

## 0) Purpose

Phase E2 showed:
- mixed (uniform + boundary) dominates
- mixed curve is slightly non-monotonic (peaks at N=1000)

E3 tests two hypotheses:
1) The best mix ratio may not be exactly 50/50.
2) 1-NN may be overly sensitive; 3-NN smoothing may reduce boundary jaggedness and restore monotonic behavior.

---

## 1) Fixed components

- Holdout: `project_11/results/phase_c3_sat_margin/holdout_points.json` (800 pts)
- System hard: `project_11/results/transfer_t4_system.json`
- Soft clamp k: `project_11/results/phase_d_soft_clamp/system_soft_clamp.json`
- Ground truth labels: softplus-based soft clamp (same as Phase E1/E2)

---

## 2) Sweep grid (LOCKED)

N ∈ {1000, 1500}  
uniform_fraction ∈ {0.2, 0.5, 0.8}  
Seeds ∈ {111, 222, 333, 444, 555}

For each (seed, N, uniform_fraction):
- Build mixed reference set:
  - n_uniform = round(N * uniform_fraction)
  - n_boundary = N - n_uniform
- boundary candidates selected from a fixed pool (pool_size=60000) scored by V3 boundary score

Predictors evaluated:
- 1-NN on the mixed reference set
- 3-NN (majority vote) on the same reference set

Baselines for context (computed once):
- V3.1
- NN41
- NN81

---

## 3) Outputs

Folder:
- `project_11/results/phase_e3_ratio_knn/`

Files:
- `artifact.json`
- `report.md`

---
