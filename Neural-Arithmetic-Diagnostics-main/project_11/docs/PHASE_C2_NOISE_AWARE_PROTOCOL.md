# PROJECT 11 — PHASE C2
## Noise-aware Decision (V3-MC) vs NN11 (Pre-Registered)

**Date:** April 2026  
**Status:** DRAFT → LOCKED when run is executed  
**Test:** phase_c2_noise_aware_v3_mc

---

## 0) Purpose

Phase C1 showed Rule V3 loses to NN11 under measurement noise.

Phase C2 tests a targeted fix:

> Use a noise-aware decision rule: Monte-Carlo smoothing around the observed (H_obs, P_obs).

This is not a change to ground truth; it is a change to the decision process under noisy measurements.

---

## 1) Data (Locked)

Same locked holdout points (true H,P):
- `project_11/results/transfer_t4_large/holdout_points.json`

Same system mechanics:
- `project_11/results/transfer_t4_system.json`

---

## 2) Predictors compared

A) V3-hard:
- apply Rule V3 once at (H_obs,P_obs)

B) V3-MC (noise-aware):
- for each observed point, sample K perturbed points around (H_obs,P_obs)
- apply Rule V3 to each sampled point
- output the majority-vote label (ties -> transition)

C) NN11:
- nearest-neighbor label from 11×11 grid using (H_obs,P_obs)

---

## 3) Noise sweep settings (same as C1)

Noise model:
- H_obs = clip(H_true + Normal(0, sigma_H), [H_min,H_max])
- P_obs = clip(P_true + Normal(0, sigma_P), [P_min,P_max])

Settings:
- (0.0000, 0.0000)
- (0.0005, 0.0020)
- (0.0010, 0.0040)
- (0.0015, 0.0060)
- (0.0020, 0.0080)

Replicates:
- 20 seeds per setting.

Monte-Carlo parameter:
- K = 25 samples per point (LOCKED)

---

## 4) Outputs (single clear folder)

- `project_11/results/phase_c2_noise/`
  - `artifact.json`
  - `report.md`

---
