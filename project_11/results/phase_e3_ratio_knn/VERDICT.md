# PROJECT 11 — PHASE E3 VERDICT
## Ratio Sweep + kNN Smoothing (Soft labels)

**Date:** April 2026  
**Status:** CLOSED — SUCCESS (ratio insight + kNN conclusion)  
**Test:** phase_e3_ratio_knn

---

## 1) What was tested

- N ∈ {1000, 1500}
- uniform_frac ∈ {0.2, 0.5, 0.8}
- seeds ∈ {111, 222, 333, 444, 555}
- compare 1-NN vs 3-NN on the same reference sets
- evaluate on the fixed 800-point holdout (C3 holdout)
- metric: macroF1_present
- ground truth: soft-clamp labels (k=15)

Artifacts:
- `artifact.json`
- `report.md`

---

## 2) Key results (mean over seeds, macroF1_present)

From report.md:

### 1-NN
- N=1000:
  - frac=0.2 → 0.9494
  - frac=0.5 → 0.9682
  - frac=0.8 → 0.9666
- N=1500:
  - frac=0.2 → 0.9663
  - frac=0.5 → 0.9747  (best)
  - frac=0.8 → 0.9722

### 3-NN
- consistently lower than 1-NN across conditions
- prefers higher uniform fractions (0.8) but still underperforms 1-NN

Baselines (for context):
- V3.1: 0.9353
- NN41: 0.9674
- NN81: 0.9847

---

## 3) Verdict (interpretation)

1) Best operating point found:
- **1-NN, N=1500, uniform_frac=0.5 → 0.9747**

2) Coverage is necessary:
- frac=0.2 (boundary-heavy) underperforms consistently vs 0.5/0.8.

3) kNN smoothing did NOT help:
- 3-NN reduces performance (likely blurs sharp transitions).

4) Clarification:
- The best 1-NN setting (0.9747) closes most of the gap to NN81 (0.9847) with far fewer reference points, but does not exceed NN81.

---
