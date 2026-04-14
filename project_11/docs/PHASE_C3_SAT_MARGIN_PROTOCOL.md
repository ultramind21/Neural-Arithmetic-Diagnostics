# PROJECT 11 — PHASE C3
## Saturation-Aware Margins (Rule V3.1) vs V3-hard vs NN11 (Pre-Registered)

**Date:** April 2026  
**Status:** DRAFT → LOCKED after generation  
**Test:** phase_c3_sat_margin

---

## 0) Purpose

T4-Large postmortem showed:
- Rule V3 errors are concentrated near decision thresholds
- 100% of Rule V3 errors involve saturation/clamp in ground truth (sat_uni>0 or sat_fam>0)

Phase C3 tests a minimal structural fix:
- keep Rule V3 core
- add a saturation-risk indicator computed from system parameters
- expand decision margins under high saturation risk (be more conservative near boundaries)

This is evaluated on a NEW holdout set (seed locked).

---

## 1) System (locked)

- `project_11/results/transfer_t4_system.json`

---

## 2) Holdout (NEW, locked by generator)

Generated and saved to:
- `project_11/results/phase_c3_sat_margin/holdout_points.json`

Generation:
- seed = 223311 (LOCKED)
- N = 800 points (400 uniform, 400 boundary-focused by V3 boundary score)
- same ranges as T4-Large:
  - H in [0.001, 0.020]
  - P in [0.260, 0.420]

---

## 3) Predictors compared

A) V3-hard:
- Rule V3 as-is on (H,P)

B) V3.1 sat-margin:
Compute saturation risk on the observed (H,P):

sat_risk = count over families of:
  (base_global + P*shared_failure >= 1.0) OR (base_global + 0.30*shared_failure + 0.80*H >= 1.0)

Then apply margin expansion:
- base thresholds: +0.005 (fam), -0.003 (uni), ±0.005 (wins)
- if sat_risk >= 1:
  - use stricter fam condition: gap_est > 0.0065
  - use stricter uni condition: gap_est < -0.0045
  - and require wins margins ±0.0065 instead of ±0.005
This makes the rule "more conservative" under saturation risk.

Tie-breaking: if both conditions fail -> transition.

C) NN11:
- nearest neighbor on an 11×11 grid labeled by ground truth.

---

## 4) Ground truth

Ground truth uses the full clamped mechanics (same as previous):
- universal_score = clamp(base + P*sf)
- family_score = clamp(base + 0.30*sf + 0.80*H)
- per-family margin = 0.005
- region rules:
  - family-aware if fam_wins>=3 AND gap>0.005
  - universal if uni_wins>=2 OR gap<-0.003
  - else transition

---

## 5) Outputs

All outputs go to:
- `project_11/results/phase_c3_sat_margin/`

Files:
- `holdout_points.json` (generated)
- `report.md`
- `artifact.json`

---

## 6) Success criterion (diagnostic)

This phase is diagnostic (not a gate).
We will consider V3.1 a meaningful improvement if:
- V3.1 macro-F1 > V3-hard macro-F1 by at least +0.03
AND
- V3.1 reduces the fraction of errors with sat_risk>=1 compared to V3-hard.

---
