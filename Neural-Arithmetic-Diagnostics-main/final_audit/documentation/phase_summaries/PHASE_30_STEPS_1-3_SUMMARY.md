================================================================================
PHASE 30 INTERROGATION: STEPS 1-3 SUMMARY & FINDINGS
================================================================================

Investigation Date: 2026-03-30
Methodology: Behavioral Analysis (following killer test protocol)
Status: IN PROGRESS — STEP 4 needed before final interpretation

================================================================================
STEP 0: THEORETICAL HYPOTHESES (Documented)
================================================================================

✅ Created PHASE_30_INTERROGATION_STEP0.md with 5 hypotheses:
   H1: Broad correctness with rare edge cases
   H2: Pattern-masked localized weaknesses
   H3: Position-specific degradation
   H4: Carry-conditioned weakness
   H5: Boundary saturation at specific sum ranges

================================================================================
STEP 1: REPRODUCE OFFICIAL RESULT
================================================================================

Model Used: MLPSequenceArithmetic (from phase_30_multidigit_learning.py)
- Embedding dim: 8 for each digit
- FC layers: 64 → 32 hidden units
- Output heads: digit (10 classes) + carry (2 classes)  
- Training: 30 epochs, batch size 32, Adam optimizer

Training Data:
- Sequences of lengths 2-5
- 500 samples per length
- 2000 total sequences
- Random seed: 42

Status: ✅ REPRODUCIBLE (no issues with training, converges quickly)

================================================================================
STEP 2-3: EXTRACT LOCAL ERROR STRUCTURE
================================================================================

### Test Configuration:
- Single position (first position, position=0)
- Carry_in = 0 (model starts with no carry)
- All 100 (a,b) pairs: a∈[0,9], b∈[0,9]
- Expected sum for each: digit_true = (a+b) % 10

### Key Results:

┌─────────────────────────────────────────────────────────┐
│ LOCAL DIGIT ACCURACY: 100/100 = 100.0%                 │
│                                                         │
│ Model correctly predicts digit for ALL (a,b) pairs    │
│ when carry_in = 0                                      │
│                                                         │
│ Examples verified:                                      │
│   (0,0) → digit_true=0, digit_pred=0 ✓                │
│   (5,7) → digit_true=2, digit_pred=2 ✓                │
│   (9,9) → digit_true=8, digit_pred=8 ✓                │
│   ... (all 100 correct)                                │
└─────────────────────────────────────────────────────────┘

### Contrast with Killer Test:
```
Killer Test (ResidualLogicAdder):
  - Local failures: 1/200 (0.5%) - specifically (0,0,carry=1)
  - Explained 99.6% vs 50% dichotomy perfectly

Phase 30 (MLPSequenceArithmetic):
  - Local failures: 0/100 (0.0%) - at carry_in=0
  - Expected accuracy at carry_in=0: 100%
  - Actual global accuracy: 99.6%
  
Discrepancy: Where do the 0.4% errors come from?
```

================================================================================
STEP 4: FREQUENCY MASKING ANALYSIS (PRELIMINARY)
================================================================================

Since there are NO local failures at carry_in=0:

Expected accuracy from local digit error rate:
  Failure rate (local) = 0%
  Expected accuracy ≈ 100%
  
But observed accuracy = 99.6%

### This means errors must come from one of:
  A) Carry prediction mismatches
     - If carry prediction is wrong, downstream positions fail
     - But local digit prediction still correct
  
  B) Behavior different when carry_in=1
     - Need to test (a,b) pairs when previous carry=1
     - May find failures that don't appear at carry_in=0
  
  C) Cascade effects in multi-position sequences
     - Position 1 error cascades to position 2, etc.
     - Overall sequence accuracy lower than local accuracy

================================================================================
KEY QUESTIONS REQUIRING STEP 4+ TESTING
================================================================================

1. **Carry Fidelity Test:**
   - What is the accuracy of carry prediction separately?
   - If carry_acc < 99.6%, this explains the gap
   
2. **Carry-Conditioned Test:**
   - What is accuracy when carry_in=1 (previous position had carry)?
   - Do failures appear here that don't appear at carry_in=0?
   
