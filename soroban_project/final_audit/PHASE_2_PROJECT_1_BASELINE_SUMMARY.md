# PHASE 2: PROJECT 1 BASELINE SUMMARY
## Revalidation from Zero — Project 1 / Phase 26c

---

## Status

**Phase:** 2  
**Target:** `src/train/phase_26c_failure_audit.py`  
**Current Status:** **PASS WITH QUALIFICATIONS**

---

## Purpose

This document records the final outcome of the revalidation of the official Project 1 baseline script:

- `src/train/phase_26c_failure_audit.py`

The goal of Phase 2 was to determine whether the Project 1 baseline result is trustworthy at the level of:

- source/setup,
- data generation and split,
- target semantics,
- metric semantics,
- official reproduction,
- and behavioral error-structure framing.

---

## Scope Covered

Phase 2 included the following verification steps:

### Step 2A — Source / Setup Verification
**Status:** PASS  
**Artifact:** `final_audit/code_audit/verify_phase26c_step2a_source_setup.py`

**Finding summary:**  
The official file exists, imports successfully, and contains a structurally clear baseline setup:
- fixed seeds at source level (torch=42, numpy=42),
- a visible `SimpleMLP` baseline (3 inputs, 128-hidden layer),
- explicit train/test logic (70/30 split structure),
- explicit digit and carry losses (CrossEntropy + BCE),
- and visible evaluation logic.

This step supports trust in the structural setup of the baseline script.

---

### Step 2B — Data Generation / Split Verification
**Status:** PASS  
**Artifact:** `final_audit/code_audit/verify_phase26c_step2b_data_split.py`

**Finding summary:**  
The source visibly defines:
- the full ordered pair space `(a,b)` over `0..9 × 0..9` (100 pairs),
- a trial-level shuffle with deterministic seed (seed=trial_number),
- a 70/30 train/test split by list slicing,
- and held-out pair evaluation semantics.

This step supports the interpretation that the baseline is built around a genuine held-out pair split at the source-definition level.

**Qualification:**  
This step verifies split logic structurally, not yet through full runtime split-trace inspection.

---

### Step 2C — Ground-Truth / Target Semantics
**Status:** PASS  
**Artifact:** `final_audit/code_audit/verify_phase26c_step2c_ground_truth.py`

**Finding summary:**  
The source defines targets consistently and correctly:

```python
sum_val = a + b + carry_in
digit_out = sum_val % 10
carry_out = 1 if sum_val >= 10 else 0
```

Training and evaluation both use the same semantics:
- digit target in position 0 of the label tensor,
- carry target in position 1.

Verified through 8 hand-checked cases (100% correct arithmetic).

This step supports that the baseline task is semantically well-defined.

---

### Step 2D — Metric Verification
**Status:** PASS  
**Artifact:** `final_audit/code_audit/verify_phase26c_step2d_metrics.py`

**Finding summary:**  
Synthetic controlled examples (5 test cases) confirmed that:
- digit accuracy semantics are correct,
- carry accuracy semantics are correct,
- exact match semantics are correct (binary: 100% or 0%),
- digit/carry divergence is mathematically legitimate (50% digit + 100% carry confirmed as valid),
- and dataset-level averaging differs from exact match in the expected way.

This step supports trust in metric interpretation.

---

### Step 2E — Official Reproduction
**Status:** PASS WITH QUALIFICATIONS  
**Artifact:** `final_audit/code_audit/verify_phase26c_step2e_reproduction.py`  
**Raw Output:** `final_audit/code_audit/step2e_phase26c_raw_output.txt`

**Finding summary:**  
The official baseline script ran successfully (return code 0) and produced a reproduced baseline result:

- **Overall success rate:** **61.4%**
- This falls within the documented Project 1 baseline range:
  - **MLP held-out baseline ≈ 61–73%** (from Project 1 closure docs)

Additional reproduced findings over 30 trials (1800 held-out examples total):
- Carry-conditioned cases are harder than non-carry cases
- **Carry failure rate:** 43.3%
- **Non-carry failure rate:** 33.9%
- **Relative difficulty:** 1.27× (carry cases 27% harder)

**Qualification:**  
The reproduction itself succeeded, but the parser did not automatically extract the key metric from the output. The result was therefore confirmed via raw-output manual review rather than clean parser automation. This represents a pipeline qualification, not a data qualification.

---

### Step 2F — Behavioral Error Structure
**Status:** PARTIAL / FRAMEWORK READY  
**Artifact:** `final_audit/code_audit/verify_phase26c_step2f_error_structure.py`

**Finding summary:**  
This step successfully defined the correct behavioral-analysis framework:

