# PROJECT 11 — PHASE E SYNTHESIS V1
## Structure vs Resolution vs Adaptive Sampling

**Date:** April 2026  
**Status:** ACTIVE SYNTHESIS (Phase E)

---

## 1) Context

Phase D established:
- Hard clamp creates discontinuity artifacts.
- Soft clamp (k=15) restores smoother regime structure.
- V3.1 becomes strong and interpretable, but dense NN can still win with enough resolution.

---

## 2) Core question of Phase E

Can we use *structure* (rule-based boundary geometry) to reduce the number of labeled reference points needed for NN-style performance?

---

## 3) Phase E1 result (Adaptive NN)

Adaptive reference set:
- 2000 points (1000 uniform + 1000 boundary-focused)
- boundary-focused selection uses V3 boundary score only (no ground truth used for selection)
- labels come from the soft-clamp ground truth

Outcome:
- NN_adaptive_2000 beats NN41 overall and improves boundary performance relative to NN41.
- NN81 still wins overall and on boundary, but at much higher reference cost.

This yields a clean tradeoff:
- V3.1: interpretable structure
- NN81: brute-force resolution
- NN_adaptive: structure-guided sample efficiency

---

## 4) Next step

Phase E2:
- sample-efficiency curve:
  - N ∈ {250, 500, 1000, 1500, 2000}
  - multiple seeds
- ablation:
  - uniform-only vs boundary-only vs mixed

Goal:
- quantify how much boundary-focused sampling buys per added reference point.

---
