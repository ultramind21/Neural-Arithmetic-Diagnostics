# P11_VALIDATION_REPORT_REVALIDATE_P11PROC.md

## Summary
Procedure-Preserving Re-validation of Project 11 Claims (Sprint 2C.1)

**Key Design:**
- Holdout: Generated with Project 11 Phase C3 procedure (seed=424242)
- Pool: Internal RNG-based (Project 11 procedure, no external file)
- Seeds: Independent from Project 11
- Statistics: Mean ± Std for E2/E3 rows

---
## Claim P11-C01: Soft clamp performance

**Observed:**
- V3.1 macroF1_present: 0.939055
- V3 macroF1_present: 0.838622
- Gap (V3.1 − V3): 0.100432

**Targets:**
- V3.1 ≥ 0.93: ✅ PASS
- Gap ≥ 0.07: ✅ PASS

**Status:** ✅ PASS

---
## Claim P11-C02: NN resolution monotonicity (Type: STRONG)

**Observed:**
- NN11 macroF1_present: 0.887658
- NN21 macroF1_present: 0.940866
- NN41 macroF1_present: 0.976043
- NN81 macroF1_present: 0.977052

**Targets:**
- NN81 ≥ 0.97: ✅ PASS
- Monotonicity (11→21→41→81): ✅ PASS

**Status:** ✅ PASS

---
## Claim P11-C03: Boundary-only poor, mixed necessary (Type: STRONG)

**Observed (N=1000, mean ± std over seeds):**
- Boundary-only: 0.673921 ± 0.004519 (n=3 seeds)
- Uniform: 0.954000
- Mixed: 0.978698 ± 0.001713
- Gap (mixed − boundary): 0.304777

**Targets:**
- Boundary ≤ 0.8: ✅ PASS
- Mixed ≥ 0.97: ✅ PASS
- Uniform ≥ 0.94: ✅ PASS
- Gap ≥ 0.15: ✅ PASS

**Status:** ✅ PASS

---
## Claim P11-C04: Mixed sampling efficiency (flagship) (Type: STRONG)

**Observed:**
- Mixed @ N=1000: 0.978698 ± 0.001713
- NN81 baseline: 0.977052
- Performance gap: -0.001646
- Cost ratio (1000/6561): 0.1524

**Targets:**
- Mixed ≥ 0.97: ✅ PASS
- NN81 ≥ 0.97: ✅ PASS
- Gap ≤ 0.02: ✅ PASS
- Cost ratio ≤ 0.2: ✅ PASS

**Status:** ✅ PASS

---
## Claim P11-C05: kNN with balanced frac competitive (Type: MEDIUM)

**Observed (mean ± std over seeds):**
- Best config (N=1500, frac=0.5, k=1): 0.975567 ± 0.004044
- Same config 3-NN: 0.970458
- kNN gap (1-NN − 3-NN): 0.005109
- Frac performance @ N=1500 (1-NN):
  - frac=0.2: 0.972016
  - frac=0.5: 0.975567
  - frac=0.8: 0.974756

**Targets:**
- Best config ≥ 0.97: ✅ PASS
- kNN gap ≥ 0.005: ✅ PASS
- All fracs within 0.01 of best: ✅ PASS

**Status:** ✅ PASS

---
## Claim P11-C06: Resolution tradeoff (Type: MEDIUM)

**Observed:**
- NN11 macroF1_present: 0.887658
- NN41 macroF1_present: 0.976043
- Improvement (NN41 − NN11): 0.088386

**Targets:**
- Improvement ≥ 0.02: ✅ PASS

**Status:** ✅ PASS

---
## Claim P11-C07: Uniform sampling baseline (Type: MEDIUM)

**Observed (mean ± std over seeds):**
- Uniform @ N=1000: 0.954000 ± 0.004596

**Targets:**
- Uniform ≥ 0.94: ✅ PASS

**Status:** ✅ PASS

---
## Claim P11-C08: kNN scalability (Type: WEAK)

**Observed (N=1000 vs N=1500, frac=0.5, 1-NN):**
- N=1000: 0.973881
- N=1500: 0.975567
- Scaling gain: 0.001686

**Target:**
- Scaling ≥ 0.0: ✅ PASS

**Status:** ✅ PASS

---
## Summary Table

| Claim | Type | Status |
|-------|------|--------|
| P11-C01 | STRONG | ✅ PASS |
| P11-C02 | STRONG | ✅ PASS |
| P11-C03 | STRONG | ✅ PASS |
| P11-C04 | STRONG | ✅ PASS |
| P11-C05 | MEDIUM | ✅ PASS |
| P11-C06 | MEDIUM | ✅ PASS |
| P11-C07 | MEDIUM | ✅ PASS |
| P11-C08 | WEAK | ✅ PASS |

**Total: 8/8 PASS**
