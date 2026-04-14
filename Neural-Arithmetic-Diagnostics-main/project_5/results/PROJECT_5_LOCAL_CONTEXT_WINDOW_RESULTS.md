# PROJECT 5 LOCAL CONTEXT WINDOW RESULTS
## Richer Local Context Intervention

**Date:** April 2026  
**Project:** 5  
**Status:** COMPLETE  
**Verdict:** PASS

---

## Purpose

This document records the first local-context-window intervention result in Project 5.

Its purpose was to test whether adding a small local neighborhood to the local processor would improve decomposition robustness.

---

## Intervention

The intervention expanded the local processor input from:

- local digit pair + carry

to:

- previous digit pair
- current digit pair
- next digit pair
- carry

The motivation was to test whether residual failure might be caused by insufficient local context rather than by carry representation alone.

---

## Main Result

The intervention did **not** improve structural robustness.

Instead:

- all three tested families remained at `0.0` exact-match
- the previously rescued `full_propagation_chain` family also collapsed
- therefore the intervention weakened the earlier partial success rather than extending it

---

## Local-Level Observation

At the local level, the intervention did improve some aspects of digit prediction relative to weaker earlier variants.

However, this local improvement did not translate into successful composed behavior.

This is an important distinction:
- local metric improvement
does not imply
- successful decomposition-level robustness

---

## What This Establishes

This result establishes the following:

1. the current decomposition bottleneck is not well explained by simple local context shortage
2. adding neighboring digit information does not automatically improve compositional robustness
3. a richer local window can improve local statistics while still harming global structured behavior
4. the earlier rescue of `full_propagation_chain` was not due to missing local neighborhood context

---

## Why This Matters

This is a valuable negative result.

It rules out another simple hypothesis:
- that the local processor only needed a slightly wider neighborhood to solve the remaining difficult families

That hypothesis is not supported by the result.

Instead, the evidence now suggests that the missing ingredient is likely more specific than:
- class weighting
- chunk size
- or local window width

This sharpens the Project 5 search space.

---

## Correct Interpretation

The strongest correct interpretation is:

> simple local context expansion does not rescue the remaining decomposition failures and may even destroy a previously rescued family.

This means the unresolved bottleneck is not captured by a naive increase in local neighborhood information.

---

## What This Does NOT Yet Prove

This result does not prove:

- that all forms of context augmentation are useless
- that no richer local architecture could work
- that decomposition is doomed
- that the final answer is already known

It only proves that:
> this specific local context-window intervention does not solve the current problem.

---

## Updated Project 5 Position

After this result, Project 5 has ruled out or bounded several candidate explanations:

- decomposition itself is not the problem
- local carry prediction alone is not enough
- class reweighting does not solve the failure
- simple local context expansion does not solve the failure

This means the remaining explanation must be more structured than any of these simple fixes.

---

## Recommended Next Step

The next step should focus on a more targeted structural hypothesis, such as:

- explicit transition-aware representation
- a different local output formulation
- a more specialized local arithmetic architecture
- or a stronger decomposition interface design

---

## Formal Status

**Result:** PASS  
**Type:** local context intervention result  
**Main message:** simple local neighborhood expansion does not explain or solve the residual decomposition failures

---
