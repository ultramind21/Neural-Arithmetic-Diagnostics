================================================================================
PHASE 30 INTERROGATION: STEP 0 — THEORETICAL HYPOTHESES
================================================================================

**Date:** 2026-03-30  
**Question:** What is the structure of 99.6% accuracy in phase_30_multidigit_learning.py?

================================================================================
LEARNING FROM KILLER TEST
================================================================================

The killer test revealed a critical principle:

```
High global accuracy can coexist with sharp localized failures.

Killer test showed:
  • 99.6% random accuracy
  • 50% alternating accuracy
  • Single subcase failure: (a=0, b=0, carry=1)
  • 0.485% frequency in random → explains ~99.5% expected accuracy
```

This means: **99.6% ≠ "the model is broadly correct"**

It could mean:
  • Model is correct almost everywhere but has rare sharp failures
  • Model is correct in high-frequency cases but weak in low-frequency cases
  • Model exploits statistical properties of random data
  • Model has position-specific or carry-specific weaknesses

================================================================================
THREE PRIMARY HYPOTHESES FOR PHASE 30
================================================================================

### HYPOTHESIS 1: "Broad correctness with rare edge cases"
```
Structure:
  • 99%+ of local (a,b,carry_in) triples work correctly
  • Small set (<1%) of specific subcases fail deterministically
  • These failures occur in rare input combinations
  • Frequency of rare failures explains 99.6% metric

Evidence if true:
  ✓ Local error table will show isolated failures
  ✓ Adjacent cases to failure will mostly succeed
  ✓ Frequency-predicted accuracy = 99.6%
  
Evidence if false:
  ✗ Systematic failures in specific regions (e.g., all zeros, all high values)
  ✗ Failures affect common cases
  ✗ Pattern-specific degradation (e.g., much better at beginning than end)
```

---

### HYPOTHESIS 2: "Pattern-masked localized weaknesses"
```
Structure:
  • Multiple failure modes exist (like killer test's (0,0,1))
  • Each is rare individually but collectively significant
  • Random data happens to avoid most failure patterns
  • Adversarial patterns could expose each one
  
Evidence if true:
  ✓ Local error table shows 3+ distinct failure modes
  ✓ Each failure is different mechanism (carry-related, boundary, etc.)
  ✓ Collective frequency = 0.4%
  
Evidence if false:
  ✗ Single dominant failure mode (like killer test)
  ✗ Failures not mechanistically distinct
```

---

### HYPOTHESIS 3: "Position-specific degradation"
```
Structure:
  • Earlier positions have higher accuracy
  • Later positions degrade as error accumulates
  • Global 99.6% is average across all positions
  • Some positions may have much lower accuracy
  
Evidence if true:
  ✓ Error rate increases with position index
  ✓ Carry errors compound over positions
  ✓ Specific position windows have 80-90% accuracy
  
Evidence if false:
  ✗ Accuracy uniform across positions
  ✗ Degradation explained by random distribution, not position
```

---

### HYPOTHESIS 4: "Carry-conditioned weakness"
```
Structure:
  • Non-carry cases: 99.9%+ accuracy
  • Carry cases: lower accuracy (but still overall 99.6%)
  • Model struggles when carry is 1, even if not (0,0,1)
  
Evidence if true:
  ✓ Separate carry=0 vs carry=1 accuracy shows gap
  ✓ Carry=1 cases form most of the 0.4% failures
  ✓ Pattern similar to killer test but broader
  
Evidence if false:
  ✗ No significant difference between carry=0 and carry=1
  ✗ Failures distributed equally among carry values
```

---

### HYPOTHESIS 5: "Boundary saturation at specific sum ranges"
```
Structure:
  • Model fails at specific sum ranges (e.g., near 10, near 20)
  • These are critical points for carry transitions
  • Rounding/saturation effects create failure bands
  
Evidence if true:
  ✓ Error table shows clustering at specific sum values
  ✓ Nearby sums have opposite behavior
  ✓ Sum ranges like 9-11 show degradation clusters
  
Evidence if false:
  ✗ No correlation with sum values
  ✗ Errors distributed across all sum ranges uniformly
```

================================================================================
SPECIFIC PREDICTIONS BY HYPOTHESIS
================================================================================

If H1 (broad correctness) is true:
  → Local error table will be mostly all-green with 5-10 red outliers
  → frequency-predicted accuracy will ≈ 99.6%

If H2 (multiple masked weaknesses) is true:
  → Local error table will show 3-5 distinct failure regions
  → Each region will have clear mechanistic pattern
  → frequency-predicted accuracy will closely match 99.6%

If H3 (position degradation) is true:
  → Accuracy by position will show monotonic decline
  → Later positions will average 95-97%
  → Early positions will average 99.8%+

If H4 (carry weakness) is true:
  → carry=1 cases will have substantially lower accuracy than carry=0
  → Failure rate for carry=1 will be 1-2% instead of 0.4%

If H5 (boundary saturation) is true:
  → Error clustering in local error table at sum=9,10,11,19,20
  → Clean patterns in error distribution by sum range

================================================================================
INVESTIGATION SEQUENCE
================================================================================

1. STEP 1: Reproduce official result
   → First, confirm 99.6% is reproducible

2. STEP 2: Extract local error structure
   → Build complete breakdown of errors by (a,b,carry_in)
   → Check for patterns against H1-H5

3. STEP 3: Build local error table
   → Create structured table of all local triples
   → Mark success/failure for each

4. STEP 4: Frequency masking analysis
   → Count occurrence of each triple in test data
   → Compare failure frequency to error impact

5. STEP 5: Compare observed vs frequency-predicted
   → Calculate expected accuracy from frequencies
   → Compare to observed 99.6%

6. STEP 6: Adjacent-case interrogation
   → For each failure, test neighbors
   → Determine isolation of failure mode

7. STEP 7: Classification
   → Which hypothesis is best supported?
   → What is the behavioral characterization?
   → What remains speculative about internal cause?

================================================================================
CRITICAL NOTES
================================================================================

### Remember from killer test:
- **Observed behavior ≠ understood mechanism**
- We can say: "failure occurs at X, is rare, explains metric"
- We CANNOT say: "therefore mechanism is Y" without probing

### Focus on behavioral precision:
- "Model fails at [specific subcase]"
- NOT: "Model doesn't understand carry"

### Distinguish levels:
- Observed facts: very high confidence
- Frequency explains metric: high confidence
- Internal reason: speculative until probed

================================================================================
SUCCESS CRITERIA FOR PHASE 30
================================================================================

This investigation succeeds if we can answer:

1. ✅ What specific local cases (a,b,c) fail?
2. ✅ How often does each appear in random test data?
3. ✅ Does frequency-predicted accuracy match observed 99.6%?
4. ✅ Are failures isolated or spread?
5. ✅ Can we characterize failure behaviorally without overclaiming internal mechanism?

================================================================================
READY FOR STEP 1: REPRODUCE OFFICIAL RESULT
================================================================================

Next: Execute phase_30_multidigit_learning.py and verify 99.6% accuracy.
