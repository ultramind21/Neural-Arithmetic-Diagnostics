# PROJECT 11 — PHASE C3 VERDICT
## Saturation-Aware Margins (V3.1)

**Date:** April 2026  
**Status:** CLOSED — PARTIAL (mixed outcome)  
**Test:** phase_c3_sat_margin

---

## 1) Lock

- seed: 223311
- holdout sha256:
  4ede0bb89dd3f4f72b983018956b94a53bda3da74e1e258ddf56118d3812607c

Artifacts:
- `holdout_points.json`
- `artifact.json`
- `report.md`

---

## 2) Main result (from report.md)

Overall (800 points):
- V3-hard macro-F1: 0.8771
- V3.1 sat-margin macro-F1: 0.8893  (Δ = +0.0122)
- NN11 macro-F1: 0.9162

Boundary subset (400 points):
- V3: 0.8280
- V3.1: 0.7755  (degraded)

Saturation-linked errors:
- V3 errors: 109 (109 with sat_risk>=1)
- V3.1 errors: 90 (90 with sat_risk>=1)

---

## 3) Verdict

- ✅ V3.1 reduced total errors and reduced sat-linked errors.
- ❌ V3.1 did not meet the +0.03 macro-F1 improvement target.
- ❌ V3.1 harmed boundary performance.

Interpretation:
- sat_risk>=1 triggers too often (737/800), so the expanded margins dilute boundary discrimination.
- clamp/saturation remains the core driver; margin-expansion alone is insufficient.

Next step:
- mechanism-level fix (soft clamp / homeostasis) rather than only threshold tweaking.

---
