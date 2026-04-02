# COMPREHENSIVE VALIDATION REPORT: Script-by-Script Analysis

**Status:** 🔴 **TRUST RECOVERY IN PROGRESS**  
**Date:** March 30, 2026

---

## Official Model Architectures (VERIFIED)

### Phase 3: Single-Digit Adder
**File:** `src/models/residual_logic_adder.py`  
**Class:** `ResidualLogicAdder`  
**Purpose:** Learn sum ∈ [0..19], logic layer computes digit/carry  
**Input:** (a, b, carry_in) where a,b ∈ [0..9], carry_in ∈ {0,1}  
**Output:** (digit, carry) from sum = a + b + carry_in

**Training:** 100 epochs, seed=42, CrossEntropyLoss on sum classification

---

### Phase 30: Multi-Digit Sequences
**File:** `src/train/phase_30_multidigit_learning.py`  
**Classes:** 
- `MLPSequenceArithmetic` (baseline, 3,345 params)
- `LSTMSequenceArithmetic` (sequence-aware)
- `TransformerSequenceArithmetic` (attention-based)

**Purpose:** Compositional generalization on multi-digit sequences  
**Input:** Padded sequences a, b ∈ [0..9] of lengths 2-5  
**Output:** digit, carry predictions per position

**Training:** 30 epochs, seed=42, lr=0.001, CrossEntropyLoss on digit+carry

**Official Test Results (MLP on in-distribution lengths 2-5):**
```
Length | Digit Acc | Carry Acc | Exact Match
-------|-----------|-----------|------------
   2   |  99.2%    |  99.4%    |  98.5%
   3   |  99.1%    |  99.2%    |  97.8%
   4   |  99.0%    |  98.9%    |  97.6%
   5   |  99.6%    |  99.7%    |  99.2%
```

---

## Scripts Under Review

### ❌ INVALIDATED: `phase_30_interrogation_main.py`

**Model Used:** `ResidualLogicAdder` (imported from src/models)  
**Expected For:** Phase 3 only  
**Claimed For:** Phase 30

**Problem:**
- Uses single-digit model (ResidualLogicAdder)
- Phase 30 should use multi-digit model (MLPSequenceArithmetic)
- Results: 66% failure frequency, 34% predicted accuracy
- **INCOMPATIBLE WITH:** Official Phase 30 (99.6%)

**Action:** ❌ **DISCARD ENTIRELY**
- Do not cite these results
- Do not draw conclusions from them
- They analyze a different problem than Phase 30

---

### ⚠️ PARTIALLY VALID: `phase_30_interrogation_corrected.py`

**Model Used:** `MLPSequenceArithmetic` (embedded definition)  
**Correct For:** Phase 30

**What's Verified:**
- ✅ Model architecture matches official definition
- ✅ Embedding dimensions: 8 (matches official)
- ✅ Hidden layer: 64 → 32 (matches official)
- ✅ Carry handling: sequential with softmax (matches official)
- ✅ Training: 30 epochs, seed=42, CrossEntropyLoss (matches official)

**What's Tested:**
- ✅ Local digit accuracy at carry_in=0: 100/100 → 100% success
- ❌ Local digit accuracy at carry_in=1: NOT TESTED
- ❌ Carry accuracy at either carry_in value: NOT TESTED
- ❌ Full (a,b,carry_in) space: INCOMPLETE

**Results Reported:**
```
carry_in=0:
  Digit accuracy: 100% (100/100 correct)
  Carry accuracy: NOT REPORTED
  
carry_in=1: NOT TESTED
```

**Confidence Level:** ⚠️ **MEDIUM**
- Model is correct
- Testing is incomplete (50% of space)
- Cannot claim "Steps 1-3 complete" with carry_in=1 untested

---

### ✅ READY TO EXECUTE: `phase_30_step2_complete_local_table_VALID.py`

**Model:** `MLPSequenceArithmetic` (embedded)  
**Status:** Not yet run  
**Scope:** Full 200-case local-state table

**What It Will Test:**
- All 100 cases with carry_in=0
- All 100 cases with carry_in=1
- Digit accuracy per case
- Carry accuracy per case
- Failure breakdown by type (digit-only, carry-only, both)
- Frequency masking preview

**Expected Output:** Complete local-state truth table

---

### ✅ VALID: Killer Test Scripts (`killer_test_carry_followup.py`, `killer_test_test4_frequency.py`)

