# PROJECT 11 — PHASE C1
## Noise / Measurement Robustness Sweep (Rule V3 vs NN 11×11)

**Date:** April 2026  
**Status:** DRAFT → LOCKED when run is executed  
**Test:** phase_c1_noise_sweep

---

## 0) Purpose

T4-Large showed Rule V3 loses to a dense NN baseline in clean (H,P) space, especially near boundaries,
and postmortem indicates errors are tightly associated with clamp/saturation.

Phase C1 tests a different question:

> Under measurement noise in (H,P), does Rule V3 become more robust than NN?

This is a geometry-break / identifiability stress test.

---

## 1) Data Source (Locked)

We reuse the LOCKED T4-Large holdout points (true underlying H,P):
- `project_11/results/transfer_t4_large/holdout_points.json`

We do NOT edit it.

Ground truth labels are computed from the T4 system mechanics:
- `project_11/results/transfer_t4_system.json`

---

## 2) Predictors compared

### A) Rule V3 predictor
Uses system shared_failure values and computes deltas:
- delta_i_est = 0.80*H_obs + (0.30 - P_obs)*sf_i
Then predicts region using the Rule V3 logic.

### B) NN baseline (11×11 grid)
Build 11×11 grid over the same ranges:
- H in [0.001, 0.020] (11 points)
- P in [0.260, 0.420] (11 points)
Label each grid point by ground truth.
Then predict by nearest neighbor using (H_obs, P_obs).

---

## 3) Noise model (measurement noise)

We generate observed inputs:
- H_obs = clip(H_true + Normal(0, sigma_H), [H_min, H_max])
- P_obs = clip(P_true + Normal(0, sigma_P), [P_min, P_max])

Ground truth remains tied to (H_true, P_true), not noisy values.

---

## 4) Sweep settings (pre-registered)

We evaluate these noise levels:

- (sigma_H, sigma_P) in:
  - (0.0000, 0.0000)
  - (0.0005, 0.0020)
  - (0.0010, 0.0040)
  - (0.0015, 0.0060)
  - (0.0020, 0.0080)

Replicates:
- 20 independent noise seeds per setting.

---

## 5) Outputs (single clear folder)

All outputs go to:
- `project_11/results/phase_c1_noise/`

Files:
- `artifact.json`
- `report.md`

---

## 6) Decision rule

This phase is diagnostic (not a gate).
We report robustness profiles and whether Rule V3 overtakes NN as noise increases.

---
