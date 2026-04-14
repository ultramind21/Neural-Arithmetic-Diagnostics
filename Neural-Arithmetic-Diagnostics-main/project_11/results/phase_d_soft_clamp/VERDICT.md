# PROJECT 11 — PHASE D VERDICT
## Soft-Clamp Ground Truth (Mechanism Shift)

**Date:** April 2026  
**Status:** CLOSED — STRONG SIGNAL (pending baseline-resolution audit)  
**Phase:** D

---

## 1) What changed

Mechanism shift:
- Hard clamp: clamp01(x) = min(max(x,0),1)
- Soft clamp: smooth saturation (k=15)

Evaluation reused the locked Phase C3 holdout (800 points, seed=223311).

---

## 2) Core results (evaluated vs SOFT labels)

From `report.md`:

- label shift hard→soft: 50 / 800 = 0.0625

Overall:
- V3:   macro-F1 = 0.8435
- V3.1: macro-F1 = 0.9353
- NN11: macro-F1 = 0.8770

Boundary subset:
- V3.1 macro-F1 = 0.8693
- NN11 macro-F1 = 0.5938

Conclusion (provisional):
- Under soft-clamp ground truth, V3.1 becomes the strongest of the tested predictors.

---

## 3) Required audit before claiming superiority

Because NN performance depends on grid resolution, we must run:
- NN grid sweep (11×11 vs 21×21 vs 41×41)

And we must record confusion matrices / prediction distributions, especially on the boundary subset.

Scripts:
- `project_11/experiments/phase_d_nn_grid_sweep.py`
- `project_11/experiments/phase_d_soft_clamp_postmortem.py`

---
