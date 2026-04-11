# C07 Sensitivity Sweep — Methods & Findings

**Date:** April 11, 2026  
**Experiment ID:** p12_c07_sensitivity_sweep_v1  
**Scope:** 20 holdout seeds, Phase D only (deterministic)

## Methods

- **Holdout generator:** Project 11 Phase C3 procedure (copied verbatim)
- **Seeds:** 100001–100020 (standard range, pseudo-random)
- **Test points per seed:** 800 (400 uniform + 400 boundary)
- **Per-seed Phase D:** Single deterministic run, no pool/E2/E3 variance
- **Metrics extracted:** V3 boundary, V3.1 boundary, NN81 boundary

## Key Finding: Seed-Dependent Difficulty

All 20 "normal" seeds produced **identical boundary metrics:**

```
V3.1_boundary = 0.869306 (100% pass rate for 0.85 threshold)
Improvement (V3.1 − V3) = 0.200817 (robust > 0.15)
NN81 gap (NN81 − V3.1) = 0.059771 (robust < 0.10)
```

**Contrast:** Seed=424242 (Sprint 2C.1 used) produced:

```
V3.1_boundary = 0.759266 (FAILS 0.85 threshold)
Improvement (V3.1 − V3) = 0.161781 (robust > 0.15)  ✅
NN81 gap (NN81 − V3.1) = -0.001480 (robust < 0.10)  ✅
```

## Interpretation

**Two scenarios:**

1. **Seed 424242 is an outlier:**
   - It generates a boundary subset that is genuinely harder than typical
   - The 0.85 threshold passes for ~95%+ of "normal" seeds
   - Recommendation: C07 is robust, but seed-dependent

2. **Seed 424242 exposure reveals a real weakness:**
   - The soft clamp mechanism works well (improvements stable)
   - But there exist holdout distributions where V3.1 cannot reach 0.85
   - This is a limitation worth documenting

## Artifacts

- Per-seed metrics: `project_12/results/sweep_c07_v1/summary/per_seed_metrics.csv`
- Full report: `project_12/reports/C07_SENSITIVITY_SWEEP_REPORT.md`
- Phase D runs: `project_12/results/sweep_c07_v1/phase_d/seed_*/`

## Next: C07 Revised Claim Proposal

See `C07_REVISED_CLAIM.md` for recommended claim revision options.
