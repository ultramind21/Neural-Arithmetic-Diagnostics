# PHASE 27C STEP 3B: DIAGNOSTIC RESULTS
## Shuffle Order Fairness Verification

**Date:** March 30, 2026  
**Phase:** 3  
**Step:** 3B  
**Status:** COMPLETE  
**Verdict:** ✗ BIASED

---

## Executive Summary

The official `src/train/phase_27c_architecture_audit.py` script does **not** distribute identical test-pairs to MLP, LSTM, and Transformer for the same trial index.

**Verdict:** Step 3B = **FAIL (BIASED)**

This establishes a **cross-architecture comparability issue at the test-pair fairness level**.

---

## Test Methodology

### Official Diagnostic Script
- File: `final_audit/code_audit/verify_phase27c_step3b_diagnostic_shuffle.py`
- Execution Date: March 30, 2026
- Runtime: <1 second

### Diagnostic Strategy

Two simulations were run:

1. **Actual Source Simulation** (**official verdict path**)
   - Reproduces the actual source behavior:
     - `all_pairs` is created once
     - then reused and shuffled in-place across architectures
   - Reflects what the official script actually does

2. **Reset Control Simulation** (**interpretive only**)
   - Resets `all_pairs` to its initial state for each architecture
   - Used only to isolate the source of the shuffle-order effect
   - Not used for the official verdict

---

## Key Findings

### Result 1: Actual Source Behavior (Official Verdict Path)

**Test-pair comparison across architectures for the same trials:**

| Trial | MLP first3 | LSTM first3 | Transformer first3 | Identical? |
|-------|------------|-------------|--------------------|:----------:|
| 0 | `[(7,5), (7,1), (6,0)]` | `[(6,8), (2,7), (9,0)]` | `[(0,1), (8,6), (8,2)]` | ❌ |
| 1 | `[(0,8), (8,9), (0,9)]` | `[(4,6), (9,6), (9,3)]` | `[(7,3), (8,1), (3,6)]` | ❌ |
| 14 | `[(5,3), (5,1), (3,7)]` | `[(8,4), (2,4), (9,4)]` | `[(2,6), (1,9), (8,3)]` | ❌ |
| 29 | `[(5,5), (2,7), (7,4)]` | `[(8,0), (8,6), (0,8)]` | `[(5,0), (4,4), (4,6)]` | ❌ |

**Critical finding:** All 30 trials show mismatched `test_pairs` across architectures.

```text
Mismatched trials: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15,
                    16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29]

Total mismatch count: 30/30 trials
Fairness status: ✗ BIASED
```

---

### Result 2: Reset Control Behavior (Interpretive Only)

**When each architecture resets `all_pairs` independently:**

| Trial | MLP first3 | LSTM first3 | Transformer first3 | Identical? |
|-------|------------|-------------|--------------------|:----------:|
| 0 | `[(7,5), (7,1), (6,0)]` | `[(7,5), (7,1), (6,0)]` | `[(7,5), (7,1), (6,0)]` | ✅ |
| 1 | `[(0,8), (8,9), (0,9)]` | `[(0,8), (8,9), (0,9)]` | `[(0,8), (8,9), (0,9)]` | ✅ |
| 14 | `[(5,3), (5,1), (3,7)]` | `[(5,3), (5,1), (3,7)]` | `[(5,3), (5,1), (3,7)]` | ✅ |
| 29 | `[(5,5), (2,7), (7,4)]` | `[(5,5), (2,7), (7,4)]` | `[(5,5), (2,7), (7,4)]` | ✅ |

**Interpretive finding:** All 30 trials become identical under reset control.

```text
Matched trials: 30/30 trials
Fairness status under reset control: ✓ FAIR
```

This shows that the issue is not the seed values themselves, but the fact that the shuffled list state is carried forward across architectures in the official source behavior.

---

## Root Cause Analysis

### Why the Bias Occurs

In the official source:

```python
all_pairs = [(a, b) for a in range(10) for b in range(10)]

for arch_name, arch_class in architectures.items():
    for trial in range(30):
        random.seed(trial)
        random.shuffle(all_pairs)  # in-place modification

        train_pairs = all_pairs[:70]
        test_pairs = all_pairs[70:]
```

