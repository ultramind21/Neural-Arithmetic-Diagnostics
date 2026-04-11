# PROJECT 11 — PHASE E1 VERDICT
## Adaptive NN via Boundary-Focused Sampling (Soft-Clamp labels)

**Date:** April 2026  
**Status:** CLOSED — SUCCESS (clear tradeoff demonstrated)  
**Test:** phase_e1_adaptive_nn

---

## 1) Reference set lock (authoritative)

Generator:
- seed: 551122
- points: 2000 (uniform=1000, boundary=1000)
- reference sha256:
  a93c355d6720163f01d6db216da9e8d80cae9ac8e60597b3ca2f522223c25be5

File:
- `reference_points.json`

---

## 2) Evaluation setup

- Holdout: 800 points (from C3 holdout)
- Soft-clamp labels (k=15)
- Metric reported: macro_f1_present

---

## 3) Results (from report.md)

Overall macro-F1:
- V3.1: 0.9353
- NN_adaptive_2000: 0.9752
- NN41 (1681 grid pts): 0.9674
- NN81 (6561 grid pts): 0.9847

Boundary macro-F1:
- V3.1: 0.8693
- NN_adaptive_2000: 0.9053
- NN41: 0.8625
- NN81: 0.9291

---

## 4) Verdict meaning

Adaptive NN (2000 pts) substantially closes the gap to dense NN81 while using far fewer reference points, and beats NN41.

This demonstrates a publishable axis:
- global structure (V3 boundary score) can guide sampling,
- producing near-high-resolution performance at reduced sampling cost.

---
