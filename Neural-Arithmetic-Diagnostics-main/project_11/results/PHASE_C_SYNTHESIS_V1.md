# PROJECT 11 — PHASE C SYNTHESIS V1
## Geometry-break + Boundary Failure Analysis

**Date:** April 2026  
**Status:** ACTIVE SYNTHESIS (Phase C)

---

## 1) Starting point (from Phase B)

T4-Large (Rule V3) failed vs NN11:
- V3 macro-F1: 0.8575
- NN11 macro-F1: 0.9050

Postmortem finding:
- 80/80 V3 errors involved saturation/clamp (sat_uni>0 or sat_fam>0).

This established clamp/saturation as the dominant failure correlate.

---

## 2) Phase C1 (Noise sweep) — FAILED hypothesis

Hypothesis:
- Rule V3 becomes more robust than NN11 under measurement noise.

Result:
- NN11 remained stronger at all noise levels.

Artifacts:
- `project_11/results/phase_c1_noise/*`

---

## 3) Phase C2 (Noise-aware V3-MC) — FAILED hypothesis

Hypothesis:
- Monte-Carlo vote around (H_obs,P_obs) improves V3 under noise.

Result:
- V3-MC ≈ V3-hard (negligible change)
- NN11 remained stronger.

Artifacts:
- `project_11/results/phase_c2_noise/*`

---

## 4) Phase C3 (V3.1 saturation-aware margins) — PARTIAL

Goal:
- reduce saturation-linked errors without destroying boundary discrimination.

Result (800-point new holdout):
- overall macro-F1 improved slightly (Δ +0.0122)
- sat-linked errors reduced (109 → 90)
- boundary macro-F1 degraded significantly (0.8280 → 0.7755)

Interpretation:
- saturation awareness matters
- but broad margin expansion is too blunt; clamp remains the deeper issue.

Artifacts:
- `project_11/results/phase_c3_sat_margin/*`

---

## 5) Conclusion of Phase C

- Dense NN interpolation dominates in this (H,P) setup, including under the tested noise model.
- Clamp/saturation introduces a piecewise/distorting effect that compact rules struggle to approximate near boundaries.
- Small "threshold tricks" help a bit but can harm boundary discrimination.

Next phase:
- Phase D: mechanism-level change (soft clamp / homeostasis-style feedback) to test whether smoother saturation removes the dominant error mode.

---
