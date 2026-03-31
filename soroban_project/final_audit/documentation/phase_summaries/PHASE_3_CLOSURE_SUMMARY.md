# PHASE 3: PHASE 27C AUDIT CLOSURE SUMMARY
## Project 03 Abacus - Verification Record

**Date:** March 31, 2026  
**Phase:** 3  
**Status:** COMPLETE  
**Overall Verdict:** MIXED — core setup/semantics/metrics verified, but cross-architecture comparability is biased and official reproduction remains incomplete

---

## Phase 3 Mandate

The Phase 3 target was:

- `src/train/phase_27c_architecture_audit.py`

The purpose of Phase 3 was to verify this file step by step, with explicit scope boundaries:

1. source/setup transparency
2. test-pair distribution fairness across architectures
3. ground-truth / target semantics
4. metric computation logic
5. bounded official reproduction attempt

The sequence followed was:

- Step 3A → Step 3B → Step 3C → Step 3D → Step 3E

---

## Summary of All Steps

| Step | Task | Status | Verdict | Core Finding |
|------|------|--------|---------|--------------|
| 3A | Source/setup verification | ✅ Complete | PASS | File structure, architecture definitions, and main pipeline are visible and auditable |
| 3B | Shuffle-order fairness | ✅ Complete | FAIL / BIASED | Same-trial test-pairs differ across architectures because `all_pairs` is shuffled in-place across architecture loops |
| 3C | Ground-truth semantics | ✅ Complete | PASS | Target generation matches correct single-digit addition semantics in both train and test |
| 3D | Metric computation | ✅ Complete | PASS | Prediction decoding, exact-match logic, carry/non-carry partitioning, and test accuracy computation are correct |
| 3E | Official reproduction attempt | ✅ Complete | INCOMPLETE / TIMEOUT | Official script did not complete within 600 seconds, so reproduction success/failure could not be established |

---

## Step 3A: Source / Setup Verification

### What Was Verified
- the target file exists
- the module is structurally readable and auditable
- the 3 architectures are defined in the source:
  - `MLP`
  - `LSTMModel`
  - `TransformerModel`
- the source visibly contains train/test data generation logic
- the main training/evaluation pipeline is present
- deterministic seeding for torch/numpy is visible in source

### Result
**PASS**

### What This Supports
Step 3A supports confidence that the file is transparent enough for deeper verification.

### What It Does Not Prove
Step 3A does not prove:
- fairness of data split
- correctness of semantics
- correctness of metrics
- successful reproduction

---

## Step 3B: Test-Pair Distribution Fairness

### Diagnostic Question
Do MLP, LSTM, and Transformer receive identical `test_pairs` for the same trial index?

### Result
**FAIL / BIASED**

### Verified Finding
The official source creates `all_pairs` once, then reuses and shuffles it in-place across architectures:

```python
all_pairs = [(a, b) for a in range(10) for b in range(10)]

for arch_name, arch_class in architectures.items():
    for trial in range(30):
        random.seed(trial)
        random.shuffle(all_pairs)
        train_pairs = all_pairs[:70]
        test_pairs = all_pairs[70:]
```

A dedicated diagnostic showed that under this actual source behavior:
- same-trial `test_pairs` differ across architectures
- this mismatch occurs in **30/30 trials**
- resetting `all_pairs` per architecture removes the mismatch in control testing

### Interpretation
This establishes a **cross-architecture comparability problem at the test-pair fairness level**.

### What This Affects
This directly affects:
- same-trial architecture-to-architecture comparison
- any claim that the 3 architectures were evaluated on identical held-out pair sets
- architecture comparison cleanliness at the split level

### What This Does Not By Itself Prove
This does not by itself prove:
- that ground-truth labels are wrong
- that metric computation is wrong
- that all numerical results are unusable
- the magnitude of the impact of this bias on final architecture rankings

### Permanent Qualification
Any future use of Phase 27c architecture-level comparisons must carry this qualification:

> Step 3B established that cross-architecture test-pair distribution is biased due to in-place shuffle state being carried across architectures. Therefore, direct architecture comparison is not methodologically clean at the held-out pair level.

---

## Step 3C: Ground-Truth / Target Semantics

### Diagnostic Question
Are training and test targets semantically correct?

### Verified Semantics
For input `(a, b, carry_in)`:

```python
digit_out = (a + b + carry_in) % 10
carry_out = 1 if (a + b + carry_in) >= 10 else 0
```

