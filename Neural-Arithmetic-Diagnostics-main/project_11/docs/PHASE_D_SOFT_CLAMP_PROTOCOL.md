# PROJECT 11 — PHASE D
## Soft-Clamp / Homeostasis Mechanism Shift (Pre-Registered)

**Date:** April 2026  
**Status:** DRAFT → LOCKED when run is executed  
**Test:** phase_d_soft_clamp

---

## 0) Purpose

Prior results show:
- Rule V3 loses to NN11 near boundaries at large scale (T4-Large).
- Postmortem: 100% of Rule V3 errors involve saturation/clamp.

Phase D tests a mechanism-level intervention:
> Replace hard clamp with soft-clamp (smooth saturation) in the ground truth scoring.

Goal:
- See if removing the piecewise information-destruction makes compact rules closer to ground truth,
  and reduces boundary failure concentration.

---

## 1) Locked inputs

System (hard-clamp system definition):
- `project_11/results/transfer_t4_system.json`

Holdout (locked, boundary-focused, large):
- `project_11/results/phase_c3_sat_margin/holdout_points.json`

Lock info:
- seed: 223311
- holdout sha256:
  4ede0bb89dd3f4f72b983018956b94a53bda3da74e1e258ddf56118d3812607c

We do NOT edit the holdout.

---

## 2) What changes

Only the clamp operator in ground truth:

### Hard clamp (baseline)
clamp01(x) = min(max(x,0),1)

### Soft clamp (mechanism shift)
soft_clamp(x;k) = softplus(kx)/k - softplus(k(x-1))/k

- For x<<0 → ~0
- For x in [0,1] → ~x (approximately identity)
- For x>>1 → ~1
- k controls sharpness.

Locked parameter:
- k = 15

---

## 3) Ground truth labeling rule (unchanged)

For each family:
- universal_score = CLAMP(base_global + P*shared_failure)
- family_aware_score = CLAMP(base_global + 0.30*shared_failure + 0.80*H)

Per-family winner threshold:
- universal if uni > fam + 0.005
- family-aware if fam > uni + 0.005
- else near_tie

Region:
- family-aware region if (fam_wins >= 3 AND gap > 0.005)
- universal region if (uni_wins >= 2 OR gap < -0.003)
- else transition region

Only CLAMP changes between hard vs soft.

---

## 4) Predictors compared (unchanged)

A) Rule V3-hard predictor (compressed deltas rule)  
B) Rule V3.1 sat-margin predictor (from Phase C3)  
C) NN11 baseline:
- build 11×11 grid over ranges:
  - H in [0.001, 0.020]
  - P in [0.260, 0.420]
- label grid using SOFT ground truth
- predict by nearest neighbor (H,P)

---

## 5) Outputs (single clear folder)

All Phase D outputs go to:
- `project_11/results/phase_d_soft_clamp/`

Files:
- `system_soft_clamp.json` (k + definition)
- `report.md`
- `artifact.json`

---

## 6) Key diagnostics to report

- label-shift rate: fraction of points whose label changes from hard→soft ground truth
- macro-F1 for V3, V3.1, NN11 under SOFT labels
- subset performance: uniform vs boundary (from holdout kind)

---
