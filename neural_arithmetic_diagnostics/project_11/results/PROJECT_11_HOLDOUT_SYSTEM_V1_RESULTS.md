# PROJECT 11 HOLDOUT SYSTEM V1 RESULTS
## Structural-OOD Prediction Attempt (V1)

**Date:** April 2026  
**Project:** 11  
**Status:** COMPLETE  
**Result type:** OOD prediction test + metric-collapse signal

---

## 1. What This Test Was

This was the first **structural-OOD** evaluation attempt in Project 11.

Goal:
- test whether the Project 10 regime/boundary intuition transfers into a new system

Constraints respected:
- sealed prediction submission (commit-before-run)
- no push during run
- OOD dynamics and stochastic evaluation

---

## 2. Main Result

- accuracy: **41.7%** (5/12)
- boundary accuracy: **44.4%** (4/9)

This is below the Prediction Gate performance and indicates **transfer failure** under this OOD system.

This is not a negative outcome.
It is a signal.

---

## 3. Confusion Matrix

```json
{
  "family_aware_region": {
    "family_aware_region": 0,
    "transition_region": 1,
    "universal_region": 0
  },
  "transition_region": {
    "family_aware_region": 2,
    "transition_region": 3,
    "universal_region": 2
  },
  "universal_region": {
    "family_aware_region": 0,
    "transition_region": 2,
    "universal_region": 2
  }
}
```

---

## 4. Key Interpretation (bounded)

The correct current interpretation is:

> under Holdout System V1 and the current metric definitions, the Project 10-derived region intuition does not transfer reliably.

This suggests a representation/metric fragility problem rather than a simple "prediction mistake".

---

## 5. Immediate Next Step

Perform a canonical metric-collapse diagnosis based strictly on:
- the artifact values
- and the evaluator code

No speculative reconstruction.

---
