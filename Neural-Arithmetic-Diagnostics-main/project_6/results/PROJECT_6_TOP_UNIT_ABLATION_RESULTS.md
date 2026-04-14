# PROJECT 6 TOP UNIT ABLATION RESULTS
## First Causal-Style Interpretability Result

**Date:** April 2026  
**Project:** 6  
**Status:** COMPLETE  
**Verdict:** PASS

---

## Purpose

This document records the first causal-style interpretability result in Project 6.

Its purpose was to test whether the units identified in the success-vs-failure probe are merely correlated with behavioral success, or whether they play a stronger functional role.

---

## Main Result

The top units identified by the success-vs-failure analysis were ablated, and this produced a clear asymmetric effect:

- digit accuracy dropped substantially
- exact accuracy dropped substantially
- carry accuracy remained unchanged

This is the strongest result in Project 6 so far.

---

## Why This Matters

The earlier probes established:
- carry-selective representation differences
- internal contrast between successful and failing cases

But those results were still correlational.

This ablation result moves one step closer to a causal claim:

> the identified units are not merely associated with successful behavior; they are functionally important for local digit accuracy under this intervention.

This is a major strengthening of the interpretability story.

---

## Observed Pattern

### Before ablation
- high digit accuracy
- perfect carry accuracy
- high exact local accuracy

### After ablating top diagnostic units
- strong degradation in digit accuracy
- strong degradation in exact accuracy
- no degradation in carry accuracy

This asymmetry is especially important.

It suggests that:
- the identified units are more important for digit-related local computation
- while carry output remains supported elsewhere or by different internal structure

---

## What This Establishes

This result establishes the following:

1. some hidden units are functionally important, not merely representationally distinctive
2. the earlier success-vs-failure contrast had real mechanistic content
3. digit-related local behavior can be disrupted selectively
4. carry-related local behavior is at least partially dissociable from the ablated digit-relevant structure

This is the first strong causal-style signal produced by Project 6.

---

## Why This Is Stronger Than Earlier Probes

The first probe showed:
- carry selectivity exists

The second probe showed:
- success and failure cases are internally distinguishable

This third result shows:
- at least some of the units driving that distinction matter functionally under intervention

That is a qualitatively stronger result.

---

## Correct Interpretation

The strongest safe interpretation is:

> a small subset of units identified through the success-vs-failure probe is causally important for local digit accuracy, while carry accuracy remains unaffected under the same ablation.

This is a strong interpretability result, but not yet a full circuit-level proof.

---

## What This Does NOT Yet Prove

This result does not yet prove:

- that these units are the only important units
- that they fully constitute a complete arithmetic circuit
- that the full mechanism is solved
- that all downstream family-level behavior is already explained by these units alone

Those questions remain open.

---

## Scientific Value

This result gives Project 6 a much stronger interpretability foundation.

Project 6 can now say:
- carry information is represented
- success vs failure is internally separable
- and some of the units associated with that distinction matter causally for local performance

This is a substantial mechanistic step.

---

## Recommended Next Step

The next natural direction is to test one of the following:

- whether the same units explain family-level successes and failures
- whether carry-relevant and digit-relevant units can be systematically dissociated
- whether ablation effects propagate into higher-level family behavior
- whether stronger causal perturbations reveal a more complete local circuit structure

---

## Formal Status

**Result:** PASS  
**Type:** causal-style ablation result  
**Main message:** top diagnostic units are functionally important for digit-related local behavior while carry performance remains intact

---
