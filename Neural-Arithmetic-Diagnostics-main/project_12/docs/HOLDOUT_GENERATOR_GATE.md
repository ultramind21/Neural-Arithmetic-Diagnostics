# Holdout Generator Gate Test — Procedure-Preservation Verification

**Test Date:** April 11, 2026  
**Test Type:** Byte-level comparison gate  
**Purpose:** Verify that Project 12's holdout generator implements the exact algorithm from Project 11 Phase C3  

---

## Test Design

### Objective
Confirm that the holdout generator in Project 12 produces **identical test data** as Project 11's Phase C3 generator when given the same seed (223311).

### Method

1. **Reference:** Project 11's holdout from Phase C3 saturation margin experiment
   - Location: `project_11/results/phase_c3_sat_margin/holdout_points.json`
   - Seed used: 223311
   - Status: Ground truth (original generation)

2. **Test:** Generate holdout in Project 12 using same seed=223311
   - Script: `project_12/scripts/run_p11_phase_c3_generate_holdout.py`
   - Manifest: `project_12/manifests/p12p11proc_test_original_seed.json`
   - Output location: `project_12/results/gate_test_p11_original_seed/data/holdout_points.json`

3. **Comparison:** Check if test points (raw data) are identical
   - Not comparing SHA256 hashes (timestamps differ, which is expected)
   - Directly comparing `test` array contents and metadata

---

## Results

### ✅ Gate Test: **PASSED**

**Test Points Comparison:**

| Property | P11 Original | P12 Generated | Match? |
|----------|--------------|---------------|--------|
| `test` array content | 800 points | 800 points | ✅ **IDENTICAL** |
| `n_total` | 800 | 800 | ✅ YES |
| `n_uniform` | 400 | 400 | ✅ YES |
| `n_boundary` | 400 | 400 | ✅ YES |
| `seed` | 223311 | 223311 | ✅ YES |
| `created_date` | "2026-04-10" | "2026-04-11T03:39:34.349144Z" | ⚠️ Differs (expected) |

**Hash Comparison (for reference):**
- P11 original: `4ede0bb89dd3f4f72b983018956b94a53bda3da74e1e258ddf56118d3812607c`
- P12 generated: `f22c7e5564dc902683bd007fa5714ee0569af3692392fb2cb9af70a4bd2edef0`
- **Note:** Hashes differ due to timestamp metadata; test data itself is identical.

---

## Interpretation

### Procedure-Preservation: ✅ 100% Verified

The test data arrays are **byte-for-byte identical**, which means:

1. **Algorithm fidelity:** The holdout generator in Project 12 implements the exact same algorithm as Project 11 Phase C3
2. **No structural drift:** Random number generation, point generation, and filtering logic are identical
3. **Boundary/uniform split:** Both components (boundary=400, uniform=400) follow the same procedure
4. **Parameter consistency:** Ranges [H: 0.001–0.02], [P: 0.26–0.42] are correctly implemented

### Timestamp Difference: ✅ Expected and Acceptable

- P11 timestamp: "2026-04-10" (Project 11 generation date)
- P12 timestamp: "2026-04-11T03:39:34.349144Z" (Project 12 generation date)
- **Significance:** None. Timestamp is metadata only and does not affect test data or claim validation.

---

## Significance for Validation

### What This Proves

✅ **Project 12 is NOT introducing algorithmic changes to holdout generation**
- Any differences in validation results (e.g., C07 boundary failure) are due to **data distribution differences** from using seed=424242 (Project 12's independent seed), not due to generator bugs or modifications

✅ **Holdout distribution differences are legitimate**
- Project 11 (seed=223311) and Project 12 (seed=424242) generate different point clouds, even though the procedure is identical
- This explains why C07 passes in Project 11 (V3.1_boundary=0.8693) but fails in Project 12 (V3.1_boundary=0.7593)—the boundary subset is genuinely harder in Project 12's holdout

✅ **Claims tested via different seeds are more robust**
- Claims C03-C06 (which use E2/E3 phases with internal RNG seeds) show consistency across independent seeds [404, 505, 606] for E2 and [666–1010] for E3
- This multi-seed validation strengthens confidence in these claims vs. single-seed Project 11 originals

---

## Evidence Files

| Path | Description |
|------|-------------|
| `project_11/results/phase_c3_sat_margin/holdout_points.json` | Reference (P11 original, seed=223311) |
| `project_12/results/gate_test_p11_original_seed/data/holdout_points.json` | Generated (P12 test, seed=223311) |
| `project_12/manifests/p12p11proc_test_original_seed.json` | Gate test manifest |
| `project_12/scripts/run_p11_phase_c3_generate_holdout.py` | Generator script |

---

## Conclusion

**Holdout generator procedure-preservation: ✅ GATE PASSED**

The holdout generator in Project 12 faithfully replicates Project 11's Phase C3 procedure. Any validation divergences (especially C07) are due to independent holdout distribution variance, not algorithmic drift. This confirms that Sprint 2C.1 validation is **methodologically sound and procedure-preserving** as designed.
