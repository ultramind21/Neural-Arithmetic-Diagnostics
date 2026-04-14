# PROJECT 11 — TRANSFER T4-LARGE VERDICT (Rule V3)

**Date:** April 2026  
**Status:** CLOSED — FAIL (Predictive vs strong NN baseline)  
**Test:** transfer_t4_large_rule_v3

---

## 1) Lock hashes (authoritative)

- holdout_points.json sha256:
  8bc1d5346f38011295910ea50b68305ad3bc54acc127c8b833b582364230f011

- predictions.json sha256:
  a7c6e6d54a362a659acba65474f7a4c20b55d309aed72b13e1478bde296f9d88

Rule compliance:
- PASS (0 mismatches)

---

## 2) Results (authoritative)

- points: 500
- model accuracy: 0.8400
- model macro-F1: 0.8575
- best baseline macro-F1 (NN 11×11): 0.9050
- PASS: False

Subset performance:
- uniform: macro-F1 = 0.9011
- boundary: macro-F1 = 0.7860

---

## 3) Pass condition (locked)

PASS requires:
- macro-F1 >= best_baseline_macroF1 + 0.10
- AND macro-F1 >= 0.80

Observed:
- 0.8575 >= 0.9050 + 0.10 → FALSE
- 0.8575 >= 0.80 → TRUE

Verdict: ❌ FAIL

---

## 4) Meaning

Rule V3 remains:
- compact
- protocol-valid
- strong on uniform points

But it underperforms a dense NN baseline near decision boundaries (boundary-focused subset).

Next step:
- run post-mortem to extract exact error patterns and determine whether clamp/saturation is a dominant contributor.

---