### The Problem Mechanism

1. **MLP trials 0-29**
   - Start from the original ordered `all_pairs`
   - Apply `random.shuffle(all_pairs)` repeatedly for trials 0 through 29
   - End with `all_pairs` left in a shuffled state after trial 29

2. **LSTM trials 0-29**
   - Do **not** start from the original ordered `all_pairs`
   - Instead start from the post-MLP shuffled state
   - Apply `random.seed(0)` and `random.shuffle(all_pairs)` to a list already in a different order
   - Therefore, LSTM trial 0 does **not** receive the same `test_pairs` as MLP trial 0

3. **Transformer trials 0-29**
   - Start from the post-LSTM state
   - Again receive a different sequence of `test_pairs`

### Conclusion

The source uses a **stateful in-place shuffle process across architectures**.  
As a result, same-trial comparisons across MLP, LSTM, and Transformer are **not performed on identical held-out pair sets**.

---

## What This Diagnostic Proves

### ✓ This Diagnostic VERIFIED

- [x] Whether same-trial `test_pairs` are identical across architectures
- [x] Whether the actual in-place shuffle behavior preserves cross-architecture fairness
- [x] That `random.seed(trial)` alone is insufficient to guarantee identical `test_pairs` when list state differs
- [x] That reset-per-architecture removes the mismatch in this diagnostic
- [x] The immediate root cause of the mismatch: stateful in-place list modification across architectures

### ✗ This Diagnostic DID NOT Verify

- [ ] Ground-truth arithmetic correctness
- [ ] Metric computation correctness
- [ ] Model training behavior or convergence
- [ ] Numerical accuracy of official reported results
- [ ] The magnitude of the effect of this bias on reported architecture differences
- [ ] Whether Phase 27c results should be discarded entirely

---

## Scope Boundary

This diagnostic is narrowly scoped to one question:

> Are the 3 architectures evaluated on identical test-pairs in the same trial?

**Answer:** No — **BIASED**

This is a **split-level comparability finding**, not a full evaluation of the entire Phase 27c experiment.

---

## Implications

### For Comparability

**Cross-architecture direct comparison is NOT methodologically sound** at this level because:
- Each architecture sees different test_pairs for the same trial index
- Reported performance differences could be partially due to different held-out data
- Cannot definitively isolate architectural effects from test-set effects

### For Project 2 Baseline

Project 2 (phase_27c_architecture_audit.py) comparison results are **compromised** unless this issue is fixed or explicitly accounted for.

---

## Recommendation

### Immediate Action
Do **NOT** proceed to Phase 3C or beyond without:

1. Explicitly acknowledging the BIASED verdict
2. Documenting this bias in the final Phase 3 report
3. User approval to either:
   - **Option A:** Flag as invalid and skip Phase 27c validation
   - **Option B:** Continue with explicit caveat about test-pair bias
   - **Option C:** Re-run phase_27c_architecture_audit.py with fix applied

### For Future Work

If validation of Project 2 is required:
- Fix the source by adding: `all_pairs = [(a, b) for a in range(10) for b in range(10)]` inside the architecture loop
- Or reset it explicitly before each architecture block
- Then re-run all trials

---

## Qualifications

### Confidence Level
**HIGH** — The diagnostic methodology correctly reproduces the source behavior and clearly demonstrates the bias.

### Limitations
- This diagnostic does NOT validate whether the bias materially affects reported metrics
- It is possible that despite the biased split, the reported results are still meaningful
- Only the fairness of test-pair distribution is verified, not result validity

### Methodological Notes
- Official verdict based ONLY on actual-source simulation
- Control simulation included for interpretive clarity, not for verdicting
- Both simulations correctly reproduce Python list shuffle semantics

---

## Formal Step Closure

**Step 3B Diagnostic:** ✗ **COMPLETE - FAIL (BIASED)**

**Next Action Required:** User review and approval before proceeding.

---

# END OF DIAGNOSTIC RESULTS

