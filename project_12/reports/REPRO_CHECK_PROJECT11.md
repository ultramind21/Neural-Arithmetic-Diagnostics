# REPRO_CHECK_PROJECT11.md

## Summary
Comparison of Project 12 reproductions against Project 11 historical artifacts.

**Overall Status:** ✅ PASS

## Phase D (Resolution Sweep)
- P11 artifact: project_11\results\phase_d_soft_clamp\RESOLUTION_SWEEP_EXTENDED_ARTIFACT.json
- P12 artifact: project_12\results\repro\phase_d\RESOLUTION_SWEEP_EXTENDED_ARTIFACT.json


## Phase E2 (Sample Efficiency)
- P11 artifact: project_11\results\phase_e2_sample_efficiency\artifact.json
- P12 artifact: project_12\results\repro\phase_e2\artifact.json

- rows_match: ✅ PASS
  - OK
- metadata: ✅ PASS

## Phase E3 (Ratio + kNN)
- P11 artifact: project_11\results\phase_e3_ratio_knn\artifact.json
- P12 artifact: project_12\results\repro\phase_e3\artifact.json

- rows_match: ✅ PASS
  - OK
- metadata: ✅ PASS
  - pool_size: ✅
  - Ns: ✅
  - fracs: ✅
  - seeds: ✅

## Acceptance Criteria
- Phase D: Metrics table must match exactly (tol ≤ 1e-9)
- Phase E2/E3: Rows (main results) must match (tol ≤ 1e-9)
- Metadata: SEEDS/POOL_SIZE/etc must match exactly
- Allowed variance: `elapsed_seconds` only

**Report generated** at Sprint 2B completion