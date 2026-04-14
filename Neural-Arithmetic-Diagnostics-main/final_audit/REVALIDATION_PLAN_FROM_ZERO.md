# REVALIDATION FROM ZERO: Complete Plan

**Date:** March 30, 2026  
**Status:** 🔴 FROZEN - All previous results under review  
**Approach:** Sequential revalidation, small steps, no hidden assumptions

---

## Current Trust Status (FROZEN)

| Result Set | Status | Reason |
|---|---|---|
| Project 1–2 | ❓ UNKNOWN | Not yet verified from scratch |
| Project 3 Killer Test | ⚠️ SUSPICIOUS | Used in analysis but not revalidated |
| Phase 30 | ❌ BROKEN | Script 1 used wrong model; Script 2 incomplete |
| Phase 30b, 26c, 27c | ❓ UNKNOWN | Depends on Phase 30 foundation |
| Project 4 Planning | ⛔ BLOCKED | Cannot proceed until foundation verified |

**Decision:** Do not cite ANY previous results until they pass revalidation.

---

## Core Principle

> **Confidence is rebuilt through verification of small, isolated claims—not through grand summaries.**

---

## Revalidation Strategy

### Phase 0: Freeze & Acknowledge
- ✅ **Done:** Acknowledge model mismatch in `phase_30_interrogation_main.py`
- ✅ **Done:** Acknowledge incomplete testing in `phase_30_interrogation_corrected.py`
- ✅ **Done:** Create this revalidation plan
- **Next:** Build verification scripts for smallest verifiable claims

### Phase 1: Killer Test Foundation (Highest Priority)
**Why start here?**
- Killer test is the deepest investigation in Project 3
- If we can revalidate it from scratch, it demonstrates our process works
- Its claims are concrete and testable
- All other Phase 3 conclusions depend on it

**What we'll verify:**
- Pattern generation (alternating, chain, block patterns)
- Target computation (digit/carry ground truth)
- Metric computation (accuracy calculations)
- Official result reproducibility

### Phase 2: Project 1–2 Baseline (After Phase 1)
**What we'll verify:**
- Basic digit addition model training
- Accuracy metrics
- No major red flags in architecture/data

### Phase 3: Phase 30 Revalidation (After Phase 2)
**What we'll verify:**
- Correct model usage (`MLPSequenceArithmetic`)
- Complete local-state testing (all 200 cases)
- Consistency with official 99.6% result
- Ability to explain 0.4% gap

### Phase 4: Phases 26c, 27c (After Phase 3)
**Only if Phase 30 is clean**

---

## Phase 1: Killer Test Revalidation (4 Steps)

### Step 1A: Verify Pattern Generation

**File to create:** `verify_killer_test_step1a_pattern_generation.py`

**What it does:**
- Generate alternating patterns
- Generate chain patterns  
- Generate block patterns
- Print examples (5-10 each)

**What we check manually:**
```
Example alternating: [9,0,9,0,9,0]
Are these actually alternating? Yes/No

Example chain: [1,1,1,1,1,1]
Are all digits the same? Yes/No

Example block: [9,9,9,0,0,0,9,9,9,0,0,0]
Are they in blocks? Yes/No
```

**Acceptance criteria:**
- Patterns match their names
- No off-by-one errors
- Seed is consistent

---

### Step 1B: Verify Target Computation

**File to create:** `verify_killer_test_step1b_targets.py`

**What it does:**
- Takes (a, b) sequences
- Computes digit_true and carry_true
- **NO model involved**
- Prints ground truth for 20+ examples

**What we check manually:**
```
a=[9,9,9], b=[1,1,1]
Position 0: 9+1=10 → digit=0, carry=1 ✓
Position 1: 9+1+1=11 → digit=1, carry=1 ✓
Position 2: 9+1+1=11 → digit=1, carry=1 ✓

a=[0,0,0], b=[0,0,0]  
Position 0: 0+0=0 → digit=0, carry=0 ✓
```

**Acceptance criteria:**
- All manual calculations match script output
- Carry propagation is correct
- No edge cases missed

---

### Step 1C: Verify Metric Computation

**File to create:** `verify_killer_test_step1c_metrics.py`

**What it does:**
- Takes **synthetic model predictions** (we set manually)
- Computes digit_accuracy, carry_accuracy, exact_match
- **Uses made-up predictions we control completely**

**Example:**
```python
# We know the true values
digit_true = [0, 1, 1]
carry_true = [1, 1, 1]

# We set a prediction: perfect
digit_pred = [0, 1, 1]
carry_pred = [1, 1, 1]
# Expected: 100% accuracy

# We set a prediction: one digit wrong
digit_pred = [0, 2, 1]  # Position 1 is wrong
carry_pred = [1, 1, 1]
# Expected: 2/3 = 66.7% digit accuracy

# We set a prediction: one carry wrong
digit_pred = [0, 1, 1]
carry_pred = [1, 0, 1]  # Position 1 is wrong
# Expected: 2/3 = 66.7% carry accuracy
```

**Acceptance criteria:**
- Our calculations match script output exactly
- No metric computation bugs
- Exact match is only 100% when BOTH digit and carry are correct

---

### Step 1D: Reproduce Killer Test Official Result

**File to create:** `verify_killer_test_step1d_reproduce.py`

**What it does:**
- Load official killer test file: `src/train/project_3_killer_test_adversarial_carry_chain.py`
- Train model exactly as specified
- Run on killer test patterns
- Print result

