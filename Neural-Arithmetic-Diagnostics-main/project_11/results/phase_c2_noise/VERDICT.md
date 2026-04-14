# PROJECT 11 — PHASE C2 VERDICT
## Noise-aware Decision (V3-MC) vs NN11

**Date:** April 2026  
**Status:** CLOSED — No meaningful improvement  
**Test:** phase_c2_noise_aware_v3_mc

---

## 1) Purpose

Phase C2 tested whether a noise-aware decision (Monte-Carlo vote around observed inputs) improves Rule V3 under measurement noise.

---

## 2) Result (from report.md)

MC voting did not materially improve V3:

- V3-MC ≈ V3-hard across all noise settings
- NN11 remained superior at all noise levels

Conclusion:
- uncertainty voting alone does not address the structural error source (clamp/saturation boundary behavior).

Artifacts:
- `project_11/results/phase_c2_noise/artifact.json`
- `project_11/results/phase_c2_noise/report.md`

---
