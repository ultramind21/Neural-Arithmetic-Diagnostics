# REPRO_CHECK_PROJECT4_BASELINES — Project 12 Baseline Reproduction Report

**Purpose:** Verify that Project 12 baseline reproductions match Project 4 historical artifacts.

**Methodology:**
- Compare scorecard metrics (in-distribution accuracy, pattern accuracies, mean adversarial)
- Tolerance: 1e-6 absolute difference (quasi-deterministic evaluation)
- PASS: All metrics within tolerance
- FAIL: Any metric differs beyond tolerance

---

## MLP Baseline
**Status:** ✅ PASS

All load-bearing metrics match within tolerance (1e-6).

**P12 Metadata:**
- Git Hash: `eaca6585db1d094a59c866eb56b8f6fa3ba3be77`
- Timestamp: 2026-04-11T06:30:17.831094+00:00
- Entrypoint: `run_p4_mlp_baseline_repro.py`
- Python Version: 3.12.0
- PyTorch Version: 2.11.0+cpu

---

## LSTM Baseline
**Status:** ✅ PASS

All load-bearing metrics match within tolerance (1e-6).

**P12 Metadata:**
- Git Hash: `eaca6585db1d094a59c866eb56b8f6fa3ba3be77`
- Timestamp: 2026-04-11T06:30:26.238465+00:00
- Entrypoint: `run_p4_lstm_baseline_repro.py`
- Python Version: 3.12.0
- PyTorch Version: 2.11.0+cpu

---

## TRANSFORMER Baseline
**Status:** ✅ PASS

All load-bearing metrics match within tolerance (1e-6).

**P12 Metadata:**
- Git Hash: `eaca6585db1d094a59c866eb56b8f6fa3ba3be77`
- Timestamp: 2026-04-11T06:30:58.004310+00:00
- Entrypoint: `run_p4_transformer_baseline_repro.py`
- Python Version: 3.12.0
- PyTorch Version: 2.11.0+cpu

---

## Summary

**Overall Status:** ✅ ALL ARCHITECTURES PASS REPRO CHECK

All Project 12 baseline reproductions match Project 4 historical artifacts within tolerance.

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
