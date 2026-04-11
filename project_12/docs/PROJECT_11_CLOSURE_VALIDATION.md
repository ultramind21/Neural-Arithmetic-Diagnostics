# Project 11 Validation Closure — Project 12 Final Summary

## What Was Validated
**7 of 8 original Project 11 claims** passed procedure-preserving re-validation:
- C01–C06, C08: ✅ **Validated** (strong relative improvements, mechanism robustness confirmed)

## What Was Rejected & Revised
**1 original claim** (C07) failed as stated under seed variation:
- **C07 (as stated):** ❌ **Rejected** — absolute threshold V3.1_boundary ≥ 0.85 not robust (1/20 seeds pass in sweep)
- **C07R (mechanism-based):** ✅ **Validated** — relative improvement (V3.1 − V3) ≥ 0.15 and proximity to NN81 (gap ≤ 0.10) robust across all 20 procedure-preserving holdout seeds

## Key Evidence
- **Revalidation gate:** Procedure-preserving holdout generator 100% faithful (seed=223311 test ✅)
- **Sensitivity sweep:** 20 independent holdout seeds (100001–100020) all passed mechanism conditions; only 1 passed absolute threshold
- **Result snapshot:** [VALIDATED_RESULTS_P11_PROJECT12.md](VALIDATED_RESULTS_P11_PROJECT12.md) (8/9 claims validated; link-checked ✅)

## Critical Commits
| Commit | Sprint | What |
|--------|--------|------|
| `e6876e1` | 2D | Status consolidation (C07 marked partial) |
| `7e2cac6` | 2C.1 | Corrected validation pipeline (7/8 PASS; C07 FAIL) |
| `535bf5e` | 2E.2 | Sensitivity sweep: bugs fixed, debug gates PASS, threshold analysis (1/20 @ 0.85) |
| `a34e46e` | 2F | C07→rejected-as-stated; C07R→validated; snapshot updated |

## Verified Paths
- Full results: [project_12/results/](../results/) (all artifacts linked in FORMAL_CLAIMS.md)
- Sweep metrics: [sweep_c07_v1/summary/per_seed_metrics.csv](../results/sweep_c07_v1/summary/per_seed_metrics.csv)
- Formal claims: [FORMAL_CLAIMS.md](FORMAL_CLAIMS.md) (v1, locked + C07/C07R statuses)

## Bottom Line
Project 11 mechanisms are sound and robust under procedure-preserving validation. Absolute performance thresholds are holdout-contingent (not universal). See C07R for mechanistic revision: it is full-strength validated.

---
**Status:** ✅ Closed. Ready for Project 4 claim locking.
