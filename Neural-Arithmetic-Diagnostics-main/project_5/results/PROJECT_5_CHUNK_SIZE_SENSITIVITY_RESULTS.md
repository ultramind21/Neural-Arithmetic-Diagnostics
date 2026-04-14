# PROJECT 5 CHUNK SIZE SENSITIVITY RESULTS
## Granularity Analysis under Explicit Carry Representation

**Date:** April 2026  
**Project:** 5  
**Status:** COMPLETE  
**Verdict:** PASS

---

## Purpose

This document records the chunk-size sensitivity analysis performed after the explicit carry-conditioned representation result.

Its goal was to test whether the remaining family split depends on decomposition granularity.

---

## Question

After explicit carry-conditioned representation, one family was rescued while two others still failed.

This raised the question:

> Is the remaining failure explained by chunk size itself?

To test this, the same learned local processor was evaluated under multiple chunk sizes.

---

## Tested Chunk Sizes

The following chunk sizes were tested:

- `1`
- `2`
- `3`
- `6`

This range spans:
- digit-wise decomposition
- small-block decomposition
- larger local blocks
- and a full-length block condition

---

## Main Result

The family pattern remained unchanged across all tested chunk sizes.

### Observed family-level exact-match pattern
- `alternating_carry` → `0.0` at all tested chunk sizes
- `full_propagation_chain` → `1.0` at all tested chunk sizes
- `block_boundary_stress` → `0.0` at all tested chunk sizes

---

## Interpretation

This result strongly suggests that the remaining family split is **not** explained by decomposition granularity alone.

In other words:

- changing chunk size does not rescue the failing families
- and does not remove the success on `full_propagation_chain`

Therefore, chunk size is not the main bottleneck behind the current family-level split.

---

## What This Establishes

This experiment establishes the following:

1. the current residual family split is stable across multiple chunk-size choices
2. the rescued family (`full_propagation_chain`) is not rescued merely because of one lucky block granularity
3. the still-failing families (`alternating_carry`, `block_boundary_stress`) are not failing merely because of one unlucky chunk-size choice
4. decomposition granularity alone does not explain the remaining selective failure

---

## Why This Matters

This is a strong negative result in the useful sense.

It removes one natural explanation:
- that the current decomposition behavior is primarily a chunk-size artifact

That means the project can now focus on stronger candidate explanations, such as:
- pattern-specific local transition structure
- local state-distribution mismatch
- representational limits not captured by chunk-size changes

---

## What This Does NOT Yet Prove

This result does not prove:

- the exact cause of the remaining family split
- that chunking is irrelevant in every possible architecture
- that no alternative decomposition design could help
- that Project 5 is complete

It only proves that:
> within the tested chunk-size range, granularity alone does not explain the residual failure pattern.

---

## Correct Scientific Position

The strongest correct interpretation is:

> explicit carry-conditioned local representation changes the local decomposition problem in a meaningful way, but the remaining selective failure is stable across chunk-size variation and therefore cannot be explained simply by decomposition granularity.

This is the central result of the chunk-size study.

---

## Recommended Next Step

The next logical question is now:

> What specific structural property distinguishes `full_propagation_chain` from `alternating_carry` and `block_boundary_stress`, if not chunk size?

This points toward a more refined family-structure analysis rather than another simple chunking variant.

---

## Formal Status

**Result:** PASS  
**Type:** chunk-size sensitivity analysis  
**Main message:** the residual family split is stable across chunk-size variation and is not explained by granularity alone

---
