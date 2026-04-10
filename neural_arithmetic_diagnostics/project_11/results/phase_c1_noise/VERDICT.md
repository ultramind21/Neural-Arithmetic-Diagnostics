# PROJECT 11 — PHASE C1 VERDICT
## Noise / Measurement Robustness Sweep (Rule V3 vs NN 11×11)

**Date:** April 2026  
**Status:** CLOSED — Hypothesis Failed  
**Test:** phase_c1_noise_sweep

---

## 1) Purpose

Test whether Rule V3 becomes more robust than a dense NN baseline under measurement noise in (H,P).

---

## 2) Data (Locked)

- points: 500
- source holdout: `project_11/results/transfer_t4_large/holdout_points.json` (locked by SHA256 previously)
- system: `project_11/results/transfer_t4_system.json`

Outputs:
- report: `project_11/results/phase_c1_noise/report.md`
- artifact: `project_11/results/phase_c1_noise/artifact.json`

---

## 3) Result (from report.md)

Rule V3 is worse than NN11 at all tested noise settings:

| sigma_H | sigma_P | V3 macro-F1 | NN11 macro-F1 |
|---:|---:|---:|---:|
| 0.0000 | 0.0000 | 0.8575 | 0.9050 |
| 0.0005 | 0.0020 | 0.8003 | 0.8990 |
| 0.0010 | 0.0040 | 0.7754 | 0.8766 |
| 0.0015 | 0.0060 | 0.7592 | 0.8455 |
| 0.0020 | 0.0080 | 0.7411 | 0.8186 |

---

## 4) Verdict

❌ Hypothesis failed:

- NN11 remains stronger than Rule V3 under all tested measurement noise levels.
- Rule V3 degrades faster than NN11 as noise increases.

Next step:
- introduce uncertainty-aware decision (Phase C2) rather than hard-threshold decisions.

---
