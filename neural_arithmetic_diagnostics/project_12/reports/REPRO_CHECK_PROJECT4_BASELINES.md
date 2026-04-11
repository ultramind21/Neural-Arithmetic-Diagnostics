# REPRO_CHECK_PROJECT4_BASELINES — Project 12 Baseline Reproduction Report

**Purpose:** Verify that Project 12 baseline reproductions match Project 4 historical artifacts.

**Methodology:**
- Compare scorecard metrics (in-distribution accuracy, pattern accuracies, mean adversarial)
- Tolerance: 1e-6 absolute difference (quasi-deterministic evaluation)
- PASS: All metrics within tolerance
- FAIL: Any metric differs beyond tolerance

---

## MLP Baseline
**Status:** ❌ FAIL

**Metric Differences:**
  - `in_distribution_accuracy`: historical=0.06250000, p12=0.00000000, diff=6.25e-02
  - `mean_adversarial_accuracy`: historical=0.33333333, p12=0.00000000, diff=3.33e-01
  - `pattern_block_boundary_stress`: historical=1.00000000, p12=0.00000000, diff=1.00e+00

**P12 Metadata:**
- Git Hash: `6832904b76ff964bf08b38eaf15cd7bb94d842fb`
- Timestamp: 2026-04-11T06:13:44.761535+00:00
- Entrypoint: `run_p4_mlp_baseline_repro.py`
- Python Version: 3.12.0
- PyTorch Version: 2.11.0+cpu

---

## LSTM Baseline
**Status:** ❌ FAIL

**Metric Differences:**
  - `in_distribution_accuracy`: historical=0.03906250, p12=0.00000000, diff=3.91e-02

**P12 Metadata:**
- Git Hash: `6832904b76ff964bf08b38eaf15cd7bb94d842fb`
- Timestamp: 2026-04-11T06:14:15.161460+00:00
- Entrypoint: `run_p4_lstm_baseline_repro.py`
- Python Version: 3.12.0
- PyTorch Version: 2.11.0+cpu

---

## TRANSFORMER Baseline
**Status:** ❌ FAIL

**Metric Differences:**
  - `in_distribution_accuracy`: historical=0.03906250, p12=0.00000000, diff=3.91e-02
  - `mean_adversarial_accuracy`: historical=0.33333333, p12=0.00000000, diff=3.33e-01
  - `pattern_block_boundary_stress`: historical=1.00000000, p12=0.00000000, diff=1.00e+00

**P12 Metadata:**
- Git Hash: `6832904b76ff964bf08b38eaf15cd7bb94d842fb`
- Timestamp: 2026-04-11T06:16:02.346573+00:00
- Entrypoint: `run_p4_transformer_baseline_repro.py`
- Python Version: 3.12.0
- PyTorch Version: 2.11.0+cpu

---

## Summary

**Overall Status:** ❌ SOME ARCHITECTURES FAILED REPRO CHECK

Failures:
- **MLP**: 3 metric(s) differ beyond tolerance
- **LSTM**: 1 metric(s) differ beyond tolerance
- **TRANSFORMER**: 3 metric(s) differ beyond tolerance

---

## Tolerance Policy

Tolerance: 1e-6 absolute difference

Rationale: Project 4 baseline artifacts lack seed/environment metadata, so we assume
quasi-deterministic evaluation (same code, same hyperparameters, same hardware should
produce identical results within floating-point precision).

## Load-Bearing Metrics

Compared metrics:
- `in_distribution_accuracy`: Exact match on in-distribution test set
- `pattern_*`: Accuracy per adversarial family (alternating_carry, full_propagation_chain, block_boundary_stress)
- `mean_adversarial_accuracy`: Average accuracy across all adversarial families
