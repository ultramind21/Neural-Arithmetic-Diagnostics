# P11_VALIDATION_REPORT_REVALIDATE_P11PROC.md

## Summary
Procedure-Preserving Re-validation of Project 11 Claims (Sprint 2C.1 — CANONICAL)

**Key Design:**
- Holdout: Generated with Project 11 Phase C3 procedure (seed=424242)
- Pool: Internal RNG-based (Project 11 procedure, no external file)
- Seeds: Independent from Project 11
- Claims: Canonical definitions from FORMAL_CLAIMS.md (Sprint 1.6)

---
## Claim P11-C01 (Type: STRONG)
Soft clamp (k=15) restores smoother regime structure vs hard clamp.

**Observed (Phase D overall):**
- V3.1 macroF1_present: 0.939055
- V3 macroF1_present: 0.838622
- Gap (V3.1 − V3): 0.100432

**Targets:**
- V3.1 ≥ 0.93: ✅ PASS
- Gap ≥ 0.07: ✅ PASS
**Status:** ✅ PASS

---
## Claim P11-C02 (Type: MEDIUM)
Dense nearest-neighbor performance improves with resolution (monotonic, upper bound).

**Observed (Phase D overall):**
- NN11: 0.887658
- NN21: 0.940866
- NN41: 0.976043
- NN81: 0.977052

**Targets:**
- NN81 ≥ 0.97: ✅ PASS
- Monotonic (11≤21≤41≤81): ✅ PASS
**Status:** ✅ PASS

---
## Claim P11-C03 (Type: STRONG)
Boundary-only sampling is poor; global coverage (uniform + boundary mix) is necessary.

**Observed (E2 @ N=1000, mean ± std over seeds):**
- Boundary-only: 0.673921 ± 0.004519
- Uniform: 0.954000
- Mixed: 0.978698 ± 0.001713
- Gap (mixed − boundary): 0.304777

**Targets:**
- Boundary ≤ 0.80: ✅ PASS
- Mixed ≥ 0.97: ✅ PASS
- Uniform ≥ 0.94: ✅ PASS
- Gap ≥ 0.15: ✅ PASS
**Status:** ✅ PASS

---
## Claim P11-C04 (Type: STRONG)
Mixed @ N=1000 achieves near-dense performance with significantly reduced cost.

**Observed:**
- Mixed @ N=1000: 0.978698 ± 0.001713 (mean ± std)
- NN81 (dense baseline): 0.977052
- Performance gap (NN81 − mixed): -0.001646
- Cost ratio (1000/6561): 0.1524

**Targets:**
- Mixed ≥ 0.97: ✅ PASS
- NN81 ≥ 0.97: ✅ PASS
- Gap ≤ 0.02: ✅ PASS
- Cost ratio ≤ 0.20: ✅ PASS
**Status:** ✅ PASS

---
## Claim P11-C05 (Type: MEDIUM)
Uniform fraction near 0.5 is competitive; 1-NN outperforms 3-NN.

**Observed (mean ± std over seeds):**
- Best config (N=1500, frac=0.5, 1-NN): 0.975567 ± 0.004044
- Same config 3-NN: 0.970458
- kNN gap (1-NN − 3-NN): 0.005109
- Frac performance at N=1500 (1-NN):
  - frac=0.2: 0.972016
  - frac=0.5: 0.975567
  - frac=0.8: 0.974756

**Targets:**
- Best config ≥ 0.97: ✅ PASS
- kNN gap ≥ 0.005: ✅ PASS
- frac=0.5 within 0.01 of best: ✅ PASS
**Status:** ✅ PASS

---
## Claim P11-C06 (Type: WEAK)
Diminishing returns: increasing N beyond 1000 shows marginal gain.

**Observed (E2 mixed strategy, mean over seeds):**
- Mixed @ N=1000: 0.978698
- Mixed @ N=1500: 0.980924
- Mixed @ N=2000: 0.977267
- max(N=1500, N=2000) − N=1000: 0.002227

**Targets:**
- Mixed @ N=1000 ≥ 0.96: ✅ PASS
- Improvement ≤ 0.02: ✅ PASS
**Status:** ✅ PASS

---
## Claim P11-C07 (Type: STRONG)
Soft clamp significantly improves boundary performance; V3.1 achieves near-competitive.

**Observed (Phase D boundary subset):**
- V3.1 boundary macroF1_present: 0.759266
- V3 boundary macroF1_present: 0.597485
- NN81 boundary macroF1_present: 0.757786
- Gap (V3.1 − V3): 0.161781
- Gap (NN81 − V3.1): -0.001480

**Targets:**
- V3.1 boundary ≥ 0.85: ❌ FAIL
- (V3.1 − V3) boundary ≥ 0.15: ✅ PASS
- (NN81 − V3.1) boundary ≤ 0.10: ✅ PASS
**Status:** ❌ FAIL

---
## Claim P11-C08 (Type: WEAK)
Reference set retrieval is efficient; pool-based design supports no leakage.

**Observed:**
- NN81 build_seconds: 0.052270
- Leakage check (holdout ∩ reference): ✅ PASS (by internal design)

**Targets:**
- Build time < 0.10s: ✅ PASS
- Leakage assertion: ✅ PASS (by design)
**Status:** ✅ PASS

---
## Summary Table

| Claim | Type | Status |
|-------|------|--------|
| P11-C01 | STRONG | ✅ PASS |
| P11-C02 | MEDIUM | ✅ PASS |
| P11-C03 | STRONG | ✅ PASS |
| P11-C04 | STRONG | ✅ PASS |
| P11-C05 | MEDIUM | ✅ PASS |
| P11-C06 | WEAK | ✅ PASS |
| P11-C07 | STRONG | ❌ FAIL |
| P11-C08 | WEAK | ✅ PASS |

**Total: 7/8 PASS**