**Model:** `ResidualLogicAdder` (imported from src/models)  
**Correct For:** Phase 3

**What's Verified:**
- ✅ Uses correct Phase 3 model
- ✅ Findings are internally consistent
- ✅ Adjacent-case interrogation is rigorous
- ✅ Frequency analysis explains 99.6% → 99.5% gap

**Results (VALID):**
```
✅ Carry locally encoded but structurally fragile
✅ Specific failure at (0,0,1)
✅ Works in 99% of input space (delta ≈ 1.0)
✅ Failure explains both 99.6% and 50% results
⏳ Internal mechanism (zero-embedding saturation) is speculative
```

**Confidence Level:** ✅ **HIGH (behavioral level)**

---

## Trustworthiness Summary

| Discovery | Model Verified | Testing Complete | Match Official | Confidence |
|-----------|---|---|---|---|
| Killer Test (Phase 3 failures) | ✅ Yes | ✅ Yes | ✅ 99.6%→99.5% | ✅ HIGH |
| Phase 30 local (carry_in=0) | ✅ Yes | ❌ Partial | — | ⚠️ MEDIUM |
| Phase 30 local (carry_in=1) | — | ❌ No | — | ❌ UNKNOWN |
| Phase 30 full local space | ✅ Yes (staged) | ⏳ Pending | — | ⏳ PENDING |

---

## Critical Trust Violations

### Trust Violation #1: Wrong Model in Phase 30 Analysis
- **Script:** `phase_30_interrogation_main.py`
- **Error:** Used `ResidualLogicAdder` (single-digit)
- **Consequence:** All results invalid for Phase 30
- **Impact:** Lost credibility on Phase 30 entirely
- **Recovery:** Must redo with correct `MLPSequenceArithmetic`

### Trust Violation #2: Incomplete Local-State Space
- **Script:** `phase_30_interrogation_corrected.py`
- **Error:** Tested only carry_in=0 (50% of space)
- **Consequence:** Cannot claim Steps 1-3 are "complete"
- **Impact:** Cannot proceed to frequency analysis
- **Recovery:** Run `phase_30_step2_complete_local_table_VALID.py`

---

## What We Can Claim NOW (High Confidence)

✅ **Phase 3 (Killer Test):**
- Carry is locally encoded (not ignored)
- Specific vulnerability at (0,0,1)
- Failure explains observed behavior in both 99.6% and 50% cases

❌ **Phase 30 (Not Yet):**
- Cannot claim "Steps 1-3 complete" until carry_in=1 is tested
- Cannot claim "100% local accuracy" because carry accuracy unknown
- Cannot proceed to frequency masking until full table is built

---

## Immediate Next Actions

### PRIORITY 1: Execute Validated Phase 30 Script
```bash
python phase_30_step2_complete_local_table_VALID.py
```
**Expected Output:**
- Full 200-case table (carry_in=0 & carry_in=1)
- Digit accuracy breakdown
- Carry accuracy breakdown
- Failure locations if any exist

### PRIORITY 2: Compare to Official Results
- Official Phase 30 MLP: 99.6% exact match on length-5 sequences
- Question: Does our local analysis explain the 0.4% gap?

### PRIORITY 3: Only After Full Local Space is Closed
- Frequency masking analysis (Step 4)
- Sequence-level cascade effects (Step 5)
- Adjacent-case interrogation (Step 6)
- Final interpretation (Step 7)

---

## Trust Recovery Checklist

- [ ] Execute `phase_30_step2_complete_local_table_VALID.py`
- [ ] Verify results match or explain deviation from official
- [ ] Document all failure locations if any found
- [ ] Proceed to frequency masking ONLY after local space is complete
- [ ] Sign off on trustworthiness before moving to Phases 26c, 27c
- [ ] No Project 4 planning until foundation is verified

---

## Official Decision: HOLD on Project 4

**Rationale:**
- Model mismatch discovered in Phase 30 analysis
- Partial testing exposed as incomplete
- Cannot proceed with aggregate claims until foundation is solid

**Resume Project 4 Planning When:**
- ✅ Phase 30 full local-state table is built
- ✅ Frequency masking analysis confirms predictions
- ✅ No contradictions between observed and predicted
- ✅ All scripts explicitly declare model source
- ✅ Trustworthiness scores finalized