### Verification Method
- direct import of target functions
- direct calls to:
  - `create_train_data()`
  - `create_test_data_simple()`
- comparison against an independent reference implementation
- row-by-row checking on hand-selected cases
- train/test consistency check on matched inputs

### Result
**PASS**

### What This Supports
Step 3C supports the conclusion that Phase 27c uses correct single-digit addition semantics for target generation in both train and test paths.

### Qualification
This result is independent of Step 3B because Step 3C verifies target semantics, not cross-architecture split fairness.

---

## Step 3D: Metric Computation

### Diagnostic Question
Are evaluation metrics computed correctly from predictions and labels?

### Verified Metric Logic
The source metric logic was verified for:
- `digit_pred = argmax(digit_logits)`
- `carry_pred = (carry_logits > 0)`
- `both_correct` as exact-match on both digit and carry
- carry/non-carry partitioning using `(a + b + carry_in) >= 10`
- failure counting
- `test_acc` consistency with exact-match correctness

### Verification Method
- controlled synthetic prediction tensors
- source-style metric computation
- independent reference computation
- manual expectation check on mixed success/failure cases

### Result
**PASS**

### What This Supports
Step 3D supports the conclusion that metric computation in Phase 27c is internally consistent and semantically correct.

### Qualification
This result does not remove the Step 3B bias finding. Correct metrics can still be applied to a biased architecture comparison setup.

---

## Step 3E: Official Reproduction Attempt

### Diagnostic Question
Can the official script be run to completion and its reported results be checked?

### Verification Method
- direct subprocess execution of:
  - `src/train/phase_27c_architecture_audit.py`
- bounded runtime attempt
- stdout/stderr capture
- raw output saving
- planned parsing of architecture-level summaries if execution completed

### Result
**INCOMPLETE / TIMEOUT**

### What Happened
- the official script was launched
- the run did not complete within the configured 600-second time limit
- therefore official reproduction success/failure could not be established from this attempt

### What This Does Not Mean
This does not prove:
- that the script is broken
- that the official results are false
- that reproduction is impossible
- why the timeout occurred

It proves only:
> Under the bounded 600-second reproduction attempt used here, the official script did not complete.

---

## Phase 3 Closure Assessment

### What Phase 3 Established
Phase 3 established the following:

- **PASS:** the source/setup is transparent enough for audit (3A)
- **FAIL / BIASED:** cross-architecture test-pair fairness is broken (3B)
- **PASS:** ground-truth / target semantics are correct (3C)
- **PASS:** metric computation is correct (3D)
- **INCOMPLETE / TIMEOUT:** official reproduction did not complete within the runtime bound used here (3E)

### What Phase 3 Does Support
Phase 3 supports the following claims:

- the Phase 27c task definition is semantically correct
- the metric logic is correct
- the architecture comparison carries a serious split-level comparability caveat
- bounded official reproduction was attempted but not completed

### What Phase 3 Does Not Support
Phase 3 does not support:
- a clean architecture-to-architecture comparison claim
- a claim that official aggregate results were fully reproduced
- a claim that the magnitude of the architecture bias is known
- a mechanistic explanation of architecture differences

---

## Final Phase 3 Position

The most defensible overall position is:

> Phase 27c is partially verified.
>
> Its target semantics and metric computation are correct and auditable.
> However, its architecture comparison is not methodologically clean at the test-pair fairness level due to the Step 3B bias finding.
> In addition, bounded official reproduction remained incomplete due to timeout.

---

## Transition Guidance

If Phase 27c is referenced later, it should be referenced with both of these conditions visible:

1. **Step 3B caveat:** cross-architecture test-pair distribution is biased
2. **Step 3E qualification:** official bounded reproduction did not complete within the runtime limit used in this audit

Possible next actions after Phase 3 closure may include:
- moving to the next phase of the broader audit sequence
- returning later for a longer or differently provisioned reproduction attempt
- or creating a corrected rerun path if clean architecture comparison becomes necessary

---

## Formal Closure

**Phase 3 Status:** COMPLETE  
**Phase 3 Overall Verdict:** MIXED  
**Permanent Caveat:** Step 3B cross-architecture comparability bias  
**Additional Qualification:** Step 3E bounded reproduction incomplete / timeout

---

# END OF PHASE 3 CLOSURE SUMMARY
