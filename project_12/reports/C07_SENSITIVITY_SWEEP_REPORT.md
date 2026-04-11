# C07 Boundary Sensitivity Sweep Report

**Experiment ID:** p12_c07_sensitivity_sweep_v1
**Seeds tested:** 20 seeds (100001–100020)
**Successful runs:** 20/20

## Results Summary

### V3.1 Boundary macroF1_present Distribution

| Statistic | Value |
|-----------|-------|
| Mean | 0.785387 |
| Std Dev | 0.035725 |
| Min | 0.687689 |
| 5th percentile | 0.741225 |
| Median (50th) | 0.785989 |
| 95th percentile | 0.831276 |
| Max | 0.855788 |

### Pass Rate vs Thresholds

| Threshold | Pass Rate | Count |
|-----------|-----------|-------|
| ≥ 0.80 | 35.0% | 7/20 |
| ≥ 0.85 | 5.0% | 1/20 |
| ≥ 0.90 | 0.0% | 0/20 |

### Mechanism Conditions

**Improvement (V3.1 − V3) ≥ 0.15:**
- Mean: 0.196597
- All seeds pass: ✅ YES

**Closeness to NN81 (NN81 − V3.1) ≤ 0.10:**
- Mean gap: 0.071924
- All seeds pass: ❌ NO

## Interpretation (for C07 Revision)

1. **Absolute threshold 0.85:** Only 5.0% of seeds pass
2. **Absolute threshold 0.80:** 35.0% of seeds pass
3. **Mechanism conditions:** Improvement and NN81-closeness are NOT ROBUST

## Recommendation

❌ **Mechanism not robust:** Conditions fail in some seeds.

## Artifacts
- Per-seed metrics (CSV): `project_12/results/sweep_c07_v1/summary/per_seed_metrics.csv`
- Statistics (JSON): `project_12/results/sweep_c07_v1/summary/statistics.json`
- Phase D artifacts: `project_12/results/sweep_c07_v1/phase_d/seed_*/`