- Full local state space `(a,b,carry_in)` = 200 subcases (10×10×2),
- Conservative interpretation rules (what can and cannot be concluded behaviorally),
- and appropriate boundaries between behavioral description and mechanistic overclaiming.

However, this step did **not** complete a full prediction-level subcase error analysis, because reproduced per-case prediction records were not yet integrated into the analysis scaffold.

**Interpretation:**  
The behavioral-analysis framework is valid and ready, but the full subcase-level error structure remains only partially characterized.

---

## Revalidated Result

### Official baseline result reproduced?
**Yes — with qualifications**

### Observed key metric(s)
- **Overall held-out / test success rate:** 61.4%
- **Overall failure rate:** 38.6%
- **Carry failure rate:** 43.3%
- **Non-carry failure rate:** 33.9%

### Comparison to documented Project 1 baseline
Expected from closure documents:
- MLP held-out baseline approximately in the range: **61–73%**

Observed:
- **61.4%**

### Assessment
✓ **Matches documentation**

---

## What Phase 2 Supports

Phase 2 supports the following claims:

- ✓ The official Project 1 baseline file runs successfully
- ✓ The source/setup structure is consistent with the intended baseline
- ✓ Data generation and split logic are structurally acceptable
- ✓ No critical source-level leakage issue was found
- ✓ Target semantics are clear and valid
- ✓ Metric semantics are correct
- ✓ The official baseline result is reproducible
- ✓ Carry-conditioned cases appear genuinely harder than non-carry cases
- ✓ A conservative behavioral-analysis framework has been established

---

## What Phase 2 Does Not Yet Prove

Even after this phase, the following are **not** established:

- The full Project 1 closure interpretation in its strongest form
- The internal mechanism of the baseline model
- The full causal structure of its failure modes
- The full validity of all later projects

In particular:
- Step 2F did **not** complete full prediction-level subcase analysis,
- so behavioral characterization remains informative but partial

---

## Key Findings Summary

### Most important findings
1. The official Project 1 baseline result (**61.4%**) is reproducible and falls within the documented accepted range (60–73%).
2. The baseline task definition, targets, and metric semantics are structurally sound.
3. Carry-conditioned cases are empirically harder than non-carry cases in the reproduced result (1.27× ratio).

### Main qualifications
- The reproduction result required manual confirmation from raw output because parser automation was incomplete.
- Full subcase-level behavioral error analysis was not yet completed.

### Confidence level
**Moderate to High**

### Confidence notes
- **High confidence in:**
  - source/setup correctness
  - target semantics
  - metric semantics
  - and reproduction of the baseline range
  
- **Moderate confidence in:**
  - behavioral interpretation beyond aggregate carry-vs-noncarry findings, because the full prediction-level error-structure analysis remains incomplete

---

## Decision

### Final decision for Phase 2
# **PASS WITH QUALIFICATIONS**

### Rationale
Phase 2 successfully revalidated the Project 1 baseline at the levels of:
- source structure
- split semantics
- target semantics
- metric semantics
- and official result reproduction

However, two limitations remain:
1. Reproduction required raw-output manual review rather than complete parser automation
2. Full behavioral subcase analysis remains incomplete

These do not invalidate the baseline, but they justify a qualified rather than unconditional pass.

---

## Recommended Next Step

Proceed to the next revalidation target in sequence, while recording that:

- **Project 1 baseline is now considered provisionally trusted with qualifications**
- Any stronger Project 1 interpretation should remain appropriately bounded until deeper error-structure analysis is completed

### Recommended next target:
**Project 2 baseline revalidation**
  - `src/train/phase_27c_architecture_audit.py`

---

## Linked Artifacts

- `final_audit/code_audit/verify_phase26c_step2a_source_setup.py`
- `final_audit/code_audit/verify_phase26c_step2b_data_split.py`
- `final_audit/code_audit/verify_phase26c_step2c_ground_truth.py`
- `final_audit/code_audit/verify_phase26c_step2d_metrics.py`
- `final_audit/code_audit/verify_phase26c_step2e_reproduction.py`
- `final_audit/code_audit/verify_phase26c_step2f_error_structure.py`
- `final_audit/code_audit/step2e_phase26c_raw_output.txt`

---

## Final Note

Phase 2 does not "prove Project 1 completely."  
What it does establish is narrower and more valuable:

> The official Project 1 baseline is structurally sound, reproducible at the reported range, and sufficiently trustworthy to remain in the research line — but with explicitly documented qualifications.

---

**Document Type:** Final Summary  
**Phase:** 2  
**Status:** Completed  
**Date:** March 30, 2026
