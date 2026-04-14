# PROJECT 5 LOCAL DIGIT BOTTLENECK RESULTS
## Local Error-Structure Analysis

**Date:** April 2026  
**Project:** 5  
**Status:** COMPLETE  
**Verdict:** PASS

---

## Purpose

This document records the local bottleneck analysis performed after the first learned local processor experiment.

The goal of this analysis was to move beyond the statement:

- "local digit accuracy is low"

and determine whether that weakness has internal structure.

---

## Background

The preceding Project 5 result established:

- exact local decomposition is structurally sound
- learned local carry prediction is easy
- learned local digit prediction is much weaker
- the composed learned decomposition collapses across the tested families

This raised the next question:

> Where exactly does local digit prediction fail?

---

## Main Result

The bottleneck analysis showed that local digit failure is **not uniform**.

### Overall local behavior
- `digit_acc ≈ 0.415`
- `carry_acc = 1.0`

### Carry-conditioned split
The most important result is the strong difference between:

- cases with `carry_out = 0`
- cases with `carry_out = 1`

### Observed pattern
- `digit_acc | carry_out = 0 ≈ 0.59`
- `digit_acc | carry_out = 1 ≈ 0.24`

This is a large and meaningful gap.

---

## Interpretation

The most defensible interpretation is:

> the learned local processor is much less reliable on digit prediction when the local arithmetic case produces carry-out.

This suggests that the learned local module does not merely suffer from generic low precision.
Instead, its errors are strongly concentrated in the very cases where local arithmetic requires both:
- emitting carry
- and reducing the visible digit correctly

---

## Why This Matters

This result deepens the Project 5 story in an important way.

Before this analysis, the natural interpretation could have been:
- the local module is simply too weak overall

After this analysis, the picture becomes sharper:

- carry prediction itself is easy
- but correct digit prediction under carry-producing cases is not

This means the decomposition problem is not only about transmitting carry.
It is also about correctly handling the local transformation that separates:
- the emitted carry
from
- the retained digit output

That is a much more precise bottleneck.

---

## Additional Error Pattern Clues

The most common observed digit confusions were often near-neighbor errors, for example:
- `8 -> 9`
- `1 -> 2`
- `2 -> 3`

This suggests that the local processor often remains close to the right arithmetic neighborhood, but still fails to apply the correct carry-conditioned digit correction reliably.

This pattern is informative, but should still be treated as descriptive rather than as a full mechanistic explanation.

---

## What This Establishes

This analysis establishes the following:

1. local digit failure is structured, not uniform
2. carry output prediction can be easy even when digit prediction remains weak
3. carry-producing local cases are the dominant bottleneck
4. structural decomposition and learned local implementation are separated by a specific arithmetic difficulty, not merely a generic collapse

---

## What This Does NOT Yet Prove

This result does not yet prove:

- the exact internal representation used by the local model
- whether the failure is best explained by representation, optimization, or architecture
- whether a better local model, better supervision, or explicit modular constraints would solve the problem
- a full mechanistic theory of the local digit/carry interaction

---

## Correct Scientific Position

The strongest correct scientific position is:

> the learned local processor fails primarily on carry-producing digit cases, not because carry itself is hard to predict, but because digit prediction under carry-conditioned transformation remains weak.

This is the central result of the bottleneck analysis.

---

## Recommended Next Step

A natural next question is now:

> Can local digit prediction under carry-producing cases be improved by changing the local architecture, supervision, or output representation?

This opens the door to a focused new intervention branch in Project 5.

---

## Formal Status

**Result:** PASS  
**Type:** local bottleneck analysis  
**Main message:** the decomposition bottleneck is concentrated in carry-conditioned digit prediction, not in carry emission itself

---
