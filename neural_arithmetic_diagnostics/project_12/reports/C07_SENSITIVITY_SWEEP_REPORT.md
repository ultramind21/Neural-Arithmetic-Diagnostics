# C07 Boundary Sensitivity Sweep Report

**Experiment ID:** p12_c07_sensitivity_sweep_v1
**Seeds tested:** 20 seeds (100001–100020)
**Successful runs:** 20/20

## Results Summary

### V3.1 Boundary macroF1_present Distribution

| Statistic | Value |
|-----------|-------|
| Mean | 0.869306 |
| Std Dev | 0.000000 |
| Min | 0.869306 |
| 5th percentile | 0.869306 |
| Median (50th) | 0.869306 |
| 95th percentile | 0.869306 |
| Max | 0.869306 |

### Pass Rate vs Thresholds

| Threshold | Pass Rate | Count |
|-----------|-----------|-------|
| ≥ 0.80 | 100.0% | 20/20 |
| ≥ 0.85 | 100.0% | 20/20 |
| ≥ 0.90 | 0.0% | 0/20 |

### Mechanism Conditions

**Improvement (V3.1 − V3) ≥ 0.15:**
- Mean: 0.200817
- All seeds pass: ✅ YES

**Closeness to NN81 (NN81 − V3.1) ≤ 0.10:**
- Mean gap: 0.059771
- All seeds pass: ✅ YES

## Interpretation (for C07 Revision)

1. **Absolute threshold 0.85:** Only 100.0% of seeds pass
2. **Absolute threshold 0.80:** 100.0% of seeds pass
3. **Mechanism conditions:** Improvement and NN81-closeness are ROBUST

## Recommendation

✅ **Mechanism is robust:** Soft clamp reliably improves boundary and stays near NN81.

**Option A (Mechanism-based revision):** Remove absolute threshold 0.85; keep only:
- (V3.1_boundary − V3_boundary) ≥ 0.15
- (NN81_boundary − V3.1_boundary) ≤ 0.10

**Option B (Data-driven threshold):** Propose new absolute target based on percentiles:
- P50 = 0.8693 (median)
- P5 = 0.8693 (conservative lower bound)

## Artifacts
- Per-seed metrics (CSV): `project_12/results/sweep_c07_v1/summary/per_seed_metrics.csv`
- Statistics (JSON): `project_12/results/sweep_c07_v1/summary/statistics.json`
- Phase D artifacts: `project_12/results/sweep_c07_v1/phase_d/seed_*/`