# MODEL VALIDATION REPORT: Script Contradiction Analysis

**Date:** March 30, 2026  
**Status:** ⚠️ CRITICAL METHODOLOGICAL ERROR DETECTED AND RESOLVED

---

## Executive Summary

The two Phase 30 interrogation scripts use **fundamentally different neural network architectures** and therefore produce **incomparable results**. 

**Verdict:**
- ❌ `phase_30_interrogation_main.py` — **INVALID for Phase 30 analysis**
- ✅ `phase_30_interrogation_corrected.py` — **VALID baseline** (though incomplete)

---

## Evidence of Model Mismatch

### Script 1: `phase_30_interrogation_main.py`
**Line 32:**
```python
from models.residual_logic_adder import ResidualLogicAdder
```

**Model Type:** `ResidualLogicAdder`  
**Architecture:** External model class (3,345 parameters per conversation history)  
**Results Reported:**
- 132/200 local failures
- 66% failure frequency
- **34% predicted accuracy**

---

### Script 2: `phase_30_interrogation_corrected.py`
**Lines 18-66 (embedded model definition):**
```python
class MLPSequenceArithmetic(nn.Module):
    """MLP baseline: process sequence with sequential carry propagation"""
    def __init__(self, max_length):
        super().__init__()
        self.embed_a = nn.Embedding(10, 8)
        self.embed_b = nn.Embedding(10, 8)
        self.fc1 = nn.Linear(8 + 8 + 2, 64)
        ...
```

**Model Type:** `MLPSequenceArithmetic`  
**Architecture:** Embedded, sequential carry propagation design  
**Results Reported:**
- 100/100 local success (carry_in=0)
- **100% local accuracy** at first position
- Consistent with 99.6% global accuracy

---

## Why This Matters

| Dimension | Script 1 | Script 2 | Reality |
|-----------|---------|---------|---------|
| **Model Class** | ResidualLogicAdder | MLPSequenceArithmetic | MLPSequenceArithmetic |
| **Training Data** | Different pipeline | Different pipeline | Official training |
| **Results** | 34% → 99.6% gap | 100% local → 99.6% global | ✓ Makes sense |
| **Validity** | ❌ Wrong model | ✅ Correct model | — |

---

## Root Cause

When the interrogation investigation began, the agent initially **misidentified the Phase 30 model architecture**:
- Assumed `ResidualLogicAdder` was the Phase 30 model
- Only later discovered the official Phase 30 uses `MLPSequenceArithmetic`
- Script 2 corrected this error

**Result:** Script 1 is **analyzing a completely different model** than Phase 30.

---

## Decision

### Invalidate Script 1
- **Do not cite** `phase_30_interrogation_main.py` results in any conclusion
- **Do not use** the "34% predicted accuracy" figure
- **Do not continue** development of Script 1

### Adopt Script 2 as Baseline
- Use `phase_30_interrogation_corrected.py` as the valid starting point
- **Extend it** to test full (a, b, carry_in) local space
- Proceed to frequency masking analysis only after full local-state is documented

---

## What We Know (Valid)

From `phase_30_interrogation_corrected.py`:
- ✅ MLPSequenceArithmetic achieves **100% accuracy on 100 (a,b) pairs at carry_in=0**
- ✅ Global result is **99.6%** (official)
- ⏳ **Unknown:** Behavior at carry_in=1

---

## What We Don't Know Yet (Required)

1. **Local accuracy at carry_in=1** → Full (a,b) × {0,1} table needed
2. **Digit vs carry accuracy** breakdown → Both metrics needed locally
3. **Failure concentration** → Are failures isolated or distributed?
4. **Frequency prediction** → Can local failures explain 0.4% global gap?

---

## Next Step

Create `phase_30_step2_complete_local_table_VALID.py`:
- Uses **MLPSequenceArithmetic** (confirmed correct)
- Tests **all 200 cases**: (a ∈ [0..9], b ∈ [0..9], carry_in ∈ {0,1})
- Reports **digit accuracy** and **carry accuracy** separately
- Identifies **failure locations** and patterns
- Feeds results into frequency masking analysis

**Scientific Standard:** No aggregate conclusions until local space is fully closed.

