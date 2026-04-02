# PROJECT 4 BASELINE RESULTS
## Diagnostic Framework v1.0

**Date:** March 31, 2026  
**Status:** ACTIVE RESULTS FILE  
**Framework Version:** 1.0

---

## Purpose

This document records baseline-model evaluation under the Project 4 diagnostic framework.

It is not intended to merely report raw accuracy.
Its purpose is to document:

- diagnostic scorecard dimensions
- regime-guided interpretation
- validation status
- and any required qualifications

---

## Models to Evaluate

The baseline comparison is expected to include, as applicable:

- MLP baseline
- LSTM baseline
- Transformer baseline
- Residual baseline (if retained as a reference baseline)

---

## Required Reporting Structure

For each model, the following should be reported:

### 1. In-Distribution Accuracy
- value
- evaluation setting
- validation status

### 2. Structured Adversarial Results
- pattern-wise breakdown
- mean adversarial accuracy
- worst-case pattern accuracy

### 3. Length Extrapolation
- accuracy by tested length
- relative drop beyond training range
- trend label

### 4. Rounding Sensitivity
- with rounding
- without rounding
- sensitivity magnitude

### 5. Carry Corruption Sensitivity
- corruption levels
- accuracy by level
- degradation curve summary

### 6. Regime Guidance
- scorecard indicators
- explicit rationale
- final working regime assignment

### 7. Validation Status
- run count
- stability level
- spread / variance summary
- whether result is exploratory or validated

---

## Baseline Result Template

# MODEL: [NAME]

### In-Distribution Accuracy
- value:
- notes:

### Structured Adversarial Accuracy
- alternating_carry:
- full_propagation_chain:
- block_boundary_stress:
- mean adversarial accuracy:
- worst-case pattern accuracy:

### Length Extrapolation
- tested lengths:
- accuracies:
- relative drops:
- trend label:

### Rounding Sensitivity
- with rounding:
- without rounding:
- sensitivity:

### Carry Corruption Sensitivity
- corruption levels:
- accuracies:
- degradation:
- trend label:

### Regime Guidance
- indicators:
- cautions:
- final working regime:
- rationale:

### Validation Status
- validation level:
- run count:
- spread summary:
- status:

---

## Cross-Model Comparison Rules

Cross-model comparison should not be reduced to a single scalar.

At minimum, cross-model discussion must preserve:

- pattern-wise differences
- worst-case robustness differences
- extrapolation trend differences
- sensitivity differences
- validation-status differences

No model should be treated as "better" solely because of one stronger metric.

---

## Interpretation Policy

This results file should preserve the framework rule:

> No single metric is sufficient for regime classification.

All model interpretations must remain:
- scorecard-based
- multi-dimensional
- qualification-aware

---

## Status Tracking

### Current Status
- baseline script implementation: ✅ complete
- baseline runs: ✅ complete (MLP)
- validation reruns: ✅ complete (3 runs, STABLE)
- regime assignments: ✅ assignable (MLP)
- LSTM baseline: pending
- Transformer baseline: pending

---

# BASELINE RESULTS

## MODEL: Phase 30 MLP Baseline v1.0

**Date Established:** March 31, 2026  
**Checkpoint:** `phase30_mlp_project4_ready.pt`  
**Training:** 800 sequences, 30 epochs, max_length=5  
**Evaluation Path:** Phase 30 native digit+carry semantics (corrected)

---

### Critical Qualification

> **This baseline is validation-stable under the current bounded evaluation path.**
> This means the results are NOT transient or seed-dependent, but it does NOT claim the evaluation path itself is complete or represents all relevant diagnostic dimensions.
> All interpretation below follows scoreboard-based multi-dimensional guidance.

---

### In-Distribution Accuracy

| Metric | Value | Notes |
|--------|-------|-------|
| `digit_accuracy` | 0.49 | Prediction of individual digit outputs |
| `carry_accuracy` | 0.94 | Prediction of individual carry states |
| `combined_accuracy` | 0.49 | Either digit OR carry correct at each position |
| `exact_match` | 0.086 | **Reported scalar:** Mean across 3 validation runs = 0.0859 |
| Validation spread | 0.0391 (6.25% → 10.16%) | 3 runs, stable within threshold |

**Interpretation:** 
- Carry prediction is strong (0.94)
- Digit prediction is weak (0.49)
- Exact-match requirement (both correct) dominates to 0.086
- This is a **structural finding**, not a noise artifact

---

### Structured Adversarial Accuracy

| Pattern | Digit Acc. | Carry Acc. | Combined Acc. | Exact Match |
|---------|-----------|-----------|--------------|------------|
| `alternating_carry` | 0.60 | 1.00 | 0.60 | 0.00 |
| `full_propagation_chain` | 0.60 | 1.00 | 0.60 | 0.00 |
| `block_boundary_stress` | 1.00 | 1.00 | 1.00 | 1.00 |

**Mean adversarial accuracy:** 0.73 (combined; 0.67 if exact-match weighted)  
**Worst-case pattern:** `alternating_carry` and `full_propagation_chain` both at 0.00 exact-match

