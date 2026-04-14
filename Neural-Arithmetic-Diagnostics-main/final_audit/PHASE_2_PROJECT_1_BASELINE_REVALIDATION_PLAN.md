# PHASE 2: PROJECT 1 BASELINE REVALIDATION PLAN
## Revalidation from Zero — Project 1 / Phase 26c

---

## Purpose

This document defines the revalidation plan for the **Project 1 baseline** using the official reference file:

- `src/train/phase_26c_failure_audit.py`

The purpose of this phase is to rebuild trust in the foundational Project 1 result through a controlled, source-linked verification process.

This phase does **not** aim to reinterpret all of Project 1 immediately.  
Its first goal is narrower and more important:

> **Verify that the official Project 1 baseline result is generated correctly, measured correctly, and understood at the appropriate level of confidence.**

---

## Why This Phase Matters

Project 1 established one of the core claims of the research line:

- arithmetic behavior depends strongly on architecture, task formulation, and representation,
- and the MLP baseline exhibits meaningful but limited generalization.

Because later projects build on this interpretation, the Project 1 baseline must be revalidated carefully before it is used as trusted evidence.

---

## Official Target

### Primary file
- `src/train/phase_26c_failure_audit.py`

### Related official document
- `PROJECT_1_CLOSURE_DOCUMENT.md`

### Expected role in research line
This file serves as the official baseline reference for:
- Project 1 arithmetic fitting and held-out behavior,
- and the earliest evidence for bounded competence rather than unrestricted generalization.

---

## Phase Objective

This phase will verify five things:

1. **The official baseline script runs correctly**
2. **The data generation and split logic are sound**
3. **The metric computation is correct**
4. **The reported baseline result is reproducible**
5. **The observed errors can be described behaviorally without overclaiming mechanism**

---

## Revalidation Strategy

As in Phase 1, this phase will proceed through **small, explicit verification steps** rather than a large all-in-one audit script.

The intention is to build trust incrementally.

---

## Planned Steps

### Step 2A — Source and Setup Verification
Verify the basic structure of the official baseline script:

- what model class it uses,
- how data is generated,
- how train/test split is defined,
- what metrics are reported,
- and whether seeds / determinism are documented.

**Output artifact:**
- `final_audit/code_audit/verify_phase26c_step2a_source_setup.py`

---

### Step 2B — Data Generation and Split Verification
Verify:
- the number of arithmetic pairs,
- the nature of the 70/30 split,
- whether held-out pairs are genuinely unseen,
- and whether any leakage exists between train and test.

This step should confirm:
- what "in-distribution" means,
- what "held-out pair" means,
- and whether those terms are implemented consistently.

**Output artifact:**
- `final_audit/code_audit/verify_phase26c_step2b_data_split.py`

---

### Step 2C — Ground Truth and Label Semantics
Verify:
- the arithmetic targets being learned,
- the role of carry labels if present,
- whether digit and carry are supervised directly or indirectly,
- and whether target semantics match the documentation.

**Output artifact:**
- `final_audit/code_audit/verify_phase26c_step2c_ground_truth.py`

---

### Step 2D — Metric Verification
Verify the correctness of:
- training accuracy reporting,
- held-out accuracy reporting,
- digit accuracy and carry accuracy (if both are used),
- and the exact meaning of the reported baseline result.

As in Phase 1, this should be done with synthetic controlled examples when possible.

**Output artifact:**
- `final_audit/code_audit/verify_phase26c_step2d_metrics.py`

---

### Step 2E — Official Reproduction
Run the official baseline script and verify that the documented result can be reproduced.

This step should answer:
- does the script run successfully?
- what result does it report?
- does that result match the project documentation within a reasonable tolerance?

**Output artifact:**
- `final_audit/code_audit/verify_phase26c_step2e_reproduction.py`

---

### Step 2F — Behavioral Error Structure
After successful reproduction, inspect the behavior of the baseline:

- what kinds of pairs fail?
- are failures concentrated around carry transitions?
- are there specific local subcases with sharply lower accuracy?
- does the result reflect broad competence with narrow failures, or broad weakness?

This step must remain **behavioral**, not mechanistically overclaimed.

**Output artifact:**
- `final_audit/code_audit/verify_phase26c_step2f_error_structure.py`

---

## Acceptance Standard

Phase 2 is considered successful if the following are established:

### Required
- the official baseline file runs successfully,
- data generation and split logic are valid,
- no obvious train/test leakage is found,
- metrics are correctly defined and computed,
- the documented result is reproduced within acceptable tolerance.

### Optional but desirable
- error structure is localized and clearly described,
- failure modes are characterized behaviorally,
- Project 1 closure claims can be linked directly to reproduced evidence.

---

## What This Phase Will Not Claim

Even if successful, Phase 2 will **not automatically prove**:

- the full Project 1 interpretation,
- the exact internal mechanism of the baseline model,
- or the full validity of the entire research line.

Instead, it will establish:

> **the Project 1 baseline result is experimentally trustworthy at the script / data / metric / reproduction level**

That is the goal of this phase.

---

## Output Files

Planned outputs:

- `final_audit/code_audit/verify_phase26c_step2a_source_setup.py`
- `final_audit/code_audit/verify_phase26c_step2b_data_split.py`
- `final_audit/code_audit/verify_phase26c_step2c_ground_truth.py`
- `final_audit/code_audit/verify_phase26c_step2d_metrics.py`
- `final_audit/code_audit/verify_phase26c_step2e_reproduction.py`
- `final_audit/code_audit/verify_phase26c_step2f_error_structure.py`
- `final_audit/PHASE_2_PROJECT_1_BASELINE_SUMMARY.md`

---

## Recommended Order of Execution

1. Step 2A — source/setup
2. Step 2B — data/split
3. Step 2C — ground truth
4. Step 2D — metrics
5. Step 2E — official reproduction
6. Step 2F — behavioral error structure
7. Summary document

This order is deliberate:
- first verify setup,
- then verify labels,
- then verify metrics,
- then reproduce,
- only then interpret behavior.

---

## Decision Rule

### PASS
- baseline reproduced,
- supporting logic verified,
- no critical issue found.

### PASS WITH QUALIFICATIONS
- result reproduced,
- but some naming/documentation/threshold issue requires clarification.

### HOLD
- reproduction fails,
- data split is invalid,
- metric logic is unsound,
- or leakage is detected.

---

## Final Note

This phase should be approached with the same standard established in Phase 1:

- no large audit scripts first,
- no interpretive overreach,
- no automatic trust,
- and no claim stronger than the evidence supports.

The goal is to rebuild trust one verified component at a time.

---

**Document Status:** Active Plan  
**Phase:** 2  
**Target:** Project 1 baseline (`phase_26c_failure_audit.py`)  
**Decision Status:** Pending