3. **Sequence-Level Analysis:**
   - Generate random test sequences
   - Test on full multi-position sequences
   - Identify which positions fail and how frequently

4. **Classification Questions:**
   Which hypothesis is most supported?
   - H1 (broad correctness, rare edge): UNLIKELY — no local failures found
   - H2 (multiple masked weaknesses): POSSIBLE — could be in carry or sequences
   - H3 (position degradation): POSSIBLE — later positions may degrade
   - H4 (carry weakness): POSSIBLE — may have carry-specific issues
   - H5 (boundary saturation): UNLIKELY — no sum-range saturation observed locally

================================================================================
BEHAVIORAL CHARACTERIZATION (SO FAR)
================================================================================

OBSERVED (High Confidence):
  ✅ Model achieves 100% digit accuracy locally (carry_in=0)
  ✅ No evidence of local single-digit failures
  ✅ Training is stable and reproducible

FREQUENCY-PREDICTED vs OBSERVED:
  - Expected from local analysis: ~100%
  - Observed global (Phase 30): 99.6%
  - Gap: 0.4% unexplained

HYPOTHESIZED INTERNAL CAUSE (Speculative):
  - May be linked to carry propagation
  - May be linked to carry prediction errors
  - May be multi-position sequence effects
  → Requires STEP 4 testing to determine

================================================================================
STATUS & NEXT STEPS
================================================================================

Current Status: ⏳ STEP 3 COMPLETE, STEP 4 REQUIRED

To Complete Investigation:
  STEP 4: Test carry prediction accuracy
    □ Separate digit and carry accuracy
    □ Test at carry_in=1 scenarios
    □ Build full (a,b,carry_in) table with accuracy

  STEP 5: Compare frequency-predicted vs observed
    □ If carry_acc is the limiting factor, compute expected
    □ Match expected vs observed 99.6%
    □ Quantify contribution of each failure type

  STEP 6: Adjacent-case interrogation
    □ For any failures found, test nearby cases
    □ Determine if failures are isolated or broader

  STEP 7: Final interpretation
    □ Separate observed behavior from internal cause
    □ Classify against 5 hypotheses
    □ Provide behavioral characterization without overclaiming

================================================================================
SCIENTIFIC INTEGRITY NOTES
================================================================================

This investigation maintains separation between:

✅ OBSERVED: "Model shows 100% on local first-position digits"
✅ FREQUENCY: "This predicts ~100% accuracy, but observed is 99.6%"
⚠️ NOT YET PROVEN: "Therefore, errors are in carry propagation"

The last statement is a hypothesis, not a finding.
Further testing is required before claiming carry is the issue.

================================================================================
COMPARISON TO KILLER TEST PROTOCOL
================================================================================

Killer Test (Now Completed):
  • Observed specific failures: (0,0,carry=1)
  • Isolated failures via TEST 4
  • Quantified frequency via analysis
  • Explained aggregate metrics from frequency
  → Conclusion: SOLID with high confidence

Phase 30 (Current):
  • Observed: No local failures at carry_in=0
  • Need: Test at carry_in=1 and multi-position
  • Need: Isolate where 0.4% error comes from
  • Need: Match frequency prediction to obs observed
  → Conclusion: PREMATURE without further testing

================================================================================
FILES CREATED
================================================================================

Documentation:
  ✅ PHASE_30_INTERROGATION_STEP0.md — Theoretical hypotheses
  ✅ phase_30_interrogation_corrected.py — STEP 1-3 analysis script

Findings:
  ✅ This summary document

Next Artifacts Needed:
  ⏳ phase_30_step4_carry_analysis.py — Carry testing
  ⏳ PHASE_30_INTERROGATION_STEPS_4-7.md — Final analysis
  ⏳ PHASE_30_FINAL_VERDICT.md — Behavioral conclusion

================================================================================
READY FOR STEP 4?
================================================================================

Yes. The next technical step is clear:

Implement phase_30_step4_carry_analysis.py that:
1. Tests (a,b) pairs with carry_in=1
2. Measures carry prediction accuracy separately
3. Builds full (a,b,carry_in) results table
4. Quantifies where the 0.4% gap originates

This will determine whether Phase 30 follows the killer test pattern
or exhibits a different form of limitation.
