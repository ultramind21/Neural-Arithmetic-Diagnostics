# P11_VALIDATION_REPORT_REVALIDATE.md

## Summary
Re-validation of Project 11 claims using independent holdout, pool, and seeds.

---
## Claim P11-C01: Soft clamp performance

**Observed:**
- V3.1 macroF1_present: 0.973221
- V3 macroF1_present: 0.918356
- Gap (V3.1 − V3): 0.054865

**Targets:**
- V3.1 ≥ 0.93: ✅ PASS
- Gap ≥ 0.07: ❌ FAIL

**Status:** ❌ FAIL

---
## Claim P11-C02: NN resolution monotonicity

**Observed:**
- NN11 macroF1_present: 0.920207
- NN21 macroF1_present: 0.960246
- NN41 macroF1_present: 0.987390
- NN81 macroF1_present: 0.986811

**Targets:**
- NN81 ≥ 0.97: ✅ PASS
- Monotonicity (11→21→41→81): ❌ FAIL

**Status:** ❌ FAIL

---
## Claim P11-C03: Boundary-only poor, mixed necessary

**Observed (N=1000, mean over seeds):**
- Boundary-only: 0.531690 (n=3 seeds)
- Uniform: 0.963733
- Mixed: 0.965109
- Gap (mixed − boundary): 0.433419

**Targets:**
- Boundary ≤ 0.8: ✅ PASS
- Mixed ≥ 0.97: ❌ FAIL
- Uniform ≥ 0.94: ✅ PASS
- Gap ≥ 0.15: ✅ PASS

**Status:** ❌ FAIL

---
## Claim P11-C04: Mixed sampling efficiency (flagship)

**Observed:**
- Mixed @ N=1000: 0.965109
- NN81 baseline: 0.986811
- Performance gap: 0.021702
- Cost ratio (1000/6561): 0.1524

**Targets:**
- Mixed ≥ 0.97: ❌ FAIL
- NN81 ≥ 0.97: ✅ PASS
- Gap ≤ 0.02: ❌ FAIL
- Cost ratio ≤ 0.2: ✅ PASS

**Status:** ❌ FAIL

---
## Claim P11-C05: kNN with balanced frac competitive

**Observed:**
- Best config (N=1500, frac=0.5, k=1): 0.963732
- Same config 3-NN: 0.950318
- kNN gap (1-NN − 3-NN): 0.013414
- Frac performance @ N=1500 (1-NN):
  - frac=0.2: 0.940664
  - frac=0.5: 0.963732
  - frac=0.8: 0.972477

**Targets:**
- Best config ≥ 0.97: ❌ FAIL
- kNN gap ≥ 0.005: ✅ PASS
- All fracs within 0.01 of best: ❌ FAIL

**Status:** ❌ FAIL

---
## Summary Table

| Claim | Type | Status |
|-------|------|--------|
| P11-C01 | strong/medium | ❌ FAIL |
| P11-C02 | strong/medium | ❌ FAIL |
| P11-C03 | strong/medium | ❌ FAIL |
| P11-C04 | strong/medium | ❌ FAIL |
| P11-C05 | strong/medium | ❌ FAIL |

**Report generated:** Sprint 2C re-validation completion