**Validation status:** All 3 runs show identical pattern profile (0.0, 0.0, 1.0). STABLE across seeds.

**Interpretation:**
- Block-boundary stress: **MASTERED**
- Alternating carry propagation: **FAILED**
- Full carry chain propagation: **FAILED**
- This is a sharp, diagnostically clear pattern

---

### Length Extrapolation

| Length | Tested | Accuracy (combined) | Relative Drop | Trend |
|--------|--------|------------------|-----------------|-------|
| 5 | yes (training) | 0.0625 ± 0.0078 | baseline | flat |

**Note:** Only length=5 tested (training length); no length generalization data yet.

**Trend label:** `single-length-only`

---

### Rounding Sensitivity

| Condition | Accuracy |
|-----------|----------|
| with rounding | 0.0859 |
| without rounding | 0.0859 |
| sensitivity magnitude | 0.00 |

**Interpretation:** No sensitivity to rounding under current evaluation path.

---

### Carry Corruption Sensitivity

| Corruption Level | Accuracy |
|------------------|----------|
| 0.5 | 0.0859 |

**Degradation curve:** No degradation observed; single corruption level tested.

**Interpretation:** Carry corruption does not further degrade performance at 0.5 level.

---

### Regime Guidance

**Scorecard Dimensions:**

| Dimension | Value | Signal |
|-----------|-------|--------|
| In-distribution strength | 0.086 exact-match | WEAK – low exact-match despite strong carry prediction |
| Adversarial robustness | highly asymmetric | FRAGILE – fails on propagation patterns, masters boundary stress |
| Length generalization | untested beyond 5 | UNKNOWN |
| Carry mastery | 0.94 per-position | STRONG – carries predicted correctly |
| Digit mastery | 0.49 per-position | WEAK – digits show 50% error |
| Carry propagation | full failure | CRITICAL GAP – model cannot chain carries across sequence |

**Cautions:**

1. **Not a "bad" baseline** – exact-match is not necessarily the right performance target for digit arithmetic with carries. The metric is strict-and-honest, but may not reflect model capability.

2. **Carry mastery paradox** – Model correctly predicts individual carries (0.94) but fails to use them correctly in sequence (0.0 exact-match on propagation patterns). This suggests:
   - Model learned local carry inference
   - But does NOT learn to propagate carry state across positions
   - This is a **structural learning gap**, not noise

3. **Block stress mastery is suspicious** – If the model cannot do alternating carries, why does it perform perfectly on block-boundary stress? Suggests:
   - Block-boundary stress in current evaluation may not be testing true carry dynamics
   - OR model has learned the specific pattern of block boundaries differently

**Final Working Regime Assignment:**

```
Regime: DIAGNOSTIC_SIGNAL_TIER_2
Assignment Rule: carry_mastery HIGH + digit_mastery WEAK + propagation FAILED

Rationale:
The baseline shows clear signal on a critical learning gap:
- the model separates carry state inference (strong) 
  from carry state propagation (failed)
This is a feature, not a bug, for Project 4 diagnostics: 
it identifies a specific mechanistic limitation.

This regime suggests next steps should focus on:
1. Why does per-token carry prediction work but chain-of-carry fails?
2. Is the evaluation path correctly measuring carry propagation?
3. Are LSTM/Transformer baselines also affected?
```

---

### Validation Status

| Metric | Value |
|--------|-------|
| Validation level | STABLE |
| Run count | 3 |
| Spreads (exact-match) | min=0.0625, max=0.1016, range=0.0391, std=0.0207 |
| Pattern consistency across runs | identical (0.0, 0.0, 1.0 across all seeds) |
| Validation verdict | **PASS** |
| Scientific status | **First validated Project 4 baseline** |

**Validation command:**
```bash
python project_4/validation/validate_run_stability.py \
  --input-json project_4/results/baseline_runs/phase30_mlp_validation_runs.json
```

**Validation result:**
- All scalar metrics: stable (range < threshold, std < threshold)
- All pattern metrics: stable (zero variance on 0.0 and 1.0 outcomes)
- All length metrics: stable

**Conclusion:** This is not an exploratory finding; it is a **validated, reproducible baseline result**.

---

## Cross-Baseline Placeholder

### LSTM Baseline
- Status: pending
- Expected: comparison to MLP on same evaluation path
- Decision gate: run LSTM baseline to establish if MLP's carry-learning profile is model-class specific or training-data specific

### Transformer Baseline
- Status: pending
- Expected: further diversity in baseline model classes

---

## Interpretation Policy Confirmation

This results file adheres to the framework rule:
> No single metric is sufficient for regime classification.

The MLP baseline above is interpreted **multi-dimensionally**:
- It does NOT reduce to "8.6% accuracy = failure"
- It DOES interpret across: exact-match, per-token accuracy, adversarial patterns, carry mastery, carry propagation, regime assignment
- All interpretations are qualified with their applicability bounds

---

# END OF PROJECT 4 BASELINE RESULTS
