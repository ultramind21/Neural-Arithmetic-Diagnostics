# PROJECT 11 — PHASE E2 VERDICT
## Sample-Efficiency Curve + Ablations (Soft labels)

**Date:** April 2026  
**Status:** CLOSED — SUCCESS (clear curve + ablation outcome)  
**Test:** phase_e2_sample_efficiency

---

## 1) What was tested

NN performance vs reference-set size and strategy under soft-clamp labels.

- N ∈ {250, 500, 1000, 1500, 2000}
- strategies: uniform-only, boundary-only, mixed (50/50)
- seeds: {101, 202, 303}
- holdout: 800 points (C3 holdout)
- metric: macroF1_present

Artifacts:
- `artifact.json`
- `report.md`

---

## 2) Key results (from report.md)

Baselines:
- V3.1 macroF1 = 0.9353
- NN41 macroF1 = 0.9674
- NN81 macroF1 = 0.9847

Mean macroF1 over seeds:

- N=250:  uniform 0.8957 | boundary 0.6776 | mixed 0.9252
- N=500:  uniform 0.9150 | boundary 0.7024 | mixed 0.9388
- N=1000: uniform 0.9574 | boundary 0.7011 | mixed 0.9780
- N=1500: uniform 0.9647 | boundary 0.7133 | mixed 0.9714
- N=2000: uniform 0.9683 | boundary 0.7238 | mixed 0.9748

---

## 3) Verdict

1) Mixed (coverage + boundary) is the winning strategy across all tested sizes.
2) Boundary-only fails without coverage.
3) Mixed reaches near-dense NN performance with far fewer reference points.
   - In particular: N=1000 mixed is close to NN81 (0.9780 vs 0.9847).

Next step:
- run an analysis pass on artifact.json to inspect per-seed variance and explain the non-monotonic mean behavior at higher N.

---