**What we compare:**
```
Official says: "Alternating pattern → 50% accuracy"
Our script says: ???

If they match:
  ✅ Killer test is REVALIDATED
If they don't match:
  ❌ We found a discrepancy that needs investigation
  (This is GOOD - we'd rather find it now)
```

**Acceptance criteria:**
- Reproduces within ±2% of official
- Uses exact model class (ResidualLogicAdder)
- Uses exact training procedure (100 epochs, seed=42)

---

## Phase 2: Project 1–2 Baseline Revalidation

### After Phase 1 succeeds

**File to create:** `verify_phase_1_2_baseline.py`

**Scope (TBD - minimal):**
- Generate digit pairs
- Train model
- Check: Does it reach >95% accuracy on in-distribution?

**Why minimal?**
- Phase 1–2 are "baseline" work, not novel claims
- Main risk: were the official numbers even real?
- We just need to verify model trains at all

---

## Phase 3: Phase 30 Revalidation

### After Phase 2 succeeds

**File to create:** `verify_phase_30_complete_local_state.py`

**Scope:**
- Train `MLPSequenceArithmetic` with seed=42
- Test ALL 200 cases: (a,b) ∈ [0..9]², carry_in ∈ {0,1}
- Report digit_accuracy AND carry_accuracy per case
- Identify any failures

**Key difference from before:**
- ✅ Explicitly uses `MLPSequenceArithmetic`
- ✅ Tests all 200 cases (not just 100)
- ✅ Reports both digit and carry accuracy
- ✅ No claims until complete

---

## Trust Levels After Revalidation

### ✅ Level 1: Trusted (Can cite in reports)
Results that passed Step 1A-1D completely

### ⚠️ Level 2: Plausible (Can mention, but with caveats)
Results that passed Step 1A-1C but not Step 1D yet

### ❌ Level 3: Untrusted (Do not cite)
Results that haven't been revalidated yet

---

## Implementation Timeline

| Phase | Start | Est. Duration | Output |
|-------|-------|---|---|
| 1A (pattern gen) | Now | 15 min | Simple script + manual check |
| 1B (targets) | After 1A | 15 min | Synthetic examples |
| 1C (metrics) | After 1B | 15 min | Metric validation |
| 1D (reproduce) | After 1C | 30 min | Official result verification |
| **Phase 1 Complete** | | **~75 min** | Killer test trusted or not |
| Phase 2 | After 1D | ~30 min | Baseline trust |
| Phase 3 | After 2 | ~30 min | Phase 30 foundation |
| **TOTAL** | | **~2.5 hours** | Full foundation rebuilt |

---

## What We Will Know After Revalidation

### Best Case (Everything verifies)
- ✅ Killer test results are real and reproducible
- ✅ Phase 30 local space is understood
- ✅ 0.4% gap explained or identified as sequence-level effect
- ✅ Ready to proceed with Project 4 planning

### Expected Case (Some issues found)
- ✓ Specific weaknesses identified
- ✓ Can work around them or understand them
- ✓ Better to know limits than pretend everything works

### Worst Case (Foundation broken)
- ✗ Major architectural errors found
- ✗ Metrics computed incorrectly
- ✗ But at least we'd KNOW this instead of building on sand

---

## What We Will NOT Do

❌ **Don't cite** previous results until revalidated  
❌ **Don't write** Project 4 plans until Phase 3 complete  
❌ **Don't assume** anything about Phases 26c, 27c  
❌ **Don't aggregate** results into grand summaries yet  
❌ **Don't use** model predictions without verifying metrics first  

---

## Sacred Rules for Revalidation Scripts

Every verification script must include:

```python
"""
VERIFICATION SCRIPT: [Name]
=============================

Official target:
  - File: [path]
  - Model class: [ClassName]
  - Training source: [where model was trained]
  
What this script verifies:
  - [Claim 1]
  - [Claim 2]
  
What this script does NOT verify:
  - [Out of scope]
  
Acceptance criteria:
  - [Criterion 1]
  - [Criterion 2]
"""
```

No hidden assumptions. Everything explicit.

---

## Master Status Board

### Now (Frozen)
```
Killer Test:    ⚠️ REVALIDATING
Phase 30:       ❌ BROKEN
Projects 1-2:   ❓ PENDING
Project 4:      ⛔ BLOCKED
```

### After Phase 1 Complete
```
Killer Test:    ✅ OR ❌ (verified either way)
Phase 30:       ⏳ NEXT
Projects 1-2:   ⏳ AFTER
Project 4:      ⏳ WHEN READY
```

### After All Phases Complete
```
Killer Test:    ✅ [Confidence level]
Phase 30:       ✅ [Confidence level]
Projects 1-2:   ✅ [Confidence level]
Project 4:      🟢 READY TO PLAN
```

---

## Decision: Start Phase 1 Now?

**Choose one:**

### Option A: Start 1A immediately
```
Next step: Create verify_killer_test_step1a_pattern_generation.py
Proceed: Now
```

### Option B: Review this plan first
```
Next step: Read REVALIDATION_PLAN_FROM_ZERO.md thoroughly
Proceed: After review
```

**Recommendation:** Option A (building scripts forces clarity on the plan)

---

## Final Philosophy

> **We don't need to prove everything is perfect.**  
> **We need to know exactly what we can trust and what we can't.**

After this revalidation:
- Some results will be ✅ Trusted
- Some will be ⚠️ Plausible
- Some will be ❌ Broken

**And that's infinitely better than not knowing which is which.**

---

**Are you ready to start Phase 1?**

