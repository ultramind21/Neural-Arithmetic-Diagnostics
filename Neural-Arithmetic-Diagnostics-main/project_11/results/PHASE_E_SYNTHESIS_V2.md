# PROJECT 11 — PHASE E SYNTHESIS V2
## Structure vs Resolution vs Adaptive Sampling (Soft labels)

**Date:** April 2026  
**Status:** ACTIVE SYNTHESIS (Phase E)

---

## 1) Phase E question

Given soft-clamp ground truth (k=15), we observed:

- Rule V3.1 is strong and interpretable.
- Dense NN improves with grid resolution, but costs more reference points.

Phase E asks:
> Can structure-guided sampling approach dense NN performance with far fewer reference points?

---

## 2) Phase E1 (single adaptive reference set, N=2000)

Reference set (locked by SHA256):
- 2000 points (1000 uniform + 1000 boundary-focused)
- boundary selection uses V3 boundary score (no ground truth used for selection)

Result:
- NN_adaptive_2000 overall macroF1: 0.9752
- NN81 overall macroF1: 0.9847

Meaning:
- Adaptive sampling + labeling by ground truth yields high performance with reduced cost.

---

## 3) Phase E2 (sample-efficiency curve + ablations)

N ∈ {250,500,1000,1500,2000}, seeds {101,202,303}

Mean macroF1_present:
- uniform-only grows monotonically with N
- boundary-only fails (low performance, unstable)
- mixed dominates across all N

Peak observed:
- N=1000 mixed: 0.9780 ± 0.0038 (close to NN81)

Core lesson:
- coverage + boundary focus is the winning recipe.

---

## 4) Phase E3 (ratio sweep + kNN smoothing)

Goal:
- explain E2 behavior and test if 3-NN smoothing helps.

Results:
- Best found: **1-NN, N=1500, uniform_frac=0.5 → 0.9747**
- boundary-heavy (0.2) is consistently worse.
- 3-NN smoothing does not help (performance drops).

Interpretation:
- The best strategy is not "boundary only".
- The system benefits from structure-guided sampling while preserving global coverage.
- Simple smoothing by kNN vote is not the right knob here.

---

## 5) Paper-ready axis (what we can claim safely)

1) Hard clamp introduces discontinuity artifacts that disproportionately harm compact rules near boundaries.
2) Soft clamp restores smoother structure where interpretable rules become competitive.
3) Dense interpolation (high-resolution NN) still wins with enough reference points.
4) Structure-guided sampling (mixed coverage + boundary focus) closes most of the gap with far fewer points.

---

## 6) Next step (Phase F)

Packaging:
- convert Phase D/E results into figures + a single evidence table:
  - NN resolution curve (11/21/41/81)
  - E2 sample-efficiency curve (uniform vs mixed vs boundary)
  - E3 ratio sweep heatmap/table (N × frac, 1-NN and 3-NN)

---
